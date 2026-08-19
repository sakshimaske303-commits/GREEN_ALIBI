import pandas as pd
import numpy as np
import os

# Bootstrap CI on cross_correlation_lag.py's lag estimate. Case resampling of the
# ~17 sparse post-peak observations/year, not block bootstrap on the interpolated
# series -- block-shuffling destroyed the trend and collapsed every CI to lag=0.
# 2000 reps/year, 2.5/97.5 pct = 95% CI.

MERGED_CSV = "data/processed/marathwada_sif_ndvi_merged.csv"
OUT_CSV = "data/processed/cross_correlation_lag_bootstrap_ci.csv"

# drought classification from data (anomaly_zscore < -0.5), see compare_sif_ndvi.py
_rain_anomaly = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(_rain_anomaly.loc[_rain_anomaly["anomaly_zscore"] < -0.5, "year"])
N_BOOT = 2000
RNG_SEED = 42

rng = np.random.default_rng(RNG_SEED)

df = pd.read_csv(MERGED_CSV)
df["sif_norm"] = df.groupby("year")["mean_sif"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
df["ndvi_norm"] = df.groupby("year")["mean_ndvi"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))


def lag_from_daily(sif_daily, ndvi_daily, max_lag):
    sif_c = sif_daily - sif_daily.mean()
    ndvi_c = ndvi_daily - ndvi_daily.mean()
    lags = np.arange(0, max_lag + 1)
    corrs = []
    for lag in lags:
        if lag == 0:
            c = np.corrcoef(sif_c, ndvi_c)[0, 1]
        elif len(sif_c) - lag < 5:
            c = np.nan
        else:
            c = np.corrcoef(sif_c[:-lag], ndvi_c[lag:])[0, 1]
        corrs.append(c)
    corrs = np.array(corrs)
    if np.all(np.isnan(corrs)):
        return np.nan, np.nan
    best_idx = int(np.nanargmax(corrs))
    return int(lags[best_idx]), float(corrs[best_idx])


def interp_and_lag(sub_doy, sub_sif, sub_ndvi, grid_min, grid_max):
    # average duplicate DOYs (can occur when a bootstrap replicate
    # draws the same observation more than once), then sort
    tmp = pd.DataFrame({"doy": sub_doy, "sif": sub_sif, "ndvi": sub_ndvi})
    tmp = tmp.groupby("doy", as_index=False).mean().sort_values("doy")
    if len(tmp) < 6:
        return np.nan, np.nan
    doy_grid = np.arange(grid_min, grid_max + 1)
    sif_daily = np.interp(doy_grid, tmp["doy"], tmp["sif"])
    ndvi_daily = np.interp(doy_grid, tmp["doy"], tmp["ndvi"])
    max_lag = int(len(doy_grid) / 4)
    return lag_from_daily(sif_daily, ndvi_daily, max_lag)


results = []
for year in sorted(df["year"].unique()):
    sub = df[df["year"] == year].sort_values("doy").reset_index(drop=True)
    sif_peak_doy = sub.loc[sub["sif_norm"].idxmax(), "doy"]
    decline = sub[sub["doy"] >= sif_peak_doy].reset_index(drop=True)
    n_obs = len(decline)
    grid_min, grid_max = decline["doy"].min(), decline["doy"].max()

    orig_lag, orig_corr = interp_and_lag(
        decline["doy"].values, decline["sif_norm"].values, decline["ndvi_norm"].values, grid_min, grid_max
    )

    boot_lags = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, n_obs, size=n_obs)  # case resample, with replacement
        b_lag, b_corr = interp_and_lag(
            decline["doy"].values[idx], decline["sif_norm"].values[idx], decline["ndvi_norm"].values[idx],
            grid_min, grid_max
        )
        if not np.isnan(b_lag):
            boot_lags.append(b_lag)

    boot_lags = np.array(boot_lags)
    ci_low, ci_high = np.percentile(boot_lags, [2.5, 97.5])
    pct_positive = float((boot_lags > 0).mean() * 100)
    pct_nonneg = float((boot_lags >= 0).mean() * 100)
    results.append({
        "year": year,
        "is_drought_year": year in DROUGHT_YEARS,
        "n_observations": n_obs,
        "point_estimate_lag_days": orig_lag,
        "point_estimate_r": round(orig_corr, 4),
        "bootstrap_n_valid": len(boot_lags),
        "ci_2.5pct_days": float(ci_low),
        "ci_97.5pct_days": float(ci_high),
        "bootstrap_median_days": float(np.median(boot_lags)),
        "bootstrap_std_days": float(np.std(boot_lags)),
        "pct_replicates_lag_gt_0": round(pct_positive, 1),
        "pct_replicates_lag_geq_0": round(pct_nonneg, 1),
    })

res_df = pd.DataFrame(results)
res_df.to_csv(OUT_CSV, index=False)
print(res_df.to_string(index=False))

print("\nPairwise CI overlap check (does the gap between years survive sampling uncertainty?):")
years = res_df["year"].tolist()
for i in range(len(years)):
    for j in range(i + 1, len(years)):
        a, b = res_df.iloc[i], res_df.iloc[j]
        overlap = not (a["ci_97.5pct_days"] < b["ci_2.5pct_days"] or b["ci_97.5pct_days"] < a["ci_2.5pct_days"])
        print(f"  {int(a['year'])} [{a['ci_2.5pct_days']:.1f}, {a['ci_97.5pct_days']:.1f}] vs "
              f"{int(b['year'])} [{b['ci_2.5pct_days']:.1f}, {b['ci_97.5pct_days']:.1f}] -> "
              f"{'OVERLAP (not statistically distinguishable)' if overlap else 'no overlap (distinguishable)'}")
