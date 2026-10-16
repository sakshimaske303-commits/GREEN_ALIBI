# GEE: rainfall Trigger-1 in every CHIRPS pixel (monsoon dry spells, 25% deficit) -> data/external/chirps_trigger/
#   python src/acquisition/gee_chirps_dryspell_area.py [first_year last_year]

import os
import sys

import ee
import geemap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gee_data_acquisition  # noqa: E402,F401  (initialises Earth Engine)

FIRST, LAST = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (2015, 2023)
OUT_DIR = "data/external/chirps_trigger"
GRID = [0.05, 0, -180.0, 0, -0.05, 90.0]
REGION = ee.Geometry.Rectangle([74.3, 17.4, 78.6, 20.9])
DEFICIT, DRY_MM, SPELL = 0.25, 2.5, 21
CHIRPS = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").select("precipitation")
CLIM = CHIRPS.filter(ee.Filter.calendarRange(2001, 2020, "year"))


def trigger_image(year):
    start = ee.Date.fromYMD(year, 6, 1)
    n_days = ee.Date.fromYMD(year, 10, 1).difference(start, "day")
    days = ee.List.sequence(0, n_days.subtract(1))
    zero = ee.Image.constant([0, 0, 0, 0, 0]).rename(["cum", "ncum", "run", "spell_doy", "trigger_doy"]).toFloat()

    def step(d, acc):
        acc = ee.Image(acc)
        date = start.advance(ee.Number(d), "day")
        doy = date.getRelative("day", "year").add(1)
        rain = CHIRPS.filterDate(date, date.advance(1, "day")).first().unmask(0)
        clim = (CLIM.filter(ee.Filter.calendarRange(date.get("month"), date.get("month"), "month"))
                    .filter(ee.Filter.calendarRange(date.get("day"), date.get("day"), "day_of_month"))
                    .mean().unmask(0))
        cum = acc.select("cum").add(rain)
        ncum = acc.select("ncum").add(clim)
        in_window = ee.Number(doy).gte(182)  # from 1 July
        dry = rain.lt(DRY_MM).And(ee.Image.constant(in_window))
        run = acc.select("run").add(1).multiply(dry)
        spell = acc.select("spell_doy")
        spell = spell.where(spell.eq(0).And(run.gte(SPELL)), ee.Image.constant(doy))
        deficit = ee.Image.constant(1).subtract(cum.divide(ncum.max(0.1)))
        cond = spell.gt(0).And(deficit.gt(DEFICIT)).And(ee.Image.constant(in_window))
        trig = acc.select("trigger_doy")
        trig = trig.where(trig.eq(0).And(cond), ee.Image.constant(doy))
        return ee.Image.cat([cum.rename("cum"), ncum.rename("ncum"), run.rename("run"),
                             spell.rename("spell_doy"), trig.rename("trigger_doy")]).toFloat()

    out = ee.Image(days.iterate(step, zero))
    return out.select(["spell_doy", "trigger_doy"]).clip(REGION)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for y in range(FIRST, LAST + 1):
        out = os.path.join(OUT_DIR, f"trigger_{y}.tif")
        geemap.ee_export_image(trigger_image(y), filename=out, region=REGION, crs="EPSG:4326",
                               crs_transform=GRID, file_per_band=False)
        print(f"  {y}: saved {out}")
    print("Next: python src/analysis/rainfall_trigger_pixel.py")
