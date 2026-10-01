# district rainfall climatology and anomalies

import pandas as pd

TOTALS_CSV = "data/raw/chirps_seasonal_totals_1981_2023.csv"
BASELINE = (2001, 2020)
tot = pd.read_csv(TOTALS_CSV)
base = tot[tot["year"].between(*BASELINE)]
REGION_MEAN_MM = base.loc[base["unit"] == "Marathwada", "rainfall_mm"].mean()
REGION_STD_MM = base.loc[base["unit"] == "Marathwada", "rainfall_mm"].std()

district_rain = pd.read_csv("data/processed/rainfall_anomaly_by_district.csv")[["district", "year", "rainfall_mm"]]
clim = (base[base["unit"] != "Marathwada"].groupby("unit")["rainfall_mm"]
        .agg(climatology_mean_mm="mean", climatology_std_mm="std").reset_index()
        .rename(columns={"unit": "district"}))

df = district_rain.merge(clim, on="district", how="left")
df["zscore_region_baseline"] = (df["rainfall_mm"] - REGION_MEAN_MM) / REGION_STD_MM
df["zscore_district_baseline"] = (df["rainfall_mm"] - df["climatology_mean_mm"]) / df["climatology_std_mm"]
df["drought_under_region_baseline"] = df["zscore_region_baseline"] < -0.5
df["drought_under_district_baseline"] = df["zscore_district_baseline"] < -0.5
df["classification_changes"] = df["drought_under_region_baseline"] != df["drought_under_district_baseline"]

print("=" * 70)
print("Per-district climatology mean/std vs. the one pooled region-wide baseline")
print("=" * 70)
print(clim.to_string(index=False))
print(f"\nPooled region-wide baseline used everywhere else in this study: mean={REGION_MEAN_MM:.1f} mm, std={REGION_STD_MM:.1f} mm")
print("Each district's own baseline differs from the pooled one by up to "
      f"{(clim['climatology_mean_mm'] - REGION_MEAN_MM).abs().max():.0f} mm in its mean alone "
      "(Nanded and Hingoli sit well above the pooled mean, Osmanabad and Aurangabad well below it) "
      "-- so a district that's always wetter or drier than the regional average gets its rainfall "
      "compared against a baseline that isn't really its own normal.")

print("\n" + "=" * 70)
print("DISTRICT-YEAR COMPARISON: region-wide baseline vs. district's own baseline")
print("=" * 70)
cols = ["district", "year", "rainfall_mm", "zscore_region_baseline", "zscore_district_baseline", "classification_changes"]
print(df[cols].sort_values(["year", "district"]).to_string(index=False))

n_changed = df["classification_changes"].sum()
print(f"\n{n_changed} of {len(df)} district-year drought/normal classifications change "
      f"depending on which baseline is used (region-wide vs. that district's own).")
if n_changed:
    print("Changed cases:")
    print(df.loc[df["classification_changes"], cols].to_string(index=False))

corr = df["zscore_region_baseline"].corr(df["zscore_district_baseline"])
print(f"\nCorrelation between the two z-score series: r = {corr:.3f}")
print("A high correlation here means the district-baseline correction mostly re-scales rather than")
print("reorders which district-years look driest -- but any classification flips listed above are the")
print("concrete cases where the choice of baseline, not just the rainfall number itself, changes the")
print("conclusion, and are reported here rather than left as an unquantified caveat.")

df.to_csv("data/processed/district_climatology_anomaly_comparison.csv", index=False)
print("\nSaved data/processed/district_climatology_anomaly_comparison.csv")
