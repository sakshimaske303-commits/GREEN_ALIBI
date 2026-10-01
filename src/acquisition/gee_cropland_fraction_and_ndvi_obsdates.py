# GEE: cropland fraction + MODIS NDVI observation dates

import os
import sys

import ee
import geemap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gee_data_acquisition import marathwada_boundary, get_cropland_mask

YEARS = list(range(2015, 2024))
OUT_DIR_FRAC = "data/external/cropland_fraction"
OUT_CSV_NDVI = "data/raw/ndvi_obsdate_2015_2023.csv"

GRID_STANDARD = [0.05, 0, -180.0, 0, -0.05, 90.0]

REGION = ee.Geometry.Rectangle([74.3, 17.4, 78.6, 20.9])


def mcd12q1_year(year):
    coll = ee.ImageCollection("MODIS/061/MCD12Q1")
    for y in range(year, year - 4, -1):
        if coll.filter(ee.Filter.calendarRange(y, y, "year")).size().getInfo() > 0:
            if y != year:
                print(f"  MCD12Q1 {year} not available, using {y} instead")
            return coll.filter(ee.Filter.calendarRange(y, y, "year")).first().select("LC_Type1"), y
    raise RuntimeError(f"No MCD12Q1 image found for {year} or the 3 years before it")


def cropland_fraction(year):
    lc, used_year = mcd12q1_year(year)
    both = lc.eq(12).Or(lc.eq(14)).rename("crop_12_14")
    only12 = lc.eq(12).rename("crop_12")
    img = both.addBands(only12).toFloat()
    transform = GRID_STANDARD
    frac = (img.reduceResolution(reducer=ee.Reducer.mean(), maxPixels=1024)
               .reproject(crs="EPSG:4326", crsTransform=transform))
    return frac, transform, used_year


def ndvi_obsdate_features(year):
    start = ee.Date(f"{year}-06-01")
    end = ee.Date(f"{year}-12-27")
    cropland = get_cropland_mask(year)
    days_in_year = ee.Date.fromYMD(year, 12, 31).getRelative("day", "year").add(1)

    def per_image(img):
        start_doy = img.date().getRelative("day", "year").add(1)
        good = img.select("SummaryQA").lte(1)
        ndvi = img.select("NDVI").multiply(0.0001).rename("ndvi")
        doy = img.select("DayOfYear").toFloat()
        doy = doy.where(doy.lt(ee.Image.constant(start_doy).subtract(20)), doy.add(days_in_year))
        doy = doy.updateMask(img.select("DayOfYear").gt(0)).rename("obs_doy")
        stack = ndvi.addBands(doy).updateMask(good).updateMask(cropland)
        stats = stack.reduceRegion(
            reducer=ee.Reducer.mean().combine(ee.Reducer.count(), sharedInputs=True),
            geometry=marathwada_boundary, scale=250, maxPixels=1e9,
        )
        return ee.Feature(None, {
            "year": year,
            "date": img.date().format("YYYY-MM-dd"),
            "doy_start": start_doy,
            "mean_ndvi": stats.get("ndvi_mean"),
            "mean_obs_doy": stats.get("obs_doy_mean"),
            "valid_pixel_count": stats.get("ndvi_count"),
        })

    coll = (ee.ImageCollection("MODIS/061/MOD13Q1")
              .filterDate(start, end).filterBounds(marathwada_boundary))
    return ee.FeatureCollection(coll.map(per_image))


if __name__ == "__main__":
    os.makedirs(OUT_DIR_FRAC, exist_ok=True)

    print("1) Cropland fraction on the GOSIF grid")
    for year in YEARS:
        frac, transform, used_year = cropland_fraction(year)
        out = os.path.join(OUT_DIR_FRAC, f"cropland_fraction_{year}.tif")
        geemap.ee_export_image(frac, filename=out, region=REGION, crs="EPSG:4326",
                               crs_transform=transform, file_per_band=False)
        print(f"  {year}: saved {out} (MCD12Q1 {used_year}, grid origin {transform[2]})")

    print("\n2) NDVI with actual observation dates")
    fcs = [ndvi_obsdate_features(y) for y in YEARS]
    geemap.ee_export_vector(ee.FeatureCollection(fcs).flatten(), filename=OUT_CSV_NDVI)
    print(f"  saved {OUT_CSV_NDVI}")
    print("\nDone. Next: python src/analysis/cropmask_obsdate_sensitivity.py")
