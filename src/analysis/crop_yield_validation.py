# crop yield validation

import os
import zipfile

RAW_ZIP = "data/external/Crop_Wise_Area_Production_Yield.zip"
if not os.path.exists("data/external/extracted/crop-wise-area-production-yield.csv") and os.path.exists(RAW_ZIP):
    with zipfile.ZipFile(RAW_ZIP) as z:
        z.extractall("data/external/extracted")
import numpy as np
import pandas as pd
from scipy import stats

RAW_CSV = "data/external/extracted/crop-wise-area-production-yield.csv"
OUT_CSV = "data/processed/crop_yield_validation_summary.csv"

GOV_TO_GA_DISTRICT = {
    "Chhatrapati Sambhajinagar": "Aurangabad",
    "Dharashiv": "Osmanabad",
    "Beed": "Bid",
    "Jalna": "Jalna",
    "Parbhani": "Parbhani",
    "Hingoli": "Hingoli",
    "Nanded": "Nanded",
    "Latur": "Latur",
}
MIN_YEARS_FOR_BASELINE = 10

df = pd.read_csv(RAW_CSV, low_memory=False)
df = df[
    (df["state_name"] == "Maharashtra")
    & (df["district_name"].isin(GOV_TO_GA_DISTRICT.keys()))
    & (df["season"] == "Kharif")
].copy()
df["district"] = df["district_name"].map(GOV_TO_GA_DISTRICT)
df["study_year"] = df["year"].str.split("-").str[0].astype(int)

print("=" * 70)
print("Loaded", len(df), "Kharif-season crop-district-year rows for the 8 Marathwada districts")
print("Years available:", df["study_year"].min(), "-", df["study_year"].max())
print("=" * 70)

rows = []
for (district, crop), g in df.groupby(["district", "crop_name"]):
    if g["study_year"].nunique() < MIN_YEARS_FOR_BASELINE:
        continue
    mu, sd = g["yield"].mean(), g["yield"].std()
    if sd == 0 or np.isnan(sd):
        continue
    for _, r in g.iterrows():
        rows.append({
            "district": district, "crop": crop, "study_year": r["study_year"],
            "yield": r["yield"], "yield_zscore": (r["yield"] - mu) / sd,
        })
zdf = pd.DataFrame(rows)
print(f"\n{zdf['crop'].nunique()} crops retained (>= {MIN_YEARS_FOR_BASELINE} years of district history each)")
print(f"{zdf[['district','crop']].drop_duplicates().shape[0]} district-crop series scored")

district_year = zdf.groupby(["district", "study_year"])["yield_zscore"].mean().reset_index()
district_year.columns = ["district", "study_year", "yield_anomaly_index"]

STUDY_YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
_rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(_rain.loc[_rain["anomaly_zscore"] < -0.5, "year"])

region_year = district_year[district_year["study_year"].isin(STUDY_YEARS)].groupby("study_year")["yield_anomaly_index"].mean().reset_index()

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")[["year", "anomaly_zscore"]].rename(columns={"year": "study_year", "anomaly_zscore": "rainfall_anomaly_zscore"})
# season-mean (Jun-Dec) cropland-weighted SIF, the same measure as crop_yield_sensitivity.py
sif = (pd.read_csv("data/processed/sif_by_district_seasonal.csv").groupby("year")["season_jun_dec"].mean()
       .reset_index().rename(columns={"year": "study_year", "season_jun_dec": "mean_sif"}))

summary = region_year.merge(rain, on="study_year", how="outer").merge(sif, on="study_year", how="outer").sort_values("study_year")
summary["is_drought_year"] = summary["study_year"].isin(DROUGHT_YEARS)
summary["has_yield_data"] = summary["study_year"].isin(district_year["study_year"].unique())

print("\n" + "=" * 70)
print("MARATHWADA-REGION-YEAR SUMMARY (Kharif season)")
print("=" * 70)
print(summary.to_string(index=False))

valid = summary.dropna(subset=["yield_anomaly_index", "rainfall_anomaly_zscore", "mean_sif"])
r_yield_rain, p_yield_rain = stats.pearsonr(valid["yield_anomaly_index"], valid["rainfall_anomaly_zscore"])
r_yield_sif, p_yield_sif = stats.pearsonr(valid["yield_anomaly_index"], valid["mean_sif"])
print(f"\nn = {len(valid)} region-years with complete data (2023 excluded -- no yield data published yet)")
print(f"corr(yield anomaly, rainfall anomaly)  = {r_yield_rain:.3f}  p={p_yield_rain:.4f}  (sanity check: expect positive)")
print(f"corr(yield anomaly, season-mean regional SIF) = {r_yield_sif:.3f}  p={p_yield_sif:.4f}")

d = valid.loc[valid["is_drought_year"], "yield_anomaly_index"]
n = valid.loc[~valid["is_drought_year"], "yield_anomaly_index"]
t_stat, p_ttest = stats.ttest_ind(d, n, equal_var=False)
print(f"\nMean yield anomaly in this study's {len(d)} drought years ({sorted(DROUGHT_YEARS)}): {d.mean():.3f}")
print(f"Mean yield anomaly in this study's {len(n)} normal years:      {n.mean():.3f}")
print(f"Welch's t-test (n={len(d)} vs n={len(n)}, deliberately not treated as confirmatory given the tiny n):")
print(f"  t={t_stat:.3f}  p={p_ttest:.4f}")
print("Drought years show LOWER actual crop yield than normal years." if d.mean() < n.mean()
      else "Drought years do NOT show lower actual crop yield than normal years in this data.")

summary.to_csv(OUT_CSV, index=False)
district_year.to_csv("data/processed/crop_yield_anomaly_by_district_year.csv", index=False)
print(f"\nSaved region-year summary to {OUT_CSV}")
print("Saved district-year detail to data/processed/crop_yield_anomaly_by_district_year.csv")
