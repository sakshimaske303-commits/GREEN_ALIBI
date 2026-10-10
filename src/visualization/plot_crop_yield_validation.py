# crop yield validation plot

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

INPUT_CSV = "data/processed/crop_yield_validation_summary.csv"
OUTPUT_PNG = "outputs/figures/crop_yield_anomaly_by_year.png"

df = pd.read_csv(INPUT_CSV).sort_values("study_year").reset_index(drop=True)
plot_df = df[df["has_yield_data"]].reset_index(drop=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [2.2, 1]})

ax = axes[0]
colors = ["#B23A48" if drought else "#2FA88C" for drought in plot_df["is_drought_year"]]
x = range(len(plot_df))
ax.bar(x, plot_df["yield_anomaly_index"], color=colors, edgecolor="black", zorder=3)
ax.axhline(0, color="gray", linestyle=":", linewidth=1)
ax.set_xticks(list(x))
ax.set_xticklabels(
    [f"{int(y)}" + (" (drought)" if d else "") for y, d in zip(plot_df["study_year"], plot_df["is_drought_year"])],
    rotation=20, ha="right"
)
ax.set_ylabel("Yield Anomaly Index (z-score vs. own 26-year mean)")
ax.set_title(f"Official Kharif crop-yield anomaly by year, Marathwada region ({len(plot_df)} years with data)",
             fontsize=11)
ax.grid(axis="y", alpha=0.25)

ax2 = axes[1]
# every year is shown as a point: with n = 2 drought years a bar of means hides how little data there is
rng_x = {True: 0, False: 1}
for is_drought, color in [(True, "#B23A48"), (False, "#2FA88C")]:
    sub = plot_df[plot_df["is_drought_year"] == is_drought]
    xs = [rng_x[is_drought]] * len(sub)
    ax2.scatter(xs, sub["yield_anomaly_index"], s=70, color=color, edgecolor="black", zorder=3)
    for xv, (yr, v) in zip(xs, zip(sub["study_year"], sub["yield_anomaly_index"])):
        ax2.annotate(str(int(yr)), (xv, v), xytext=(8, -3), textcoords="offset points", fontsize=8)
    ax2.hlines(sub["yield_anomaly_index"].mean(), rng_x[is_drought] - 0.25, rng_x[is_drought] + 0.25,
               color="black", lw=2, zorder=4)
    ax2.annotate(f"mean {sub['yield_anomaly_index'].mean():+.2f}", (rng_x[is_drought] - 0.25,
                 sub["yield_anomaly_index"].mean()), xytext=(-4, 6), textcoords="offset points",
                 ha="right", fontsize=9, fontweight="bold")
ax2.set_xticks([0, 1])
n_d = int(plot_df["is_drought_year"].sum())
ax2.set_xticklabels([f"Drought years\n(n={n_d})", f"Normal years\n(n={len(plot_df) - n_d})"])
ax2.set_xlim(-0.8, 1.6)
ax2.axhline(0, color="gray", linestyle=":", linewidth=1)
ax2.set_ylabel("Yield Anomaly Index")
_p = stats.ttest_ind(plot_df.loc[plot_df["is_drought_year"], "yield_anomaly_index"],
                     plot_df.loc[~plot_df["is_drought_year"], "yield_anomaly_index"], equal_var=False).pvalue
ax2.set_title(f"Drought vs normal years (Welch p = {_p:.2f})", fontsize=11)
ax2.grid(axis="y", alpha=0.25)

fig.suptitle("Crop-yield check: official district Kharif yield statistics vs. this study's rainfall-based drought classification",
             fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved to {OUTPUT_PNG}")
plt.close(fig)
