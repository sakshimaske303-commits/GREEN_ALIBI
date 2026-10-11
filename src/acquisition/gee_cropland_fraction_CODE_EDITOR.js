// GEE Code Editor version of the cropland-fraction part of gee_cropland_fraction_and_ndvi_obsdates.py
//
// I weight every 0.05 deg GOSIF cell by the share of its 500 m MCD12Q1 pixels that are cropland,
// so that my regional and district SIF series describe mainly farmland, as my NDVI series does.
// Band 1 crop_12_14 = share of IGBP classes 12 and 14 (cropland, cropland/natural mosaic)
// Band 2 crop_12    = share of class 12 only (used in the class-12-only sensitivity check)
// The grid is exactly the GOSIF/CHIRPS 0.05 deg grid.
//
// How I run it:
//   1. Set FIRST_YEAR and LAST_YEAR (2001-2014 for the out-of-sample extension), paste into
//      https://code.earthengine.google.com and press Run.
//   2. Open the Tasks tab and run the exports cropland_fraction_YYYY (to Google Drive, folder GREEN_ALIBI).
//   3. Download the .tif files into data/external/cropland_fraction/ with the names
//      cropland_fraction_YYYY.tif

var FIRST_YEAR = 2001;
var LAST_YEAR = 2014;
var DRIVE_FOLDER = "GREEN_ALIBI";

var GRID = [0.05, 0, -180.0, 0, -0.05, 90.0];
var REGION = ee.Geometry.Rectangle([74.3, 17.4, 78.6, 20.9]);

// MCD12Q1 starts in 2001 and lags a year or two at the recent end; I take the latest map up to that year
function landCover(year) {
  return ee.ImageCollection("MODIS/061/MCD12Q1")
    .filterDate("2001-01-01", (year + 1) + "-01-01")
    .sort("system:time_start", false)
    .first()
    .select("LC_Type1");
}

function croplandFraction(year) {
  var lc = landCover(year);
  var both = lc.eq(12).or(lc.eq(14)).rename("crop_12_14");
  var only12 = lc.eq(12).rename("crop_12");
  return both.addBands(only12).toFloat()
    .reduceResolution({reducer: ee.Reducer.mean(), maxPixels: 1024})
    .reproject({crs: "EPSG:4326", crsTransform: GRID})
    .clip(REGION);
}

// quick look: most of Marathwada should be bright (fraction close to 1)
Map.centerObject(REGION, 7);
Map.addLayer(croplandFraction(FIRST_YEAR).select("crop_12_14"), {min: 0, max: 1}, "cropland fraction " + FIRST_YEAR);

for (var y = FIRST_YEAR; y <= LAST_YEAR; y++) {
  Export.image.toDrive({
    image: croplandFraction(y),
    description: "cropland_fraction_" + y,
    folder: DRIVE_FOLDER,
    fileNamePrefix: "cropland_fraction_" + y,
    region: REGION,
    crs: "EPSG:4326",
    crsTransform: GRID,
    maxPixels: 1e9
  });
}
