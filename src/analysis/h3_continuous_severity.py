# H3 as a continuous severity test

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

RAINFALL_CSV = "data/processed/rainfall_anomaly_summary.csv"
LAG_CSV = "data/processed/sif_ndvi_lag_by_threshold.csv"
OUTPUT_CSV = "data/processed/h3_continuous_severity_correlation.csv"
OUTPUT_PLOT = "outputs/figures/h3_continuous_severity_scatter.png"

rain = pd.read_csv(RAINFALL_CSV)[["year", "anomaly_pct", "anomaly_zscore"]]
lag = pd.read_csv(LAG_CSV).groupby("year", as_index=False)["lag_days"].mean()

df = rain.merge(lag, on="year").sort_values("year").reset_index(drop=True)
df["is_drought_year"] = df["anomaly_zscore"] < -0.5

pearson_r, pearson_p = stats.pearsonr(df["anomaly_pct"], df["lag_days"])
spearman_rho, spearman_p = stats.spearmanr(df["anomaly_pct"], df["lag_days"])
slope, intercept, lr_r, lr_p, lr_se = stats.linregress(df["anomaly_pct"], df["lag_days"])

print("Rainfall anomaly (%) vs. mean SIF-to-NDVI lag (days), n = 9 years:\n")
print(df[["year", "anomaly_pct", "anomaly_zscore", "is_drought_year", "lag_days"]].round(2).to_string(index=False))
print(f"\nPearson r  = {pearson_r:.4f}  (p = {pearson_p:.4f})")
print(f"Spearman rho = {spearman_rho:.4f}  (p = {spearman_p:.4f})")
print(f"OLS slope  = {slope:.4f} days per percentage-point of anomaly  (p = {lr_p:.4f}, se = {lr_se:.4f})")
print("\nH3 predicts anomaly_pct and lag_days move in OPPOSITE directions (r < 0).")
print(f"Observed direction: r is {'negative, matching H3' if pearson_r < 0 else 'positive, opposite of H3'}.")

df["pearson_r"] = pearson_r
df["pearson_p"] = pearson_p
df["spearman_rho"] = spearman_rho
df["spearman_p"] = spearman_p
df["ols_slope_days_per_pct"] = slope
df["ols_p"] = lr_p
df.to_csv(OUTPUT_CSV, index=False)
print(f"\nSaved to {OUTPUT_CSV}")

fig, ax = plt.subplots(figsize=(8, 6))
colors = ["#B23A48" if d else "#2FA88C" for d in df["is_drought_year"]]
ax.scatter(df["anomaly_pct"], df["lag_days"], c=colors, s=90, edgecolors="white", linewidths=1, zorder=3)
for _, row in df.iterrows():
    ax.annotate(str(int(row["year"])), (row["anomaly_pct"], row["lag_days"]),
                textcoords="offset points", xytext=(6, 6), fontsize=9)
xs = df["anomaly_pct"].sort_values()
ax.plot(xs, intercept + slope * xs, color="#888888", linestyle="--", linewidth=1.5, zorder=2,
        label=f"OLS fit (r={pearson_r:.2f}, p={pearson_p:.2f})")
ax.axvline(0, color="black", linewidth=0.8, alpha=0.4)
ax.set_xlabel("Rainfall anomaly (% departure from 2001-2020 mean)")
ax.set_ylabel("Mean SIF-to-NDVI lag (days)")
ax.set_title("Rainfall-anomaly severity vs. SIF-to-NDVI lag, continuous test of H3 (n=9)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"Plot saved to {OUTPUT_PLOT}")
