// GEE Code Editor version of gee_extended_years.py

var EXTRA_YEARS = [2021];

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

function getCroplandMask(year) {
  var lc = ee.ImageCollection("MODIS/061/MCD12Q1")
    .filter(ee.Filter.calendarRange(year, year, "year"))
    .first()
    .select("LC_Type1");
  return lc.eq(12).or(lc.eq(14));
}

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

      doy: img.date().getRelative("day", "year").add(1),
      mean_ndvi: stats.get("NDVI_mean"),
      ndvi_valid_pixel_count: stats.get("NDVI_count")
    });
  });
  return ee.FeatureCollection(fc);
}

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
    scale: 5566,
    maxPixels: 1e9
  });
  return stats.get("precipitation");
}

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
