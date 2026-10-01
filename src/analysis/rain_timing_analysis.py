# rainfall timing vs lag

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


def longest_run(mask):
    best = cur = 0
    for m in mask:
        cur = cur + 1 if m else 0
        best = max(best, cur)
    return best


def timing_metrics(df):
    df = df.sort_values("date")
    doy = df["date"].dt.dayofyear.values
    r = df["rain_mm"].fillna(0).values
    m = df["date"].dt.month.values
    total = r.sum()
    cum = np.cumsum(r) / total
    jjas = (m >= 6) & (m <= 9)
    return {
        "total_mm": total,
        "jun_jul_mm": r[(m == 6) | (m == 7)].sum(),
        "aug_mm": r[m == 8].sum(),
        "sep_mm": r[m == 9].sum(),
        "oct_dec_mm": r[m >= 10].sum(),
        "centroid_doy": (doy * r).sum() / total,
        "doy_50pct": doy[np.argmax(cum >= 0.5)],
        "doy_90pct": doy[np.argmax(cum >= 0.9)],
        "longest_dry_spell_jjas": longest_run(r[jjas] < 1.0),
        "dry_days_aug_sep": int(((r < 1.0) & ((m == 8) | (m == 9))).sum()),
    }


METRICS = ["total_mm", "jun_jul_mm", "aug_mm", "sep_mm", "oct_dec_mm", "centroid_doy",
           "doy_50pct", "doy_90pct", "longest_dry_spell_jjas", "dry_days_aug_sep"]

reg = pd.read_csv("data/raw/chirps_daily_region_2001_2023.csv", parse_dates=["date"])
reg["year"] = reg["date"].dt.year
yr = pd.DataFrame([{"year": y, **timing_metrics(g)} for y, g in reg.groupby("year")])

chk = yr.merge(pd.read_csv("data/processed/rainfall_anomaly_summary.csv")[["year", "total_rainfall_mm"]], on="year")
print("Check: daily sums vs the seasonal totals used everywhere else (mm):")
print((chk["total_mm"] - chk["total_rainfall_mm"]).round(2).describe()[["min", "max"]].to_string())

base = yr[(yr["year"] >= 2001) & (yr["year"] <= 2020)]
study = yr[yr["year"] >= 2015].copy()
for c in METRICS:
    study[f"{c}_z"] = (study[c] - base[c].mean()) / base[c].std()
study.to_csv("data/processed/rain_timing_by_year.csv", index=False)

pd.set_option("display.width", 200)
print("\nRainfall timing, study years (z = vs 2001-2020 normal):")
show = study[["year"] + METRICS].round(1)
print(show.to_string(index=False))
print("\n2001-2020 normal:  " + ", ".join(f"{c}={base[c].mean():.1f}±{base[c].std():.1f}" for c in METRICS))
print("\n2018 z-scores and rank among the 9 study years (1 = lowest):")
for c in METRICS:
    rank = int(study[c].rank(method="min").loc[study["year"] == 2018].iloc[0])
    print(f"  {c:24s} 2018 = {study.loc[study.year == 2018, c].iloc[0]:7.1f}   z = "
          f"{study.loc[study.year == 2018, c + '_z'].iloc[0]:+.2f}   rank {rank}/9")

lag = pd.read_csv("data/processed/final_summary_rainfall_lag.csv")[["year", "mean_lag_days"]]
rs = study.merge(lag, on="year")
out = []
print("\nSpearman correlation with the regional lag (n = 9 years, exploratory):")
for c in METRICS:
    rho, p = stats.spearmanr(rs[c], rs["mean_lag_days"])
    out.append({"level": "region (n=9)", "metric": c, "statistic": rho, "p_value": p, "method": "Spearman rho"})
    print(f"  {c:24s} rho = {rho:+.2f}  p = {p:.3f}")

dd = pd.read_csv("data/raw/chirps_daily_by_district_2015_2023.csv", parse_dates=["date"])
dd["district"] = dd["district"].str.strip()
dd["year"] = dd["date"].dt.year
dm = pd.DataFrame([{"district": d, "year": y, **timing_metrics(g)} for (d, y), g in dd.groupby(["district", "year"])])
dm.to_csv("data/processed/rain_timing_by_district_year.csv", index=False)
dl = dm.merge(pd.read_csv("data/processed/district_lag_by_year.csv")[["district", "year", "threshold_lag"]],
              on=["district", "year"]).dropna(subset=["threshold_lag"])
print(f"\nDistrict-level (n = {len(dl)} district-years): within-year correlation and OLS clustered by year")
for c in METRICS:
    w = dl.assign(x=dl[c] - dl.groupby("year")[c].transform("mean"),
                  y=dl["threshold_lag"] - dl.groupby("year")["threshold_lag"].transform("mean"))
    rw, pw = stats.pearsonr(w["x"], w["y"])
    fit = smf.ols(f"threshold_lag ~ {c}", data=dl).fit(cov_type="cluster", cov_kwds={"groups": dl["year"]})
    out.append({"level": "district, within-year", "metric": c, "statistic": rw, "p_value": pw, "method": "Pearson r (year-demeaned)"})
    out.append({"level": "district, pooled", "metric": c, "statistic": fit.params[c], "p_value": fit.pvalues[c],
                "method": "OLS slope, SE clustered by year"})
    print(f"  {c:24s} within-year r = {rw:+.2f} (p = {pw:.3f})   pooled slope p = {fit.pvalues[c]:.3f}")

pd.DataFrame(out).to_csv("data/processed/rain_timing_vs_lag.csv", index=False)
print("\nSaved rain_timing_by_year.csv, rain_timing_by_district_year.csv, rain_timing_vs_lag.csv")
print("Note: 10 timing measures are tested here, so about one p < 0.05 would be expected by chance alone.")
