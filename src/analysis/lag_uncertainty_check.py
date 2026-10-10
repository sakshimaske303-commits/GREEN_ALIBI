# lag uncertainty check

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

N_BOOT = 2000
SEED = 42
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]

m = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
ndvi = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv")
rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])
YEARS = sorted(m["year"].unique())


def xcorr_lag(doy, s, n, grid_min, grid_max, frac):
    tmp = pd.DataFrame({"doy": doy, "s": s, "n": n}).groupby("doy", as_index=False).mean().sort_values("doy")
    if len(tmp) < 6:
        return np.nan, np.nan
    grid = np.arange(grid_min, grid_max + 1)
    sd = np.interp(grid, tmp["doy"], tmp["s"]); nd = np.interp(grid, tmp["doy"], tmp["n"])
    sd, nd = sd - sd.mean(), nd - nd.mean()
    ml = int(len(grid) * frac)
    lags = np.arange(-ml, ml + 1)
    c = []
    for L in lags:
        if abs(L) >= len(sd) - 4:
            c.append(np.nan)
        elif L > 0:
            c.append(np.corrcoef(sd[:-L], nd[L:])[0, 1])
        elif L < 0:
            c.append(np.corrcoef(sd[-L:], nd[:L])[0, 1])
        else:
            c.append(np.corrcoef(sd, nd)[0, 1])
    c = np.array(c)
    if np.all(np.isnan(c)):
        return np.nan, np.nan
    return int(lags[int(np.nanargmax(c))]), ml


xrows = []
for y in YEARS:
    sub = m[m["year"] == y].sort_values("doy").reset_index(drop=True)
    pk = sub.loc[sub["sif_norm"].idxmax(), "doy"]
    dec = sub[sub["doy"] >= pk].dropna(subset=["sif_norm", "ndvi_norm"]).reset_index(drop=True)
    d, s, n = dec["doy"].values, dec["sif_norm"].values, dec["ndvi_norm"].values
    lo, hi, N = d.min(), d.max(), len(d)
    point, _ = xcorr_lag(d, s, n, lo, hi, 0.25)
    variants = {"current (fixed range, N/4)": [], "own range, N/4": [], "own range, N/2": []}
    edge_hits, extrap = 0, 0
    rng = np.random.default_rng(SEED + int(y))
    for _ in range(N_BOOT):
        idx = rng.integers(0, N, size=N)
        dd = d[idx]
        if dd.min() > lo or dd.max() < hi:
            extrap += 1
        L, ml = xcorr_lag(dd, s[idx], n[idx], lo, hi, 0.25)
        if not np.isnan(L):
            variants["current (fixed range, N/4)"].append(L)
            edge_hits += abs(L) == ml
        L2, _ = xcorr_lag(dd, s[idx], n[idx], dd.min(), dd.max(), 0.25)
        if not np.isnan(L2):
            variants["own range, N/4"].append(L2)
        L3, _ = xcorr_lag(dd, s[idx], n[idx], dd.min(), dd.max(), 0.5)
        if not np.isnan(L3):
            variants["own range, N/2"].append(L3)
    for v, arr in variants.items():
        arr = np.array(arr)
        xrows.append({"year": y, "variant": v, "point_lag": point, "n_valid": len(arr),
                      "ci_low": np.percentile(arr, 2.5), "ci_high": np.percentile(arr, 97.5),
                      "pct_lt_0": 100 * (arr < 0).mean(),
                      "pct_at_search_edge": 100 * edge_hits / len(arr) if v.startswith("current") else np.nan,
                      "pct_replicates_extrapolated": 100 * extrap / N_BOOT if v.startswith("current") else np.nan})
xr = pd.DataFrame(xrows)
xr.to_csv("data/processed/lag_uncertainty_xcorr.csv", index=False)

pd.set_option("display.width", 220)
print("PART A -- cross-correlation bootstrap")
cur = xr[xr["variant"].str.startswith("current")]
print("How often the current bootstrap hits a problem (% of 2000 replicates):")
print(cur[["year", "point_lag", "pct_at_search_edge", "pct_replicates_extrapolated"]].round(1).to_string(index=False))
print("\n95% interval (days) under each variant:")
xr["ci"] = xr.apply(lambda r: f"[{r['ci_low']:.0f}, {r['ci_high']:.0f}]  <0: {r['pct_lt_0']:.0f}%", axis=1)
print(xr.pivot(index="year", columns="variant", values="ci").to_string())


def minmax(x):
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def crossing(t, v, th):
    for i in range(len(v) - 1):
        if v[i] >= th and v[i + 1] < th:
            return t[i] + (v[i] - th) / (v[i] - v[i + 1]) * (t[i + 1] - t[i])
    return np.nan


def threshold_lag(ts, sif, tn, nd):
    sn = minmax(sif)
    nn = np.interp(ts, tn, minmax(nd), left=np.nan, right=np.nan)
    ps, pn = ts[np.nanargmax(sn)], ts[np.nanargmax(nn)]
    out = {}
    for th in THRESHOLDS:
        a = crossing(ts[ts >= ps], sn[ts >= ps], th)
        b = crossing(ts[ts >= pn], nn[ts >= pn], th)
        out[th] = b - a
    vals = [v for v in out.values() if not np.isnan(v)]
    return (np.mean(vals) if vals else np.nan), out


BLOCK = 3  # residuals are resampled in moving blocks of 3 consecutive composites (they are autocorrelated)


def block_resample(res, rng, block=BLOCK):
    n = len(res)
    starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
    return np.concatenate([res[s:s + block] for s in starts])[:n]


def smooth(v):
    return savgol_filter(v, 5, 2, mode="interp")


trows, boot_means, jk = [], {}, []
for y in YEARS:
    s = m[m["year"] == y].sort_values("sif_start_doy")
    ts, sif = s["doy"].values.astype(float), s["mean_sif"].values.astype(float)
    n = ndvi[ndvi["year"] == y].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
    tn, nd = n["mean_obs_doy"].values.astype(float), n["mean_ndvi"].values.astype(float)
    point, per_th = threshold_lag(ts, sif, tn, nd)
    missing = [th for th, v in per_th.items() if np.isnan(v)]

    fs, fn = smooth(sif), smooth(nd)
    rs, rn = sif - fs, nd - fn
    rng = np.random.default_rng(SEED + 1000 + int(y))
    b = []
    for _ in range(N_BOOT):
        b.append(threshold_lag(ts, fs + block_resample(rs, rng), tn, fn + block_resample(rn, rng))[0])
    b = np.array(b)
    b = b[~np.isnan(b)]
    # the replicates scatter around the lag of the SMOOTHED curves, not around the raw-data point
    # estimate, so shift them to centre on the reported estimate before taking percentiles
    smooth_lag = threshold_lag(ts, fs, tn, fn)[0]
    b = b - smooth_lag + point
    boot_means[y] = b

    loo = []
    for i in range(len(sif)):
        keep = np.arange(len(sif)) != i
        loo.append(threshold_lag(ts[keep], sif[keep], tn, nd)[0])
    for i in range(len(nd)):
        keep = np.arange(len(nd)) != i
        loo.append(threshold_lag(ts, sif, tn[keep], nd[keep])[0])
    loo = np.array(loo)

    trows.append({"year": y, "is_drought": y in DROUGHT, "point_lag": point,
                  "thresholds_not_reached": ",".join(map(str, missing)),
                  "sif_residual_sd_pct_of_range": 100 * rs.std() / np.ptp(sif),
                  "ndvi_residual_sd_pct_of_range": 100 * rn.std() / np.ptp(nd),
                  "smoothed_curve_lag": smooth_lag,
                  "boot_ci_low": np.percentile(b, 2.5), "boot_ci_high": np.percentile(b, 97.5),
                  "boot_pct_le_0": 100 * (b <= 0).mean(),
                  "jackknife_min": np.nanmin(loo), "jackknife_max": np.nanmax(loo)})
tr = pd.DataFrame(trows)
tr.to_csv("data/processed/lag_uncertainty_threshold.csv", index=False)

print("\nPART B -- threshold-crossing lag (main method), moving-block residual bootstrap (centred on the estimate) + leave-one-out")
print(tr.drop(columns=["is_drought"]).round(1).to_string(index=False))

pairs, sep = 0, []
for i, a in tr.iterrows():
    for j, c in tr.iterrows():
        if j <= i:
            continue
        pairs += 1
        if a["boot_ci_high"] < c["boot_ci_low"] or c["boot_ci_high"] < a["boot_ci_low"]:
            sep.append(f"{int(a['year'])}-{int(c['year'])}")
print(f"\nYear pairs with non-overlapping threshold-lag intervals: {len(sep)} of {pairs}: {', '.join(sep)}")

rng = np.random.default_rng(SEED)
draws = np.array([[rng.choice(boot_means[y]) for y in YEARS] for _ in range(N_BOOT)])
isd = np.array([y in DROUGHT for y in YEARS])
diff = draws[:, isd].mean(axis=1) - draws[:, ~isd].mean(axis=1)
pt = tr.loc[tr["is_drought"], "point_lag"].mean() - tr.loc[~tr["is_drought"], "point_lag"].mean()
print(f"\nDrought minus normal mean threshold lag: {pt:+.1f} days, "
      f"95% interval (measurement uncertainty only) [{np.percentile(diff, 2.5):+.1f}, {np.percentile(diff, 97.5):+.1f}]; "
      f"{100 * (diff < 0).mean():.1f}% of draws negative")
print("  (this interval covers only how precisely each year's lag is measured -- NOT year-to-year "
      "variability; with 2 drought years that is still the binding limit)")

pd.DataFrame([{"n_pairs_distinguishable": len(sep), "n_pairs": pairs, "pairs": ";".join(sep),
               "drought_minus_normal": pt, "diff_ci_low": np.percentile(diff, 2.5),
               "diff_ci_high": np.percentile(diff, 97.5)}]).to_csv("data/processed/lag_uncertainty_summary.csv", index=False)
print("\nSaved lag_uncertainty_xcorr.csv, lag_uncertainty_threshold.csv, lag_uncertainty_summary.csv")
