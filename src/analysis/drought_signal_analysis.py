# drought-specific signal: SIF vs NDVI alarm dates

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

THRESHOLDS = [-0.5, -1.0, -1.5, -2.0, -3.0]
MAIN_THR = -3.0  # the only threshold with no false alarm in any normal year at regional scale
START_DOY = 182
DECLARATION_2015 = 289
DECLARATION_2018 = 304

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])
YEARS = sorted(rain["year"])

m = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
reg = {v: m.pivot(index="year", columns="sif_start_doy", values=c) for v, c in [("SIF", "mean_sif"), ("NDVI", "mean_ndvi")]}
DOYS = reg["SIF"].columns.values

sd = pd.read_csv("data/processed/sif_timeseries_by_district.csv")
nd = pd.read_csv("data/raw/ndvi_obsdate_by_district_2015_2023.csv")
nd["district"] = nd["district"].str.strip()
rows = []
for (d, y), g in sd.groupby(["district", "year"]):
    g = g.sort_values("doy")
    n = nd[(nd["district"] == d) & (nd["year"] == y)].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
    ndvi = np.interp(g["doy"].values + 3.5, n["mean_obs_doy"], n["mean_ndvi"], left=np.nan, right=np.nan)
    rows += [{"district": d, "year": y, "doy": a, "SIF": b, "NDVI": c} for a, b, c in zip(g["doy"], g["mean_sif"], ndvi)]
dist = pd.DataFrame(rows)
# district-years are classified against each district's own 2001-2020 rainfall baseline (main),
# and against the regional baseline as a sensitivity check
rd = pd.read_csv("data/processed/district_climatology_anomaly_comparison.csv")
DROUGHT_D = {(r.district, r.year) for r in rd.itertuples() if r.zscore_district_baseline < -0.5}
DROUGHT_D_REGIONAL = {(r.district, r.year) for r in rd.itertuples() if r.zscore_region_baseline < -0.5}


def anomaly(table, year, normal_years):
    ref = table.loc[[y for y in normal_years if y != year]]
    return ((table.loc[year] - ref.mean()) / ref.std(ddof=1)).values


def first_alarm(z, thr):
    for i in range(len(DOYS) - 1):
        if DOYS[i] >= START_DOY and z[i] < thr and z[i + 1] < thr:
            return DOYS[i] + 3.5
    return np.nan


normal_years = [y for y in YEARS if y not in DROUGHT]
zreg = {v: {y: anomaly(reg[v], y, normal_years) for y in YEARS} for v in reg}
out = []
for y in YEARS:
    r = {"year": y, "is_drought": y in DROUGHT}
    for v in ["SIF", "NDVI"]:
        z = zreg[v][y]
        zz = np.where(DOYS >= START_DOY, z, np.nan)
        r[f"{v}_min_z"] = np.nanmin(zz)
        r[f"{v}_min_z_doy"] = DOYS[np.nanargmin(zz)] + 3.5
        for thr in THRESHOLDS:
            r[f"{v}_alarm_{thr}"] = first_alarm(z, thr)
    out.append(r)
R = pd.DataFrame(out)
R.to_csv("data/processed/drought_signal_region.csv", index=False)


def fmt(doy):
    return "-" if np.isnan(doy) else (pd.Timestamp("2018-01-01") + pd.Timedelta(days=float(doy) - 1)).strftime("%d %b")


pd.set_option("display.width", 220)
print(f"REGION -- first date the anomaly stays below z = {MAIN_THR} for two composites (from 1 July)")
print(f"{'year':6s}{'':9s}{'SIF alarm':>10s}{'NDVI alarm':>12s}{'SIF lead':>10s}   min z SIF (date)   min z NDVI (date)")
for _, r in R.iterrows():
    s, n = r[f"SIF_alarm_{MAIN_THR}"], r[f"NDVI_alarm_{MAIN_THR}"]
    lead = "" if np.isnan(s) or np.isnan(n) else f"{n - s:+.0f} d"
    print(f"{int(r.year):<6d}{'drought' if r.is_drought else 'normal':9s}{fmt(s):>10s}{fmt(n):>12s}{lead:>10s}   "
          f"{r.SIF_min_z:+.2f} ({fmt(r.SIF_min_z_doy)})     {r.NDVI_min_z:+.2f} ({fmt(r.NDVI_min_z_doy)})")
for thr in THRESHOLDS:
    fa = {v: int(R.loc[~R["is_drought"], f"{v}_alarm_{thr}"].notna().sum()) for v in ["SIF", "NDVI"]}
    hit = {v: int(R.loc[R["is_drought"], f"{v}_alarm_{thr}"].notna().sum()) for v in ["SIF", "NDVI"]}
    print(f"  z < {thr}: drought years flagged SIF {hit['SIF']}/2, NDVI {hit['NDVI']}/2 | "
          f"normal years flagged (false alarms) SIF {fa['SIF']}/7, NDVI {fa['NDVI']}/7")
decl = pd.read_csv("data/external/official_drought_declarations.csv")
lag = pd.read_csv("data/processed/sif_ndvi_lag_by_threshold.csv")
lag = lag[lag["threshold"] == 0.9].set_index("year")
print("\nDays before each official declaration (seasonal 0.9 crossing vs drought-specific alarm, z < -3 = no false alarm in any normal year):")
for dcl in decl.itertuples():
    ry = R.set_index("year").loc[dcl.year]
    parts = [f"  {dcl.year} {dcl.date} ({'final' if dcl.is_final_declaration else 'first-stage'}):"]
    for v, col in [("SIF", "sif_crossing_doy"), ("NDVI", "ndvi_crossing_doy")]:
        parts.append(f"{v} 0.9 crossing {dcl.doy - lag.loc[dcl.year, col]:.0f} d")
    for v in ["SIF", "NDVI"]:
        a = ry[f"{v}_alarm_-3.0"]
        parts.append(f"{v} drought alarm {'none' if np.isnan(a) else f'{dcl.doy - a:.0f} d'}")
    print(" | ".join(parts))

# keep all composite dates, so NDVI alarms are not shifted one composite early
tabs = {v: dist.pivot_table(index=["district", "year"], columns="doy", values=v, dropna=False).reindex(columns=DOYS)
        for v in ["SIF", "NDVI"]}
assert all(list(t.columns) == list(DOYS) for t in tabs.values())


def district_alarms(drought_set):
    rows_ = []
    for (d, y) in tabs["SIF"].index:
        nrm = [yy for yy in YEARS if (d, yy) not in drought_set]
        r = {"district": d, "year": y, "is_drought": (d, y) in drought_set}
        for v in ["SIF", "NDVI"]:
            z = anomaly(tabs[v].loc[d], y, nrm)
            r[f"{v}_z"] = z
            for thr in THRESHOLDS:
                r[f"{v}_alarm_{thr}"] = first_alarm(z, thr)
        rows_.append(r)
    return pd.DataFrame(rows_)


def district_summary(D, label):
    nd_, nn_ = int(D["is_drought"].sum()), int((~D["is_drought"]).sum())
    print(f"\nDISTRICT ({label}) -- {nd_} drought and {nn_} normal district-years")
    print(f"{'threshold':10s}{'hit SIF':>9s}{'hit NDVI':>10s}{'false SIF':>11s}{'false NDVI':>12s}   among drought hits: SIF earlier / same / NDVI earlier, median SIF lead")
    out = []
    for thr in THRESHOLDS:
        dd = D[D["is_drought"]]
        both = dd.dropna(subset=[f"SIF_alarm_{thr}", f"NDVI_alarm_{thr}"])
        lead = both[f"NDVI_alarm_{thr}"] - both[f"SIF_alarm_{thr}"]
        rec = {"baseline": label, "threshold": thr, "n_drought": nd_, "n_normal": nn_,
               "hit_SIF": int(dd[f"SIF_alarm_{thr}"].notna().sum()), "hit_NDVI": int(dd[f"NDVI_alarm_{thr}"].notna().sum()),
               "false_SIF": int(D.loc[~D["is_drought"], f"SIF_alarm_{thr}"].notna().sum()),
               "false_NDVI": int(D.loc[~D["is_drought"], f"NDVI_alarm_{thr}"].notna().sum()),
               "both_flagged": len(both), "SIF_earlier": int((lead > 0).sum()), "same": int((lead == 0).sum()),
               "NDVI_earlier": int((lead < 0).sum()), "median_SIF_lead_days": lead.median() if len(lead) else np.nan}
        out.append(rec)
        print(f"z < {thr:<5}{rec['hit_SIF']:>6d}/{nd_}{rec['hit_NDVI']:>7d}/{nd_}{rec['false_SIF']:>8d}/{nn_}{rec['false_NDVI']:>8d}/{nn_}"
              f"   {rec['SIF_earlier']} / {rec['same']} / {rec['NDVI_earlier']}, "
              f"{'n/a' if lead.empty else f'{lead.median():+.0f} d'}")
    return out


D = district_alarms(DROUGHT_D)
D.drop(columns=["SIF_z", "NDVI_z"]).to_csv("data/processed/drought_signal_district.csv", index=False)
summ = district_summary(D, "own-district baseline (main)")
D_reg = district_alarms(DROUGHT_D_REGIONAL)
summ += district_summary(D_reg, "regional baseline (sensitivity)")
pd.DataFrame(summ).to_csv("data/processed/drought_signal_district_summary.csv", index=False)

auc_rows = []
for i, doy in enumerate(DOYS):
    rec = {"doy": doy + 3.5, "date": fmt(doy + 3.5)}
    for v in ["SIF", "NDVI"]:
        sc = np.array([np.nanmean(z[max(0, i - 1): i + 1]) for z in D[f"{v}_z"]])
        ok = ~np.isnan(sc)
        lab = D["is_drought"].values[ok]
        if lab.sum() and (~lab).sum():
            u = mannwhitneyu(-sc[ok][lab], -sc[ok][~lab]).statistic
            rec[f"AUC_{v}"] = u / (lab.sum() * (~lab).sum())
        else:
            rec[f"AUC_{v}"] = np.nan
    auc_rows.append(rec)
A = pd.DataFrame(auc_rows)
A.to_csv("data/processed/drought_signal_auc_by_date.csv", index=False)
print("\nHow well each index separates drought from normal district-years, date by date "
      "(AUC: 0.5 = chance, 1.0 = perfect; mean z of that composite and the one before; NDVI is "
      "interpolated onto the SIF dates, so its value at a date can include the next NDVI observation):")
print(A[(A["doy"] >= 180) & (A["doy"] <= 320)].round(2).to_string(index=False))
for v in ["SIF", "NDVI"]:
    hit = A.loc[(A["doy"] >= START_DOY) & (A[f"AUC_{v}"] >= 0.75), "date"]
    print(f"  {v}: first date with AUC >= 0.75: {hit.iloc[0] if len(hit) else 'never'}; "
          f"peak AUC {A[f'AUC_{v}'].max():.2f} on {A.loc[A[f'AUC_{v}'].idxmax(), 'date']}")
print("  (district-years share each year's weather, so these 72 are not independent -- read the AUCs as descriptive)")

os.makedirs("outputs/figures", exist_ok=True)
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), sharey=True)
for ax, v in zip(axes, ["SIF", "NDVI"]):
    for y in YEARS:
        dr = y in DROUGHT
        col = {2015: "#b2182b", 2018: "#e08214"}.get(y, "#d6604d") if dr else "#9e9e9e"
        ax.plot(DOYS + 3.5, zreg[v][y], color=col, lw=2.2 if dr else 1,
                alpha=1 if dr else 0.6, label=f"{y} (drought)" if dr else None, zorder=3 if dr else 2)
    ax.axhline(MAIN_THR, color="black", ls="--", lw=1, label=f"alarm threshold z = {MAIN_THR:g}")
    ax.axvline(DECLARATION_2015, color="#b2182b", ls=":", lw=1.5, label="16 Oct 2015 declaration (reported)")
    ax.axvline(DECLARATION_2018, color="#e08214", ls=":", lw=1.5, label="31 Oct 2018 final declaration")
    ax.set_title(f"{v}: anomaly vs normal years (grey = normal years)")
    ax.set_xlabel("Day of year")
    ax.set_xlim(180, 365)
    ax.grid(alpha=0.3)
axes[0].set_ylabel("Standardized anomaly z")
axes[0].legend(fontsize=8, loc="lower left")
plt.tight_layout()
plt.savefig("outputs/figures/drought_signal_anomaly_curves.png", dpi=200)
print("\nSaved drought_signal_region.csv, drought_signal_district.csv, drought_signal_auc_by_date.csv, "
      "outputs/figures/drought_signal_anomaly_curves.png")
