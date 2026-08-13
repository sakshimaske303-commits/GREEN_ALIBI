import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

INPUT_CSV = "data/processed/spatial_autocorrelation_morans_i.csv"
OUTPUT_PNG = "outputs/figures/spatial_autocorrelation_morans_i.png"

df = pd.read_csv(INPUT_CSV)
years = sorted(df["year"].unique())
x = np.arange(len(years))
width = 0.35

sif_vals = [df[(df["year"] == y) & (df["variable"] == "mean_sif")]["morans_i"].iloc[0] for y in years]
sif_sig = [df[(df["year"] == y) & (df["variable"] == "mean_sif")]["p_value_permutation"].iloc[0] < 0.05 for y in years]
rain_vals = [df[(df["year"] == y) & (df["variable"] == "rainfall_anomaly_pct")]["morans_i"].iloc[0] for y in years]
rain_sig = [df[(df["year"] == y) & (df["variable"] == "rainfall_anomaly_pct")]["p_value_permutation"].iloc[0] < 0.05 for y in years]

fig, ax = plt.subplots(figsize=(max(10, 1.3 * len(years)), 6))

bars_sif = ax.bar(x - width / 2, sif_vals, width, label="Mean SIF", color="#2FA88C")
bars_rain = ax.bar(x + width / 2, rain_vals, width, label="Rainfall anomaly (%)", color="#5B8FD9")

for bars, sig_flags in [(bars_sif, sif_sig), (bars_rain, rain_sig)]:
    for bar, sig in zip(bars, sig_flags):
        if sig:
            ax.annotate("*", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        ha="center", va="bottom", fontsize=14, fontweight="bold")

expected_i = df["expected_i_under_null"].iloc[0]
ax.axhline(expected_i, color="gray", linestyle=":", linewidth=1.2,
           label=f"Expected I under spatial randomness ({expected_i:.2f})")
ax.axhline(0, color="black", linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years])
ax.set_xlabel("Year")
ax.set_ylabel("Moran's I")
n_sig = int((df["p_value_permutation"] < 0.05).sum())
ax.set_title(f"Spatial autocorrelation (Moran's I) by year, {len(years)} years — "
             f"* = significant at p<0.05 ({n_sig} of {len(df)} year x variable combinations)", fontsize=12)
ax.legend(fontsize=9, loc="upper right")
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved to {OUTPUT_PNG}")
plt.close(fig)
