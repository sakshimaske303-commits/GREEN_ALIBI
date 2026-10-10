# region seasonal rainfall anomaly

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TOTALS_CSV = "data/raw/chirps_seasonal_totals_1981_2023.csv"
BASELINE = (2001, 2020)
STUDY_YEARS = list(range(2015, 2024))
OUTPUT_CSV = "data/processed/rainfall_anomaly_summary.csv"
OUTPUT_PLOT = "outputs/figures/rainfall_anomaly_2015_2023.png"

tot = pd.read_csv(TOTALS_CSV)
region = tot[tot["unit"] == "Marathwada"].rename(columns={"rainfall_mm": "total_rainfall_mm"})
clim = region[region["year"].between(*BASELINE)]
assert len(clim) == BASELINE[1] - BASELINE[0] + 1, "baseline years missing from the export"
years_df = region[region["year"].isin(STUDY_YEARS)][["year", "total_rainfall_mm"]].copy()
assert len(years_df) == len(STUDY_YEARS), "study years missing from the export"

print(f"Climatology ({BASELINE[0]}-{BASELINE[1]}) years loaded:", len(clim))
clim_mean = clim["total_rainfall_mm"].mean()
clim_std = clim["total_rainfall_mm"].std()

print(f"\n20-year climatological mean (Jun-Dec rainfall): {clim_mean:.1f} mm")
print(f"20-year climatological std dev: {clim_std:.1f} mm")

years_df["anomaly_mm"] = years_df["total_rainfall_mm"] - clim_mean
years_df["anomaly_pct"] = (years_df["anomaly_mm"] / clim_mean) * 100
years_df["anomaly_zscore"] = years_df["anomaly_mm"] / clim_std

years_df = years_df.sort_values("year")
years_df.to_csv(OUTPUT_CSV, index=False)

print("\nRainfall anomaly summary for study years:")
print(years_df[["year", "total_rainfall_mm", "anomaly_mm", "anomaly_pct", "anomaly_zscore"]].round(2))

fig, ax = plt.subplots(figsize=(8, 6))
# dark red = drought year (z < -0.5); pale red = below the mean but not a drought year
colors = ["#a50026" if z < -0.5 else ("#f4a582" if v < 0 else "#1a9850")
          for v, z in zip(years_df["anomaly_pct"], years_df["anomaly_zscore"])]
ax.bar(years_df["year"].astype(str), years_df["anomaly_pct"], color=colors)
ax.axhline(-0.5 * clim_std / clim_mean * 100, color="#a50026", ls="--", lw=1,
           label=f"drought criterion: z < -0.5 ({-0.5 * clim_std / clim_mean * 100:.1f}%)")
ax.legend(loc="upper left", fontsize=9)
lo, hi = years_df["anomaly_pct"].min(), years_df["anomaly_pct"].max()
ax.set_ylim(lo - 0.25 * (hi - lo), hi + 0.22 * (hi - lo))
ax.axhline(0, color="black", linewidth=1)
ax.set_ylabel("Rainfall anomaly (% departure from 2001-2020 mean)")
ax.set_title("Marathwada CHIRPS rainfall anomaly, 1 Jun - 26 Dec, vs 2001-2020 mean")
for i, (y, v, z) in enumerate(zip(years_df["year"], years_df["anomaly_pct"], years_df["anomaly_zscore"])):
    ax.text(i, v + (1 if v >= 0 else -1), f"{v:.1f}%\n(z {z:+.2f})" if v < 0 else f"(z {z:+.2f})\n{v:.1f}%", ha="center",
            va="bottom" if v >= 0 else "top", fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"\nPlot saved to {OUTPUT_PLOT}")
plt.show()
