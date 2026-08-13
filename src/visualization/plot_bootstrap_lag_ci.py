import pandas as pd
import matplotlib.pyplot as plt

INPUT_CSV = "data/processed/cross_correlation_lag_bootstrap_ci.csv"
OUTPUT_PNG = "outputs/figures/cross_correlation_lag_bootstrap_ci.png"

df = pd.read_csv(INPUT_CSV).sort_values("year").reset_index(drop=True)

fig, ax = plt.subplots(figsize=(max(9, 1.2 * len(df)), 6))

colors = ["#B23A48" if drought else "#2FA88C" for drought in df["is_drought_year"]]
x = range(len(df))

lower_err = df["point_estimate_lag_days"] - df["ci_2.5pct_days"]
upper_err = df["ci_97.5pct_days"] - df["point_estimate_lag_days"]

ax.errorbar(x, df["point_estimate_lag_days"], yerr=[lower_err, upper_err],
            fmt="none", ecolor="black", elinewidth=1.5, capsize=6, zorder=2)
ax.scatter(x, df["point_estimate_lag_days"], s=110, c=colors, edgecolor="black", zorder=3)

for i, row in df.iterrows():
    ax.annotate(f"{row['pct_replicates_lag_geq_0']:.0f}% ≥ 0", (i, row["ci_97.5pct_days"]),
                xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8, color="#555555")

ax.axhline(0, color="gray", linestyle=":", linewidth=1)
ax.set_xticks(list(x))
ax.set_xticklabels([f"{int(y)}" + (" (drought)" if d else "") for y, d in zip(df["year"], df["is_drought_year"])],
                    rotation=20, ha="right")
ax.set_ylabel("Cross-correlation-maximizing lag, NDVI behind SIF (days)")
ax.set_title(f"Bootstrap 95% CI on cross-correlation lag, {len(df)} years "
             f"(2,000 case-resampling replicates per year)", fontsize=12)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved to {OUTPUT_PNG}")
plt.close(fig)
