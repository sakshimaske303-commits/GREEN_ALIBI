# how many cropland pixels stand behind each NDVI composite, and does it matter?
#
# MOD13Q1 pixels are kept only where SummaryQA is good/marginal, so during the
# monsoon many 16-day composites rest on a small, shifting share of the cropland
# pixels. This script reports that share and recomputes the regional lag after
# dropping composites below 10%, 25% and 50% coverage.

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]
MIN_COVER = [0.0, 0.10, 0.25, 0.50]

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])

nd = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv").dropna(subset=["mean_ndvi", "mean_obs_doy"])
nd["coverage"] = nd["valid_pixel_count"] / nd["valid_pixel_count"].max()
ndd = pd.read_csv("data/raw/ndvi_obsdate_by_district_2015_2023.csv")
ndd["district"] = ndd["district"].str.strip()
ndd["coverage"] = ndd["valid_pixel_count"] / ndd.groupby("district")["valid_pixel_count"].transform("max")
m = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")


def crossing(t, v, th):
    for i in range(len(v) - 1):
        if v[i] >= th and v[i + 1] < th:
            return t[i] + (v[i] - th) / (v[i] - v[i + 1]) * (t[i + 1] - t[i])
    return np.nan


def minmax(v):
    return (v - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v))


def threshold_lag(ts, sif, tn, ndvi):
    sn = minmax(sif)
    nn = np.interp(ts, tn, minmax(ndvi), left=np.nan, right=np.nan)
    ps, pn = ts[np.nanargmax(sn)], ts[np.nanargmax(nn)]
    out = [crossing(ts[ts >= pn], nn[ts >= pn], th) - crossing(ts[ts >= ps], sn[ts >= ps], th) for th in THRESHOLDS]
    out = np.array(out)
    return np.nanmean(out) if np.isfinite(out).any() else np.nan


rows = []
for y in sorted(m["year"].unique()):
    s = m[m["year"] == y].sort_values("doy")
    for c in MIN_COVER:
        n = nd[(nd["year"] == y) & (nd["coverage"] >= c)].sort_values("mean_obs_doy")
        rows.append({"year": y, "is_drought": y in DROUGHT, "min_coverage": c, "n_ndvi_composites": len(n),
                     "lag_days": threshold_lag(s["doy"].values, s["mean_sif"].values,
                                               n["mean_obs_doy"].values, n["mean_ndvi"].values)})
L = pd.DataFrame(rows)
L.to_csv("data/processed/ndvi_coverage_lag_sensitivity.csv", index=False)
nd[["year", "doy_start", "mean_obs_doy", "valid_pixel_count", "coverage"]].to_csv(
    "data/processed/ndvi_coverage_region.csv", index=False)

print("Regional NDVI composites by cropland-pixel coverage (share of the best-covered composite):")
print(f"  < 10%: {(nd['coverage'] < 0.10).sum()} of {len(nd)};  < 25%: {(nd['coverage'] < 0.25).sum()};  "
      f"< 50%: {(nd['coverage'] < 0.50).sum()}")
print(f"District composites < 10%: {(ndd['coverage'] < 0.10).sum()} of {len(ndd)}; "
      f"< 25%: {(ndd['coverage'] < 0.25).sum()}")
print("\nCoverage by composite start day and year (%):")
print((nd.pivot(index="doy_start", columns="year", values="coverage") * 100).round(0).to_string())
print("\nRegional mean threshold lag (days) after dropping low-coverage NDVI composites:")
print(L.pivot(index="year", columns="min_coverage", values="lag_days").round(1).to_string())
for c in MIN_COVER:
    sub = L[L["min_coverage"] == c]
    print(f"  min coverage {c:.0%}: SIF first in {(sub['lag_days'] > 0).sum()}/9; drought mean "
          f"{sub.loc[sub['is_drought'], 'lag_days'].mean():.1f} vs normal {sub.loc[~sub['is_drought'], 'lag_days'].mean():.1f} d")

os.makedirs("outputs/figures", exist_ok=True)
pv = nd.pivot(index="year", columns="doy_start", values="coverage") * 100
fig, ax = plt.subplots(figsize=(10, 4))
im = ax.imshow(pv.values, cmap="viridis", vmin=0, vmax=100, aspect="auto")
ax.set_xticks(range(pv.shape[1]))
ax.set_xticklabels([str(c) for c in pv.columns], fontsize=8)
ax.set_yticks(range(pv.shape[0]))
ax.set_yticklabels(pv.index)
for i in range(pv.shape[0]):
    for j in range(pv.shape[1]):
        v = pv.values[i, j]
        if np.isfinite(v):
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7, color="white" if v < 50 else "black")
ax.set_xlabel("MOD13Q1 composite start day of year")
ax.set_title("Share of cropland pixels with good/marginal NDVI in each composite (%), Marathwada")
plt.colorbar(im, ax=ax, label="% of best-covered composite")
plt.tight_layout()
plt.savefig("outputs/figures/ndvi_coverage.png", dpi=200)
print("\nSaved ndvi_coverage_lag_sensitivity.csv, ndvi_coverage_region.csv, outputs/figures/ndvi_coverage.png")
