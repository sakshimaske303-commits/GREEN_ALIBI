# does the drought-year classification depend on the rainfall window?
#
# The main classification uses CHIRPS totals for 1 June - 27 December. Kharif crops depend mostly on
# the June-September monsoon, and a season can be normal in total but have a damaging dry month.
# This script classifies the study years by the Jun-Dec total, the Jun-Sep (JJAS) total and each
# monsoon month, all against the same 2001-2020 baseline, from the daily regional CHIRPS series.

import pandas as pd

BASELINE = (2001, 2020)
STUDY = list(range(2015, 2024))
CUT = -0.5

d = pd.read_csv("data/raw/chirps_daily_region_2001_2023.csv", parse_dates=["date"])
d["month"] = d["date"].dt.month
windows = {
    "Jun-Dec": d,
    "Jun-Sep (JJAS)": d[d["month"].between(6, 9)],
    "June": d[d["month"] == 6],
    "July": d[d["month"] == 7],
    "August": d[d["month"] == 8],
    "September": d[d["month"] == 9],
}
rows = []
for name, w in windows.items():
    tot = w.groupby("year")["rain_mm"].sum()
    base = tot.loc[BASELINE[0]:BASELINE[1]]
    z = (tot - base.mean()) / base.std()
    pct = 100 * (tot / base.mean() - 1)
    for y in STUDY:
        rows.append({"window": name, "year": y, "rain_mm": tot.loc[y], "anomaly_pct": pct.loc[y], "zscore": z.loc[y],
                     "drought": z.loc[y] < CUT})
R = pd.DataFrame(rows)
R.to_csv("data/processed/rainfall_window_sensitivity.csv", index=False)

pd.set_option("display.width", 200)
print(f"Regional rainfall z-score by window (baseline {BASELINE[0]}-{BASELINE[1]}; * = z < {CUT})")
tab = R.assign(cell=R["zscore"].round(2).astype(str) + R["drought"].map({True: "*", False: ""})).pivot(
    index="year", columns="window", values="cell")[list(windows)]
print(tab.to_string())
for name in ["Jun-Dec", "Jun-Sep (JJAS)"]:
    print(f"  drought years by {name}: {R[(R.window == name) & R.drought]['year'].tolist()}")
a = R[(R.window == "August") & (R.year == 2023)].iloc[0]
print(f"  August 2023: {a.rain_mm:.0f} mm ({a.anomaly_pct:+.0f}%, z = {a.zscore:.2f}), the driest August of the "
      f"{BASELINE[0]}-2023 record: {a.rain_mm <= d[d.month == 8].groupby('year')['rain_mm'].sum().min() + 1e-9}")
print("\nSaved data/processed/rainfall_window_sensitivity.csv")
