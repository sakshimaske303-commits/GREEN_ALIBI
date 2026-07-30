import pandas as pd
from scipy import stats

SIF_CSV = "data/processed/sif_by_district.csv"
RAIN_CSV = "data/processed/rainfall_anomaly_by_district.csv"
OUTPUT_CSV = "data/processed/sif_rainfall_district_merged.csv"

sif = pd.read_csv(SIF_CSV)
rain = pd.read_csv(RAIN_CSV)

merged = pd.merge(sif, rain, on=["district", "year"], how="inner")

print(f"Merged {len(merged)} district-year observations (expected: 8 districts x 3 years = 24)\n")
print(merged[["district", "year", "mean_sif", "anomaly_pct", "anomaly_zscore"]]
      .sort_values(["year", "district"])
      .to_string(index=False))

pearson_r, pearson_p = stats.pearsonr(merged["anomaly_pct"], merged["mean_sif"])
spearman_r, spearman_p = stats.spearmanr(merged["anomaly_pct"], merged["mean_sif"])

print(f"\nPearson  (rainfall anomaly % vs mean SIF): r    = {pearson_r:.3f}, p = {pearson_p:.4f}")
print(f"Spearman (rainfall anomaly % vs mean SIF): rho  = {spearman_r:.3f}, p = {spearman_p:.4f}")

merged.to_csv(OUTPUT_CSV, index=False)
print(f"\nSaved merged district-year dataset to {OUTPUT_CSV}")