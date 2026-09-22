"""Tier-3 extension #1 and #2: more study years, and a per-district (rather
than region-wide) rainfall climatology. Needs my authenticated Earth Engine
account -- ee.Authenticate() below opens a browser login the first time I
run this.

Reuses every boundary/NDVI/rainfall function already defined in
gee_data_acquisition.py (same FAO GAUL boundary, same MOD13Q1/CHIRPS calls,
same cropland mask) so this stays consistent with the rest of the project
instead of re-deriving the boundary logic and risking a second Bid/Beed-style
typo. Run from the project root: `python src/acquisition/gee_extended_years.py`

BEFORE RUNNING:
1. Confirm EE_PROJECT_ID in gee_data_acquisition.py (line 10) is still set to
   my own EE cloud project id.
2. Check what years the SIF data actually covers before adding a year here --
   NDVI/rainfall below come straight from Earth Engine (always current), but
   the matching SIF file for any new year still has to be downloaded by hand
   from https://data.globalecology.unh.edu/data/GOSIF_v2/ (GOSIF isn't an
   Earth Engine dataset) and dropped into data/raw/ as GOSIF_<year>_<doy>.tif,
   same as every other year already in that folder -- then run clip_gosif.py
   on it like normal. This script only gets the NDVI and rainfall side.
3. EXTRA_YEARS below defaults to just [2021] -- the one year Section 3.1
   flagged as "didn't make it into this expansion pass" without saying why.
   Add more years (e.g. 2024) once I've confirmed GOSIF v2 actually has that
   year's files on the UNH page above.
"""

import geemap

from gee_data_acquisition import (
    marathwada_fc,
    extract_ndvi_timeseries,
    get_seasonal_rainfall_total,
    get_district_seasonal_rainfall,
)
import ee

EXTRA_YEARS = [2021]  # edit once I've confirmed SIF coverage for whichever
                       # years I'm adding (see note 2 above)

# ---------------------------------------------------------------------------
# Extension #2: per-district rainfall climatology (2001-2020), instead of the
# single region-wide number get_climatology() in gee_data_acquisition.py
# computes. This study's own Section 6 Limitations names this exact gap:
# "District-level rainfall anomaly was computed using one region-wide
# climatological baseline. A separate baseline for each district was not
# built." -- this function is that separate baseline.
# ---------------------------------------------------------------------------
def get_district_climatology(start_year=2001, end_year=2020):
    """Returns one FeatureCollection: one feature per district, with that
    district's own 20-year seasonal-rainfall mean and standard deviation --
    the same climatology logic as get_climatology() in the main acquisition
    script, just computed separately per district instead of pooled across
    all eight."""
    years = list(range(start_year, end_year + 1))

    def reduce_district(feature):
        geom = feature.geometry()

        def seasonal_total(year):
            start = ee.Date(f"{year}-06-01")
            end = ee.Date(f"{year}-12-27")
            total_img = (
                ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
                .filterDate(start, end)
                .sum()
            )
            stats = total_img.reduceRegion(
                reducer=ee.Reducer.mean(), geometry=geom, scale=5566, maxPixels=1e9,
            )
            return stats.get("precipitation")

        yearly = ee.Array([seasonal_total(y) for y in years])
        return ee.Feature(None, {
            "district": feature.get("ADM2_NAME"),
            "climatology_mean_mm": yearly.reduce(ee.Reducer.mean(), [0]).get([0]),
            "climatology_std_mm": yearly.reduce(ee.Reducer.stdDev(), [0]).get([0]),
            "start_year": start_year,
            "end_year": end_year,
        })

    return marathwada_fc.map(reduce_district)


if __name__ == "__main__":
    print(f"Extracting NDVI + rainfall for extra year(s): {EXTRA_YEARS}")
    print("(remember: this does NOT fetch SIF -- see the module docstring, step 2)\n")

    for year in EXTRA_YEARS:
        fc = extract_ndvi_timeseries(year)
        geemap.ee_export_vector(fc, filename=f"data/raw/ndvi_timeseries_{year}.csv")
        print(f"Exported NDVI time series for {year}")

        rainfall_fc = ee.FeatureCollection([
            ee.Feature(None, {"total_rainfall_mm": get_seasonal_rainfall_total(year), "year": year})
        ])
        geemap.ee_export_vector(rainfall_fc, filename=f"data/raw/marathwada_rainfall_{year}.csv")
        print(f"Exported region-mean seasonal rainfall total for {year}")

        district_fc = get_district_seasonal_rainfall(year)
        geemap.ee_export_vector(district_fc, filename=f"data/raw/marathwada_rainfall_by_district_{year}.csv")
        print(f"Exported by-district seasonal rainfall totals for {year}")

    print("\nComputing per-district 20-year (2001-2020) rainfall climatology...")
    district_clim_fc = get_district_climatology()
    geemap.ee_export_vector(district_clim_fc, filename="data/processed/rainfall_climatology_by_district.csv")
    print("Exported data/processed/rainfall_climatology_by_district.csv")
    print("(use each district's own mean/std here instead of the one pooled")
    print(" region-wide climatology when computing that district's own anomaly")
    print(" z-scores -- this is what addresses the Section 6 limitation)")

    print("\nDone. Remaining manual steps for the new year(s):")
    print("  1. Download the matching GOSIF_<year>_<doy>.tif files from")
    print("     https://data.globalecology.unh.edu/data/GOSIF_v2/ into data/raw/")
    print("  2. Rerun clip_gosif.py so the new year gets clipped like the others")
    print("  3. Re-run the main analysis pipeline (compare_sif_ndvi.py etc.) so")
    print("     the new year flows into every downstream table and figure")
