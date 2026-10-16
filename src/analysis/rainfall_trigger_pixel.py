# pixel-level Trigger-1 summarised per district, against the SIF and NDVI alarms

import glob
import os
import re
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask

IN_DIR = "data/external/chirps_trigger"
SHARES = [0.25, 0.50]

files = sorted(glob.glob(os.path.join(IN_DIR, "trigger_*.tif")))
if not files:
    print(f"No files in {IN_DIR} -- run src/acquisition/gee_chirps_dryspell_area.py first (needs Earth Engine). Skipping.")
    sys.exit(0)

gdf = gpd.read_file("data/raw/marathwada_districts_separate.geojson")
gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf.to_crs("EPSG:4326")
gdf["district"] = gdf["ADM2_NAME"].str.strip()
sat = pd.read_csv("data/processed/drought_signal_district.csv")

rows = []
for f in files:
    year = int(re.search(r"trigger_(\d{4})", f).group(1))
    with rasterio.open(f) as src:
        trig = src.read(2).astype(float)
        tr, shape = src.transform, src.shape
    for d, geom in zip(gdf["district"], gdf.geometry):
        inside = ~geometry_mask([geom], out_shape=shape, transform=tr)
        v = trig[inside]
        v = v[np.isfinite(v)]
        fired = np.sort(v[v > 0])
        rec = {"district": d, "year": year, "n_pixels": len(v),
               "share_triggered": len(fired) / len(v) if len(v) else np.nan}
        for s in SHARES:
            k = int(np.ceil(s * len(v)))
            rec[f"doy_{int(s * 100)}pct_triggered"] = fired[k - 1] if 0 < k <= len(fired) else np.nan
        rows.append(rec)
P = pd.DataFrame(rows).merge(sat[["district", "year", "is_drought", "SIF_alarm_-3.0", "NDVI_alarm_-3.0"]],
                             on=["district", "year"], how="left")
P.to_csv("data/processed/rainfall_trigger_pixel_by_district.csv", index=False)

pd.set_option("display.width", 200)
print("Share of each district's pixels where Trigger-1 fired (1 Jul - 30 Sep):")
print((P.pivot(index="district", columns="year", values="share_triggered") * 100).round(0).to_string())
for s in SHARES:
    col = f"doy_{int(s * 100)}pct_triggered"
    dr = P[P["is_drought"] == True]  # noqa: E712
    nr = P[P["is_drought"] == False]  # noqa: E712
    print(f"\nTrigger reached {s:.0%} of district area: drought {dr[col].notna().sum()}/{len(dr)}, "
          f"normal {nr[col].notna().sum()}/{len(nr)} district-years")
    for v in ["SIF", "NDVI"]:
        both = dr.dropna(subset=[col, f"{v}_alarm_-3.0"])
        diff = both[f"{v}_alarm_-3.0"] - both[col]
        if len(both):
            print(f"  {v} alarm minus trigger date: n = {len(both)}, satellite earlier in {(diff < 0).sum()}, "
                  f"median {diff.median():+.0f} d")
print("\nSaved data/processed/rainfall_trigger_pixel_by_district.csv")
