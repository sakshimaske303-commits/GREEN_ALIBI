# graphical abstract, numbers read from data/processed

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

P = "data/processed/"
TEAL, MAGENTA, INK, GREY, FILL = "#14b8a6", "#d6338a", "#1f1f1f", "#666666", "#f3f9f9"

rain = pd.read_csv(P + "rainfall_anomaly_summary.csv")
lag = pd.read_csv(P + "final_summary_rainfall_lag.csv")
xc = pd.read_csv(P + "cross_correlation_lag_by_year.csv")
dist = pd.read_csv(P + "district_lag_by_year.csv")
trop = pd.read_csv(P + "tropomi_vs_gosif.csv")
trop = trop[trop["variant"].str.startswith("main")]
reg = pd.read_csv(P + "drought_signal_region.csv").set_index("year")
trig = pd.read_csv(P + "rainfall_trigger_vs_satellite.csv")

years = sorted(rain["year"])
drought = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])
n_years = len(years)
n_sif_first = int((lag["mean_lag_days"] > 0).sum())
n_dist_first = int((dist["threshold_lag"] > 0).sum())
xc_pos, xc_tie, xc_neg = [int(v) for v in ((xc["cross_corr_lag_days"] > 0).sum(), (xc["cross_corr_lag_days"] == 0).sum(), (xc["cross_corr_lag_days"] < 0).sum())]
trop_first = int((trop["lag_tropomi_vs_ndvi"] > 0).sum())
lag_d = lag.loc[lag["year"].isin(drought), "mean_lag_days"].mean()
lag_n = lag.loc[~lag["year"].isin(drought), "mean_lag_days"].mean()
final = trig[trig["is_final"]]
f18 = final[final["declaration"].astype(str).str.startswith("2018")].iloc[0]
lead_lo = int(np.floor(final[["SIF_alarm_days_before_declaration", "NDVI_alarm_days_before_declaration"]].min().min()))
lead_hi = int(np.ceil(final[["SIF_alarm_days_before_declaration", "NDVI_alarm_days_before_declaration"]].max().max()))


def date(doy, year=2018):
    t = pd.Timestamp(f"{year}-01-01") + pd.Timedelta(days=float(doy) - 1)
    return f"{t.day} {t:%b}"


a15 = reg.loc[2015, ["SIF_alarm_-3.0", "NDVI_alarm_-3.0"]]
a18 = reg.loc[2018, ["SIF_alarm_-3.0", "NDVI_alarm_-3.0"]]
same_2015 = a15.iloc[0] == a15.iloc[1]
ndvi_ahead_2018 = a18.iloc[0] - a18.iloc[1]

fig = plt.figure(figsize=(20, 8.15))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 20)
ax.set_ylim(0, 8.15)
ax.axis("off")


def box(x, y, w, h, edge=TEAL, face=FILL, lw=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                linewidth=lw, edgecolor=edge, facecolor=face))


ax.text(10, 7.55, "GREEN ALIBI: Does Fluorescence Catch Drought Stress Before NDVI?",
        ha="center", va="center", fontsize=26, fontweight="bold", color=INK)
ax.text(10, 7.03, f"Marathwada, Maharashtra, India  |  8 districts  |  {n_years} Kharif seasons "
        f"({years[0]}–{years[-1]})  |  TROPOMI cross-check", ha="center", va="center",
        fontsize=15, fontweight="bold", color=GREY)

steps = [
    ("STUDY", "Agricultural drought stress\nacross 8 districts"),
    ("SATELLITE + RAINFALL", "GOSIF SIF  |  MODIS NDVI\nTROPOMI SIF  |  CHIRPS"),
    ("SEASONAL LEAD", "Two normalisations\nCross-correlation\n40-variant method check"),
    ("DROUGHT SIGNAL", "Anomaly vs normal years\nRegion + 72 district-years"),
    ("POLICY CHECK", "Rainfall Trigger-1\n2015 & 2018 declarations"),
]
w, h, y0, gap = 3.35, 1.75, 4.8, 0.48
x0 = (20 - (5 * w + 4 * gap)) / 2
for i, (t, s) in enumerate(steps):
    x = x0 + i * (w + gap)
    box(x, y0, w, h)
    ax.text(x + w / 2, y0 + h - 0.42, t, ha="center", va="center", fontsize=16, fontweight="bold", color=INK)
    ax.text(x + w / 2, y0 + 0.72, s, ha="center", va="center", fontsize=12.5, color=INK, linespacing=1.35)
    if i < 4:
        ax.annotate("", xy=(x + w + gap - 0.02, y0 + h / 2), xytext=(x + w + 0.02, y0 + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2.5, mutation_scale=18))

box(0.63, 1.5, 18.74, 2.85, edge="#cccccc", face="white", lw=1.5)
ax.text(10, 3.98, "KEY RESULTS", ha="center", va="center", fontsize=17, fontweight="bold", color=INK)

ns = pd.read_csv(P + "normalisation_sensitivity_region.csv")
n_decl_first = int((ns["lag_decline"] > 0).sum())
dsum = pd.read_csv(P + "drought_signal_district_summary.csv")
d3 = dsum[(dsum["baseline"].str.startswith("own")) & (dsum["threshold"] == -3.0)].iloc[0]

cards = [
    ("NOT AN EARLIER ALARM", 16.5,
     f"Drought anomaly (z < −3): 2015 {'same day' if same_2015 else 'different days'},\n"
     f"2018 NDVI {ndvi_ahead_2018:.0f} days before SIF\n"
     f"Districts: same {int(d3.same)} | NDVI first {int(d3.NDVI_earlier)} | SIF first {int(d3.SIF_earlier)}"),
    ("SCALING-DEPENDENT LEAD", 16.5,
     f"Season-scaled: SIF first {n_sif_first}/{n_years} years\n"
     f"Decline-scaled: SIF first {n_decl_first}/{n_years} years\n"
     f"Cross-corr.: {xc_pos} SIF | {xc_tie} tie | {xc_neg} NDVI"),
    ("NO DISTRICT EFFECT", 16.5,
     f"District differences vanish when\ncurves are scaled over their own decline\n"
     f"TROPOMI: SIF first {trop_first}/{len(trop)} years (2018–2020)"),
]
cw, ch, cy = 4.1, 1.72, 1.8
cx0 = 1.0
for i, (t, fs, s) in enumerate(cards):
    x = cx0 + i * (cw + 0.36)
    box(x, cy, cw, ch)
    ax.text(x + cw / 2, cy + ch - 0.43, t, ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
    ax.text(x + cw / 2, cy + 0.6, s, ha="center", va="center", fontsize=12, color=INK, linespacing=1.35)

x = cx0 + 3 * (cw + 0.36)
box(x, cy, cw + 0.45, ch)
ax.text(x + (cw + 0.45) / 2, cy + ch - 0.3, "2018 DROUGHT TIMELINE", ha="center", va="center",
        fontsize=16, fontweight="bold", color=INK)
ax.text(x + (cw + 0.45) / 2, cy + ch - 0.6, f"alarms {f18.NDVI_alarm_days_before_declaration:.1f} (NDVI) and {f18.SIF_alarm_days_before_declaration:.1f} (SIF) days before declaration",
        ha="center", va="center", fontsize=11, fontweight="bold", color=MAGENTA)
d0, d1 = 250, 310
xa, xb = x + 0.45, x + cw
ax.plot([xa, xb], [cy + 0.5, cy + 0.5], color=GREY, lw=2.5, solid_capstyle="round")
pts = [("NDVI", a18.iloc[1], MAGENTA, -1), ("SIF", a18.iloc[0], TEAL, 1), ("Declared", 304, MAGENTA, -1)]
for lab, doy, col, side in pts:
    px = xa + (doy - d0) / (d1 - d0) * (xb - xa)
    ax.plot(px, cy + 0.5, "o", ms=11, color=col, zorder=3)
    ax.text(px, cy + 0.5 + side * 0.3, f"{lab}\n{date(doy)}", ha="center", va="center", fontsize=9.5,
            color=INK, linespacing=1.1)

ax.text(10, 0.85, "CONCLUSION  •  SIF is not an earlier drought alarm than NDVI; "
        "its seasonal lead is largely a scaling effect.", ha="center", va="center", fontsize=16.5,
        fontweight="bold", color=INK)

for ext in ["png", "svg", "pdf"]:
    fig.savefig(f"GREEN_ALIBI_graphical_abstract.{ext}", dpi=243, facecolor="white")
print("saved GREEN_ALIBI_graphical_abstract.png/.svg/.pdf")
