# SIF vs NDVI seasonal comparison

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

SIF_CSV = "data/processed/marathwada_sif_timeseries.csv"
NDVI_CSV = "data/raw/ndvi_obsdate_2015_2023.csv"
OUT_CSV = "data/processed/marathwada_sif_ndvi_merged.csv"
OUT_DIR = "outputs/figures"
os.makedirs(OUT_DIR, exist_ok=True)

SIF_COL = "mean_sif_crop1214"
LOW_COVERAGE = 0.25

_rain_anomaly = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(_rain_anomaly.loc[_rain_anomaly["anomaly_zscore"] < -0.5, "year"])


def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


sif = pd.read_csv(SIF_CSV)
ndvi = pd.read_csv(NDVI_CSV)

merged_years = []
for year in sorted(sif["year"].unique()):
    s = sif[sif["year"] == year].sort_values("doy")
    n = ndvi[ndvi["year"] == year].sort_values("doy_start")
    t = s["doy"].values + 3.5
    ndvi_interp = np.interp(t, n["mean_obs_doy"].values, n["mean_ndvi"].values, left=np.nan, right=np.nan)
    ndvi_norm = np.interp(t, n["mean_obs_doy"].values, minmax(n["mean_ndvi"].values), left=np.nan, right=np.nan)
    merged_years.append(pd.DataFrame({
        "year": year,
        "sif_start_doy": s["doy"].values,
        "doy": t,
        "date": s["date"].values,
        "mean_sif": s[SIF_COL].values,
        "mean_sif_all": s["mean_sif"].values,
        "mean_ndvi": ndvi_interp,
        "sif_norm": minmax(s[SIF_COL].values),
        "ndvi_norm": ndvi_norm,
    }))

merged = pd.concat(merged_years).reset_index(drop=True)
merged.to_csv(OUT_CSV, index=False)
print(merged[["year", "doy", "mean_sif", "mean_ndvi", "sif_norm", "ndvi_norm"]])

years = sorted(merged["year"].unique())
ncols = 4
nrows = math.ceil(len(years) / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4.5 * nrows), sharey=True)
axes = axes.flatten()
for ax, year in zip(axes, years):
    sub = merged[merged["year"] == year]
    n = ndvi[ndvi["year"] == year].sort_values("doy_start")
    ax.plot(sub["doy"], sub["sif_norm"], marker="o", label="SIF (cropland-weighted, normalized)", color="#2FA88C")
    nn = minmax(n["mean_ndvi"].values)
    ax.plot(n["mean_obs_doy"], nn, marker="s", label="NDVI (at actual observation day)", color="#D98E30")
    low = (n["valid_pixel_count"] / ndvi["valid_pixel_count"].max()).values < LOW_COVERAGE
    ax.plot(n["mean_obs_doy"].values[low], nn[low], "s", mfc="white", mec="#D98E30",
            label=f"NDVI composite with < {LOW_COVERAGE:.0%} of cropland pixels observed")
    ax.set_title(f"{year}" + (" — drought year" if year in DROUGHT_YEARS else " — normal monsoon year"))
    ax.set_xlabel("Day of Year")
    ax.grid(alpha=0.3)
for ax in axes[len(years):]:
    ax.set_visible(False)
for ax in axes[::ncols]:
    ax.set_ylabel("Normalized value (0–1 within year)")
fig.suptitle(f"SIF vs NDVI seasonal trajectory — Marathwada, {len(years)} years")
plt.tight_layout()
# legend in the empty panel space, so it covers no data
handles, labels = axes[0].get_legend_handles_labels()
spare = axes[len(years)] if len(years) < len(axes) else None
if spare is not None:
    spare.set_visible(True)
    spare.axis("off")
    spare.legend(handles, labels, loc="center", fontsize=10, frameon=False)
else:
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=9)
plt.savefig(os.path.join(OUT_DIR, "sif_vs_ndvi_seasonal_v2.png"), dpi=150)
plt.show()
