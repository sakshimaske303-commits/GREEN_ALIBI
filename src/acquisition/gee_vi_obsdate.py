# GEE: NDVI, EVI and NIRv from MOD13Q1 with per-pixel observation dates (region + districts)
#
# Same masking and dating as gee_cropland_fraction_and_ndvi_obsdates.py (SummaryQA <= 1,
# MCD12Q1 classes 12/14, mean DayOfYear), but also exports EVI and NIRv = NDVI x NIR
# reflectance, so that src/analysis/vegetation_index_lag.py can test whether the
# "SIF leads NDVI" result is really a property of NDVI (saturation, slow return to
# baseline) rather than of fluorescence: GOSIF is itself predicted from MODIS EVI.
#
# Usage (needs an authenticated Earth Engine account):
#   python src/acquisition/gee_vi_obsdate.py                 # 2015-2023
#   python src/acquisition/gee_vi_obsdate.py 2001 2014       # any year range, for the extension
# Writes data/raw/vi_obsdate_<first>_<last>.csv and data/raw/vi_obsdate_by_district_<first>_<last>.csv

import os
import sys

import ee
import geemap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gee_data_acquisition import marathwada_boundary, marathwada_fc  # noqa: E402  (also initialises EE)

FIRST, LAST = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (2015, 2023)
YEARS = list(range(FIRST, LAST + 1))
OUT_REGION = f"data/raw/vi_obsdate_{FIRST}_{LAST}.csv"
OUT_DISTRICT = f"data/raw/vi_obsdate_by_district_{FIRST}_{LAST}.csv"
TMP_DIR = "data/raw/_gee_tmp"


def mcd12q1(year):
    # MCD12Q1 starts in 2001 and lags a year or two at the recent end
    coll = ee.ImageCollection("MODIS/061/MCD12Q1")
    for y in list(range(year, year - 4, -1)) + [2001]:
        c = coll.filter(ee.Filter.calendarRange(y, y, "year"))
        if c.size().getInfo() > 0:
            return c.first().select("LC_Type1")
    raise RuntimeError(f"no MCD12Q1 image near {year}")


def vi_stack(year):
    start, end = ee.Date(f"{year}-06-01"), ee.Date(f"{year}-12-27")
    lc = mcd12q1(year)
    cropland = lc.eq(12).Or(lc.eq(14))
    days_in_year = ee.Date.fromYMD(year, 12, 31).getRelative("day", "year").add(1)

    def per_image(img):
        start_doy = img.date().getRelative("day", "year").add(1)
        good = img.select("SummaryQA").lte(1)
        ndvi = img.select("NDVI").multiply(0.0001).rename("ndvi")
        evi = img.select("EVI").multiply(0.0001).rename("evi")
        nir = img.select("sur_refl_b02").multiply(0.0001)
        nirv = ndvi.multiply(nir).rename("nirv")
        doy = img.select("DayOfYear").toFloat()
        doy = doy.where(doy.lt(ee.Image.constant(start_doy).subtract(20)), doy.add(days_in_year))
        doy = doy.updateMask(img.select("DayOfYear").gt(0)).rename("obs_doy")
        stack = ndvi.addBands([evi, nirv, doy]).updateMask(good).updateMask(cropland)
        return stack.set({"year": year, "doy_start": start_doy, "date": img.date().format("YYYY-MM-dd")})

    return (ee.ImageCollection("MODIS/061/MOD13Q1").filterDate(start, end)
            .filterBounds(marathwada_boundary).map(per_image))


REDUCER = ee.Reducer.mean().combine(ee.Reducer.count(), sharedInputs=True)


def region_features(year):
    def f(img):
        s = img.reduceRegion(reducer=REDUCER, geometry=marathwada_boundary, scale=250, maxPixels=1e9)
        return ee.Feature(None, {"year": img.get("year"), "date": img.get("date"), "doy_start": img.get("doy_start"),
                                 "mean_ndvi": s.get("ndvi_mean"), "mean_evi": s.get("evi_mean"),
                                 "mean_nirv": s.get("nirv_mean"), "mean_obs_doy": s.get("obs_doy_mean"),
                                 "valid_pixel_count": s.get("ndvi_count")})
    return ee.FeatureCollection(vi_stack(year).map(f))


def district_features(year):
    def f(img):
        fc = img.reduceRegions(collection=marathwada_fc.select(["ADM2_NAME"]), reducer=REDUCER, scale=250)
        return fc.map(lambda d: ee.Feature(None, {
            "district": d.get("ADM2_NAME"), "year": img.get("year"), "date": img.get("date"),
            "doy_start": img.get("doy_start"), "mean_ndvi": d.get("ndvi_mean"), "mean_evi": d.get("evi_mean"),
            "mean_nirv": d.get("nirv_mean"), "mean_obs_doy": d.get("obs_doy_mean"),
            "valid_pixel_count": d.get("ndvi_count")}))
    return vi_stack(year).map(f).flatten()


if __name__ == "__main__":
    import pandas as pd

    os.makedirs(TMP_DIR, exist_ok=True)
    reg, dis = [], []
    for y in YEARS:
        t1, t2 = os.path.join(TMP_DIR, f"vi_region_{y}.csv"), os.path.join(TMP_DIR, f"vi_district_{y}.csv")
        geemap.ee_export_vector(region_features(y), filename=t1, verbose=False)
        geemap.ee_export_vector(district_features(y), filename=t2, verbose=False)
        reg.append(pd.read_csv(t1))
        dis.append(pd.read_csv(t2))
        print(f"  {y}: {len(reg[-1])} regional and {len(dis[-1])} district composites")
    cols = ["year", "date", "doy_start", "mean_ndvi", "mean_evi", "mean_nirv", "mean_obs_doy", "valid_pixel_count"]
    pd.concat(reg)[cols].sort_values(["year", "doy_start"]).to_csv(OUT_REGION, index=False)
    pd.concat(dis)[["district"] + cols].sort_values(["district", "year", "doy_start"]).to_csv(OUT_DISTRICT, index=False)
    print(f"Saved {OUT_REGION} and {OUT_DISTRICT}. Next: python src/analysis/vegetation_index_lag.py")
