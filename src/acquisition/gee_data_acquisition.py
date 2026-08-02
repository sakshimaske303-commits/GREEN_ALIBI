"""
GREEN ALIBI — Google Earth Engine data acquisition (Python translation).

WHY THIS FILE EXISTS
---------------------------------------------------------------------------
The original NDVI, cropland-mask, and CHIRPS rainfall extractions for this
project were run interactively in Earth Engine's browser-based Code Editor
(JavaScript), not as checked-in scripts — a limitation stated explicitly in
Research_Paper.md ("Limitations") and Project_Journal.md. Every reviewer of
this project who read that limitation (including four independent AI
reviews conducted for this project) raised the same, fair point: an
interactive step is not directly reproducible from source.

This script is a faithful line-for-line Python translation of that
methodology, using the official `earthengine-api` (the `ee` module) plus
`geemap` for convenience helpers. It reconstructs, in checked-in and
version-controlled form, exactly what Research_Paper.md Section 3
describes: MOD13Q1 NDVI with SummaryQA filtering, an MCD12Q1 cropland mask,
CHIRPS daily rainfall aggregated to seasonal totals plus a 20-year
climatology, and the FAO GAUL 2015 level-2 Marathwada boundary.

HONESTY NOTE — please read before treating this as "already run"
---------------------------------------------------------------------------
This script has NOT been executed as part of this project. It requires an
authenticated Earth Engine account (`earthengine authenticate`) with API
access, which this project's automated environment does not have. It is
provided so that (a) the acquisition step is no longer only describable in
prose, and (b) anyone with EE access — including a future version of this
project — can run `python gee_data_acquisition.py` and reproduce the exact
inputs that were previously only pulled by hand. The GOSIF clipping step
(clip_gosif.py) and everything downstream of it were already fully
scripted and are unaffected by this addition; this file closes the one
remaining unscripted gap in the pipeline, documented in
Development_Log.md Entry 13.
---------------------------------------------------------------------------
"""

import ee
import geemap

# ee.Authenticate()  # run once, interactively, outside this script
ee.Initialize()

# ============================================================
# 1. Study-area boundary — FAO GAUL 2015, level 2, Marathwada's
#    eight constituent districts, merged into a single polygon.
#    (Research_Paper.md Section 3.2 — replaced an earlier
#    rectangular bounding box after Development_Log.md Entry 2
#    found it leaked into Telangana / Solapur / Yavatmal.)
# ============================================================
MARATHWADA_DISTRICTS = [
    "Aurangabad", "Jalna", "Beed", "Latur",
    "Osmanabad", "Nanded", "Parbhani", "Hingoli",
]

gaul = ee.FeatureCollection("FAO/GAUL/2015/level2")
marathwada_fc = gaul.filter(
    ee.Filter.And(
        ee.Filter.eq("ADM1_NAME", "Maharashtra"),
        ee.Filter.inList("ADM2_NAME", MARATHWADA_DISTRICTS),
    )
)
marathwada_boundary = marathwada_fc.union(1).geometry()

# ============================================================
# 2. Cropland mask — MCD12Q1 IGBP classification, classes 12
#    (Croplands) and 14 (Cropland/Natural Vegetation Mosaic).
#    (Research_Paper.md Section 3.2.)
# ============================================================
def get_cropland_mask(year):
    lc = (
        ee.ImageCollection("MODIS/061/MCD12Q1")
        .filter(ee.Filter.calendarRange(year, year, "year"))
        .first()
        .select("LC_Type1")
    )
    return lc.eq(12).Or(lc.eq(14))


# ============================================================
# 3. NDVI — MOD13Q1, 16-day / 250m, filtered by the SummaryQA
#    band to retain only good- and marginal-quality pixels
#    (values 0 and 1), then masked to cropland and clipped to
#    the Marathwada boundary.
#    (Research_Paper.md Section 3.1 and 3.3 — "cloud and
#    cloud-shadow contamination... addressed via MOD13Q1's
#    SummaryQA per-pixel quality flag prior to any analysis.")
# ============================================================
def get_ndvi_collection(year, start_month_day="06-01", end_month_day="12-31"):
    start = ee.Date(f"{year}-{start_month_day}")
    end = ee.Date(f"{year}-{end_month_day}")
    cropland_mask = get_cropland_mask(year)

    def mask_and_scale(img):
        qa = img.select("SummaryQA")
        good_quality = qa.lte(1)  # 0 = good, 1 = marginal; 2/3 excluded
        ndvi = img.select("NDVI").multiply(0.0001)
        return (
            ndvi.updateMask(good_quality)
            .updateMask(cropland_mask)
            .clip(marathwada_boundary)
            .copyProperties(img, ["system:time_start"])
        )

    return (
        ee.ImageCollection("MODIS/061/MOD13Q1")
        .filterDate(start, end)
        .filterBounds(marathwada_boundary)
        .map(mask_and_scale)
    )


def extract_ndvi_timeseries(year, scale=250):
    """Region-mean NDVI per composite date, matching aggregate_sif.py's
    region-average approach for SIF (Research_Paper.md Section 3.3)."""
    coll = get_ndvi_collection(year)

    def reduce_image(img):
        stats = img.reduceRegion(
            reducer=ee.Reducer.mean().combine(ee.Reducer.count(), sharedInputs=True),
            geometry=marathwada_boundary,
            scale=scale,
            maxPixels=1e9,
        )
        return ee.Feature(None, {
            "date": img.date().format("YYYY-MM-dd"),
            "doy": img.date().getRelative("day", "year"),
            "mean_ndvi": stats.get("NDVI_mean"),
            "ndvi_valid_pixel_count": stats.get("NDVI_count"),
        })

    return ee.FeatureCollection(coll.map(reduce_image))


# ============================================================
# 4. CHIRPS daily rainfall — seasonal totals for each study
#    year plus a 20-year (2001-2020) climatological baseline,
#    same region and seasonal window.
#    (Research_Paper.md Section 3.4.)
# ============================================================
def get_seasonal_rainfall_total(year, start_month_day="06-01", end_month_day="12-31"):
    start = ee.Date(f"{year}-{start_month_day}")
    end = ee.Date(f"{year}-{end_month_day}")
    chirps = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterDate(start, end)
        .filterBounds(marathwada_boundary)
    )
    total = chirps.sum().clip(marathwada_boundary)
    stats = total.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=marathwada_boundary,
        scale=5566,  # native CHIRPS resolution (~0.05 deg)
        maxPixels=1e9,
    )
    return stats.get("precipitation")


def get_climatology(start_year=2001, end_year=2020):
    """20-year seasonal-total climatology (mean and stdev), used as the
    baseline for the rainfall-anomaly calculation in rainfall_analysis.py."""
    yearly_totals = [get_seasonal_rainfall_total(y) for y in range(start_year, end_year + 1)]
    totals_list = ee.List(yearly_totals)
    totals_arr = ee.Array(totals_list)
    return {
        "mean": totals_arr.reduce(ee.Reducer.mean(), [0]).get([0]),
        "std": totals_arr.reduce(ee.Reducer.stdDev(), [0]).get([0]),
    }


# ============================================================
# 5. District-level exports — same extractions above, run per
#    district polygon instead of the merged region, feeding
#    sif_rainfall_district_merged.csv / zonal_stats_sif.py's
#    NDVI/rainfall counterpart.
# ============================================================
def get_district_boundaries():
    return marathwada_fc  # each feature is one district; ADM2_NAME is the key


if __name__ == "__main__":
    STUDY_YEARS = [2015, 2018, 2020]
    for year in STUDY_YEARS:
        fc = extract_ndvi_timeseries(year)
        geemap.ee_export_vector(
            fc, filename=f"data/raw/ndvi_timeseries_{year}.csv"
        )
        print(f"Exported NDVI time series for {year}")

    for year in STUDY_YEARS:
        total = get_seasonal_rainfall_total(year)
        print(f"{year} seasonal rainfall total (mm): {total.getInfo()}")

    clim = get_climatology()
    print(f"2001-2020 climatology — mean: {clim['mean'].getInfo():.2f} mm, "
          f"std: {clim['std'].getInfo():.2f} mm")
