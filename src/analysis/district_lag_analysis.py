# district-level lag (H2)

import glob
import os
import re

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import statsmodels.api as sm
import statsmodels.formula.api as smf
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds
from scipy import stats

CLIPPED_DIR = "data/processed/clipped"
FRAC_DIR = "data/external/cropland_fraction"
DISTRICTS = "data/raw/marathwada_districts_separate.geojson"
NDVI_CSV = "data/raw/ndvi_obsdate_by_district_2015_2023.csv"
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]

gdf = gpd.read_file(DISTRICTS)
gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf.to_crs("EPSG:4326")
gdf["district"] = gdf["ADM2_NAME"].str.strip()


def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


rows, masks = [], {}
for path in sorted(glob.glob(os.path.join(CLIPPED_DIR, "GOSIF_*_clipped.tif"))):
    m = re.search(r"GOSIF_(\d{4})(\d{3})_clipped\.tif", os.path.basename(path))
    year, doy = int(m.group(1)), int(m.group(2))
    with rasterio.open(path) as src:
        sif = src.read(1).astype("float64")
        tr, bounds, shape = src.transform, src.bounds, src.shape
    with rasterio.open(os.path.join(FRAC_DIR, f"cropland_fraction_{year}.tif")) as fsrc:
        dx = (tr.c - fsrc.transform.c) / fsrc.transform.a
        if abs(dx - round(dx)) > 1e-6:
            raise ValueError(f"{year}: SIF and cropland-fraction grids are offset by part of a pixel")
        win = from_bounds(*bounds, transform=fsrc.transform).round_offsets().round_lengths()
        frac = np.nan_to_num(fsrc.read(1, window=win).astype("float64"))
    key = (tr.c, tr.f, shape)
    if key not in masks:
        masks[key] = {d: ~geometry_mask([g], out_shape=shape, transform=tr)
                      for d, g in zip(gdf["district"], gdf.geometry)}
    valid = ~np.isnan(sif)
    for d, inside in masks[key].items():
        w = np.where(valid & inside, frac, 0.0)
        rows.append({"year": year, "doy": doy, "district": d,
                     "mean_sif": (np.where(valid, sif, 0.0) * w).sum() / w.sum() if w.sum() > 0 else np.nan})
sif_d = pd.DataFrame(rows)
sif_d.to_csv("data/processed/sif_timeseries_by_district.csv", index=False)
print(f"District SIF series: {len(sif_d)} rows "
      f"({sif_d['district'].nunique()} districts x {sif_d['year'].nunique()} years x {sif_d['doy'].nunique()} dates)")

ndvi_d = pd.read_csv(NDVI_CSV)
ndvi_d["district"] = ndvi_d["district"].str.strip()
print(f"District NDVI series: {len(ndvi_d)} rows, {ndvi_d['mean_ndvi'].isna().sum()} empty composites")


def crossing(doys, vals, t):
    for i in range(len(vals) - 1):
        v1, v2 = vals[i], vals[i + 1]
        if v1 >= t and v2 < t:
            return doys[i] + (v1 - t) / (v1 - v2) * (doys[i + 1] - doys[i])
    return np.nan


def lags_for(s, n):
    s, n = s.sort_values("doy"), n.dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
    t = s["doy"].values + 3.5
    sn = minmax(s["mean_sif"].values)
    nn = np.interp(t, n["mean_obs_doy"].values, minmax(n["mean_ndvi"].values), left=np.nan, right=np.nan)
    ps, pn = t[np.nanargmax(sn)], t[np.nanargmax(nn)]
    th = []
    for thr in THRESHOLDS:
        a = crossing(t[t >= ps], sn[t >= ps], thr)
        b = crossing(t[t >= pn], nn[t >= pn], thr)
        if not (np.isnan(a) or np.isnan(b)):
            th.append(b - a)
    keep = (t >= ps) & ~np.isnan(nn)
    tt, ss, nd = t[keep], sn[keep], nn[keep]
    grid = np.arange(tt.min(), tt.max() + 1)
    sd, ndd = np.interp(grid, tt, ss), np.interp(grid, tt, nd)
    sd, ndd = sd - sd.mean(), ndd - ndd.mean()
    ml = int(len(grid) / 4)
    lags = np.arange(-ml, ml + 1)
    cs = [np.corrcoef(sd[:-L], ndd[L:])[0, 1] if L > 0 else
          np.corrcoef(sd[-L:], ndd[:L])[0, 1] if L < 0 else np.corrcoef(sd, ndd)[0, 1] for L in lags]
    i = int(np.argmax(cs))
    return (np.mean(th) if th else np.nan), len(th), int(lags[i]), abs(lags[i]) == ml


recs = []
for (d, y), s in sif_d.groupby(["district", "year"]):
    n = ndvi_d[(ndvi_d["district"] == d) & (ndvi_d["year"] == y)]
    tl, nth, xl, edge = lags_for(s, n)
    recs.append({"district": d, "year": y, "threshold_lag": tl, "n_thresholds": nth,
                 "xcorr_lag": xl, "xcorr_at_search_edge": edge})
lag = pd.DataFrame(recs)

anom = pd.read_csv("data/processed/district_climatology_anomaly_comparison.csv")[
    ["district", "year", "zscore_region_baseline", "zscore_district_baseline"]]
lag = lag.merge(anom, on=["district", "year"], how="left")
lag.to_csv("data/processed/district_lag_by_year.csv", index=False)

print("\nThreshold-crossing lag (days), district x year:")
print(lag.pivot(index="district", columns="year", values="threshold_lag").round(1).to_string())
print(f"\nDistrict-years where SIF leads (threshold lag > 0): {(lag['threshold_lag'] > 0).sum()} of {lag['threshold_lag'].notna().sum()}")
print(f"District-years where cross-correlation says SIF leads / tie / NDVI leads: "
      f"{(lag['xcorr_lag'] > 0).sum()} / {(lag['xcorr_lag'] == 0).sum()} / {(lag['xcorr_lag'] < 0).sum()}"
      f"  ({lag['xcorr_at_search_edge'].sum()} at search edge)")

tests = []
ok = lag.dropna(subset=["threshold_lag"])
fit = smf.ols("threshold_lag ~ C(district) + C(year)", data=ok).fit()
an = sm.stats.anova_lm(fit, typ=2)
F, p = an.loc["C(district)", "F"], an.loc["C(district)", "PR(>F)"]
tests.append({"test": "H2 two-way ANOVA, district effect (threshold lag)", "statistic": F, "p_value": p})
print(f"\nH2 -- two-way ANOVA (lag ~ district + year): district F = {F:.2f}, p = {p:.4f}")
wide = ok.pivot(index="year", columns="district", values="threshold_lag").dropna()
fr = stats.friedmanchisquare(*[wide[c].values for c in wide.columns])
tests.append({"test": f"H2 Friedman test, districts across {len(wide)} complete years", "statistic": fr.statistic, "p_value": fr.pvalue})
print(f"H2 -- Friedman test (years as blocks, n={len(wide)}): chi2 = {fr.statistic:.2f}, p = {fr.pvalue:.4f}")
dm = ok.groupby("district")["threshold_lag"].agg(["mean", "std", "count"]).round(1).sort_values("mean")
print("\nMean lag by district (days):")
print(dm.to_string())

for zcol in ["zscore_region_baseline", "zscore_district_baseline"]:
    sub = ok.dropna(subset=[zcol])
    r, pr = stats.pearsonr(sub[zcol], sub["threshold_lag"])
    rho, prho = stats.spearmanr(sub[zcol], sub["threshold_lag"])
    wy = sub.assign(z_dm=sub[zcol] - sub.groupby("year")[zcol].transform("mean"),
                    l_dm=sub["threshold_lag"] - sub.groupby("year")["threshold_lag"].transform("mean"))
    rw, pw = stats.pearsonr(wy["z_dm"], wy["l_dm"])
    cl = smf.ols(f"threshold_lag ~ {zcol}", data=sub).fit(cov_type="cluster", cov_kwds={"groups": sub["year"]})
    drought = sub[sub[zcol] < -0.5]["threshold_lag"]
    normal = sub[sub[zcol] >= -0.5]["threshold_lag"]
    t, pt = stats.ttest_ind(drought, normal, equal_var=False)
    print(f"\nH3 at district level, rainfall z-score = {zcol} (n = {len(sub)} district-years):")
    print(f"  Pearson r = {r:.3f} (p = {pr:.4f}); Spearman rho = {rho:.3f} (p = {prho:.4f})")
    print(f"  within-year r = {rw:.3f} (p = {pw:.4f}); OLS slope clustered by year = "
          f"{cl.params[zcol]:.2f} days per z (p = {cl.pvalues[zcol]:.4f})")
    print(f"  drought district-years (z < -0.5): n = {len(drought)}, mean lag {drought.mean():.1f} d; "
          f"normal: n = {len(normal)}, mean lag {normal.mean():.1f} d; Welch t = {t:.2f}, p = {pt:.4f}")
    print("  (H3 predicts a NEGATIVE r: drier = bigger lag)")
    for name, st, pv in [("Pearson r", r, pr), ("within-year r", rw, pw),
                         ("clustered OLS slope", cl.params[zcol], cl.pvalues[zcol]), ("Welch t drought vs normal", t, pt)]:
        tests.append({"test": f"H3 district-level, {zcol}: {name}", "statistic": st, "p_value": pv})
    tests.append({"test": f"H3 district-level, {zcol}: n drought district-years", "statistic": len(drought), "p_value": np.nan})

pd.DataFrame(tests).to_csv("data/processed/district_lag_tests.csv", index=False)
print("\nSaved data/processed/district_lag_by_year.csv and data/processed/district_lag_tests.csv")

fig, ax = plt.subplots(figsize=(10, 6))
order = dm.index.tolist()
for i, d in enumerate(order):
    v = ok[ok["district"] == d]
    ax.scatter(np.full(len(v), i) + np.random.default_rng(i).uniform(-0.12, 0.12, len(v)), v["threshold_lag"],
               c=np.where(v["zscore_district_baseline"] < -0.5, "#B23A48", "#2FA88C"), s=45, edgecolor="white", zorder=3)
    ax.hlines(v["threshold_lag"].mean(), i - 0.3, i + 0.3, color="black", lw=2, zorder=4)
ax.axhline(0, color="gray", ls=":")
ax.set_xticks(range(len(order)))
ax.set_xticklabels(order, rotation=20)
ax.set_ylabel("Threshold-crossing lag, NDVI behind SIF (days)")
ax.set_title(f"SIF-to-NDVI lag by district, 9 years (ANOVA district effect p = {p:.3f})\n"
             "red = drought district-year (own-baseline z < -0.5), black bar = district mean")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/figures/district_lag_by_year.png", dpi=200)
print("Figure saved to outputs/figures/district_lag_by_year.png")
