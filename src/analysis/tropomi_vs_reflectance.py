# TROPOMI SIF seasonal lag against MODIS NDVI, EVI and NIRv, 2018-2020

import numpy as np
import pandas as pd

THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]
INDICES = {"NDVI": "mean_ndvi", "EVI": "mean_evi", "NIRv": "mean_nirv"}


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


def threshold_lag(ts, sif, tn, other, how):
    """mean crossing date of the reflectance index minus that of SIF (> 0 = SIF declines first)"""
    sn = scale(sif, how)
    nn = np.interp(ts, tn, scale(other, how), left=np.nan, right=np.nan)
    ps, pn = ts[np.nanargmax(sn)], ts[np.nanargmax(nn)]
    lags = np.array([crossing(ts[ts >= pn], nn[ts >= pn], th) - crossing(ts[ts >= ps], sn[ts >= ps], th)
                     for th in THRESHOLDS])
    return np.nanmean(lags) if np.isfinite(lags).any() else np.nan


tc = pd.read_csv("data/processed/tropomi_8day_composites.csv")
vi = pd.read_csv("data/raw/vi_obsdate_2015_2023.csv").dropna(subset=["mean_ndvi", "mean_obs_doy"])
rows = []
for variant, g in tc.groupby("variant", sort=False):
    for y, c in g.groupby("year"):
        c = c.sort_values("start").dropna(subset=["tropomi_sif"])
        v = vi[vi["year"] == y].sort_values("mean_obs_doy")
        ts, sif = c["start"].values + 3.5, c["tropomi_sif"].values
        rec = {"variant": variant, "year": y}
        for name, col in INDICES.items():
            for how in ["season", "decline"]:
                rec[f"TROPOMI_vs_{name}_{how}"] = threshold_lag(ts, sif, v["mean_obs_doy"].values, v[col].values, how)
        rows.append(rec)
T = pd.DataFrame(rows)
T.to_csv("data/processed/tropomi_vs_reflectance_lag.csv", index=False)

gosif = pd.read_csv("data/processed/vegetation_index_lag.csv").set_index("year").loc[[2018, 2019, 2020]]
pd.set_option("display.width", 220)
print("TROPOMI SIF lead over MODIS reflectance indices, days (> 0 = TROPOMI declines first)")
print(T.round(1).to_string(index=False))
main = T[T["variant"].str.startswith("main")].set_index("year")
print("\nMain TROPOMI variant against GOSIF, 2018-2020:")
for how in ["season", "decline"]:
    for name in ["NIRv", "EVI"]:
        tv, gv = main[f"TROPOMI_vs_{name}_{how}"], gosif[f"SIF_vs_{name}_{how}"]
        print(f"  vs {name:4s} {how:7s}: TROPOMI first in {(tv > 0).sum()}/3 (mean {tv.mean():+.1f} d), "
              f"GOSIF first in {(gv > 0).sum()}/3 (mean {gv.mean():+.1f} d)")
allv = T[[c for c in T.columns if "NIRv" in c]]
print(f"\nAcross all four TROPOMI variants, TROPOMI before NIRv in {(allv > 0).values.sum()} of {allv.size} year-scaling cases")
print("Saved data/processed/tropomi_vs_reflectance_lag.csv")
