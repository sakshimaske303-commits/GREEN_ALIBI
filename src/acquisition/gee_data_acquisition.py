"""
GREEN ALIBI — Earth Engine data acquisition.

Python version of the extraction I originally ran by hand in the EE Code
Editor: MOD13Q1 NDVI (SummaryQA-filtered), MCD12Q1 cropland mask, CHIRPS
seasonal rainfall + 20-year climatology, over the FAO GAUL Marathwada
boundary. Needs an authenticated Earth Engine account to run.

Extended for the 8-year expansion (added 2016, 2017, 2019, 2022, 2023 to
the original 2015/2018/2020) — same pipeline, just more years, plus proper
CSV exports for region and by-district rainfall instead of console prints.
"""

import ee
import geemap

# Fill in your own EE cloud project id before running.
EE_PROJECT_ID = "ecological-balance-sheet"

ee.Authenticate()  # first run only, no-ops if already logged in
ee.Initialize(project=EE_PROJECT_ID)

# --- 1. Study boundary: FAO GAUL 2015 level 2, Marathwada's 8 districts ---
MARATHWADA_DISTRICTS = [
    "Aurangabad", "Jalna", "Bid", "Latur",
    "Osmanabad", "Nanded", "Parbhani", "Hingoli",
]
# GAUL spells it "Bid", not "Beed" — used the wrong spelling here the first
# time and it silently dropped the district from every export until I
# counted rows and noticed 7 districts instead of 8.

gaul = ee.FeatureCollection("FAO/GAUL/2015/level2")
marathwada_fc = gaul.filter(
    ee.Filter.And(
        ee.Filter.eq("ADM1_NAME", "Maharashtra"),
        ee.Filter.inList("ADM2_NAME", MARATHWADA_DISTRICTS),
    )
)
marathwada_boundary = marathwada_fc.union(1).geometry()


# --- 2. Cropland mask: MCD12Q1 IGBP classes 12 (cropland) + 14 (mosaic) ---
def get_cropland_mask(year):
    lc = (
        ee.ImageCollection("MODIS/061/MCD12Q1")
        .filter(ee.Filter.calendarRange(year, year, "year"))
        .first()
        .select("LC_Type1")
    )
    return lc.eq(12).Or(lc.eq(14))


# --- 3. NDVI: MOD13Q1, SummaryQA <= 1 (good/marginal), cropland-masked ---
def get_ndvi_collection(year, start_month_day="06-01", end_month_day="12-31"):
    start = ee.Date(f"{year}-{start_month_day}")
    end = ee.Date(f"{year}-{end_month_day}")
    cropland_mask = get_cropland_mask(year)

    def mask_and_scale(img):
        qa = img.select("SummaryQA")
        good_quality = qa.lte(1)
        ndvi = img.select("NDVI").multiply(0.0001)
        # No .clip() here on purpose — clipping MOD13Q1's native sinusoidal
        # grid against this boundary throws a transform error, and
        # reduceRegion() below already restricts to the same geometry.
        return (
            ndvi.updateMask(good_quality)
            .updateMask(cropland_mask)
            .copyProperties(img, ["system:time_start"])
        )

    return (
        ee.ImageCollection("MODIS/061/MOD13Q1")
        .filterDate(start, end)
        .filterBounds(marathwada_boundary)
        .map(mask_and_scale)
    )


def extract_ndvi_timeseries(year, scale=250):
    """Region-mean NDVI per composite date."""
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


# --- 4. CHIRPS rainfall: seasonal totals + 20-year climatology ---
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
    """20-year seasonal-total climatology (mean, stdev)."""
    yearly_totals = [get_seasonal_rainfall_total(y) for y in range(start_year, end_year + 1)]
    totals_list = ee.List(yearly_totals)
    totals_arr = ee.Array(totals_list)
    return {
        "mean": totals_arr.reduce(ee.Reducer.mean(), [0]).get([0]),
        "std": totals_arr.reduce(ee.Reducer.stdDev(), [0]).get([0]),
    }


# --- 5. District-level exports ---
def get_district_boundaries():
    return marathwada_fc  # one feature per district, ADM2_NAME is the key


def get_district_seasonal_rainfall(year, start_month_day="06-01", end_month_day="12-31"):
    """One seasonal rainfall total per district."""
    start = ee.Date(f"{year}-{start_month_day}")
    end = ee.Date(f"{year}-{end_month_day}")
    total = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterDate(start, end)
        .sum()
    )

    def reduce_district(feature):
        stats = total.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=feature.geometry(),
            scale=5566,
            maxPixels=1e9,
        )
        return ee.Feature(None, {
            "district": feature.get("ADM2_NAME"),
            "rainfall_mm": stats.get("precipitation"),
            "year": year,
        })

    return marathwada_fc.map(reduce_district)


# --- 6. Main ---
if __name__ == "__main__":
    NEW_YEARS = [2016, 2017, 2019, 2022, 2023]
    STUDY_YEARS = [2015, 2018, 2020] + NEW_YEARS

    for year in STUDY_YEARS:
        fc = extract_ndvi_timeseries(year)
        geemap.ee_export_vector(
            fc, filename=f"data/raw/ndvi_timeseries_{year}.csv"
        )
        print(f"Exported NDVI time series for {year}")

    rainfall_features = [
        ee.Feature(None, {"total_rainfall_mm": get_seasonal_rainfall_total(y), "year": y})
        for y in STUDY_YEARS
    ]
    rainfall_fc = ee.FeatureCollection(rainfall_features)
    geemap.ee_export_vector(
        rainfall_fc, filename=f"data/raw/marathwada_rainfall_{min(STUDY_YEARS)}_{max(STUDY_YEARS)}_8years.csv"
    )
    print(f"Exported region-mean seasonal rainfall totals for {STUDY_YEARS}")

    district_rainfall_fcs = [get_district_seasonal_rainfall(y) for y in STUDY_YEARS]
    district_rainfall_fc = ee.FeatureCollection(district_rainfall_fcs).flatten()
    geemap.ee_export_vector(
        district_rainfall_fc, filename="data/raw/marathwada_rainfall_by_district_8years.csv"
    )
    print(f"Exported by-district seasonal rainfall totals for {STUDY_YEARS}")

    clim = get_climatology()
    print(f"2001-2020 climatology (unchanged) — mean: {clim['mean'].getInfo():.2f} mm, "
          f"std: {clim['std'].getInfo():.2f} mm")

    print("\nDone. Send back:")
    print("  - data/raw/ndvi_timeseries_<year>.csv for each of:", STUDY_YEARS)
    print(f"  - data/raw/marathwada_rainfall_{min(STUDY_YEARS)}_{max(STUDY_YEARS)}_8years.csv")
    print("  - data/raw/marathwada_rainfall_by_district_8years.csv")
