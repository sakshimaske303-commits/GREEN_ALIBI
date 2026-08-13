import rasterio
import numpy as np
import pandas as pd
import glob
import os
import re
from datetime import datetime, timedelta

CLIPPED_DIR = "data/processed/clipped"
OUT_CSV = "data/processed/marathwada_sif_timeseries.csv"

# Must match clip_gosif.py's output naming exactly: "GOSIF_<year><doy>_clipped.tif".
# Old glob matched files without the "_clipped" suffix too and silently picked up
# stale pre-boundary-fix rasters -- tightened it so that can't happen again.
tif_files = sorted(glob.glob(os.path.join(CLIPPED_DIR, "GOSIF_*_clipped.tif")))
print(f"Found {len(tif_files)} clipped files to aggregate.")

records = []

for filepath in tif_files:
    filename = os.path.basename(filepath)
    match = re.search(r"GOSIF_(\d{4})(\d{3})_clipped\.tif", filename)
    if not match:
        print(f"Skipping unrecognized filename: {filename}")
        continue

    year = int(match.group(1))
    doy = int(match.group(2))
    date = datetime(year, 1, 1) + timedelta(days=doy - 1)

    with rasterio.open(filepath) as src:
        data = src.read(1)
        valid_data = data[~np.isnan(data)]

        mean_sif = np.nanmean(data) if valid_data.size > 0 else np.nan
        std_sif = np.nanstd(data) if valid_data.size > 0 else np.nan
        valid_pixel_count = valid_data.size
        total_pixel_count = data.size

    records.append({
        "year": year,
        "doy": doy,
        "date": date.strftime("%Y-%m-%d"),
        "mean_sif": mean_sif,
        "std_sif": std_sif,
        "valid_pixel_count": valid_pixel_count,
        "total_pixel_count": total_pixel_count,
        "valid_pixel_fraction": round(valid_pixel_count / total_pixel_count, 3)
    })

    print(f"{filename}: mean_sif={mean_sif:.4f}, valid_fraction={valid_pixel_count/total_pixel_count:.2%}")

df = pd.DataFrame(records).sort_values(["year", "doy"]).reset_index(drop=True)
df.to_csv(OUT_CSV, index=False)

print(f"\nDone. Time-series saved to {OUT_CSV}")
print(f"\nQuick sanity check:")
print(df.groupby("year")["mean_sif"].agg(["mean", "min", "max"]))