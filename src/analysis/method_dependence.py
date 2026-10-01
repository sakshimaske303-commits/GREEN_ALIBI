# which findings depend on method choices

import itertools

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.stats import spearmanr

m = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
ndvi = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv")
rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv").set_index("year")["anomaly_zscore"]
YEARS = sorted(m["year"].unique())
DEFS = {"z<-0.5": {y for y in YEARS if rain[y] < -0.5}, "z<-1.0": {y for y in YEARS if rain[y] < -1.0}}


def minmax(x):
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def crossing(t, v, th):
    for i in range(len(v) - 1):
        if v[i] >= th and v[i + 1] < th:
            return t[i] + (v[i] - th) / (v[i] - v[i + 1]) * (t[i + 1] - t[i])
    return np.nan


def series(year, sif_col, pairing, smooth):
    s = m[m["year"] == year].sort_values("sif_start_doy")
    n = ndvi[ndvi["year"] == year].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("doy_start")
    sv, nv = s[sif_col].values.astype(float), n["mean_ndvi"].values.astype(float)
    if smooth:
        sv, nv = savgol_filter(sv, 5, 2), savgol_filter(nv, 5, 2)
    if pairing == "obsdate":
        t = s["doy"].values.astype(float)
        nn = np.interp(t, n["mean_obs_doy"].values, minmax(nv), left=np.nan, right=np.nan)
        return t, minmax(sv), nn
    t = s["sif_start_doy"].values.astype(float)
    idx = np.searchsorted(n["doy_start"].values, t, side="right") - 1
    nn = np.where(idx >= 0, nv[np.clip(idx, 0, None)], np.nan)
    ok = ~np.isnan(nn)
    nn[ok] = minmax(nn[ok])
    return t, minmax(sv), nn


def lag(t, sn, nn, metric):
    ps, pn = t[np.nanargmax(sn)], t[np.nanargmax(nn)]
    if metric != "xcorr":
        ths = [0.9, 0.8, 0.7, 0.6, 0.5] if metric == "mean" else [float(metric)]
        out = []
        for th in ths:
            a, b = crossing(t[t >= ps], sn[t >= ps], th), crossing(t[t >= pn], nn[t >= pn], th)
            if not (np.isnan(a) or np.isnan(b)):
                out.append(b - a)
        return np.mean(out) if out else np.nan
    keep = (t >= ps) & ~np.isnan(nn)
    tt, ss, nd = t[keep], sn[keep], nn[keep]
    g = np.arange(tt.min(), tt.max() + 1)
    a, b = np.interp(g, tt, ss), np.interp(g, tt, nd)
    a, b = a - a.mean(), b - b.mean()
    ml = int(len(g) / 4)
    L = np.arange(-ml, ml + 1)
    c = [np.corrcoef(a[:-k], b[k:])[0, 1] if k > 0 else np.corrcoef(a[-k:], b[:k])[0, 1] if k < 0
         else np.corrcoef(a, b)[0, 1] for k in L]
    return float(L[int(np.argmax(c))])


CHOICES = {"sif": ["mean_sif", "mean_sif_all"], "pairing": ["obsdate", "window"], "smooth": [False, True],
           "metric": ["mean", "0.9", "0.7", "0.5", "xcorr"]}
rows = []
for sif_col, pairing, smooth, metric in itertools.product(*CHOICES.values()):
    name = (f"{'crop' if sif_col == 'mean_sif' else 'allpix'}|{pairing}|{'smooth' if smooth else 'raw'}|{metric}")
    for y in YEARS:
        t, sn, nn = series(y, sif_col, pairing, smooth)
        rows.append({"variant": name, "sif": sif_col, "pairing": pairing, "smooth": smooth, "metric": metric,
                     "year": y, "lag": lag(t, sn, nn, metric)})
L = pd.DataFrame(rows)
L.to_csv("data/processed/method_dependence_lags.csv", index=False)

MAIN = "crop|obsdate|raw|mean"
main = L[L["variant"] == MAIN].set_index("year")["lag"]
print("Main-method lags reproduced:", main.round(1).to_dict())

claims = []
for v, g in L.groupby("variant", sort=False):
    s = g.set_index("year")["lag"]
    rec = {"variant": v, "metric": g["metric"].iloc[0],
           "C1_years_SIF_leads": int((s > 0).sum()), "C1_years_tie": int((s == 0).sum()),
           "C1_years_NDVI_leads": int((s < 0).sum()), "C1_years_not_measurable": int(s.isna().sum())}
    for dn, dset in DEFS.items():
        d, n = s[[y for y in YEARS if y in dset]].mean(), s[[y for y in YEARS if y not in dset]].mean()
        rec[f"C2_drought_minus_normal_{dn}"] = d - n
    rec["C3_2018_rank_smallest"] = int(s.rank(method="min")[2018])
    rec["C4_spearman_vs_main"] = spearmanr(s, main, nan_policy="omit").statistic
    claims.append(rec)
C = pd.DataFrame(claims)
C.to_csv("data/processed/method_dependence_claims.csv", index=False)

pd.set_option("display.width", 220)
print("\nEvery variant (lags in days; C2 < 0 means drought years have the smaller lag):")
print(C.round(2).to_string(index=False))

n = len(C)
thr = C[C["metric"] != "xcorr"]
xc = C[C["metric"] == "xcorr"]
print(f"\nSUMMARY over {n} variants ({len(thr)} threshold-based, {len(xc)} cross-correlation):")
meas = C["C1_years_not_measurable"] == 0
print(f"  C1 no year where NDVI leads (among measurable years): {int((C['C1_years_NDVI_leads'] == 0).sum())}/{n}; "
      f"variants with unmeasurable years (a threshold never reached): {int((~meas).sum())}")
print(f"  C1 SIF leads in all 9 years:     threshold {int((thr['C1_years_SIF_leads'] == 9).sum())}/{len(thr)}, "
      f"cross-corr {int((xc['C1_years_SIF_leads'] == 9).sum())}/{len(xc)}; "
      f"fewest SIF-lead years in any variant: {C['C1_years_SIF_leads'].min()}; "
      f"variants where NDVI leads in some year: {int((C['C1_years_NDVI_leads'] > 0).sum())}")
for dn in DEFS:
    col = f"C2_drought_minus_normal_{dn}"
    print(f"  C2 drought lag < normal ({dn}): {int((C[col] < 0).sum())}/{n} "
          f"(range {C[col].min():+.1f} to {C[col].max():+.1f} d)")
print(f"  C3 2018 smallest lead:           {int((C['C3_2018_rank_smallest'] == 1).sum())}/{n}; "
      f"2018 in the smallest two: {int((C['C3_2018_rank_smallest'] <= 2).sum())}/{n}")
print(f"  C4 ranking vs main: median rho threshold {thr['C4_spearman_vs_main'].median():.2f}, "
      f"cross-corr {xc['C4_spearman_vs_main'].median():.2f}; min {C['C4_spearman_vs_main'].min():.2f}")
bad = L[L["lag"] < 0].groupby("year")["variant"].count()
print(f"  Years where some variant has NDVI leading: {bad.to_dict()}")
print("\nSaved method_dependence_lags.csv, method_dependence_claims.csv")
