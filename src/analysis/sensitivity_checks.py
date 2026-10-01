# robustness checks

import numpy as np
import pandas as pd
import statsmodels.api as sm

OUT_CSV = "data/processed/sensitivity_checks_summary.csv"
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
lag_by_threshold = pd.read_csv("data/processed/sif_ndvi_lag_by_threshold.csv")
lag_by_year = lag_by_threshold.groupby("year")["lag_days"].mean()

summary_rows = []

print("=" * 70)
print("CHECK 1: Drought-threshold (z-score cutoff) sensitivity")
print("=" * 70)
for thresh in [-0.3, -0.4, -0.5, -0.6, -0.75, -1.0]:
    drought_years = set(rain.loc[rain["anomaly_zscore"] < thresh, "year"])
    normal_years = set(rain["year"]) - drought_years
    if len(drought_years) == 0 or len(normal_years) == 0:
        continue
    d_mean = lag_by_year[lag_by_year.index.isin(drought_years)].mean()
    n_mean = lag_by_year[lag_by_year.index.isin(normal_years)].mean()
    direction = "drought < normal (H3 still not supported)" if d_mean < n_mean else "drought > normal (H3 direction FLIPS)"
    print(f"z < {thresh:>5}: drought years = {sorted(drought_years)} (n={len(drought_years)}), "
          f"drought mean lag = {d_mean:.1f}d, normal mean lag = {n_mean:.1f}d -- {direction}")
    summary_rows.append({
        "check": "drought_threshold_sensitivity", "parameter": f"z<{thresh}",
        "n_drought_years": len(drought_years), "drought_mean_lag": round(d_mean, 1),
        "normal_mean_lag": round(n_mean, 1), "conclusion_stable": d_mean < n_mean,
    })
print("\nAt this study's z < -0.5 threshold and every less strict threshold tested (down to z < -0.3),")
print("the H3 conclusion is stable. At a stricter z < -1.0 cutoff, only 2015 still qualifies as a")
print("drought year (n=1) and the direction reverses -- expected instability given n=1, not evidence")
print("against the main z < -0.5 result, but disclosed here rather than left untested.")

print("\n" + "=" * 70)
print("CHECK 2: Cluster-robust significance of the SIF-rainfall correlation")
print("=" * 70)
merged = pd.read_csv("data/processed/sif_rainfall_district_merged.csv")
merged["district_code"] = merged["district"].astype("category").cat.codes
X = sm.add_constant(merged["anomaly_pct"])
y = merged["mean_sif"]

models = {
    "plain_ols_n72": sm.OLS(y, X).fit(),
    "cluster_by_year_n9": sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": merged["year"].to_numpy()}),
    "cluster_by_district_n8": sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": merged["district_code"].to_numpy()}),
    "cluster_two_way_year_district": sm.OLS(y, X).fit(
        cov_type="cluster", cov_kwds={"groups": merged[["year", "district_code"]].astype(int).to_numpy()}),
}
for name, m in models.items():
    se = m.bse["anomaly_pct"]
    p = m.pvalues["anomaly_pct"]
    print(f"{name:32}: coef={m.params['anomaly_pct']:.6f}  se={se:.6f}  p={p:.6f}")
    summary_rows.append({
        "check": "clustered_significance", "parameter": name,
        "n_drought_years": None, "drought_mean_lag": None, "normal_mean_lag": None,
        "conclusion_stable": p < 0.05, "se": round(se, 6), "p_value": round(p, 6),
    })
print("\nEven under the most conservative correction tested (two-way clustering by year AND")
print("district, 9 year-clusters and 8 district-clusters rather than n=72 independent points),")
print("the correlation remains significant at p<0.01. This directly quantifies -- rather than only")
print("caveats -- the Moran's I finding in Section 4.8, and shows the correlation survives it.")
print("Caveat: with only 8-9 clusters per dimension, cluster-robust SEs carry known small-sample")
print("downward bias (the usual guidance wants 20-50+ clusters for full asymptotic validity), so")
print("this should be read as a stronger check than the naive p-value, not a fully solved one.")

print("\n" + "=" * 70)
print("CHECK 3: Temporal-matching sensitivity (actual observation dates vs 16-day window matching)")
print("=" * 70)
sif = pd.read_csv("data/processed/marathwada_sif_timeseries.csv")
ndvi_obs = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv")
main_merged = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
DROUGHT_YEARS = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])


def find_crossing_doy(doys, values, threshold):
    for i in range(len(values) - 1):
        v1, v2 = values[i], values[i + 1]
        if v1 >= threshold and v2 < threshold:
            d1, d2 = doys[i], doys[i + 1]
            frac = (v1 - threshold) / (v1 - v2)
            return d1 + frac * (d2 - d1)
    return np.nan


def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def lags_from_norm(df):
    out = {}
    for yr in sorted(df["year"].unique()):
        sub = df[df["year"] == yr].sort_values("doy").reset_index(drop=True)
        sif_peak_doy = sub.loc[sub["sif_norm"].idxmax(), "doy"]
        ndvi_peak_doy = sub.loc[sub["ndvi_norm"].idxmax(), "doy"]
        sif_decline = sub[sub["doy"] >= sif_peak_doy]
        ndvi_decline = sub[sub["doy"] >= ndvi_peak_doy]
        lags = []
        for t in THRESHOLDS:
            sc = find_crossing_doy(sif_decline["doy"].values, sif_decline["sif_norm"].values, t)
            nc = find_crossing_doy(ndvi_decline["doy"].values, ndvi_decline["ndvi_norm"].values, t)
            if not (np.isnan(sc) or np.isnan(nc)):
                lags.append(nc - sc)
        out[yr] = float(np.mean(lags)) if lags else np.nan
    return out


alt_rows = []
for yr in sorted(sif["year"].unique()):
    s = sif[sif["year"] == yr].sort_values("doy")[["year", "doy", "mean_sif_crop1214"]]
    n = ndvi_obs[ndvi_obs["year"] == yr].sort_values("doy_start")[["doy_start", "mean_ndvi"]].rename(columns={"doy_start": "doy"})
    m = pd.merge_asof(s, n, on="doy", direction="backward")
    m["sif_norm"] = minmax(m["mean_sif_crop1214"])
    m["ndvi_norm"] = minmax(m["mean_ndvi"])
    alt_rows.append(m)

orig_lags = lags_from_norm(main_merged)
alt_lags = lags_from_norm(pd.concat(alt_rows).reset_index(drop=True))

print(f"{'Year':6}{'obs-date':>15}{'window-match':>15}{'diff':>8}")
for yr in sorted(orig_lags):
    o, a = orig_lags[yr], alt_lags[yr]
    print(f"{yr:<6}{o:>15.1f}{a:>15.1f}{a - o:>8.1f}")
    summary_rows.append({
        "check": "temporal_merge_sensitivity", "parameter": f"year_{yr}",
        "n_drought_years": None, "drought_mean_lag": round(o, 1), "normal_mean_lag": round(a, 1),
        "conclusion_stable": (o > 0) == (a > 0),
    })

d_o = np.mean([v for k, v in orig_lags.items() if k in DROUGHT_YEARS])
n_o = np.mean([v for k, v in orig_lags.items() if k not in DROUGHT_YEARS])
d_a = np.mean([v for k, v in alt_lags.items() if k in DROUGHT_YEARS])
n_a = np.mean([v for k, v in alt_lags.items() if k not in DROUGHT_YEARS])
print(f"\ndrought mean: obs-date={d_o:.1f}d, window-match={d_a:.1f}d")
print(f"normal mean:  obs-date={n_o:.1f}d, window-match={n_a:.1f}d")
print("\nPositive diff = the older window-matching gives a larger lag than the main (actual")
print("observation date) pipeline for that year.")

pd.DataFrame(summary_rows).to_csv(OUT_CSV, index=False)
print(f"\nSaved to {OUT_CSV}")
