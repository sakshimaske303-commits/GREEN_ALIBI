# satellite signal vs rainfall drought trigger

import numpy as np
import pandas as pd

BASELINE = (2001, 2020)
START_DOY = 182
MONSOON_END_DOY = 273  # 30 Sep: dry spells are counted only inside the monsoon (1 Jul - 30 Sep)
# (deficit %, dry-day mm, spell days, rule, last DOY on which a dry day can count towards a spell)
# Earlier versions counted dry days to 26 Dec, so the natural post-monsoon dry season (Oct-Dec)
# satisfied the spell criterion every year; that variant is kept as "old: spell counted to Dec".
VARIANTS = {
    "main: deficit>25% & spell>=21d": (25, 2.5, 21, "both", MONSOON_END_DOY),
    "deficit>20% & spell>=21d": (20, 2.5, 21, "both", MONSOON_END_DOY),
    "deficit>30% & spell>=21d": (30, 2.5, 21, "both", MONSOON_END_DOY),
    "dry day <1mm": (25, 1.0, 21, "both", MONSOON_END_DOY),
    "deficit>25% only": (25, 2.5, 21, "deficit", MONSOON_END_DOY),
    "spell>=21d only": (25, 2.5, 21, "spell", MONSOON_END_DOY),
    "old: spell counted to Dec": (25, 2.5, 21, "both", 366),
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
T = pd.DataFrame(rows)
T.to_csv("data/processed/rainfall_trigger_dates.csv", index=False)


def fmt(doy):
    return "-" if pd.isna(doy) else (pd.Timestamp("2018-01-01") + pd.Timedelta(days=float(doy) - 1)).strftime("%d %b")


sat = pd.read_csv("data/processed/drought_signal_region.csv").set_index("year")
lag = pd.read_csv("data/processed/sif_ndvi_lag_by_threshold.csv")
lag = lag[lag["threshold"] == 0.9].set_index("year")
decl = pd.read_csv("data/external/official_drought_declarations.csv")
main_v = list(VARIANTS)[0]
tr = T[(T["unit"] == "Marathwada")].pivot(index="year", columns="variant", values="trigger_doy")

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
print("Note: Trigger-1 is applied by the state at taluka level; this region/district version applies a dry-spell rule\n"
      "to spatially averaged rainfall, which smooths out local dry spells. See gee_chirps_dryspell_area.py for the\n"
      "pixel-level version.")
