# H4 alarm comparison with NDVI interpolated onto the SIF dates vs taken as observed, both periods

import numpy as np
import pandas as pd

THRESHOLDS = [-1.0, -1.5, -2.0, -3.0]
START_DOY = 182
ONE_COMPOSITE = 8
OUT = "data/processed"


def place_ndvi(t, obs_doy, ndvi, mode):
    if mode == "interpolated":
        return np.interp(t, obs_doy, ndvi, left=np.nan, right=np.nan)
    out = np.full(len(t), np.nan)
    for i, tt in enumerate(t):
        k = np.where(obs_doy <= tt + 3.5)[0]
        if len(k):
            out[i] = ndvi[k[-1]]
    return out


def first_alarm(doys, z, thr):
    for i in range(len(doys) - 1):
        if doys[i] >= START_DOY and z[i] < thr and z[i + 1] < thr:
            return doys[i] + 3.5
    return np.nan


def anomaly(table, key, normal_keys):
    ref = table.loc[[k for k in normal_keys if k != key]]
    return ((table.loc[key] - ref.mean()) / ref.std(ddof=1)).values


def tables(sif, vi, keys, sif_col, mode):
    rows = []
    for key, g in sif.groupby(keys):
        g = g.sort_values("doy")
        sel = np.ones(len(vi), bool)
        for k, v in zip(keys, key if isinstance(key, tuple) else (key,)):
            sel &= (vi[k] == v).values
        n = vi[sel].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
        nd = place_ndvi(g["doy"].values + 3.5, n["mean_obs_doy"].values, n["mean_ndvi"].values, mode)
        rows.append(pd.DataFrame({**{k: g[k].values for k in keys}, "doy": g["doy"].values,
                                  "SIF": g[sif_col].values, "NDVI": nd}))
    d = pd.concat(rows)
    doys = np.array(sorted(d["doy"].unique()))
    tabs = {v: d.pivot_table(index=keys, columns="doy", values=v, dropna=False).reindex(columns=doys)
            for v in ["SIF", "NDVI"]}
    return tabs, doys


def compare(tabs, doys, drought, normal_of, period, level, mode):
    alarms, summary = [], []
    for key in tabs["SIF"].index:
        r = {"period": period, "level": level, "ndvi_dating": mode, "unit": key, "is_drought": key in drought}
        for v in ["SIF", "NDVI"]:
            z = anomaly(tabs[v], key, normal_of(key))
            for thr in THRESHOLDS:
                r[f"{v}_alarm_{thr}"] = first_alarm(doys, z, thr)
        alarms.append(r)
    A = pd.DataFrame(alarms)
    for thr in THRESHOLDS:
        dd = A[A["is_drought"]]
        both = dd.dropna(subset=[f"SIF_alarm_{thr}", f"NDVI_alarm_{thr}"])
        lead = both[f"NDVI_alarm_{thr}"] - both[f"SIF_alarm_{thr}"]
        summary.append({"period": period, "level": level, "ndvi_dating": mode, "threshold": thr,
                        "n_drought": len(dd), "n_normal": int((~A["is_drought"]).sum()),
                        "flagged_SIF": int(dd[f"SIF_alarm_{thr}"].notna().sum()),
                        "flagged_NDVI": int(dd[f"NDVI_alarm_{thr}"].notna().sum()),
                        "false_SIF": int(A.loc[~A["is_drought"], f"SIF_alarm_{thr}"].notna().sum()),
                        "false_NDVI": int(A.loc[~A["is_drought"], f"NDVI_alarm_{thr}"].notna().sum()),
                        "both_flagged": len(both), "SIF_earlier": int((lead > 0).sum()),
                        "same": int((lead == 0).sum()), "NDVI_earlier": int((lead < 0).sum()),
                        "within_one_composite": int((lead.abs() <= ONE_COMPOSITE).sum()),
                        "median_SIF_lead_days": lead.median() if len(lead) else np.nan})
    return A, summary


def rainfall_z(years):
    tot = pd.read_csv("data/raw/chirps_seasonal_totals_1981_2023.csv")
    clim = tot[tot["year"].between(2001, 2020)].groupby("unit")["rainfall_mm"].agg(["mean", "std"])
    t = tot[tot["year"].isin(years)].join(clim, on="unit")
    t["z"] = (t["rainfall_mm"] - t["mean"]) / t["std"]
    return t


periods = [
    ("2015-2023", list(range(2015, 2024)), "data/processed/marathwada_sif_timeseries.csv",
     "data/processed/sif_timeseries_by_district.csv", "data/raw/ndvi_obsdate_2015_2023.csv",
     "data/raw/ndvi_obsdate_by_district_2015_2023.csv"),
    ("2001-2014", list(range(2001, 2015)), "data/processed/oos_sif_region_2001_2014.csv",
     "data/processed/oos_sif_district_2001_2014.csv", "data/raw/vi_obsdate_2001_2014.csv",
     "data/raw/vi_obsdate_by_district_2001_2014.csv"),
]

all_alarms, all_summary = [], []
for period, years, sreg, sdis, vreg, vdis in periods:
    t = rainfall_z(years)
    reg_drought = set(t.loc[(t["unit"] == "Marathwada") & (t["z"] < -0.5), "year"])
    dis_drought = {(r.unit, r.year) for r in t.itertuples() if r.unit != "Marathwada" and r.z < -0.5}
    sr, sd = pd.read_csv(sreg), pd.read_csv(sdis)
    vr, vd = pd.read_csv(vreg), pd.read_csv(vdis)
    vd["district"] = vd["district"].str.strip()
    for mode in ["interpolated", "available"]:
        tabs, doys = tables(sr, vr, ["year"], "mean_sif_crop1214", mode)
        A, S = compare(tabs, doys, reg_drought, lambda y: [x for x in years if x not in reg_drought],
                       period, "region", mode)
        all_alarms.append(A)
        all_summary += S
        tabs, doys = tables(sd, vd, ["district", "year"], "mean_sif", mode)
        A, S = compare(tabs, doys, dis_drought,
                       lambda k: [(k[0], x) for x in years if (k[0], x) not in dis_drought],
                       period, "district", mode)
        all_alarms.append(A)
        all_summary += S

S = pd.DataFrame(all_summary)
A = pd.concat(all_alarms)
A["unit"] = A["unit"].astype(str)
S.to_csv(f"{OUT}/alarm_dating_sensitivity.csv", index=False)
A.to_csv(f"{OUT}/alarm_dating_sensitivity_alarms.csv", index=False)

pd.set_option("display.width", 220)
cols = ["period", "level", "ndvi_dating", "threshold", "both_flagged", "SIF_earlier", "same", "NDVI_earlier",
        "within_one_composite", "median_SIF_lead_days"]
print("Drought units flagged by both indices: SIF earlier / same / NDVI earlier, by how NDVI is placed in time")
print(S[cols].to_string(index=False))
reg = A[(A["level"] == "region") & A["is_drought"]]
print("\nRegional drought-year alarm dates at z < -3 (day of year):")
print(reg[["period", "ndvi_dating", "unit", "SIF_alarm_-3.0", "NDVI_alarm_-3.0"]].to_string(index=False))
print("\nSaved alarm_dating_sensitivity.csv and alarm_dating_sensitivity_alarms.csv")
