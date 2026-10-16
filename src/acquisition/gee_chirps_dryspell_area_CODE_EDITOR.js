// GEE Code Editor version of gee_chirps_dryspell_area.py: Trigger-1 in every CHIRPS pixel
// I run it in the Code Editor, export trigger_YYYY.tif to Drive and save them in data/external/chirps_trigger/

var FIRST_YEAR = 2015;
var LAST_YEAR = 2023;
var DRIVE_FOLDER = "GREEN_ALIBI";

var GRID = [0.05, 0, -180.0, 0, -0.05, 90.0];
var REGION = ee.Geometry.Rectangle([74.3, 17.4, 78.6, 20.9]);
var DEFICIT = 0.25, DRY_MM = 2.5, SPELL = 21;
var START_DOY = 182;   // 1 July
var END_DOY = 273;     // 30 September

var CHIRPS = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").select("precipitation");
var CLIM = CHIRPS.filter(ee.Filter.calendarRange(2001, 2020, "year"));

function triggerImage(year) {
  var start = ee.Date.fromYMD(year, 6, 1);
  var nDays = ee.Date.fromYMD(year, 10, 1).difference(start, "day");
  var days = ee.List.sequence(0, nDays.subtract(1));
  var zero = ee.Image.constant([0, 0, 0, 0, 0])
    .rename(["cum", "ncum", "run", "spell_doy", "trigger_doy"]).toFloat();

  function step(d, acc) {
    acc = ee.Image(acc);
    var date = start.advance(ee.Number(d), "day");
    var doy = date.getRelative("day", "year").add(1);
    var rain = CHIRPS.filterDate(date, date.advance(1, "day")).first().unmask(0);
    // the pixel's normal rain for this calendar day, averaged over 2001-2020
    var clim = CLIM
      .filter(ee.Filter.calendarRange(date.get("month"), date.get("month"), "month"))
      .filter(ee.Filter.calendarRange(date.get("day"), date.get("day"), "day_of_month"))
      .mean().unmask(0);
    var cum = acc.select("cum").add(rain);
    var ncum = acc.select("ncum").add(clim);
    var inWindow = ee.Number(doy).gte(START_DOY).and(ee.Number(doy).lte(END_DOY));
    var dry = rain.lt(DRY_MM).and(ee.Image.constant(inWindow));
    var run = acc.select("run").add(1).multiply(dry);
    var spell = acc.select("spell_doy");
    spell = spell.where(spell.eq(0).and(run.gte(SPELL)), ee.Image.constant(doy));
    var deficit = ee.Image.constant(1).subtract(cum.divide(ncum.max(0.1)));
    var cond = spell.gt(0).and(deficit.gt(DEFICIT)).and(ee.Image.constant(inWindow));
    var trig = acc.select("trigger_doy");
    trig = trig.where(trig.eq(0).and(cond), ee.Image.constant(doy));
    return ee.Image.cat([cum.rename("cum"), ncum.rename("ncum"), run.rename("run"),
                         spell.rename("spell_doy"), trig.rename("trigger_doy")]).toFloat();
  }

  var out = ee.Image(days.iterate(step, zero));
  return out.select(["spell_doy", "trigger_doy"]).clip(REGION);
}

// quick look: 2018 should show triggered pixels in Aurangabad and Bid (west of the region)
var check = triggerImage(2018);
Map.centerObject(REGION, 7);
Map.addLayer(check.select("trigger_doy").selfMask(),
             {min: 182, max: 273, palette: ["#fee8c8", "#e34a33"]}, "2018 trigger day (pixels that fired)");
Map.addLayer(ee.FeatureCollection("FAO/GAUL/2015/level2")
               .filter(ee.Filter.eq("ADM1_NAME", "Maharashtra")).style({color: "333333", fillColor: "00000000"}),
             {}, "district outlines");

for (var y = FIRST_YEAR; y <= LAST_YEAR; y++) {
  Export.image.toDrive({
    image: triggerImage(y),
    description: "trigger_" + y,
    folder: DRIVE_FOLDER,
    fileNamePrefix: "trigger_" + y,
    region: REGION,
    crs: "EPSG:4326",
    crsTransform: GRID,
    maxPixels: 1e9
  });
}
