# district seasonal rainfall anomaly

import pandas as pd

TOTALS_CSV = "data/raw/chirps_seasonal_totals_1981_2023.csv"
BASELINE = (2001, 2020)
STUDY_YEARS = list(range(2015, 2024))
OUTPUT_CSV = "data/processed/rainfall_anomaly_by_district.csv"

tot = pd.read_csv(TOTALS_CSV)
region = tot[tot["unit"] == "Marathwada"]
clim = region[region["year"].between(*BASELINE)]["rainfall_mm"]
clim_mean, clim_std = clim.mean(), clim.std()
print(f"Using regional {BASELINE[0]}-{BASELINE[1]} mean as baseline: {clim_mean:.1f} mm (std: {clim_std:.1f} mm)")

rain_district = tot[(tot["unit"] != "Marathwada") & tot["year"].isin(STUDY_YEARS)].rename(columns={"unit": "district"})
rain_district = rain_district[["district", "year", "rainfall_mm"]].copy()
assert len(rain_district) == 8 * len(STUDY_YEARS), f"expected 72 district-years, got {len(rain_district)}"

rain_district["anomaly_mm"] = rain_district["rainfall_mm"] - clim_mean
rain_district["anomaly_pct"] = (rain_district["anomaly_mm"] / clim_mean) * 100
rain_district["anomaly_zscore"] = rain_district["anomaly_mm"] / clim_std

rain_district = rain_district.sort_values(["year", "district"])
rain_district.to_csv(OUTPUT_CSV, index=False)

print("\nDistrict-level rainfall anomaly (relative to regional 20-year normal):")
print(rain_district.pivot(index="district", columns="year", values="anomaly_pct").round(1))
print(f"\nSaved to {OUTPUT_CSV}")
