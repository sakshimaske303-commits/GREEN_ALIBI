import pandas as pd

RAINFALL_CSV = "data/processed/rainfall_anomaly_summary.csv"
LAG_CSV = "data/processed/sif_ndvi_lag_by_threshold.csv"
OUTPUT_CSV = "data/processed/final_summary_rainfall_lag.csv"

rainfall = pd.read_csv(RAINFALL_CSV)
lag = pd.read_csv(LAG_CSV)

lag_summary = lag.groupby("year")["lag_days"].mean().reset_index()
lag_summary = lag_summary.rename(columns={"lag_days": "mean_lag_days"})

combined = rainfall.merge(lag_summary, on="year", how="left")
combined = combined[["year", "total_rainfall_mm", "anomaly_pct", "anomaly_zscore", "mean_lag_days"]]
combined = combined.sort_values("year")

combined.to_csv(OUTPUT_CSV, index=False)

print("Final combined summary — rainfall anomaly vs SIF-NDVI lag:")
print(combined.round(2).to_string(index=False))