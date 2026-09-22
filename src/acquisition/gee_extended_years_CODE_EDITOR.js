// ============================================================================
// GREEN ALIBI — Tier-3 extension, GEE CODE EDITOR (JavaScript) version
// ============================================================================
// Paste this whole file into a New Script at code.earthengine.google.com and
// hit Run. This is a JS port of gee_extended_years.py, written specifically
// for the browser Code Editor you already have open (project
// "ecological-balance-sheet" shown top right -- matches EE_PROJECT_ID in the
// Python scripts, so this is the same account/project as the rest of this
// project). Same boundary, same districts, same date windows as every other
// GEE script in this repo -- just JS syntax instead of Python.
//
// WHAT THIS DOES:
//   1. NDVI + rainfall for 2021 (the one year this study's own paper says
//      "didn't make it into this expansion pass", Section 3.1)
//   2. A per-district 20-year (2001-2020) rainfall climatology, instead of
//      the one pooled region-wide number the rest of the study uses --
//      Section 6's own Limitations names this exact gap
//
// WHAT TO DO WITH THE OUTPUT: every Export.table.toDrive() call below adds a
// task to the "Tasks" tab (top right of this editor, next to Console). Click
// each one, then "Run" in the popup -- it writes a CSV into a
// "GREEN_ALIBI_exports" folder in your Google Drive. Download those CSVs
// from Drive and drop them straight into this project's data/raw/ (for the
// two NDVI/rainfall files) and data/processed/ (for the district climatology
// file) folders, same as every other file already there.
//
// STILL MANUAL AFTER THIS: SIF for 2021 isn't in Earth Engine at all (GOSIF
// is distributed as GeoTIFFs from a university server, not a GEE dataset) --
// you still need to download the matching GOSIF_2021_<doy>.tif files by hand
// from https://data.globalecology.unh.edu/data/GOSIF_v2/ into data/raw/, then
// rerun clip_gosif.py on them like every other year already in this project.
// ============================================================================

var EXTRA_YEARS = [2021];

// ----------------------------------------------------------------------------
// Study boundary — identical to gee_data_acquisition.py: FAO GAUL 2015 level
// 2, same 8 districts, same "Bid" spelling (GAUL's own spelling, not "Beed")
// ----------------------------------------------------------------------------
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

// ----------------------------------------------------------------------------
// Cropland mask — MCD12Q1 IGBP classes 12 (cropland) + 14 (mosaic)
// ----------------------------------------------------------------------------
function getCroplandMask(year) {
  var lc = ee.ImageCollection("MODIS/061/MCD12Q1")
    .filter(ee.Filter.calendarRange(year, year, "year"))
    .first()
    .select("LC_Type1");
  return lc.eq(12).or(lc.eq(14));
}

// ----------------------------------------------------------------------------
// NDVI — MOD13Q1, SummaryQA <= 1 (good/marginal), cropland-masked
// ----------------------------------------------------------------------------
function getNdviCollection(year) {
  var start = ee.Date(year + "-06-01");
  var end = ee.Date(year + "-12-27");
  var croplandMask = getCroplandMask(year);

  return ee.ImageCollection("MODIS/061/MOD13Q1")
    .filterDate(start, end)
    .filterBounds(marathwadaBoundary)
    .map(function(img) {
      var qa = img.select("SummaryQA");
      var goodQuality = qa.lte(1);
      var ndvi = img.select("NDVI").multiply(0.0001);
      // no .clip() here on purpose, same reason as the Python version:
      // clipping MOD13Q1's native sinusoidal grid throws a transform error,
      // and reduceRegion() below already restricts to this geometry
      return ndvi.updateMask(goodQuality).updateMask(croplandMask)
        .copyProperties(img, ["system:time_start"]);
    });
}

function extractNdviTimeseries(year) {
  var coll = getNdviCollection(year);
  var scale = 250;

  var fc = coll.map(function(img) {
    var stats = img.reduceRegion({
      reducer: ee.Reducer.mean().combine({reducer2: ee.Reducer.count(), sharedInputs: true}),
      geometry: marathwadaBoundary,
      scale: scale,
      maxPixels: 1e9
    });
    return ee.Feature(null, {
      date: img.date().format("YYYY-MM-dd"),
      doy: img.date().getRelative("day", "year"),
      mean_ndvi: stats.get("NDVI_mean"),
      ndvi_valid_pixel_count: stats.get("NDVI_count")
    });
  });
  return ee.FeatureCollection(fc);
}

// ----------------------------------------------------------------------------
// CHIRPS rainfall — region-wide seasonal total
// ----------------------------------------------------------------------------
function getSeasonalRainfallTotal(year) {
  var start = ee.Date(year + "-06-01");
  var end = ee.Date(year + "-12-27");
  var chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
    .filterDate(start, end)
    .filterBounds(marathwadaBoundary);
  var total = chirps.sum().clip(marathwadaBoundary);
  var stats = total.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: marathwadaBoundary,
    scale: 5566, // native CHIRPS resolution (~0.05 deg)
    maxPixels: 1e9
  });
  return stats.get("precipitation");
}

// ----------------------------------------------------------------------------
// CHIRPS rainfall — per-district seasonal total
// ----------------------------------------------------------------------------
function getDistrictSeasonalRainfall(year) {
  var start = ee.Date(year + "-06-01");
  var end = ee.Date(year + "-12-27");
  var total = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
    .filterDate(start, end)
    .sum();

  return marathwadaFc.map(function(feature) {
    var stats = total.reduceRegion({
      reducer: ee.Reducer.mean(),
      geometry: feature.geometry(),
      scale: 5566,
      maxPixels: 1e9
    });
    return ee.Feature(null, {
      district: feature.get("ADM2_NAME"),
      rainfall_mm: stats.get("precipitation"),
      year: year
    });
  });
}

// ----------------------------------------------------------------------------
// NEW: per-district 20-year (2001-2020) rainfall climatology — this is what
// addresses Section 6's "a separate baseline for each district was not
// built" limitation
// ----------------------------------------------------------------------------
function getDistrictClimatology(startYear, endYear) {
  var years = [];
  for (var y = startYear; y <= endYear; y++) { years.push(y); }

  return marathwadaFc.map(function(feature) {
    var geom = feature.geometry();
    var yearlyTotals = years.map(function(year) {
      var start = ee.Date(year + "-06-01");
      var end = ee.Date(year + "-12-27");
      var totalImg = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterDate(start, end)
        .sum();
      var stats = totalImg.reduceRegion({
        reducer: ee.Reducer.mean(), geometry: geom, scale: 5566, maxPixels: 1e9
      });
      return stats.get("precipitation");
    });
    var yearlyArr = ee.Array(yearlyTotals);
    return ee.Feature(null, {
      district: feature.get("ADM2_NAME"),
      climatology_mean_mm: yearlyArr.reduce(ee.Reducer.mean(), [0]).get([0]),
      climatology_std_mm: yearlyArr.reduce(ee.Reducer.stdDev(), [0]).get([0]),
      start_year: startYear,
      end_year: endYear
    });
  });
}

// ============================================================================
// RUN — builds every export task. Go to the "Tasks" tab (top right) and
// click Run on each one after this script finishes.
// ============================================================================
EXTRA_YEARS.forEach(function(year) {
  var ndviFc = extractNdviTimeseries(year);
  Export.table.toDrive({
    collection: ndviFc,
    description: "ndvi_timeseries_" + year,
    folder: "GREEN_ALIBI_exports",
    fileNamePrefix: "ndvi_timeseries_" + year,
    fileFormat: "CSV"
  });

  var rainfallFc = ee.FeatureCollection([
    ee.Feature(null, {total_rainfall_mm: getSeasonalRainfallTotal(year), year: year})
  ]);
  Export.table.toDrive({
    collection: rainfallFc,
    description: "marathwada_rainfall_" + year,
    folder: "GREEN_ALIBI_exports",
    fileNamePrefix: "marathwada_rainfall_" + year,
    fileFormat: "CSV"
  });

  var districtRainfallFc = getDistrictSeasonalRainfall(year);
  Export.table.toDrive({
    collection: districtRainfallFc,
    description: "marathwada_rainfall_by_district_" + year,
    folder: "GREEN_ALIBI_exports",
    fileNamePrefix: "marathwada_rainfall_by_district_" + year,
    fileFormat: "CSV"
  });

  print("Queued exports for " + year + " — check the Tasks tab.");
});

var districtClimFc = getDistrictClimatology(2001, 2020);
Export.table.toDrive({
  collection: districtClimFc,
  description: "rainfall_climatology_by_district",
  folder: "GREEN_ALIBI_exports",
  fileNamePrefix: "rainfall_climatology_by_district",
  fileFormat: "CSV"
});
print("Queued per-district climatology export — check the Tasks tab.");

print("All export tasks queued. Click each one in the Tasks tab (top right) and press Run.");
print("Files will appear in a 'GREEN_ALIBI_exports' folder in your Google Drive.");
