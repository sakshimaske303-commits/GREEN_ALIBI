# GEE: daily CHIRPS rain in every pixel over Marathwada, 1 June - 30 September -> data/external/chirps_daily/
#   python src/acquisition/gee_chirps_dryspell_area.py [first_year last_year]
# One GeoTIFF per year with 122 bands (d000 = 1 June ... d121 = 30 September).
# src/analysis/rainfall_spi.py and rainfall_trigger_pixel.py apply the Manual's Trigger 1 to these:
# 1981-2020 give each pixel its normal rain and its SPI distribution, 2015-2023 are the study years.

import os
import sys

import ee
import geemap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gee_data_acquisition  # noqa: E402,F401  (initialises Earth Engine)

FIRST, LAST = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (1981, 2023)
OUT_DIR = "data/external/chirps_daily"
GRID = [0.05, 0, -180.0, 0, -0.05, 90.0]
REGION = ee.Geometry.Rectangle([74.3, 17.4, 78.6, 20.9])
N_DAYS = 122
CHIRPS = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").select("precipitation")


def daily_stack(year):
    col = CHIRPS.filterDate(ee.Date.fromYMD(year, 6, 1), ee.Date.fromYMD(year, 10, 1)).sort("system:time_start")
    names = [f"d{i:03d}" for i in range(N_DAYS)]
    return col.toBands().rename(names).unmask(0).clip(REGION).toFloat(), col.size()


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for y in range(FIRST, LAST + 1):
        out = os.path.join(OUT_DIR, f"chirps_{y}.tif")
        if os.path.exists(out):
            print(f"  {y}: already saved, skipping")
            continue
        img, n = daily_stack(y)
        if n.getInfo() != N_DAYS:
            raise SystemExit(f"{y}: expected {N_DAYS} daily images, found {n.getInfo()}")
        geemap.ee_export_image(img, filename=out, region=REGION, crs="EPSG:4326",
                               crs_transform=GRID, file_per_band=False)
        print(f"  {y}: saved {out}")
    print("Next: python src/analysis/rainfall_spi.py, then python src/analysis/rainfall_trigger_pixel.py")
