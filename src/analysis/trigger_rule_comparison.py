# combined drought-trigger rules on the district-years (policy extension)
# each rule fires on a date; a rule that combines signals fires when its condition is first met

import ast

import numpy as np
import pandas as pd

THR = "-3.0"
IN_SEASON_DOY = 273  # 30 Sep, end of the monsoon window used for the dry-spell rule


def fmt(doy):
    return "-" if pd.isna(doy) else (pd.Timestamp("2018-01-01") + pd.Timedelta(days=float(doy) - 1)).strftime("%d %b")


def all_of(d, *cols):
    # fires when the last of the signals has fired; never if any one never fires
    return d[list(cols)].max(axis=1, skipna=False)


def any_of(d, *cols):
    return d[list(cols)].min(axis=1)


def k_of(d, k, *cols):
    # date of the k-th signal to fire
    v = np.sort(d[list(cols)].to_numpy(dtype=float), axis=1)
    return pd.Series(v[:, k - 1], index=d.index)


def then(d, first, second):
    # second signal on or after the first (deficit seen first, vegetation confirms)
    return d[second].where(d[second] >= d[first]).where(d[first].notna())


def rules(d, rain=True):
    # rain: True = every rule; "trigger" = the Trigger-1 rules but not the 25% deficit (2001-2014); False = satellite only
    r = {}
    if rain:
        r["Rainfall Trigger-1 (district average)"] = d["T1"]
        r["Rainfall Trigger-1 (25% of pixels)"] = d["T1px"]
    if rain is True:
        r["Rainfall deficit > 25% alone"] = d["D"]
    r["NDVI anomaly (z < -3)"] = d["N"]
    r["SIF anomaly (z < -3)"] = d["S"]
    if rain is True:
        r["Deficit AND NDVI"] = all_of(d, "D", "N")
        r["Deficit AND SIF"] = all_of(d, "D", "S")
        r["Deficit, then NDVI confirms"] = then(d, "D", "N")
    r["NDVI AND SIF"] = all_of(d, "N", "S")
    r["NDVI OR SIF"] = any_of(d, "N", "S")
    if rain:
        r["Trigger-1 OR NDVI"] = any_of(d, "T1", "N")
    if rain is True:
        r["2 of 3: deficit, NDVI, SIF"] = k_of(d, 2, "D", "N", "S")
    return r


def score(d, label, rain=True):
    dr, nm = d["is_drought"].astype(bool), ~d["is_drought"].astype(bool)
    rows, miss = [], []
    for name, s in rules(d, rain).items():
        hit = s.notna() & dr
        rows.append({
            "setting": label, "rule": name,
            "drought_flagged": int(hit.sum()), "drought_n": int(dr.sum()),
            "false_alarms": int((s.notna() & nm).sum()), "normal_n": int(nm.sum()),
            "flagged_by_30_sep": int((hit & (s <= IN_SEASON_DOY)).sum()),
            "median_alarm_doy": float(s[hit].median()) if hit.any() else np.nan,
        })
        for r in d[dr & s.isna()].itertuples():
            miss.append({"setting": label, "rule": name, "district": r.district, "year": r.year})
    R = pd.DataFrame(rows)
    print(f"\n{label}: {int(dr.sum())} drought, {int(nm.sum())} normal district-years")
    print(f"{'rule':38s}{'drought':>9s}{'false':>8s}{'by 30 Sep':>11s}{'median':>9s}")
    for r in R.itertuples():
        print(f"{r.rule:38s}{r.drought_flagged:>5d}/{r.drought_n:<3d}{r.false_alarms:>4d}/{r.normal_n:<3d}"
              f"{r.flagged_by_30_sep:>8d}{fmt(r.median_alarm_doy):>11s}")
    return R, pd.DataFrame(miss)


# rainfall rules, district level, 2015-2023
T = pd.read_csv("data/processed/rainfall_trigger_dates.csv")
T = T[T["unit"] != "Marathwada"].rename(columns={"unit": "district"})
tr = T.pivot_table(index=["district", "year"], columns="variant", values="trigger_doy", aggfunc="first").reset_index()
tr = tr[["district", "year", "main: Manual Trigger 1, 4 dry weeks", "deficit>25% only"]].rename(
    columns={"main: Manual Trigger 1, 4 dry weeks": "T1", "deficit>25% only": "D"})
px = pd.read_csv("data/processed/rainfall_trigger_pixel_by_district.csv")
px = px[px["variant"] == "main: Manual Trigger 1, 4 dry weeks"][["district", "year", "doy_25pct_triggered"]]
px = px.rename(columns={"doy_25pct_triggered": "T1px"})

# main: satellite alarms as in the paper (NDVI interpolated onto the SIF dates)
sd = pd.read_csv("data/processed/drought_signal_district.csv")
main = sd[["district", "year", "is_drought", f"SIF_alarm_{THR}", f"NDVI_alarm_{THR}"]].rename(
    columns={f"SIF_alarm_{THR}": "S", f"NDVI_alarm_{THR}": "N"})
main = main.merge(tr, on=["district", "year"], how="left").merge(px, on=["district", "year"], how="left")
assert len(main) == 72 and main["is_drought"].sum() == 15

# sensitivity inputs from the alarm-dating check (NDVI as observed; 2001-2014 test)
al = pd.read_csv("data/processed/alarm_dating_sensitivity_alarms.csv")
al = al[al["level"] == "district"].copy()
al[["district", "year"]] = pd.DataFrame(al["unit"].map(ast.literal_eval).tolist(), index=al.index)
al = al.rename(columns={f"SIF_alarm_{THR}": "S", f"NDVI_alarm_{THR}": "N"})


def alarms(period, dating):
    a = al[(al["period"] == period) & (al["ndvi_dating"] == dating)]
    return a[["district", "year", "is_drought", "S", "N"]].reset_index(drop=True)


chk = alarms("2015-2023", "interpolated").merge(main[["district", "year", "S", "N"]], on=["district", "year"], suffixes=("", "_m"))
assert np.allclose(chk["N"].fillna(-1), chk["N_m"].fillna(-1)) and np.allclose(chk["S"].fillna(-1), chk["S_m"].fillna(-1))

avail = alarms("2015-2023", "available").merge(tr, on=["district", "year"], how="left").merge(px, on=["district", "year"], how="left")
oos = alarms("2001-2014", "interpolated").merge(tr, on=["district", "year"], how="left").merge(px, on=["district", "year"], how="left")

out, miss = [], []
for d, label, rain in [(main, "2015-2023 (main)", True),
                       (avail, "2015-2023, NDVI as observed", True),
                       (oos, "2001-2014 out-of-sample", "trigger")]:
    R, M = score(d, label, rain)
    out.append(R)
    miss.append(M)
R, M = pd.concat(out, ignore_index=True), pd.concat(miss, ignore_index=True)

print("\nMissed drought district-years, main setting:")
for name, g in M[M["setting"] == "2015-2023 (main)"].groupby("rule", sort=False):
    print(f"  {name}: " + ", ".join(f"{a} {b}" for a, b in zip(g['district'], g['year'])))

R["median_alarm_date"] = R["median_alarm_doy"].map(fmt)
R.to_csv("data/processed/trigger_rule_comparison.csv", index=False)
M.to_csv("data/processed/trigger_rule_missed_droughts.csv", index=False)
print("\nSaved trigger_rule_comparison.csv, trigger_rule_missed_droughts.csv")
print("Note: the 25% deficit and the rules built on it are scored only for 2015-2023, where district daily rainfall from\n"
      "Earth Engine is available; Trigger-1 comes from the CHIRPS pixel stacks and is scored in both periods.")
