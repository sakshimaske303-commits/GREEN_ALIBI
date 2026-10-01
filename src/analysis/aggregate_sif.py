# regional mean SIF per 8-day composite

import rasterio
import numpy as np
import pandas as pd
import glob
import os
import re
from datetime import datetime, timedelta
from rasterio.windows import from_bounds

CLIPPED_DIR = "data/processed/clipped"
FRAC_DIR = "data/external/cropland_fraction"
OUT_CSV = "data/processed/marathwada_sif_timeseries.csv"

tif_files = sorted(glob.glob(os.path.join(CLIPPED_DIR, "GOSIF_*_clipped.tif")))
print(f"Found {len(tif_files)} clipped files to aggregate.")


def cropland_window(year, sif_transform, sif_bounds, shape):
    with rasterio.open(os.path.join(FRAC_DIR, f"cropland_fraction_{year}.tif")) as fsrc:
        dx = (sif_transform.c - fsrc.transform.c) / fsrc.transform.a
        dy = (sif_transform.f - fsrc.transform.f) / fsrc.transform.e
        if abs(dx - round(dx)) > 1e-6 or abs(dy - round(dy)) > 1e-6:
            raise ValueError(f"{year}: SIF grid and cropland-fraction grid are offset by part of a pixel")
        win = from_bounds(*sif_bounds, transform=fsrc.transform).round_offsets().round_lengths()
        frac = fsrc.read(window=win).astype("float64")
    if frac.shape[1:] != shape:
        raise ValueError(f"{year}: cropland window {frac.shape[1:]} != SIF raster {shape}")
    return np.nan_to_num(frac[0]), np.nan_to_num(frac[1])


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
        transform, bounds = src.transform, src.bounds
    valid = ~np.isnan(data)
    valid_data = data[valid]

    mean_sif = np.nanmean(data) if valid_data.size > 0 else np.nan
    std_sif = np.nanstd(data) if valid_data.size > 0 else np.nan

    f1214, f12 = cropland_window(year, transform, bounds, data.shape)
    sif0 = np.where(valid, data, 0.0)
    w1214, w12 = np.where(valid, f1214, 0.0), np.where(valid, f12, 0.0)

    records.append({
        "year": year,
        "doy": doy,
        "date": date.strftime("%Y-%m-%d"),
        "mean_sif": mean_sif,
        "mean_sif_crop1214": (sif0 * w1214).sum() / w1214.sum(),
        "mean_sif_crop12": (sif0 * w12).sum() / w12.sum(),
        "mean_cropland_fraction_1214": f1214[valid].mean(),
        "std_sif": std_sif,
        "valid_pixel_count": valid_data.size,
        "total_pixel_count": data.size,
        "valid_pixel_fraction": round(valid_data.size / data.size, 3)
    })

    print(f"{filename}: mean_sif={mean_sif:.4f}, cropland-weighted={records[-1]['mean_sif_crop1214']:.4f}")

df = pd.DataFrame(records).sort_values(["year", "doy"]).reset_index(drop=True)
df.to_csv(OUT_CSV, index=False)

print(f"\nDone. Time-series saved to {OUT_CSV}")
print(f"\nQuick sanity check:")
print(df.groupby("year")[["mean_sif", "mean_sif_crop1214"]].mean().round(4))
