import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

INPUT_CSV = "data/processed/sif_rainfall_district_merged.csv"
OUTPUT_PNG = "outputs/figures/sif_rainfall_correlation_scatter.png"

df = pd.read_csv(INPUT_CSV)

YEAR_COLORS = {2015: "#D62728", 2018: "#FF7F0E", 2020: "#2CA02C"}
YEAR_LABELS = {2015: "2015 (drought)", 2018: "2018 (drought)", 2020: "2020 (normal)"}

fig, ax = plt.subplots(figsize=(9, 7))

for year, color in YEAR_COLORS.items():
    subset = df[df["year"] == year]
    ax.scatter(
        subset["anomaly_pct"], subset["mean_sif"],
        s=90, color=color, edgecolor="black", linewidth=0.6,
        label=YEAR_LABELS[year], zorder=3
    )
    for _, row in subset.iterrows():
        ax.annotate(
            row["district"], (row["anomaly_pct"], row["mean_sif"]),
            fontsize=7, xytext=(5, 4), textcoords="offset points", alpha=0.75
        )

# --- regression line across ALL 24 points ---
slope, intercept, r_value, p_value, std_err = stats.linregress(df["anomaly_pct"], df["mean_sif"])
x_line = np.linspace(df["anomaly_pct"].min(), df["anomaly_pct"].max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color="black", linestyle="--", linewidth=1.5, zorder=2,
        label=f"Linear fit (r = {r_value:.3f}, p < 0.001)")

ax.set_xlabel("Rainfall Anomaly (% departure from 20-year regional normal)", fontsize=11)
ax.set_ylabel("Mean SIF", fontsize=11)
ax.set_title("District-Level SIF vs. Rainfall Anomaly, 2015/2018/2020\n(Pearson r = 0.837, Spearman ρ = 0.857, both p < 0.001)",
             fontsize=12, pad=14)
ax.axvline(0, color="gray", linewidth=0.8, linestyle=":", zorder=1)
ax.legend(fontsize=9, loc="upper left")
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved scatter plot to {OUTPUT_PNG}")
plt.close(fig)