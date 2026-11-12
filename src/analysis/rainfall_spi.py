# daily rain per district and for the region from the CHIRPS pixel stacks, and SPI at each month end
#   needs data/external/chirps_daily/ from src/acquisition/gee_chirps_dryspell_area.py

import glob
import os
import re
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manual_trigger import MONTH_ENDS, N_DAYS, spi  # noqa: E402

IN_DIR = "data/external/chirps_daily"
SPI_BASE = (1981, 2020)

files = sorted(glob.glob(os.path.join(IN_DIR, "chirps_*.tif")))
if not files:
    print(f"No files in {IN_DIR} -- run src/acquisition/gee_chirps_dryspell_area.py first (needs Earth Engine). Skipping;"
          " rainfall_trigger_comparison.py then uses the saved chirps_daily_units_jun_sep.csv.")
    sys.exit(0)

gdf = gpd.read_file("data/raw/marathwada_districts_separate.geojson")
gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf.to_crs("EPSG:4326")
gdf["district"] = gdf["ADM2_NAME"].str.strip()

with rasterio.open(files[0]) as src:
    tr, shape = src.transform, src.shape
masks = {d: ~geometry_mask([g], out_shape=shape, transform=tr) for d, g in zip(gdf["district"], gdf.geometry)}
masks["Marathwada"] = np.logical_or.reduce(list(masks.values()))

rows = []
for f in files:
    year = int(re.search(r"chirps_(\d{4})", f).group(1))
    with rasterio.open(f) as src:
        assert src.count == N_DAYS and src.transform == tr
        a = src.read().astype(float)
    for unit, m in masks.items():
        v = a[:, m].mean(1)
        rows += [{"unit": unit, "year": year, "day": i, "rain_mm": v[i]} for i in range(N_DAYS)]
D = pd.DataFrame(rows)
D["date"] = pd.to_datetime(dict(year=D["year"], month=6, day=1)) + pd.to_timedelta(D["day"], unit="D")
D.to_csv("data/processed/chirps_daily_units_jun_sep.csv", index=False)

out = []
for unit, g in D.groupby("unit"):
    cum = g.pivot(index="year", columns="day", values="rain_mm").cumsum(1)
    base = (cum.index >= SPI_BASE[0]) & (cum.index <= SPI_BASE[1])
    for me in MONTH_ENDS:
        s = spi(cum[me].to_numpy(), base)
        out += [{"unit": unit, "year": y, "month_end_day": me, "cum_mm": c, "spi": z}
                for y, c, z in zip(cum.index, cum[me], s)]
S = pd.DataFrame(out)
S.to_csv("data/processed/rainfall_spi_by_district.csv", index=False)

n_years = D["year"].nunique()
print(f"{n_years} years ({D['year'].min()}-{D['year'].max()}), {len(masks)} units; SPI base {SPI_BASE[0]}-{SPI_BASE[1]}")
print("\nSPI at 30 September, 2015-2023:")
print(S[(S["month_end_day"] == 121) & (S["year"] >= 2015)].pivot(index="unit", columns="year", values="spi").round(2).to_string())
chk = pd.read_csv("data/raw/chirps_daily_by_district_2015_2023.csv", parse_dates=["date"])
m = chk.merge(D.drop(columns="year").rename(columns={"unit": "district"}), on=["district", "date"], suffixes=("_gee", "_px"))
print(f"\nCheck against the district means exported from Earth Engine (2015-2023, Jun-Sep, n = {len(m)}): "
      f"r = {m['rain_mm_gee'].corr(m['rain_mm_px']):.3f}, seasonal totals differ by "
      f"{(m.groupby(['district', 'year'])[['rain_mm_px', 'rain_mm_gee']].sum().pipe(lambda t: 100 * (t.rain_mm_px / t.rain_mm_gee - 1)).abs().median()):.1f}% (median)")
print("\nSaved chirps_daily_units_jun_sep.csv, rainfall_spi_by_district.csv")
