# rainfall baseline sensitivity

import numpy as np
import pandas as pd
from scipy import stats

TOTALS = "data/raw/chirps_seasonal_totals_1981_2023.csv"
OLD_CLIM = "data/raw/marathwada_rainfall_climatology_2001_2020.csv"
STUDY = list(range(2015, 2024))
DROUGHT_Z = -0.5
BASELINES = {"B0_2001_2020": (2001, 2020), "B1_2001_2014": (2001, 2014),
             "B2_1981_2014": (1981, 2014), "B3_1991_2020": (1991, 2020)}

tot = pd.read_csv(TOTALS)
region = tot[tot["unit"] == "Marathwada"].set_index("year")["rainfall_mm"].sort_index()
dist = tot[tot["unit"] != "Marathwada"].rename(columns={"unit": "district"})
assert len(region) == 43 and dist["district"].nunique() == 8, "unexpected export size"

old = pd.read_csv(OLD_CLIM).set_index("year")["total_rainfall_mm"]
diff = (region.loc[old.index] - old).abs().max()
print(f"Check vs existing 2001-2020 climatology file: max |difference| = {diff:.2f} mm "
      f"(mean {region.loc[2001:2020].mean():.1f} vs {old.mean():.1f})")

yrs = region.index.values
lr = stats.linregress(yrs, region.values)
tau, tp = stats.kendalltau(yrs, region.values)
print(f"Trend 1981-2023: {lr.slope * 10:+.1f} mm/decade (p = {lr.pvalue:.3f}); Kendall tau = {tau:+.2f} (p = {tp:.3f})")
for name, (a, b) in BASELINES.items():
    s = region.loc[a:b]
    print(f"  {name}: mean {s.mean():.1f} mm, std {s.std():.1f} mm, n = {len(s)}")

lag = pd.read_csv("data/processed/sif_ndvi_lag_by_threshold.csv").groupby("year")["lag_days"].mean()
yld = pd.read_csv("data/processed/crop_yield_validation_summary.csv").set_index("study_year")

reg_rows, summ = [], []
for name, (a, b) in BASELINES.items():
    mu, sd = region.loc[a:b].mean(), region.loc[a:b].std()
    for y in STUDY:
        z = (region[y] - mu) / sd
        reg_rows.append({"baseline": name, "year": y, "rainfall_mm": region[y],
                         "anomaly_pct": (region[y] - mu) / mu * 100, "zscore": z,
                         "is_drought": z < DROUGHT_Z, "lag_days": lag[y]})
reg = pd.DataFrame(reg_rows)

print("\nRegional z-score of each study year under each baseline (D = drought, z < -0.5):")
pv = reg.pivot(index="year", columns="baseline", values="zscore")
flag = reg.pivot(index="year", columns="baseline", values="is_drought")
print(pv.round(2).astype(str).where(~flag, pv.round(2).astype(str) + " D").to_string())
print("\nRegional anomaly % under each baseline:")
print(reg.pivot(index="year", columns="baseline", values="anomaly_pct").round(1).to_string())

print("\nRegional H3 (drought vs normal mean lag) and crop-yield check under each baseline:")
for name in BASELINES:
    r = reg[reg["baseline"] == name]
    dy = sorted(r.loc[r["is_drought"], "year"])
    d, n = r.loc[r["is_drought"], "lag_days"], r.loc[~r["is_drought"], "lag_days"]
    ys = yld.loc[[y for y in STUDY if y in yld.index and bool(yld.loc[y, "has_yield_data"])]]
    yd = ys.loc[[y for y in ys.index if y in dy], "yield_anomaly_index"]
    yn = ys.loc[[y for y in ys.index if y not in dy], "yield_anomaly_index"]
    print(f"  {name}: drought years {dy} | lag drought {d.mean():.1f} vs normal {n.mean():.1f} d "
          f"| yield index drought {yd.mean():+.2f} vs normal {yn.mean():+.2f}")
    summ.append({"baseline": name, "level": "region", "drought_units": ",".join(map(str, dy)),
                 "n_drought": len(dy), "lag_drought": d.mean(), "lag_normal": n.mean(),
                 "yield_drought": yd.mean(), "yield_normal": yn.mean()})

dl = pd.read_csv("data/processed/district_lag_by_year.csv")[["district", "year", "threshold_lag"]]
drows = []
for name, (a, b) in BASELINES.items():
    mu_r, sd_r = region.loc[a:b].mean(), region.loc[a:b].std()
    clim_d = dist[(dist["year"] >= a) & (dist["year"] <= b)].groupby("district")["rainfall_mm"].agg(["mean", "std"])
    cur = dist[dist["year"].isin(STUDY)].merge(clim_d, left_on="district", right_index=True)
    cur["z_region_baseline"] = (cur["rainfall_mm"] - mu_r) / sd_r
    cur["z_district_baseline"] = (cur["rainfall_mm"] - cur["mean"]) / cur["std"]
    cur["baseline"] = name
    drows.append(cur.drop(columns=["mean", "std"]))
dd = pd.concat(drows).merge(dl, on=["district", "year"])
assert len(dd) == 72 * len(BASELINES)

print("\nDistrict level (72 district-years): drought district-years and H3 under each baseline")
b0 = dd[dd["baseline"] == "B0_2001_2020"].set_index(["district", "year"])
for name in BASELINES:
    x = dd[dd["baseline"] == name].set_index(["district", "year"])
    for zc in ["z_region_baseline", "z_district_baseline"]:
        dr = x[zc] < DROUGHT_Z
        changed = int((dr != (b0[zc] < DROUGHT_Z)).sum())
        t, p = stats.ttest_ind(x.loc[dr, "threshold_lag"], x.loc[~dr, "threshold_lag"], equal_var=False)
        print(f"  {name} {zc:20s}: n drought = {dr.sum():2d} ({changed:2d} changed vs B0) | lag {x.loc[dr, 'threshold_lag'].mean():.1f} "
              f"vs {x.loc[~dr, 'threshold_lag'].mean():.1f} d, Welch t = {t:+.2f}, p = {p:.3f}")
        summ.append({"baseline": name, "level": f"district_{zc}", "n_drought": int(dr.sum()),
                     "n_changed_vs_B0": changed, "lag_drought": x.loc[dr, "threshold_lag"].mean(),
                     "lag_normal": x.loc[~dr, "threshold_lag"].mean(), "welch_t": t, "welch_p": p})

for zc in ["z_region_baseline", "z_district_baseline"]:
    rs = [stats.pearsonr(dd.loc[dd["baseline"] == b, zc], dd.loc[dd["baseline"] == b, "threshold_lag"])[0] for b in BASELINES]
    print(f"District lag vs {zc}: Pearson r across baselines = {', '.join(f'{r:.3f}' for r in rs)}")

reg.to_csv("data/processed/baseline_sensitivity_region.csv", index=False)
dd.to_csv("data/processed/baseline_sensitivity_district.csv", index=False)
pd.DataFrame(summ).to_csv("data/processed/baseline_sensitivity_summary.csv", index=False)
print("\nSaved baseline_sensitivity_region.csv, baseline_sensitivity_district.csv, baseline_sensitivity_summary.csv")
