# satellite drought alarms vs rainfall trigger vs official drought declarations (RQ3)
#
# For each declaration year (2015, 2018) the figure shows, on one time axis:
#   - the drought-specific alarms (first date z < -3 for two composites, region)
#   - the regional rainfall Trigger-1 date (if it fired)
#   - the official declarations
#   - the seasonal 0.9-threshold crossings, drawn faintly, because they happen at a
#     similar time in every year and mark the normal start of the decline, not drought
# Needs drought_signal_analysis.py and rainfall_trigger_comparison.py to have run first.

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

LAG_TABLE = "data/processed/sif_ndvi_lag_by_threshold.csv"
ALARMS = "data/processed/drought_signal_region.csv"
TRIGGER = "data/processed/rainfall_trigger_dates.csv"
DECL = "data/external/official_drought_declarations.csv"
OUT_CSV = "data/processed/rq3_official_declaration_comparison.csv"
OUT_FIG = "outputs/figures/rq3_declaration_timeline.png"
MAIN_TRIGGER = "main: deficit>25% & spell>=21d"


def doy_to_date(year, doy):
    return datetime(year, 1, 1) + timedelta(days=float(doy) - 1)


lag = pd.read_csv(LAG_TABLE)
lag = lag[lag["threshold"] == 0.9].set_index("year")
alarms = pd.read_csv(ALARMS).set_index("year")
trig = pd.read_csv(TRIGGER)
trig = trig[(trig["variant"] == MAIN_TRIGGER) & (trig["unit"] == "Marathwada")].set_index("year")["trigger_doy"]
decl = pd.read_csv(DECL)

rows = []
for y in sorted(decl["year"].unique()):
    ev = [("SIF drought alarm (z < -3)", alarms.loc[y, "SIF_alarm_-3.0"], "alarm"),
          ("NDVI drought alarm (z < -3)", alarms.loc[y, "NDVI_alarm_-3.0"], "alarm"),
          ("Rainfall Trigger-1 (region)", trig.get(y, np.nan), "trigger"),
          ("SIF seasonal 0.9 crossing", lag.loc[y, "sif_crossing_doy"], "seasonal"),
          ("NDVI seasonal 0.9 crossing", lag.loc[y, "ndvi_crossing_doy"], "seasonal")]
    for d in decl[decl["year"] == y].itertuples():
        ev.append(("Final declaration" if d.is_final_declaration else "First-stage declaration", d.doy, "declaration"))
    final_doy = decl[(decl["year"] == y) & decl["is_final_declaration"]]["doy"].iloc[0]
    for name, doy, kind in ev:
        rows.append({"year": y, "event": name, "kind": kind, "doy": doy,
                     "date": "" if pd.isna(doy) else doy_to_date(y, doy).strftime("%Y-%m-%d"),
                     "days_before_final_declaration": final_doy - doy if pd.notna(doy) else np.nan})
R = pd.DataFrame(rows)
R.to_csv(OUT_CSV, index=False)
print(R.round(1).to_string(index=False))

colors = {"SIF": "#2FA88C", "NDVI": "#D9822B", "Rainfall": "#2166ac", "Final": "#B23A48", "First-stage": "#B23A48"}
order = ["SIF drought alarm (z < -3)", "NDVI drought alarm (z < -3)", "Rainfall Trigger-1 (region)",
         "First-stage declaration", "Final declaration", "SIF seasonal 0.9 crossing", "NDVI seasonal 0.9 crossing"]
years = sorted(R["year"].unique())
fig, axes = plt.subplots(len(years), 1, figsize=(10, 2.7 * len(years)), sharex=True)
axes = np.atleast_1d(axes)
for ax, y in zip(axes, years):
    sub = R[R["year"] == y].set_index("event")
    sub = sub.reindex([o for o in order if o in sub.index]).reset_index()
    n = len(sub)
    for i, r in sub.iterrows():
        yy = n - 1 - i
        col = colors[r["event"].split()[0]]
        if pd.isna(r["doy"]):
            ax.text(227, yy, "did not fire", va="center", fontsize=8, color="#555555", style="italic")
            continue
        faint = r["kind"] == "seasonal"
        ax.scatter(r["doy"], yy, s=70, color=col, alpha=0.35 if faint else 1, edgecolor="black", zorder=3,
                   marker="D" if r["kind"] == "declaration" else "o")
        ax.text(r["doy"] + 1.5, yy, doy_to_date(y, r["doy"]).strftime("%d %b"), va="center", fontsize=8,
                color="#333333")
    ax.set_yticks(range(n))
    ax.set_yticklabels(list(sub["event"])[::-1], fontsize=8)
    for d in sub.loc[sub["kind"] == "declaration", "doy"]:
        ax.axvline(d, color="#B23A48", lw=0.8, ls=":")
    ax.set_title(f"{y} (rainfall-defined drought year)", fontsize=10, loc="left")
    ax.grid(axis="x", alpha=0.3)
    ax.set_xlim(225, 312)
axes[-1].set_xlabel("Day of year")
fig.suptitle("Satellite drought alarms, rainfall trigger and official declarations, Marathwada\n"
             "(faint: seasonal 0.9 crossings, which fall at a similar date in normal years as well)", fontsize=10)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=170)
print(f"\nSaved {OUT_CSV} and {OUT_FIG}")
