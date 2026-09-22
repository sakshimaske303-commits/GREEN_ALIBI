"""Tier-3 follow-through on the per-district climatology pulled from Earth
Engine (data/processed/rainfall_climatology_by_district.csv, 2001-2020,
one mean/std per district instead of one pooled region-wide number).

This recomputes each district-year's rainfall anomaly z-score against its
OWN district's 20-year baseline, and compares that against the anomaly
z-score this study has used everywhere so far -- one region-wide 2001-2020
mean/std (826.4 mm, 158.8 mm) applied to every district alike. This is
exactly the check Section 6's own Limitations names as missing: "District-
level rainfall anomaly was computed using one region-wide climatological
baseline. A separate baseline for each district was not built."

Outputs data/processed/district_climatology_anomaly_comparison.csv and
prints how much the two approaches actually disagree.
"""
import pandas as pd

REGION_MEAN_MM = 826.4310  # recovered from rainfall_anomaly_summary.csv --
REGION_STD_MM = 158.7780   # the one pooled baseline used everywhere so far

district_rain = pd.read_csv("data/processed/sif_rainfall_district_merged.csv")[
    ["district", "year", "rainfall_mm"]
].drop_duplicates()
clim = pd.read_csv("data/processed/rainfall_climatology_by_district.csv")[
    ["district", "climatology_mean_mm", "climatology_std_mm"]
]

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
