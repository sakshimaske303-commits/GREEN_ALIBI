import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

MERGED_CSV = "data/processed/marathwada_sif_ndvi_merged.csv"
OUT_DIR = "outputs/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# drought classification from data (anomaly_zscore < -0.5), see compare_sif_ndvi.py
_rain_anomaly = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(_rain_anomaly.loc[_rain_anomaly["anomaly_zscore"] < -0.5, "year"])
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]

df = pd.read_csv(MERGED_CSV)

# Normalize each series 0-1 within its own year (peak = 1, seasonal min = 0)
df["sif_norm"] = df.groupby("year")["mean_sif"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
df["ndvi_norm"] = df.groupby("year")["mean_ndvi"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))


def find_crossing_doy(doys, values, threshold):
    """Linearly-interpolated DOY at which a declining series first drops
    below `threshold`. Returns NaN if it never crosses within the window."""
    for i in range(len(values) - 1):
        v1, v2 = values[i], values[i + 1]
        if v1 >= threshold and v2 < threshold:
            d1, d2 = doys[i], doys[i + 1]
            frac = (v1 - threshold) / (v1 - v2)
            return d1 + frac * (d2 - d1)
    return np.nan


records = []

for year in sorted(df["year"].unique()):
    sub = df[df["year"] == year].sort_values("doy").reset_index(drop=True)

    sif_peak_doy = sub.loc[sub["sif_norm"].idxmax(), "doy"]
    ndvi_peak_doy = sub.loc[sub["ndvi_norm"].idxmax(), "doy"]

    # Restrict to each series' own decline phase (from its own peak onward)
    sif_decline = sub[sub["doy"] >= sif_peak_doy]
    ndvi_decline = sub[sub["doy"] >= ndvi_peak_doy]

    for t in THRESHOLDS:
        sif_cross = find_crossing_doy(sif_decline["doy"].values, sif_decline["sif_norm"].values, t)
        ndvi_cross = find_crossing_doy(ndvi_decline["doy"].values, ndvi_decline["ndvi_norm"].values, t)
        lag = ndvi_cross - sif_cross if not (np.isnan(sif_cross) or np.isnan(ndvi_cross)) else np.nan

        records.append({
            "year": year,
            "is_drought_year": year in DROUGHT_YEARS,
            "threshold": t,
            "sif_crossing_doy": round(sif_cross, 1) if not np.isnan(sif_cross) else None,
            "ndvi_crossing_doy": round(ndvi_cross, 1) if not np.isnan(ndvi_cross) else None,
            "lag_days": round(lag, 1) if not np.isnan(lag) else None
        })

lag_df = pd.DataFrame(records)
lag_df.to_csv("data/processed/sif_ndvi_lag_by_threshold.csv", index=False)

print("Per-threshold crossing dates and lag (days):\n")
print(lag_df.to_string(index=False))

print("\nMean lag per year (across all thresholds that resolved):")
print(lag_df.groupby("year")["lag_days"].mean().round(1))

print("\nMean lag: drought years vs normal year:")
print(lag_df.groupby("is_drought_year")["lag_days"].mean().round(1))

# Plot: lag (days) by threshold, one line per year
fig, ax = plt.subplots(figsize=(9, 6))
_years_for_palette = sorted(lag_df["year"].unique())
_palette = matplotlib.colormaps["tab10"].resampled(max(len(_years_for_palette), 3))
colors = {y: _palette(i) for i, y in enumerate(_years_for_palette)}
for year in sorted(lag_df["year"].unique()):
    sub = lag_df[lag_df["year"] == year]
    label = f"{year}" + (" (drought)" if year in DROUGHT_YEARS else " (normal)")
    ax.plot(sub["threshold"], sub["lag_days"], marker="o", label=label, color=colors.get(year))

ax.set_xlabel("Decline threshold (fraction of seasonal peak)")
ax.set_ylabel("NDVI lag behind SIF (days)")
ax.set_title("SIF-to-NDVI decline lag, by threshold and year — Marathwada")
ax.invert_xaxis()
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "sif_ndvi_lag_by_threshold.png"), dpi=150)
print(f"\nPlot saved to {OUT_DIR}/sif_ndvi_lag_by_threshold.png")
plt.show()