# the trigger and the satellite alarms scored against three definitions of a drought district-year
#   rainfall z < -0.5 against the district's own 2001-2020 baseline (the study's definition, Jun-Dec),
#   June-September rainfall 20% or more below the district's 2001-2020 mean (IMD's "deficient"),
#   and a Kharif yield anomaly index below -0.5 (crop loss, 2015-2022)

import pandas as pd

THR = "-3.0"
BASE = (2001, 2020)
DEFICIENT_PCT = -20
YIELD_CUT = -0.5
MAIN = "main: Manual Trigger 1, 4 dry weeks"

sd = pd.read_csv("data/processed/drought_signal_district.csv")
T = pd.read_csv("data/processed/rainfall_trigger_dates.csv")
P = pd.read_csv("data/processed/rainfall_trigger_pixel_by_district.csv")
U = pd.read_csv("data/processed/chirps_daily_units_jun_sep.csv")
Y = pd.read_csv("data/processed/crop_yield_anomaly_by_district_year.csv").rename(columns={"study_year": "year"})

tot = U.groupby(["unit", "year"])["rain_mm"].sum().unstack()
dep = (100 * (tot.div(tot.loc[:, BASE[0]:BASE[1]].mean(axis=1), axis=0) - 1)).stack().rename("jun_sep_departure_pct")

d = sd[["district", "year", "is_drought", f"SIF_alarm_{THR}", f"NDVI_alarm_{THR}"]].copy()
d = d.merge(T[(T["variant"] == MAIN) & (T["unit"] != "Marathwada")].rename(columns={"unit": "district"})
            [["district", "year", "trigger_doy"]], on=["district", "year"], how="left")
d = d.merge(P[P["variant"] == MAIN][["district", "year", "share_triggered", "doy_25pct_triggered"]],
            on=["district", "year"], how="left")
d = d.merge(dep.reset_index().rename(columns={"unit": "district"}), on=["district", "year"], how="left")
d = d.merge(Y, on=["district", "year"], how="left")

fired = {
    "Rainfall Trigger-1 (district average)": d["trigger_doy"].notna(),
    "Rainfall Trigger-1 (25% of pixels)": d["doy_25pct_triggered"].notna(),
    "NDVI anomaly (z < -3)": d[f"NDVI_alarm_{THR}"].notna(),
    "SIF anomaly (z < -3)": d[f"SIF_alarm_{THR}"].notna(),
    "Trigger-1 OR NDVI": d["trigger_doy"].notna() | d[f"NDVI_alarm_{THR}"].notna(),
}
truths = {
    "rainfall z < -0.5, own baseline (2015-2023)": (d["is_drought"].astype(bool), pd.Series(True, index=d.index)),
    "Jun-Sep rainfall 20% or more below normal (2015-2023)": (d["jun_sep_departure_pct"] <= DEFICIENT_PCT,
                                                             pd.Series(True, index=d.index)),
    "yield anomaly index < -0.5 (2015-2022)": (d["yield_anomaly_index"] < YIELD_CUT, d["yield_anomaly_index"].notna()),
}

rows = []
for tname, (truth, have) in truths.items():
    for rname, f in fired.items():
        t, f = truth[have], f[have]
        rows.append({"truth": tname, "rule": rname, "true_n": int(t.sum()), "flagged": int((f & t).sum()),
                     "other_n": int((~t).sum()), "false_alarms": int((f & ~t).sum())})
S = pd.DataFrame(rows)
S.to_csv("data/processed/trigger_truth_check.csv", index=False)

D = d[d["is_drought"].astype(bool) | (d["yield_anomaly_index"] < YIELD_CUT)].copy()
D["trigger_fired"] = fired["Rainfall Trigger-1 (district average)"][D.index]
D["ndvi_fired"] = fired["NDVI anomaly (z < -3)"][D.index]
D = D[["district", "year", "is_drought", "jun_sep_departure_pct", "yield_anomaly_index", "share_triggered",
       "trigger_fired", "ndvi_fired"]].sort_values(["year", "district"])
D.to_csv("data/processed/trigger_truth_district_years.csv", index=False)

pd.set_option("display.width", 200)
for tname, g in S.groupby("truth", sort=False):
    print(f"\n{tname}: {g['true_n'].iloc[0]} true, {g['other_n'].iloc[0]} other district-years")
    for r in g.itertuples():
        print(f"  {r.rule:40s} flagged {r.flagged:2d}/{r.true_n:<2d}  false alarms {r.false_alarms:2d}/{r.other_n}")
miss = D[D["is_drought"] & ~D["trigger_fired"]]
print(f"\nDrought district-years the district-average trigger missed: {len(miss)}; "
      f"Jun-Sep departure {miss['jun_sep_departure_pct'].min():.1f}% to {miss['jun_sep_departure_pct'].max():.1f}%, "
      f"{(miss['jun_sep_departure_pct'] > DEFICIENT_PCT).sum()} of them less than 20% below normal")
print(D.round(2).to_string(index=False))
print("\nSaved trigger_truth_check.csv, trigger_truth_district_years.csv")
