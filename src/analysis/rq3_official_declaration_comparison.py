import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# RQ3: satellite stress signal vs the official government drought
# declaration timeline. Only 2018 has a clean, publicly documented
# declaration date (Maharashtra govt, 31 Oct 2018, all 8 Marathwada
# districts included among 151 talukas / 26 districts). Couldn't find
# a comparably clean single date for 2015, so this stays a 2018-only
# comparison.

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
sif_date_str = doy_to_date(2018, sif_doy).strftime("%-d %b %Y")
ndvi_date_str = doy_to_date(2018, ndvi_doy).strftime("%-d %b %Y")
events = [
    (sif_doy, f"SIF: 90% decline\n({sif_date_str})", "#2FA88C"),
    (ndvi_doy, f"NDVI: 90% decline\n({ndvi_date_str})", "#D9822B"),
    (DECLARATION_DOY_2018, "Official drought\ndeclaration\n(31 Oct 2018)", "#B23A48"),
]
ax.hlines(0, min(e[0] for e in events) - 5, max(e[0] for e in events) + 5, color="gray", linewidth=1.5, zorder=1)
# SIF and NDVI can land only a few days apart on the x-axis, so stagger
# label heights whenever two points are close enough to collide.
y_offsets = [28] * len(events)
for i in range(1, len(events)):
    if events[i][0] - events[i - 1][0] < 15:
        y_offsets[i] = y_offsets[i - 1] + 40
for (doy, label, color), y_off in zip(events, y_offsets):
    ax.scatter([doy], [0], s=140, color=color, zorder=3, edgecolor="black")
    ax.annotate(label, (doy, 0), xytext=(0, y_off), textcoords="offset points",
                ha="center", fontsize=9, color=color, fontweight="bold")

ax.annotate("", xy=(DECLARATION_DOY_2018, -0.35), xytext=(sif_doy, -0.35),
            arrowprops=dict(arrowstyle="<->", color="#555555"))
ax.text((sif_doy + DECLARATION_DOY_2018) / 2, -0.55, f"{DECLARATION_DOY_2018 - sif_doy:.0f} days",
        ha="center", fontsize=9, color="#555555")

ax.set_ylim(-0.9, max(0.6, 0.15 * max(y_offsets)))
ax.set_yticks([])
ax.set_xlabel("Day of year, 2018")
ax.set_title("2018: Satellite Stress Signal vs. Official Drought Declaration Timeline (RQ3)", fontsize=11)
for spine in ["top", "left", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/figures/rq3_declaration_timeline_2018.png", dpi=150)
print("\nFigure saved to outputs/figures/rq3_declaration_timeline_2018.png")
