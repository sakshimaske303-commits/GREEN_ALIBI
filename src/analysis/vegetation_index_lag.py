# is the "SIF leads NDVI" result a property of NDVI?
#
# GOSIF is predicted from MODIS EVI (plus reanalysis weather). If MODIS EVI or NIRv
# also "lead" NDVI by about as much as GOSIF does, the seasonal lead says more about
# NDVI (saturation over dense canopy, slow return to its pre-season level) than about
# fluorescence. Every pair is run with the same threshold-crossing code under both
# normalisations used in normalisation_sensitivity.py.
#
# Input: data/raw/vi_obsdate_2015_2023.csv from src/acquisition/gee_vi_obsdate.py
# (needs Earth Engine). The script exits quietly if that file has not been made yet.

import os
import sys

import numpy as np
import pandas as pd

VI_CSV = "data/raw/vi_obsdate_2015_2023.csv"
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]

if not os.path.exists(VI_CSV):
    print(f"{VI_CSV} not found -- run src/acquisition/gee_vi_obsdate.py first (needs Earth Engine). Skipping.")
    sys.exit(0)

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])
vi = pd.read_csv(VI_CSV).dropna(subset=["mean_ndvi", "mean_obs_doy"])
sif = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
old = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv")


def crossing(t, v, th):
    for i in range(len(v) - 1):
        if v[i] >= th and v[i + 1] < th:
            return t[i] + (v[i] - th) / (v[i] - v[i + 1]) * (t[i + 1] - t[i])
    return np.nan


def scale(v, how):
    v = np.asarray(v, float)
    if how == "season":
        return (v - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v))
    ip = int(np.nanargmax(v))
    lo = np.nanmin(v[ip:])
    return (v - lo) / (v[ip] - lo)


def lag(t_lead, v_lead, t_lag, v_lag, how):
    """mean (crossing date of the second series - crossing date of the first) on the first series' dates"""
    a = scale(v_lead, how)
    b = np.interp(t_lead, t_lag, scale(v_lag, how), left=np.nan, right=np.nan)
    pa, pb = t_lead[np.nanargmax(a)], t_lead[np.nanargmax(b)]
    out = np.array([crossing(t_lead[t_lead >= pb], b[t_lead >= pb], th) -
                    crossing(t_lead[t_lead >= pa], a[t_lead >= pa], th) for th in THRESHOLDS])
    return np.nanmean(out) if np.isfinite(out).any() else np.nan


# sanity check: the NDVI in the new export should match the NDVI used everywhere else
chk = vi.merge(old, on=["year", "doy_start"], suffixes=("", "_old"))
if len(chk):
    print(f"NDVI check against ndvi_obsdate_2015_2023.csv: max |difference| = "
          f"{(chk['mean_ndvi'] - chk['mean_ndvi_old']).abs().max():.4f} over {len(chk)} composites")

rows = []
for y in sorted(vi["year"].unique()):
    s = sif[sif["year"] == y].sort_values("doy")
    v = vi[vi["year"] == y].sort_values("mean_obs_doy")
    if s.empty:
        continue
    ts, ss = s["doy"].values.astype(float), s["mean_sif"].values.astype(float)
    tv = v["mean_obs_doy"].values.astype(float)
    series = {"NDVI": v["mean_ndvi"].values, "EVI": v["mean_evi"].values, "NIRv": v["mean_nirv"].values}
    rec = {"year": y, "is_drought": y in DROUGHT}
    for how in ["season", "decline"]:
        for name in ["NDVI", "EVI", "NIRv"]:
            rec[f"SIF_vs_{name}_{how}"] = lag(ts, ss, tv, series[name], how)
        for name in ["EVI", "NIRv"]:
            # same composites, same observation dates: compare on the native 16-day dates
            rec[f"{name}_vs_NDVI_{how}"] = lag(tv, series[name], tv, series["NDVI"], how)
    rows.append(rec)
R = pd.DataFrame(rows)
R.to_csv("data/processed/vegetation_index_lag.csv", index=False)

pd.set_option("display.width", 220)
print("\nMean threshold lag, days (> 0 = the first-named series declines first):")
print(R.round(1).to_string(index=False))
print("\nYears with a lead (> 0):")
for c in [c for c in R.columns if "_vs_" in c]:
    print(f"  {c:28s} {(R[c] > 0).sum()}/{R[c].notna().sum()}   mean {R[c].mean():+.1f} d")
print("\nRead: if EVI_vs_NDVI and NIRv_vs_NDVI are about as large as SIF_vs_NDVI, the 'SIF lead' is mostly an "
      "NDVI property;\nif SIF_vs_EVI / SIF_vs_NIRv stay clearly positive, SIF declines earlier than reflectance-based "
      "greenness as well.")
print("Saved data/processed/vegetation_index_lag.csv")
