# crop yield check, weighting sensitivity

import os
import zipfile

RAW_ZIP = "data/external/Crop_Wise_Area_Production_Yield.zip"
if not os.path.exists("data/external/extracted/crop-wise-area-production-yield.csv") and os.path.exists(RAW_ZIP):
    with zipfile.ZipFile(RAW_ZIP) as z:
        z.extractall("data/external/extracted")
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

RAW = "data/external/extracted/crop-wise-area-production-yield.csv"
GOV = {"Chhatrapati Sambhajinagar": "Aurangabad", "Dharashiv": "Osmanabad", "Beed": "Bid", "Jalna": "Jalna",
       "Parbhani": "Parbhani", "Hingoli": "Hingoli", "Nanded": "Nanded", "Latur": "Latur"}
MAJOR = ["Cotton(Lint)", "Soyabean", "Arhar/Tur", "Jowar", "Bajra", "Moong(Green Gram)", "Urad", "Maize"]
STUDY = list(range(2015, 2024))
MIN_YEARS = 10

df = pd.read_csv(RAW, low_memory=False)
df = df[(df["state_name"] == "Maharashtra") & df["district_name"].isin(GOV) & (df["season"] == "Kharif")].copy()
df["district"] = df["district_name"].map(GOV)
df["year"] = df["year"].str[:4].astype(int)

sug = df[df["crop_name"] == "Sugarcane"].groupby("district")["year"].nunique()
print(f"Sugarcane 'Kharif' rows: {int((df['crop_name'] == 'Sugarcane').sum())}; years per district: "
      f"{sug.to_dict()} -> {'none' if (sug < MIN_YEARS).all() else 'some'} pass the {MIN_YEARS}-year filter")

n0 = len(df)
df = df[df["yield"] > 0]
med = df.groupby(["district", "crop_name"])["yield"].transform("median")
mad = df.groupby(["district", "crop_name"])["yield"].transform(lambda v: (v - v.median()).abs().median())
out = (df["yield"] - med).abs() > 5 * 1.4826 * mad.replace(0, np.nan)
print(f"Dropped {n0 - len(df)} zero yields and {int(out.sum())} extreme outliers "
      f"(max dropped yield {df.loc[out, 'yield'].max():.1f} t/ha)")
df = df[~out]


def zscores(g, detrend):
    y = g["yield"].values
    if detrend:
        b = np.polyfit(g["year"].values, y, 1)
        y = y - np.polyval(b, g["year"].values)
    sd = y.std(ddof=1)
    return (y - y.mean()) / sd if sd > 0 else np.full(len(y), np.nan)


def yai(detrend, weighted, crops=None):
    d = df if crops is None else df[df["crop_name"].isin(crops)]
    parts = []
    for (dist, crop), g in d.groupby(["district", "crop_name"]):
        if g["year"].nunique() < MIN_YEARS:
            continue
        g = g.sort_values("year").copy()
        g["z"] = zscores(g, detrend)
        parts.append(g)
    z = pd.concat(parts).dropna(subset=["z"])
    z["w"] = z["area"] if weighted else 1.0
    dy = z.groupby(["district", "year"]).apply(lambda g: np.average(g["z"], weights=g["w"]), include_groups=False)
    area = z.groupby(["district", "year"])["area"].sum()
    dy = pd.DataFrame({"yai": dy, "area": area}).reset_index()
    ry = dy.groupby("year").apply(lambda g: np.average(g["yai"], weights=g["area"] if weighted else None),
                                  include_groups=False).rename("yai").reset_index()
    return dy, ry, z["crop_name"].nunique()


VARIANTS = {"Y0_cleaned": (False, False, None), "Y1_area_weighted": (False, True, None),
            "Y2_detrended": (True, False, None), "Y3_area_detrended": (True, True, None),
            "Y4_major_crops": (True, True, MAJOR)}

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")[["year", "anomaly_zscore"]]
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])
rain_d = pd.read_csv("data/processed/rainfall_anomaly_by_district.csv")[["district", "year", "anomaly_zscore"]]
sif_d = pd.read_csv("data/processed/sif_by_district_seasonal.csv")[["district", "year", "season_jun_dec", "doy273"]]
sif_r = sif_d.groupby("year")[["season_jun_dec", "doy273"]].mean().reset_index()

reg_all, dist_all, tests = [], [], []
for name, (dt, wt, crops) in VARIANTS.items():
    dy, ry, ncrop = yai(dt, wt, crops)
    r = ry[ry["year"].isin(STUDY)].merge(rain, on="year").merge(sif_r, on="year")
    r["variant"] = name
    reg_all.append(r)
    dr, nr = r.loc[r["year"].isin(DROUGHT), "yai"], r.loc[~r["year"].isin(DROUGHT), "yai"]
    t, p = stats.ttest_ind(dr, nr, equal_var=False)
    rr, pr = stats.pearsonr(r["yai"], r["anomaly_zscore"])
    rs, ps = stats.pearsonr(r["yai"], r["season_jun_dec"])
    rank = r.sort_values("yai")["year"].tolist()

    d = dy[dy["year"].isin(STUDY)].merge(rain_d, on=["district", "year"]).merge(sif_d, on=["district", "year"])
    d["variant"] = name
    dist_all.append(d)
    ds, dps = stats.pearsonr(d["yai"], d["season_jun_dec"])
    dr_, dpr = stats.pearsonr(d["yai"], d["anomaly_zscore"])
    wy = lambda c: d[c] - d.groupby("year")[c].transform("mean")
    wys, wyp = stats.pearsonr(wy("yai"), wy("season_jun_dec"))
    fe = smf.ols("yai ~ season_jun_dec + C(district) + C(year)", d).fit(cov_type="cluster", cov_kwds={"groups": d["district"]})
    tests.append({"variant": name, "n_crops": ncrop, "n_region_years": len(r),
                  "yai_drought": dr.mean(), "yai_normal": nr.mean(), "welch_t": t, "welch_p": p,
                  "lowest_two_years": f"{rank[0]},{rank[1]}",
                  "region_r_rain": rr, "region_p_rain": pr, "region_r_sif": rs, "region_p_sif": ps,
                  "n_district_years": len(d), "district_r_sif": ds, "district_p_sif": dps,
                  "district_r_rain": dr_, "district_p_rain": dpr,
                  "district_within_year_r_sif": wys, "district_within_year_p_sif": wyp,
                  "twoway_fe_p_sif": fe.pvalues["season_jun_dec"]})

T = pd.DataFrame(tests)
pd.set_option("display.width", 220)
print("\nRegion level (8 years with yield data; 2023 not yet published):")
print(T[["variant", "n_crops", "yai_drought", "yai_normal", "welch_p", "lowest_two_years",
         "region_r_rain", "region_p_rain", "region_r_sif", "region_p_sif"]].round(3).to_string(index=False))
print("\nDistrict level (64 district-years), yield anomaly vs seasonal SIF and rainfall:")
print(T[["variant", "n_district_years", "district_r_sif", "district_p_sif", "district_r_rain", "district_p_rain",
         "district_within_year_r_sif", "district_within_year_p_sif", "twoway_fe_p_sif"]].round(3).to_string(index=False))
print("\nYield Anomaly Index by year and variant:")
print(pd.concat(reg_all).pivot(index="year", columns="variant", values="yai").round(2).to_string())

pd.concat(reg_all).to_csv("data/processed/crop_yield_sensitivity_region.csv", index=False)
pd.concat(dist_all).to_csv("data/processed/crop_yield_sensitivity_district.csv", index=False)
T.to_csv("data/processed/crop_yield_sensitivity_tests.csv", index=False)
print("\nSaved crop_yield_sensitivity_region.csv, _district.csv, _tests.csv")
