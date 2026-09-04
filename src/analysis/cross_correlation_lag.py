import math
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

# Cross-correlation lag: a second, independent check on the threshold-
# crossing method in lag_analysis.py. That method asks "when does each
# series cross X% of peak" (onset-sensitive); this asks "what single
# shift best aligns the whole curve" (weighs the full decline, not just
# onset). Different questions -- worth seeing if they actually agree.

MERGED_CSV = "data/processed/marathwada_sif_ndvi_merged.csv"
OUT_CSV = "data/processed/cross_correlation_lag_by_year.csv"
OUT_DIR = "outputs/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# drought classification from data (anomaly_zscore < -0.5), see compare_sif_ndvi.py
_rain_anomaly = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(_rain_anomaly.loc[_rain_anomaly["anomaly_zscore"] < -0.5, "year"])

df = pd.read_csv(MERGED_CSV)
df["sif_norm"] = df.groupby("year")["mean_sif"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
df["ndvi_norm"] = df.groupby("year")["mean_ndvi"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

results = []
curves = {}

for year in sorted(df["year"].unique()):
    sub = df[df["year"] == year].sort_values("doy").reset_index(drop=True)

    # restrict to the post-peak decline phase (from SIF's own peak onward),
    # matching the scope of the threshold-crossing method so both methods
    # are measuring the same phenomenon over the same window
    sif_peak_doy = sub.loc[sub["sif_norm"].idxmax(), "doy"]
    decline = sub[sub["doy"] >= sif_peak_doy].reset_index(drop=True)

    # interpolate both series onto a common daily grid — SIF is native 8-day,
    # NDVI is native 16-day nearest-matched, so cross-correlation would
    # otherwise be biased by uneven sampling between the two series
    doy_grid = np.arange(decline["doy"].min(), decline["doy"].max() + 1)
    sif_daily = np.interp(doy_grid, decline["doy"], decline["sif_norm"])
    ndvi_daily = np.interp(doy_grid, decline["doy"], decline["ndvi_norm"])
    n_days = len(doy_grid)

    sif_c = sif_daily - sif_daily.mean()
    ndvi_c = ndvi_daily - ndvi_daily.mean()

    def lagged_corr(x, y, lag):
        # lag > 0: shift y forward relative to x (NDVI lagging behind SIF,
        # i.e. SIF leads). lag < 0: shift x forward relative to y (SIF
        # lagging behind NDVI, i.e. NDVI leads). lag == 0: no shift.
        if lag > 0:
            return np.corrcoef(x[:-lag], y[lag:])[0, 1]
        elif lag < 0:
            return np.corrcoef(x[-lag:], y[:lag])[0, 1]
        else:
            return np.corrcoef(x, y)[0, 1]

    # Cap the tested lag at N/4 (a standard cross-correlation guideline) —
    # testing lags close to the full series length leaves too few
    # overlapping points for a reliable estimate and produces spurious
    # peaks pinned to the search boundary rather than a genuine optimum.
    #
    # BUG (found in code review, fixed before publishing — see Development
    # Log Entry 17): this used to be `np.arange(0, max_lag + 1)`, a
    # one-sided search that could only ever find SIF leading NDVI or a
    # zero lag. It was structurally impossible for this script to ever
    # report NDVI leading SIF, no matter what the data actually showed,
    # which made the "SIF never lags NDVI" claim built on it a tautology
    # of the search space rather than a real finding. Fixed by searching
    # both directions.
    max_lag = int(n_days / 4)
    lags = np.arange(-max_lag, max_lag + 1)
    corrs = np.array([lagged_corr(sif_c, ndvi_c, lag) for lag in lags])

    best_idx = int(np.argmax(corrs))
    best_lag = int(lags[best_idx])
    best_corr = float(corrs[best_idx])
    zero_idx = int(np.where(lags == 0)[0][0])

    results.append({
        "year": year,
        "is_drought_year": year in DROUGHT_YEARS,
        "decline_window_days": n_days,
        "max_lag_tested": max_lag,
        "cross_corr_lag_days": best_lag,
        "max_correlation": round(best_corr, 4),
        "corr_at_zero_lag": round(float(corrs[zero_idx]), 4),
        "peak_at_upper_boundary": best_lag == max_lag,
        "peak_at_lower_boundary": best_lag == -max_lag,
    })
    curves[year] = (lags, corrs)

res_df = pd.DataFrame(results)
res_df.to_csv(OUT_CSV, index=False)
print(res_df.to_string(index=False))

# --- Plot: correlation-vs-lag curve per year, peak marked ---
years_sorted = sorted(curves.keys())
_palette = matplotlib.colormaps["tab10"].resampled(max(len(years_sorted), 3))
colors = {y: _palette(i) for i, y in enumerate(years_sorted)}
ncols = 4
nrows = math.ceil(len(years_sorted) / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4.5 * nrows), sharey=True)
axes = axes.flatten()
for ax, year in zip(axes, years_sorted):
    lags, corrs = curves[year]
    ax.plot(lags, corrs, color=colors.get(year), linewidth=2)
    best_idx = int(np.argmax(corrs))
    ax.scatter([lags[best_idx]], [corrs[best_idx]], color="black", zorder=5, s=60,
               label=f"Peak: lag={lags[best_idx]}d, r={corrs[best_idx]:.3f}")
    ax.axvline(0, color="gray", linestyle=":", linewidth=1)
    label = f"{year}" + (" (drought)" if year in DROUGHT_YEARS else " (normal)")
    ax.set_title(label, fontsize=12)
    ax.set_xlabel("Lag applied to NDVI (days)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc="lower center")
for ax in axes[len(years_sorted):]:
    ax.set_visible(False)
axes[0].set_ylabel("Cross-correlation, SIF(t) vs NDVI(t + lag)")
fig.suptitle("Cross-Correlation-Based Lag, Two-Sided Search — Independent Check on the Threshold-Crossing Method, 8 years", fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "cross_correlation_lag.png"), dpi=150)
print(f"\nPlot saved to {OUT_DIR}/cross_correlation_lag.png")
plt.show()
