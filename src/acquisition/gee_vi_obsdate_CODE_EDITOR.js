// GEE Code Editor version of gee_vi_obsdate.py: NDVI, EVI and NIRv at observation day
// I export both CSVs to Drive and save them in data/raw/ as vi_obsdate_<years>.csv

var FIRST_YEAR = 2015;
var LAST_YEAR = 2023;
var DRIVE_FOLDER = "GREEN_ALIBI";

var MARATHWADA_DISTRICTS = [
  "Aurangabad", "Jalna", "Bid", "Latur",
  "Osmanabad", "Nanded", "Parbhani", "Hingoli"
];

var gaul = ee.FeatureCollection("FAO/GAUL/2015/level2");
var marathwadaFc = gaul.filter(
  ee.Filter.and(
    ee.Filter.eq("ADM1_NAME", "Maharashtra"),
    ee.Filter.inList("ADM2_NAME", MARATHWADA_DISTRICTS)
  )
);
var marathwadaBoundary = marathwadaFc.union(1).geometry();

// MCD12Q1 lags a year or two at the recent end, so I take the latest map up to that year
function getCroplandMask(year) {
  var lc = ee.ImageCollection("MODIS/061/MCD12Q1")
    .filterDate("2001-01-01", (year + 1) + "-01-01")
    .sort("system:time_start", false)
    .first()
    .select("LC_Type1");
  return lc.eq(12).or(lc.eq(14));
}

function viStack(year) {
  var start = ee.Date(year + "-06-01");
  var end = ee.Date(year + "-12-27");
  var cropland = getCroplandMask(year);
  var daysInYear = ee.Date.fromYMD(year, 12, 31).getRelative("day", "year").add(1);

  return ee.ImageCollection("MODIS/061/MOD13Q1")
    .filterDate(start, end)
    .filterBounds(marathwadaBoundary)
    .map(function(img) {
      var startDoy = img.date().getRelative("day", "year").add(1);
      var good = img.select("SummaryQA").lte(1);
      var ndvi = img.select("NDVI").multiply(0.0001).rename("ndvi");
      var evi = img.select("EVI").multiply(0.0001).rename("evi");
      var nir = img.select("sur_refl_b02").multiply(0.0001);
      var nirv = ndvi.multiply(nir).rename("nirv");
      // a late-December composite can contain early-January days; I keep them on the same
      // day-of-year scale by adding the length of the year
      var doyRaw = img.select("DayOfYear");
      var doy = doyRaw.toFloat();
      doy = doy.where(doy.lt(ee.Image.constant(startDoy).subtract(20)), doy.add(daysInYear));
      doy = doy.updateMask(doyRaw.gt(0)).rename("obs_doy");
      return ndvi.addBands([evi, nirv, doy])
        .updateMask(good)
        .updateMask(cropland)
        .set({year: year, doy_start: startDoy, date: img.date().format("YYYY-MM-dd")});
    });
}

var REDUCER = ee.Reducer.mean().combine({reducer2: ee.Reducer.count(), sharedInputs: true});

function regionFeatures(year) {
  return viStack(year).map(function(img) {
    var s = img.reduceRegion({
      reducer: REDUCER, geometry: marathwadaBoundary, scale: 250, maxPixels: 1e9, tileScale: 4
    });
    return ee.Feature(null, {
      year: img.get("year"), date: img.get("date"), doy_start: img.get("doy_start"),
      mean_ndvi: s.get("ndvi_mean"), mean_evi: s.get("evi_mean"), mean_nirv: s.get("nirv_mean"),
      mean_obs_doy: s.get("obs_doy_mean"), valid_pixel_count: s.get("ndvi_count")
    });
  });
}

function districtFeatures(year) {
  return viStack(year).map(function(img) {
    var fc = img.reduceRegions({
      collection: marathwadaFc.select(["ADM2_NAME"]), reducer: REDUCER, scale: 250, tileScale: 4
    });
    return fc.map(function(d) {
      return ee.Feature(null, {
        district: d.get("ADM2_NAME"), year: img.get("year"), date: img.get("date"),
        doy_start: img.get("doy_start"), mean_ndvi: d.get("ndvi_mean"), mean_evi: d.get("evi_mean"),
        mean_nirv: d.get("nirv_mean"), mean_obs_doy: d.get("obs_doy_mean"),
        valid_pixel_count: d.get("ndvi_count")
      });
    });
  }).flatten();
}

var years = [];
for (var y = FIRST_YEAR; y <= LAST_YEAR; y++) { years.push(y); }

var region = ee.FeatureCollection(years.map(regionFeatures)).flatten();
var district = ee.FeatureCollection(years.map(districtFeatures)).flatten();

var COLS = ["year", "date", "doy_start", "mean_ndvi", "mean_evi", "mean_nirv", "mean_obs_doy", "valid_pixel_count"];

// quick look before exporting: the first year's composites should have NDVI around 0.3-0.8
print("Composites per run (regional):", region.size());
print("First rows:", region.limit(5));
Map.centerObject(marathwadaBoundary, 7);
Map.addLayer(marathwadaFc, {color: "teal"}, "Marathwada districts");

Export.table.toDrive({
  collection: region,
  description: "vi_obsdate_" + FIRST_YEAR + "_" + LAST_YEAR,
  folder: DRIVE_FOLDER,
  fileNamePrefix: "vi_obsdate_" + FIRST_YEAR + "_" + LAST_YEAR,
  fileFormat: "CSV",
  selectors: COLS
});

Export.table.toDrive({
  collection: district,
  description: "vi_obsdate_by_district_" + FIRST_YEAR + "_" + LAST_YEAR,
  folder: DRIVE_FOLDER,
  fileNamePrefix: "vi_obsdate_by_district_" + FIRST_YEAR + "_" + LAST_YEAR,
  fileFormat: "CSV",
  selectors: ["district"].concat(COLS)
});
