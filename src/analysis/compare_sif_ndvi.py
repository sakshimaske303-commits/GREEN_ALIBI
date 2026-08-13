import math
import pandas as pd
import matplotlib.pyplot as plt
import os

SIF_CSV = "data/processed/marathwada_sif_timeseries.csv"
NDVI_CSV = "data/raw/marathwada_ndvi_mod13q1_timeseries_8years.csv"  # 8-year consolidated export
OUT_DIR = "outputs/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# drought year = Jun-Dec rainfall anomaly z-score < -0.5 vs 2001-2020 mean,
# same rule as rainfall_analysis.py. Only 2015 and 2018 clear it at 8 years.
_rain_anomaly = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(_rain_anomaly.loc[_rain_anomaly["anomaly_zscore"] < -0.5, "year"])

sif = pd.read_csv(SIF_CSV).rename(columns={
    "valid_pixel_count": "sif_valid_pixel_count",
    "valid_pixel_fraction": "sif_valid_pixel_fraction"
})
ndvi = pd.read_csv(NDVI_CSV).rename(columns={"valid_pixel_count": "ndvi_valid_pixel_count"})

merged_years = []
for year in sorted(sif["year"].unique()):
    sif_y = sif[sif["year"] == year].sort_values("doy")
    ndvi_y = ndvi[ndvi["year"] == year].sort_values("doy")
    m = pd.merge_asof(sif_y, ndvi_y, on="doy", by="year", direction="nearest")
    merged_years.append(m)

merged = pd.concat(merged_years).reset_index(drop=True)
merged.to_csv("data/processed/marathwada_sif_ndvi_merged.csv", index=False)
print(merged[["year", "doy", "mean_sif", "mean_ndvi"]])

merged["sif_norm"] = merged.groupby("year")["mean_sif"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
merged["ndvi_norm"] = merged.groupby("year")["mean_ndvi"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

years = sorted(merged["year"].unique())
ncols = 4  # wrap into a grid instead of one long row of 8 panels
nrows = math.ceil(len(years) / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4.5 * nrows), sharey=True)
axes = axes.flatten()
for ax, year in zip(axes, years):
    sub = merged[merged["year"] == year]
    ax.plot(sub["doy"], sub["sif_norm"], marker="o", label="SIF (normalized)", color="#2FA88C")
    ax.plot(sub["doy"], sub["ndvi_norm"], marker="s", label="NDVI (normalized, cloud-screened)", color="#D98E30")
    ax.set_title(f"{year}" + (" — drought year" if year in DROUGHT_YEARS else " — normal monsoon year"))
    ax.set_xlabel("Day of Year")
    ax.grid(alpha=0.3)
for ax in axes[len(years):]:
    ax.set_visible(False)
axes[0].set_ylabel("Normalized value (0–1 within year)")
axes[0].legend()
fig.suptitle("SIF vs NDVI (cloud-screened) seasonal trajectory — Marathwada, 8 years")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "sif_vs_ndvi_seasonal_v2.png"), dpi=150)
plt.show()