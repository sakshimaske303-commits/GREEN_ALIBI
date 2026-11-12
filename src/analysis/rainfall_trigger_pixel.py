# the Manual's Trigger 1 in every CHIRPS pixel, summarised per district, against the SIF and NDVI alarms
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
from manual_trigger import MONTH_ENDS, VARIANTS, day_to_doy, spi, trigger_day  # noqa: E402

IN_DIR = "data/external/chirps_daily"
BASELINE, SPI_BASE, YEARS = (2001, 2020), (1981, 2020), range(2001, 2024)
SHARES = [0.25, 0.50]

files = sorted(glob.glob(os.path.join(IN_DIR, "chirps_*.tif")))
if not files:
    print(f"No files in {IN_DIR} -- run src/acquisition/gee_chirps_dryspell_area.py first (needs Earth Engine). Skipping.")
    sys.exit(0)

stack = {}
for f in files:
    with rasterio.open(f) as src:
        stack[int(re.search(r"chirps_(\d{4})", f).group(1))] = src.read().astype(float)
        tr, shape = src.transform, src.shape
years = np.array(sorted(stack))
A = np.stack([stack[y] for y in years])  # (year, day, row, col)
normal = A[(years >= BASELINE[0]) & (years <= BASELINE[1])].mean(0)  # each pixel's normal daily rain
cum = A.cumsum(1)[:, MONTH_ENDS]  # (year, 3, row, col)
base = (years >= SPI_BASE[0]) & (years <= SPI_BASE[1])
gdf = gpd.read_file("data/raw/marathwada_districts_separate.geojson")
gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf.to_crs("EPSG:4326")
gdf["district"] = gdf["ADM2_NAME"].str.strip()
inside = np.logical_or.reduce([~geometry_mask([g], out_shape=shape, transform=tr) for g in gdf.geometry])
rr, cc = np.where(inside)
Z = np.full(cum.shape, np.nan)
for r, c in zip(rr, cc):
    for k in range(len(MONTH_ENDS)):
        Z[:, k, r, c] = spi(cum[:, k, r, c], base)

sat = pd.read_csv("data/processed/drought_signal_district.csv")
rows = []
for v, (weeks, first_day) in VARIANTS.items():
    for y in YEARS:
        i = int(np.where(years == y)[0][0])
        day, _ = trigger_day(A[i][:, rr, cc], normal[:, rr, cc], Z[i][:, rr, cc], weeks, first_day)
        img = np.full(shape, np.nan)
        img[rr, cc] = [day_to_doy(y, d) for d in day]
        for d, geom in zip(gdf["district"], gdf.geometry):
            vals = img[~geometry_mask([geom], out_shape=shape, transform=tr)]
            fired = np.sort(vals[np.isfinite(vals)])
            rec = {"variant": v, "district": d, "year": y, "n_pixels": len(vals),
                   "share_triggered": len(fired) / len(vals) if len(vals) else np.nan}
            for s in SHARES:
                k = int(np.ceil(s * len(vals)))
                rec[f"doy_{int(s * 100)}pct_triggered"] = fired[k - 1] if 0 < k <= len(fired) else np.nan
            rows.append(rec)
P = pd.DataFrame(rows).merge(sat[["district", "year", "is_drought", "SIF_alarm_-3.0", "NDVI_alarm_-3.0"]],
                             on=["district", "year"], how="left")
P.to_csv("data/processed/rainfall_trigger_pixel_by_district.csv", index=False)

pd.set_option("display.width", 200)
for v in VARIANTS:
    Q = P[(P["variant"] == v) & (P["year"] >= 2015)]
    print(f"\n{v}\nShare of each district's pixels where Trigger 1 was met by 30 Sep, 2015-2023 (%):")
    print((Q.pivot(index="district", columns="year", values="share_triggered") * 100).round(0).to_string())
    for s in SHARES:
        col = f"doy_{int(s * 100)}pct_triggered"
        dr, nr = Q[Q["is_drought"] == True], Q[Q["is_drought"] == False]  # noqa: E712
        print(f"Trigger met on {s:.0%} of district area: drought {dr[col].notna().sum()}/{len(dr)}, "
              f"normal {nr[col].notna().sum()}/{len(nr)} district-years")
        for sig in ["SIF", "NDVI"]:
            both = dr.dropna(subset=[col, f"{sig}_alarm_-3.0"])
            diff = both[f"{sig}_alarm_-3.0"] - both[col]
            if len(both):
                print(f"  {sig} alarm minus trigger date: n = {len(both)}, satellite earlier in {(diff < 0).sum()}, "
                      f"median {diff.median():+.0f} d")
print("\nSaved data/processed/rainfall_trigger_pixel_by_district.csv")
