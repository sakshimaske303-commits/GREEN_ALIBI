# district seasonal SIF

import geopandas as gpd
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from esda.moran import Moran
from libpysal.weights import Queen
from scipy import stats

TS_CSV = "data/processed/sif_timeseries_by_district.csv"
OLD_CSV = "data/processed/sif_by_district.csv"
RAIN_CSV = "data/processed/rainfall_anomaly_by_district.csv"
GEOJSON = "data/raw/marathwada_districts_separate.geojson"
OUT_SIF = "data/processed/sif_by_district_seasonal.csv"
OUT_TESTS = "data/processed/district_seasonal_sif_tests.csv"
OUT_MORAN = "data/processed/spatial_autocorrelation_morans_i_seasonal_sif.csv"

ts = pd.read_csv(TS_CSV)
old = pd.read_csv(OLD_CSV)
rain = pd.read_csv(RAIN_CSV)[["district", "year", "anomaly_pct", "anomaly_zscore"]]


def window_mean(lo, hi):
    return ts[(ts["doy"] >= lo) & (ts["doy"] <= hi)].groupby(["district", "year"])["mean_sif"].mean()


key = ["district", "year"]
sif = pd.DataFrame({
    "doy273": ts[ts["doy"] == 273].set_index(key)["mean_sif"],
    "season_jun_dec": window_mean(152, 366),
    "jas": window_mean(182, 273),
    "aug_oct": window_mean(213, 304),
    "peak": ts.groupby(key)["mean_sif"].max(),
    "n_composites": ts.groupby(key)["mean_sif"].count(),
}).reset_index()
sif = sif.merge(old[key + ["mean_sif"]].rename(columns={"mean_sif": "doy273_old_unweighted"}), on=key)
sif.to_csv(OUT_SIF, index=False)

chk = sif["doy273"].corr(sif["doy273_old_unweighted"])
print(f"Check: cropland-weighted DOY 273 vs old unweighted DOY 273, r = {chk:.4f} "
      f"(max |diff| = {(sif['doy273'] - sif['doy273_old_unweighted']).abs().max():.4f})")
print(f"Composites per district-year: {sif['n_composites'].min()}-{sif['n_composites'].max()}\n")

m = sif.merge(rain, on=key)
assert len(m) == 72, f"expected 72 district-years, got {len(m)}"

rows = []
print(f"{'SIF measure':24s} {'pooled r':>9s} {'rho':>6s} {'within-yr r':>12s} {'within-dist r':>14s} "
      f"{'clust(yr) p':>12s} {'2-way FE p':>11s}")
for c in ["doy273_old_unweighted", "doy273", "season_jun_dec", "jas", "aug_oct", "peak"]:
    r, p = stats.pearsonr(m["anomaly_pct"], m[c])
    rho, prho = stats.spearmanr(m["anomaly_pct"], m[c])
    wy_s = m[c] - m.groupby("year")[c].transform("mean")
    wy_a = m["anomaly_pct"] - m.groupby("year")["anomaly_pct"].transform("mean")
    wy_r, wy_p = stats.pearsonr(wy_a, wy_s)
    wd_s = m[c] - m.groupby("district")[c].transform("mean")
    wd_a = m["anomaly_pct"] - m.groupby("district")["anomaly_pct"].transform("mean")
    wd_r, wd_p = stats.pearsonr(wd_a, wd_s)
    cl = smf.ols(f"{c} ~ anomaly_pct", m).fit(cov_type="cluster", cov_kwds={"groups": m["year"]})
    fe = smf.ols(f"{c} ~ anomaly_pct + C(district) + C(year)", m).fit(
        cov_type="cluster", cov_kwds={"groups": m["district"]})
    rows.append({"sif_measure": c, "n": len(m), "pearson_r": r, "pearson_p": p, "spearman_rho": rho,
                 "spearman_p": prho, "within_year_r": wy_r, "within_year_p": wy_p,
                 "within_district_r": wd_r, "within_district_p": wd_p,
                 "ols_clustered_year_p": cl.pvalues["anomaly_pct"],
                 "twoway_fe_slope": fe.params["anomaly_pct"], "twoway_fe_p_clustered_district": fe.pvalues["anomaly_pct"]})
    print(f"{c:24s} {r:9.3f} {rho:6.3f} {wy_r:8.3f}{'*' if wy_p < .05 else ' ':4s} {wd_r:10.3f}{'*' if wd_p < .05 else ' ':4s} "
          f"{cl.pvalues['anomaly_pct']:12.4f} {fe.pvalues['anomaly_pct']:11.4f}")
pd.DataFrame(rows).to_csv(OUT_TESTS, index=False)
print("(* = p < 0.05)")

print("\nLowest / highest SIF district per year:")
for c in ["doy273", "season_jun_dec"]:
    lo = m.loc[m.groupby("year")[c].idxmin()]
    hi = m.loc[m.groupby("year")[c].idxmax()]
    print(f"  {c:15s} lowest: {lo['district'].value_counts().to_dict()}   highest: {hi['district'].value_counts().to_dict()}")

print("\nDistrict means over 9 years (seasonal SIF, rainfall anomaly % vs region-wide baseline):")
print(m.groupby("district")[["season_jun_dec", "anomaly_pct"]].mean().sort_values("season_jun_dec").round(3).to_string())

gdf = gpd.read_file(GEOJSON)
w = Queen.from_dataframe(gdf, use_index=False, ids=gdf["ADM2_NAME"].str.strip().tolist())
w.transform = "r"
np.random.seed(42)
mo = []
for y in sorted(m["year"].unique()):
    v = m[m["year"] == y].set_index("district").loc[w.id_order, "season_jun_dec"].values
    mi = Moran(v, w, permutations=9999)
    mo.append({"year": y, "variable": "season_mean_sif", "morans_i": round(mi.I, 4),
               "p_value_permutation": round(mi.p_sim, 4)})
mo = pd.DataFrame(mo)
mo.to_csv(OUT_MORAN, index=False)
print("\nMoran's I, seasonal SIF:")
print(mo.to_string(index=False))
print(f"Significant (p < 0.05) in {(mo['p_value_permutation'] < 0.05).sum()} of {len(mo)} years")
print(f"\nSaved {OUT_SIF}, {OUT_TESTS}, {OUT_MORAN}")
