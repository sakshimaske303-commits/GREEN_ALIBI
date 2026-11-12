// GEE Code Editor version of gee_chirps_dryspell_area.py: daily CHIRPS rain, 1 June - 30 September, every pixel
// I run it in the Code Editor, export chirps_YYYY.tif to Drive and save them in data/external/chirps_daily/

var FIRST_YEAR = 1981;
var LAST_YEAR = 2023;
var DRIVE_FOLDER = "GREEN_ALIBI";

var GRID = [0.05, 0, -180.0, 0, -0.05, 90.0];
var REGION = ee.Geometry.Rectangle([74.3, 17.4, 78.6, 20.9]);
var CHIRPS = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").select("precipitation");

function dailyStack(year) {
  var col = CHIRPS.filterDate(ee.Date.fromYMD(year, 6, 1), ee.Date.fromYMD(year, 10, 1)).sort("system:time_start");
  var names = ee.List.sequence(0, 121).map(function (i) {
    return ee.String("d").cat(ee.Number(i).format("%03d"));
  });
  return col.toBands().rename(names).unmask(0).clip(REGION).toFloat();
}

print("daily images in 2018 (should be 122):",
      CHIRPS.filterDate("2018-06-01", "2018-10-01").size());

for (var y = FIRST_YEAR; y <= LAST_YEAR; y++) {
  Export.image.toDrive({
    image: dailyStack(y),
    description: "chirps_" + y,
    folder: DRIVE_FOLDER,
    fileNamePrefix: "chirps_" + y,
    region: REGION,
    crs: "EPSG:4326",
    crsTransform: GRID,
    maxPixels: 1e9
  });
}
