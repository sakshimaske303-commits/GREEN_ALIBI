import pandas as pd
import matplotlib.pyplot as plt

INPUT_CSV = "data/processed/crop_yield_validation_summary.csv"
OUTPUT_PNG = "outputs/figures/crop_yield_anomaly_by_year.png"

df = pd.read_csv(INPUT_CSV).sort_values("study_year").reset_index(drop=True)
plot_df = df[df["has_yield_data"]].reset_index(drop=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [2.2, 1]})

# Left panel: Yield Anomaly Index by year
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

# Right panel: grouped mean, drought vs normal
ax2 = axes[1]
grp = plot_df.groupby("is_drought_year")["yield_anomaly_index"].agg(["mean", "count"])
labels = []
means = []
bar_colors = []
for is_drought, color, label in [(True, "#B23A48", "Drought years"), (False, "#2FA88C", "Normal years")]:
    if is_drought in grp.index:
        n = int(grp.loc[is_drought, "count"])
        labels.append(f"{label}\n(n={n})")
        means.append(grp.loc[is_drought, "mean"])
        bar_colors.append(color)
ax2.bar(labels, means, color=bar_colors, edgecolor="black", zorder=3)
ax2.axhline(0, color="gray", linestyle=":", linewidth=1)
ax2.set_ylabel("Mean Yield Anomaly Index")
ax2.set_title("Grouped comparison", fontsize=11)
ax2.grid(axis="y", alpha=0.25)
for i, v in enumerate(means):
    ax2.annotate(f"{v:.2f}", (i, v), xytext=(0, 6 if v >= 0 else -14), textcoords="offset points",
                 ha="center", fontsize=10, fontweight="bold")

fig.suptitle("Ground-truth validation: official government crop-yield statistics vs. this study's drought classification",
             fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved to {OUTPUT_PNG}")
plt.close(fig)
