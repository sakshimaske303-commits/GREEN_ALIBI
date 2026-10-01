# GEE: district NDVI and rainfall timing

import os
import sys

import ee
import geemap
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gee_data_acquisition import marathwada_fc, marathwada_boundary, get_cropland_mask

STUDY_YEARS = list(range(2015, 2024))
BASELINE_YEARS = list(range(2001, 2021))
TMP_DIR = "data/raw/_gee_tmp"
CHIRPS_SCALE = 5566

districts = marathwada_fc.select(["ADM2_NAME"])


def ndvi_by_district(year):
    start, end = ee.Date(f"{year}-06-01"), ee.Date(f"{year}-12-27")
    cropland = get_cropland_mask(year)
    days_in_year = ee.Date.fromYMD(year, 12, 31).getRelative("day", "year").add(1)

    def per_image(img):
        start_doy = img.date().getRelative("day", "year").add(1)
        date_str = img.date().format("YYYY-MM-dd")
        good = img.select("SummaryQA").lte(1)
        ndvi = img.select("NDVI").multiply(0.0001).rename("ndvi")
        doy = img.select("DayOfYear").toFloat()
        doy = doy.where(doy.lt(ee.Image.constant(start_doy).subtract(20)), doy.add(days_in_year))
        doy = doy.updateMask(img.select("DayOfYear").gt(0)).rename("obs_doy")
        stack = ndvi.addBands(doy).updateMask(good).updateMask(cropland)
        stats = stack.reduceRegions(
            collection=districts,
            reducer=ee.Reducer.mean().combine(ee.Reducer.count(), sharedInputs=True),
            scale=250,
        )
        return stats.map(lambda f: ee.Feature(None, {
            "year": year, "district": f.get("ADM2_NAME"), "date": date_str, "doy_start": start_doy,
            "mean_ndvi": f.get("ndvi_mean"), "mean_obs_doy": f.get("obs_doy_mean"),
            "valid_pixel_count": f.get("ndvi_count"),
        }))

    coll = (ee.ImageCollection("MODIS/061/MOD13Q1")
              .filterDate(start, end).filterBounds(marathwada_boundary))
    return ee.FeatureCollection(coll.map(per_image)).flatten()


def chirps_daily(year, by_district):
    start, end = ee.Date(f"{year}-06-01"), ee.Date(f"{year}-12-27")
    coll = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").filterDate(start, end)

    if not by_district:
        def per_day(img):
            v = img.reduceRegion(ee.Reducer.mean(), marathwada_boundary, CHIRPS_SCALE, maxPixels=1e9)
            return ee.Feature(None, {"date": img.date().format("YYYY-MM-dd"),
                                     "rain_mm": v.get("precipitation")})
        return ee.FeatureCollection(coll.map(per_day))

    def per_day_d(img):
        d = img.date().format("YYYY-MM-dd")
        r = img.reduceRegions(collection=districts, reducer=ee.Reducer.mean(), scale=CHIRPS_SCALE)
        return r.map(lambda f: ee.Feature(None, {"date": d, "district": f.get("ADM2_NAME"),
                                                 "rain_mm": f.get("mean")}))
    return ee.FeatureCollection(coll.map(per_day_d)).flatten()


def export_years(make_fc, years, out_csv, label):
    os.makedirs(TMP_DIR, exist_ok=True)
    parts = []
    for y in years:
        tmp = os.path.join(TMP_DIR, f"{label}_{y}.csv")
        geemap.ee_export_vector(make_fc(y), filename=tmp, verbose=False)
        df = pd.read_csv(tmp)
        df["year"] = y
        parts.append(df.drop(columns=[c for c in ["system:index", ".geo"] if c in df.columns]))
        print(f"  {label} {y}: {len(df)} rows")
    out = pd.concat(parts, ignore_index=True)
    out.to_csv(out_csv, index=False)
    print(f"  -> saved {out_csv} ({len(out)} rows)")


if __name__ == "__main__":
    print("1) District NDVI with observation dates")
    export_years(ndvi_by_district, STUDY_YEARS, "data/raw/ndvi_obsdate_by_district_2015_2023.csv", "ndvi_district")

    print("\n2) CHIRPS daily rainfall, region mean, 2001-2023")
    export_years(lambda y: chirps_daily(y, False), BASELINE_YEARS + [y for y in STUDY_YEARS if y > 2020],
                 "data/raw/chirps_daily_region_2001_2023.csv", "chirps_region")

    print("\n3) CHIRPS daily rainfall, by district, 2015-2023")
    export_years(lambda y: chirps_daily(y, True), STUDY_YEARS,
                 "data/raw/chirps_daily_by_district_2015_2023.csv", "chirps_district")

    print("\nDone. Next: python src/analysis/district_lag_analysis.py")
    print("      then: python src/analysis/rain_timing_analysis.py")
