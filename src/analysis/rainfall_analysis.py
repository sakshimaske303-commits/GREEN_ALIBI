import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CLIM_CSV = "data/raw/marathwada_rainfall_climatology_2001_2020.csv"
YEARS_CSV = "data/raw/marathwada_rainfall_2015_2018_2020.csv"
OUTPUT_CSV = "data/processed/rainfall_anomaly_summary.csv"
OUTPUT_PLOT = "outputs/figures/rainfall_anomaly_2015_2018_2020.png"

# --- Load data ---
clim = pd.read_csv(CLIM_CSV)
years_df = pd.read_csv(YEARS_CSV)

print("Climatology (2001-2020) years loaded:", len(clim))
print(clim.sort_values("year"))

clim_mean = clim["total_rainfall_mm"].mean()
clim_std = clim["total_rainfall_mm"].std()

print(f"\n20-year climatological mean (Jun-Dec rainfall): {clim_mean:.1f} mm")
print(f"20-year climatological std dev: {clim_std:.1f} mm")

# --- Compute anomaly for study years ---
years_df["anomaly_mm"] = years_df["total_rainfall_mm"] - clim_mean
years_df["anomaly_pct"] = (years_df["anomaly_mm"] / clim_mean) * 100
years_df["anomaly_zscore"] = years_df["anomaly_mm"] / clim_std

years_df = years_df.sort_values("year")
years_df.to_csv(OUTPUT_CSV, index=False)

print("\nRainfall anomaly summary for study years:")
print(years_df[["year", "total_rainfall_mm", "anomaly_mm", "anomaly_pct", "anomaly_zscore"]].round(2))

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 6))
colors = ["#a50026" if v < 0 else "#1a9850" for v in years_df["anomaly_pct"]]
ax.bar(years_df["year"].astype(str), years_df["anomaly_pct"], color=colors)
ax.axhline(0, color="black", linewidth=1)
ax.set_ylabel("Rainfall anomaly (% departure from 2001-2020 mean)")
ax.set_title("Marathwada Jun-Dec rainfall anomaly, by year")
for i, (y, v) in enumerate(zip(years_df["year"], years_df["anomaly_pct"])):
    ax.text(i, v + (1 if v >= 0 else -1), f"{v:.1f}%", ha="center",
            va="bottom" if v >= 0 else "top", fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"\nPlot saved to {OUTPUT_PLOT}")
plt.show()