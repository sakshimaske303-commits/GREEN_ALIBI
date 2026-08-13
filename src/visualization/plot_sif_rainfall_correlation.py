import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

INPUT_CSV = "data/processed/sif_rainfall_district_merged.csv"
RAIN_ANOMALY_CSV = "data/processed/rainfall_anomaly_summary.csv"
OUTPUT_PNG = "outputs/figures/sif_rainfall_correlation_scatter.png"

df = pd.read_csv(INPUT_CSV)

# drought/normal label from the same anomaly_zscore < -0.5 rule used everywhere else
_rain_anomaly = pd.read_csv(RAIN_ANOMALY_CSV)
DROUGHT_YEARS = set(_rain_anomaly.loc[_rain_anomaly["anomaly_zscore"] < -0.5, "year"])
_years_sorted = sorted(df["year"].unique())
_palette = matplotlib.colormaps["tab10"].resampled(max(len(_years_sorted), 3))
YEAR_COLORS = {y: _palette(i) for i, y in enumerate(_years_sorted)}
YEAR_LABELS = {y: f"{y} ({'drought' if y in DROUGHT_YEARS else 'normal'})" for y in _years_sorted}

fig, ax = plt.subplots(figsize=(10, 8))

for year in _years_sorted:
    color = YEAR_COLORS[year]
    subset = df[df["year"] == year]
    ax.scatter(
        subset["anomaly_pct"], subset["mean_sif"],
        s=70, color=color, edgecolor="black", linewidth=0.6,
        label=YEAR_LABELS[year], zorder=3
    )
    # no per-point district labels -- at 64 points they'd just overlap into a smear

# --- regression line across ALL district-year points ---
slope, intercept, r_value, p_value, std_err = stats.linregress(df["anomaly_pct"], df["mean_sif"])
spearman_rho, spearman_p = stats.spearmanr(df["anomaly_pct"], df["mean_sif"])
x_line = np.linspace(df["anomaly_pct"].min(), df["anomaly_pct"].max(), 100)
y_line = slope * x_line + intercept
p_label = "p < 0.001" if p_value < 0.001 else f"p = {p_value:.4f}"
ax.plot(x_line, y_line, color="black", linestyle="--", linewidth=1.5, zorder=2,
        label=f"Linear fit (r = {r_value:.3f}, {p_label})")

_n_years = df["year"].nunique()
_n_districts = df["district"].nunique()
_years_range = f"{min(_years_sorted)}-{max(_years_sorted)}"
ax.set_xlabel("Rainfall Anomaly (% departure from 20-year regional normal)", fontsize=11)
ax.set_ylabel("Mean SIF", fontsize=11)
ax.set_title(f"District-Level SIF vs. Rainfall Anomaly, {_years_range} ({_n_districts} districts x {_n_years} years)\n"
             f"(Pearson r = {r_value:.3f}, Spearman ρ = {spearman_rho:.3f}, {p_label})",
             fontsize=12, pad=14)
ax.axvline(0, color="gray", linewidth=0.8, linestyle=":", zorder=1)
ax.legend(fontsize=8, loc="upper left", ncol=2)
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved scatter plot to {OUTPUT_PNG}")
plt.close(fig)