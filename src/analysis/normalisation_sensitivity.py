# how much of the SIF-NDVI lag is timing and how much is amplitude?
#
# The main lag (lag_analysis.py) scales each year's series between its seasonal
# minimum (always the June pre-season value) and its peak. NDVI does not fall back
# to that June level by 27 December, but SIF does, so a fixed threshold such as 0.5
# sits much deeper into NDVI's own decline than into SIF's. This script recomputes
# the lag three ways on the same data:
#   season  -- the main method (min-max over 1 Jun - 27 Dec)
#   decline -- each series scaled between its peak and its own post-peak minimum,
#              so 0.5 means "halfway through that index's own decline"
#   dlogist -- an amplitude-free end-of-season date: the decline inflection point of
#              a double-logistic curve fitted to each index separately
# for the region (GOSIF and TROPOMI) and for the 72 district-years.

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit

THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]
OUT_DIR = "outputs/figures"
os.makedirs(OUT_DIR, exist_ok=True)

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])


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


def threshold_lag(ts, sif, tn, ndvi, how):
    """mean NDVI-minus-SIF crossing date over the thresholds both series reach"""
    sn = scale(sif, how)
    nn = np.interp(ts, tn, scale(ndvi, how), left=np.nan, right=np.nan)
    ps, pn = ts[np.nanargmax(sn)], ts[np.nanargmax(nn)]
    lags = []
    for th in THRESHOLDS:
        a = crossing(ts[ts >= ps], sn[ts >= ps], th)
        b = crossing(ts[ts >= pn], nn[ts >= pn], th)
        lags.append(b - a)
    lags = np.array(lags)
    return (np.nanmean(lags) if np.isfinite(lags).any() else np.nan), lags


def dlog(t, base, amp1, k1, t1, amp2, k2, t2):
    # asymmetric double logistic: green-up of size amp1, decline of size amp2, so the
    # series does not have to return to its pre-season level (NDVI does not)
    return base + amp1 / (1 + np.exp(-k1 * (t - t1))) - amp2 / (1 + np.exp(-k2 * (t - t2)))


def fit_dlog(t, v):
    t, v = np.asarray(t, float), np.asarray(v, float)
    ok = np.isfinite(v)
    t, v = t[ok], v[ok]
    vn = (v - v.min()) / np.ptp(v)
    ip = t[np.argmax(vn)]
    p0 = [0.0, 1.0, 0.1, (t.min() + ip) / 2, 0.7, 0.08, (ip + t.max()) / 2]
    lo = [-0.5, 0.2, 0.01, t.min() - 10, 0.1, 0.01, ip - 10]
    hi = [0.8, 2.0, 1.0, ip + 20, 2.0, 1.0, t.max()]
    p, _ = curve_fit(dlog, t, vn, p0=p0, bounds=(lo, hi), maxfev=20000)
    return t, vn, p


def end_of_season(t, v):
    """decline inflection date of a double-logistic fit (amplitude-free)"""
    t, v = np.asarray(t, float), np.asarray(v, float)
    ok = np.isfinite(v)
    t, v = t[ok], v[ok]
    vn = (v - v.min()) / np.ptp(v)
    ip = t[np.argmax(vn)]
    p0 = [0.0, 1.0, 0.1, (t.min() + ip) / 2, 0.7, 0.08, (ip + t.max()) / 2]
    lo = [-0.5, 0.2, 0.01, t.min() - 10, 0.1, 0.01, ip - 10]
    hi = [0.8, 2.0, 1.0, ip + 20, 2.0, 1.0, t.max()]
    try:
        p, _ = curve_fit(dlog, t, vn, p0=p0, bounds=(lo, hi), maxfev=20000)
    except RuntimeError:
        return np.nan, np.nan
    rmse = np.sqrt(np.mean((dlog(t, *p) - vn) ** 2))
    return p[6], rmse


# ---------------- region, GOSIF ----------------
m = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
nd = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv").dropna(subset=["mean_ndvi", "mean_obs_doy"])
rows = []
for y in sorted(m["year"].unique()):
    s = m[m["year"] == y].sort_values("doy")
    n = nd[nd["year"] == y].sort_values("mean_obs_doy")
    ts, sif = s["doy"].values.astype(float), s["mean_sif"].values.astype(float)
    tn, nv = n["mean_obs_doy"].values.astype(float), n["mean_ndvi"].values.astype(float)
    rec = {"year": y, "is_drought": y in DROUGHT}
    for how in ["season", "decline"]:
        mean, per = threshold_lag(ts, sif, tn, nv, how)
        rec[f"lag_{how}"] = mean
        for th, v in zip(THRESHOLDS, per):
            rec[f"lag_{how}_{th}"] = v
    ip_s, ip_n = int(np.argmax(sif)), int(np.argmax(nv))
    rec["sif_postpeak_min_season_scaled"] = scale(sif, "season")[ip_s:].min()
    rec["ndvi_postpeak_min_season_scaled"] = scale(nv, "season")[ip_n:].min()
    eos_s, r_s = end_of_season(ts, sif)
    eos_n, r_n = end_of_season(tn, nv)
    rec.update({"eos_sif": eos_s, "eos_ndvi": eos_n, "lag_dlogist": eos_n - eos_s,
                "fit_rmse_sif": r_s, "fit_rmse_ndvi": r_n})
    rows.append(rec)
R = pd.DataFrame(rows)

# ---------------- region, TROPOMI (2018-2020) ----------------
trows = []
tc = pd.read_csv("data/processed/tropomi_8day_composites.csv")
tc = tc[tc["variant"].str.startswith("main")]
for y, c in tc.groupby("year"):
    c = c.sort_values("start").dropna(subset=["tropomi_sif"])
    n = nd[nd["year"] == y].sort_values("mean_obs_doy")
    ts, sif = c["start"].values + 3.5, c["tropomi_sif"].values
    tn, nv = n["mean_obs_doy"].values, n["mean_ndvi"].values
    rec = {"year": y}
    for how in ["season", "decline"]:
        rec[f"lag_{how}"] = threshold_lag(ts, sif, tn, nv, how)[0]
    eos_s, _ = end_of_season(ts, sif)
    eos_n, _ = end_of_season(tn, nv)
    rec["lag_dlogist"] = eos_n - eos_s
    trows.append(rec)
T = pd.DataFrame(trows)

# ---------------- districts ----------------
sd = pd.read_csv("data/processed/sif_timeseries_by_district.csv")
sd["district"] = sd["district"].str.strip()
ndd = pd.read_csv("data/raw/ndvi_obsdate_by_district_2015_2023.csv")
ndd["district"] = ndd["district"].str.strip()
clim = pd.read_csv("data/processed/district_climatology_anomaly_comparison.csv")
drows = []
for (d, y), s in sd.groupby(["district", "year"]):
    s = s.sort_values("doy")
    n = ndd[(ndd["district"] == d) & (ndd["year"] == y)].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
    ts, sif = s["doy"].values + 3.5, s["mean_sif"].values
    tn, nv = n["mean_obs_doy"].values, n["mean_ndvi"].values
    rec = {"district": d, "year": y}
    for how in ["season", "decline"]:
        rec[f"lag_{how}"] = threshold_lag(ts, sif, tn, nv, how)[0]
    eos_s, _ = end_of_season(ts, sif)
    eos_n, _ = end_of_season(tn, nv)
    rec["lag_dlogist"] = eos_n - eos_s
    drows.append(rec)
D = pd.DataFrame(drows).merge(
    clim[["district", "year", "zscore_region_baseline", "zscore_district_baseline"]], on=["district", "year"], how="left")

R.to_csv("data/processed/normalisation_sensitivity_region.csv", index=False)
T.to_csv("data/processed/normalisation_sensitivity_tropomi.csv", index=False)
D.to_csv("data/processed/normalisation_sensitivity_district.csv", index=False)

# ---------------- summary ----------------
pd.set_option("display.width", 220)
print("REGION (GOSIF) -- mean lag, days (> 0 = SIF first)")
print(R[["year", "is_drought", "lag_season", "lag_decline", "lag_dlogist", "eos_sif", "eos_ndvi",
         "sif_postpeak_min_season_scaled", "ndvi_postpeak_min_season_scaled"]].round(2).to_string(index=False))
print("\nREGION (TROPOMI)")
print(T.round(1).to_string(index=False))

summary = []
for metric in ["lag_season", "lag_decline", "lag_dlogist"]:
    v = R[metric]
    dr, nr = R.loc[R["is_drought"], metric].mean(), R.loc[~R["is_drought"], metric].mean()
    dv = D[metric]
    w = D.pivot(index="year", columns="district", values=metric).dropna()
    fr = stats.friedmanchisquare(*[w[c].values for c in w.columns]) if len(w) > 2 else None
    out = {"metric": metric,
           "region_years_sif_first": int((v > 0).sum()), "region_years": int(v.notna().sum()),
           "region_min": v.min(), "region_max": v.max(),
           "region_drought_mean": dr, "region_normal_mean": nr,
           "district_years_sif_first": int((dv > 0).sum()), "district_years": int(dv.notna().sum()),
           "district_median": dv.median(), "district_min": dv.min(), "district_max": dv.max(),
           "district_friedman_chi2": fr.statistic if fr else np.nan,
           "district_friedman_p": fr.pvalue if fr else np.nan,
           "tropomi_years_sif_first": int((T[metric] > 0).sum())}
    for zc in ["zscore_region_baseline", "zscore_district_baseline"]:
        a = D.loc[D[zc] < -0.5, metric].dropna()
        b = D.loc[D[zc] >= -0.5, metric].dropna()
        out[f"district_drought_mean_{zc}"] = a.mean()
        out[f"district_normal_mean_{zc}"] = b.mean()
        out[f"district_welch_p_{zc}"] = stats.ttest_ind(a, b, equal_var=False).pvalue
    summary.append(out)
S = pd.DataFrame(summary)
S.to_csv("data/processed/normalisation_sensitivity_summary.csv", index=False)
print("\nSUMMARY")
print(S.round(3).T.to_string())

# ---------------- figure ----------------
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={"width_ratios": [1.25, 1]})
ax = axes[0]
x = np.arange(len(R))
wdt = 0.27
cols = {"lag_season": "#9e9e9e", "lag_decline": "#2FA88C", "lag_dlogist": "#D98E30"}
labs = {"lag_season": "Season-range thresholds (main method)",
        "lag_decline": "Decline-range thresholds",
        "lag_dlogist": "Double-logistic end-of-season date"}
for i, mtr in enumerate(["lag_season", "lag_decline", "lag_dlogist"]):
    ax.bar(x + (i - 1) * wdt, R[mtr], wdt, color=cols[mtr], label=labs[mtr])
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels([f"{y}\n(drought)" if d else str(y) for y, d in zip(R["year"], R["is_drought"])], fontsize=9)
ax.set_ylabel("NDVI date minus SIF date (days)\n> 0 = SIF first")
ax.set_title("Regional SIF-NDVI lag under three definitions")
ax.legend(fontsize=8, loc="upper right")
ax.grid(axis="y", alpha=0.3)

ax = axes[1]
ax.scatter(R["sif_postpeak_min_season_scaled"], R["ndvi_postpeak_min_season_scaled"], s=60,
           c=["#b2182b" if d else "#555555" for d in R["is_drought"]], zorder=3)
for _, r in R.iterrows():
    ax.annotate(str(int(r["year"])), (r["sif_postpeak_min_season_scaled"], r["ndvi_postpeak_min_season_scaled"]),
                xytext=(4, 3), textcoords="offset points", fontsize=8)
ax.plot([0, 0.7], [0, 0.7], ls=":", color="gray")
ax.set_xlim(-0.03, 0.7)
ax.set_ylim(-0.03, 0.7)
ax.set_xlabel("SIF: lowest value after peak (0 = June level, 1 = peak)")
ax.set_ylabel("NDVI: lowest value after peak (same scale)")
ax.set_title("By late December NDVI stays far above its June level")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "normalisation_sensitivity.png"), dpi=200)
# diagnostic: the double-logistic fits behind lag_dlogist
fig, axes = plt.subplots(3, 3, figsize=(13, 9), sharex=True, sharey=True)
for ax, y in zip(axes.ravel(), sorted(m["year"].unique())):
    s = m[m["year"] == y].sort_values("doy")
    n = nd[nd["year"] == y].sort_values("mean_obs_doy")
    for t, v, col, lab in [(s["doy"].values, s["mean_sif"].values, "#2FA88C", "SIF"),
                           (n["mean_obs_doy"].values, n["mean_ndvi"].values, "#D98E30", "NDVI")]:
        try:
            tt, vn, p = fit_dlog(t, v)
        except RuntimeError:
            continue
        grid = np.linspace(150, 366, 300)
        ax.plot(tt, vn, "o", ms=3, color=col)
        ax.plot(grid, dlog(grid, *p), color=col, label=lab)
        ax.axvline(p[6], color=col, ls=":", lw=1)
    ax.set_title(f"{y}{' (drought)' if y in DROUGHT else ''}", fontsize=10)
    ax.grid(alpha=0.3)
axes[0, 0].legend(fontsize=8)
for ax in axes[-1]:
    ax.set_xlabel("Day of year")
for ax in axes[:, 0]:
    ax.set_ylabel("Scaled 0-1 (season range)")
fig.suptitle("Double-logistic fits; dotted line = fitted decline inflection (end-of-season date)", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "normalisation_sensitivity_fits.png"), dpi=150)

print(f"\nSaved normalisation_sensitivity_*.csv and {OUT_DIR}/normalisation_sensitivity.png")
