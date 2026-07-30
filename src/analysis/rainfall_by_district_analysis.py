import pandas as pd

RAW_CSV = "data/raw/marathwada_rainfall_by_district.csv"
CLIM_CSV = "data/raw/marathwada_rainfall_climatology_2001_2020.csv"
OUTPUT_CSV = "data/processed/rainfall_anomaly_by_district.csv"

# --- Load data ---
rain_district = pd.read_csv(RAW_CSV)
clim = pd.read_csv(CLIM_CSV)

clim_mean = clim["total_rainfall_mm"].mean()
clim_std = clim["total_rainfall_mm"].std()

print(f"Using regional 20-year climatological mean as baseline: {clim_mean:.1f} mm (std: {clim_std:.1f} mm)")

# --- Compute anomaly for each district-year, relative to the REGIONAL normal ---
rain_district["anomaly_mm"] = rain_district["rainfall_mm"] - clim_mean
rain_district["anomaly_pct"] = (rain_district["anomaly_mm"] / clim_mean) * 100
rain_district["anomaly_zscore"] = rain_district["anomaly_mm"] / clim_std

rain_district = rain_district.sort_values(["year", "district"])
rain_district.to_csv(OUTPUT_CSV, index=False)

print("\nDistrict-level rainfall anomaly (relative to regional 20-year normal):")
pivot = rain_district.pivot(index="district", columns="year", values="anomaly_pct")
print(pivot.round(1))

print(f"\nSaved to {OUTPUT_CSV}")