# satellite signal vs rainfall drought trigger

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manual_trigger import MAIN, MONTH_ENDS, VARIANTS as MANUAL, day_to_doy, trigger_day  # noqa: E402

BASELINE = (2001, 2020)
START_DOY = 182
MONSOON_END_DOY = 273  # 30 Sep: dry spells are counted only inside the monsoon (1 Jul - 30 Sep)
# my earlier approximation, kept for comparison, and the deficit alone (used in the combined rules):
# (deficit %, dry-day mm, spell days, rule, last DOY a dry day counts)
VARIANTS = {
    "earlier approximation: deficit>25% & 21 days <2.5 mm": (25, 2.5, 21, "both", MONSOON_END_DOY),
    "deficit>25% only": (25, 2.5, 21, "deficit", MONSOON_END_DOY),
}

reg = pd.read_csv("data/raw/chirps_daily_region_2001_2023.csv")
reg["doy"] = pd.to_datetime(reg["date"]).dt.dayofyear
dis = pd.read_csv("data/raw/chirps_daily_by_district_2015_2023.csv")
dis["doy"] = pd.to_datetime(dis["date"]).dt.dayofyear
tot = pd.read_csv("data/raw/chirps_seasonal_totals_1981_2023.csv")
rain_z = pd.read_csv("data/processed/rainfall_anomaly_summary.csv").set_index("year")["anomaly_zscore"]

reg = reg.sort_values(["year", "doy"])
reg["cum"] = reg.groupby("year")["rain_mm"].cumsum()
normal_cum = reg[reg["year"].between(*BASELINE)].groupby("doy")["cum"].mean()
base = tot[tot["year"].between(*BASELINE)].groupby("unit")["rainfall_mm"].mean()
scale = (base / base["Marathwada"]).to_dict()


def trigger_date(g, unit, deficit_pct, dry_mm, spell_days, rule, spell_end_doy):
    g = g.sort_values("doy")
    cum = g["rain_mm"].cumsum().values
    norm = normal_cum.reindex(g["doy"]).values * scale[unit]
    deficit = 100 * (1 - cum / norm)
    in_window = (g["doy"].values >= START_DOY) & (g["doy"].values <= spell_end_doy)
    dry = ((g["rain_mm"].values < dry_mm) & in_window).astype(int)
    run, longest, out = 0, 0, []
    for v in dry:
        run = run + 1 if v else 0
        longest = max(longest, run)
        out.append(longest)
    spell = np.array(out)
    ok_def, ok_sp = deficit > deficit_pct, spell >= spell_days
    cond = {"both": ok_def & ok_sp, "deficit": ok_def, "spell": ok_sp}[rule] & (g["doy"].values >= START_DOY)
    return float(g["doy"].values[np.argmax(cond)]) if cond.any() else np.nan


rows = []
for v, args in VARIANTS.items():
    for y, g in reg[reg["year"] >= 2015].groupby("year"):
        rows.append({"variant": v, "unit": "Marathwada", "year": y, "trigger_doy": trigger_date(g, "Marathwada", *args)})
    for (d, y), g in dis.groupby(["district", "year"]):
        rows.append({"variant": v, "unit": d, "year": y, "trigger_doy": trigger_date(g, d, *args)})
# the Manual's Trigger 1, on the district and region series built from the CHIRPS pixels (rainfall_spi.py)
U = pd.read_csv("data/processed/chirps_daily_units_jun_sep.csv")
SPI = pd.read_csv("data/processed/rainfall_spi_by_district.csv")
for unit, g in U.groupby("unit"):
    P = g.pivot(index="day", columns="year", values="rain_mm")
    normal = P.loc[:, BASELINE[0]:BASELINE[1]].mean(axis=1).to_numpy()
    z = SPI[SPI["unit"] == unit].pivot(index="month_end_day", columns="year", values="spi").loc[MONTH_ENDS]
    for y in range(2001, 2024):  # 2001-2014 for the out-of-sample check of the trigger rules
        for v, (weeks, first_day) in MANUAL.items():
            day, arm = trigger_day(P[y].to_numpy(), normal, z[y].to_numpy(), weeks, first_day)
            rows.append({"variant": v, "unit": unit, "year": y, "trigger_doy": day_to_doy(y, day[0]), "trigger_arm": arm[0]})

T = pd.DataFrame(rows)
T.to_csv("data/processed/rainfall_trigger_dates.csv", index=False)


def fmt(doy):
    return "-" if pd.isna(doy) else (pd.Timestamp("2018-01-01") + pd.Timedelta(days=float(doy) - 1)).strftime("%d %b")


sat = pd.read_csv("data/processed/drought_signal_region.csv").set_index("year")
lag = pd.read_csv("data/processed/sif_ndvi_lag_by_threshold.csv")
lag = lag[lag["threshold"] == 0.9].set_index("year")
decl = pd.read_csv("data/external/official_drought_declarations.csv")
main_v = MAIN
tr = T[(T["unit"] == "Marathwada") & (T["year"] >= 2015)].pivot(index="year", columns="variant", values="trigger_doy")

print("REGION -- Trigger-1 date (rainfall) vs satellite signals")
print(f"{'year':6s}{'rain z':>7s}{'Trigger-1':>11s}{'SIF alarm':>11s}{'NDVI alarm':>12s}{'SIF 0.9':>9s}{'NDVI 0.9':>10s}")
for y in tr.index:
    print(f"{y:<6d}{rain_z[y]:>7.2f}{fmt(tr.loc[y, main_v]):>11s}{fmt(sat.loc[y, 'SIF_alarm_-3.0']):>11s}"
          f"{fmt(sat.loc[y, 'NDVI_alarm_-3.0']):>12s}{fmt(lag.loc[y, 'sif_crossing_doy']):>9s}{fmt(lag.loc[y, 'ndvi_crossing_doy']):>10s}")
print("\nTrigger-1 date under each rule (region):")
print(tr.map(fmt).to_string())

out = []
for dcl in decl.itertuples():
    y = dcl.year
    t1 = tr.loc[y, main_v]
    rec = {"declaration": f"{dcl.date}", "is_final": dcl.is_final_declaration, "trigger1_doy": t1,
           "trigger1_days_before_declaration": dcl.doy - t1}
    for k, col in [("SIF_alarm", "SIF_alarm_-3.0"), ("NDVI_alarm", "NDVI_alarm_-3.0")]:
        rec[f"{k}_days_before_declaration"] = dcl.doy - sat.loc[y, col]
        rec[f"{k}_minus_trigger1_days"] = sat.loc[y, col] - t1
    out.append(rec)
O = pd.DataFrame(out)
print("\nDays before each declaration, and satellite alarm relative to the rainfall Trigger-1 (+ = satellite later):")
print(O.round(0).to_string(index=False))

sd = pd.read_csv("data/processed/drought_signal_district.csv")
dm = T[(T["unit"] != "Marathwada") & (T["variant"] == main_v)].rename(columns={"unit": "district"})
m = sd.merge(dm[["district", "year", "trigger_doy"]], on=["district", "year"])
dr = m[m["is_drought"]]
print(f"\nDISTRICT (main rule), {len(dr)} drought and {int((~m['is_drought']).sum())} normal district-years:")
print(f"  Trigger-1 fired: drought {dr['trigger_doy'].notna().sum()}/{len(dr)}, "
      f"normal {m.loc[~m['is_drought'], 'trigger_doy'].notna().sum()}/{int((~m['is_drought']).sum())}")
for v in ["SIF", "NDVI"]:
    both = dr.dropna(subset=["trigger_doy", f"{v}_alarm_-3.0"])
    diff = both[f"{v}_alarm_-3.0"] - both["trigger_doy"]
    print(f"  {v} alarm (z<-3) vs Trigger-1, drought district-years with both: n={len(both)}, "
          f"satellite earlier {(diff < 0).sum()}, later {(diff > 0).sum()}, median {diff.median():+.0f} d")
O.to_csv("data/processed/rainfall_trigger_vs_satellite.csv", index=False)
print("\nSaved rainfall_trigger_dates.csv, rainfall_trigger_vs_satellite.csv")
print("Note: Trigger-1 is applied by the state at taluka level; this region/district version applies it to spatially\n"
      "averaged rainfall, which smooths out local dry spells. rainfall_trigger_pixel.py applies it in every pixel.")
