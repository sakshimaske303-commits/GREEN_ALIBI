import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ============================================================
# RQ3 — how does the satellite-detected stress signal compare
# to the timing of the *official* government drought declaration?
#
# This question was posed explicitly in Project_Journal.md and
# Development_Log.md's original research-questions list, but the
# final Research_Paper.md never actually answered it — a gap
# flagged directly during external review of this project. This
# script closes that gap for the one year with a clean, publicly
# documented official declaration date: 2018 (Maharashtra
# government, 31 October 2018, all eight Marathwada study
# districts included among 151 talukas / 26 districts — see
# Research_Paper.md references for the two news sources).
#
# A single verifiable declaration date for 2015 could not be
# located via search in the time available (2015-16 Marathwada
# drought reporting mostly covers the extended, better-known 2016
# water-crisis phase, not a single dated 2015 kharif declaration),
# so this comparison is reported for 2018 only — noted explicitly
# rather than extrapolated to 2015.
# ============================================================

DECLARATION_DOY_2018 = 304  # 31 October 2018
LAG_TABLE = "data/processed/sif_ndvi_lag_by_threshold.csv"
OUT_CSV = "data/processed/rq3_official_declaration_comparison.csv"


def doy_to_date(year, doy):
    return datetime(year, 1, 1) + timedelta(days=int(round(doy)) - 1)


lag_df = pd.read_csv(LAG_TABLE)
row = lag_df[(lag_df["year"] == 2018) & (lag_df["threshold"] == 0.9)].iloc[0]

sif_doy = row["sif_crossing_doy"]
ndvi_doy = row["ndvi_crossing_doy"]

result = pd.DataFrame([
    {"event": "SIF crosses 90% of seasonal peak", "doy": sif_doy,
     "date": doy_to_date(2018, sif_doy).strftime("%Y-%m-%d"),
     "days_before_official_declaration": DECLARATION_DOY_2018 - sif_doy},
    {"event": "NDVI crosses 90% of seasonal peak", "doy": ndvi_doy,
     "date": doy_to_date(2018, ndvi_doy).strftime("%Y-%m-%d"),
     "days_before_official_declaration": DECLARATION_DOY_2018 - ndvi_doy},
    {"event": "Official Maharashtra govt drought declaration", "doy": DECLARATION_DOY_2018,
     "date": doy_to_date(2018, DECLARATION_DOY_2018).strftime("%Y-%m-%d"),
     "days_before_official_declaration": 0},
])
result.to_csv(OUT_CSV, index=False)
print(result.to_string(index=False))
print(f"\nSIF-vs-NDVI edge at this threshold: {ndvi_doy - sif_doy:.1f} days")
print(f"Satellite-vs-official-declaration gap: SIF {DECLARATION_DOY_2018 - sif_doy:.1f} days, "
      f"NDVI {DECLARATION_DOY_2018 - ndvi_doy:.1f} days")

# --- Timeline figure ---
fig, ax = plt.subplots(figsize=(9, 3.2))
events = [
    (sif_doy, "SIF: 90% decline\n(8 Sep 2018)", "#2FA88C"),
    (ndvi_doy, "NDVI: 90% decline\n(12 Sep 2018)", "#D9822B"),
    (DECLARATION_DOY_2018, "Official drought\ndeclaration\n(31 Oct 2018)", "#B23A48"),
]
ax.hlines(0, min(e[0] for e in events) - 5, max(e[0] for e in events) + 5, color="gray", linewidth=1.5, zorder=1)
for doy, label, color in events:
    ax.scatter([doy], [0], s=140, color=color, zorder=3, edgecolor="black")
    ax.annotate(label, (doy, 0), xytext=(0, 28), textcoords="offset points",
                ha="center", fontsize=9, color=color, fontweight="bold")

ax.annotate("", xy=(DECLARATION_DOY_2018, -0.35), xytext=(sif_doy, -0.35),
            arrowprops=dict(arrowstyle="<->", color="#555555"))
ax.text((sif_doy + DECLARATION_DOY_2018) / 2, -0.55, f"{DECLARATION_DOY_2018 - sif_doy:.0f} days",
        ha="center", fontsize=9, color="#555555")

ax.set_ylim(-0.9, 0.6)
ax.set_yticks([])
ax.set_xlabel("Day of year, 2018")
ax.set_title("2018: Satellite Stress Signal vs. Official Drought Declaration Timeline (RQ3)", fontsize=11)
for spine in ["top", "left", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/figures/rq3_declaration_timeline_2018.png", dpi=150)
print("\nFigure saved to outputs/figures/rq3_declaration_timeline_2018.png")
