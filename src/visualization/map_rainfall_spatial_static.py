import math
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]
DISTRICTS_PATH = "data/raw/marathwada_districts_separate.geojson"
RAINFALL_CSV = "data/processed/rainfall_anomaly_by_district.csv"
OUTPUT_PLOT = "outputs/figures/rainfall_anomaly_by_district_static.png"

districts = gpd.read_file(DISTRICTS_PATH)
if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")
elif districts.crs.to_epsg() != 4326:
    districts = districts.to_crs("EPSG:4326")

rain_df = pd.read_csv(RAINFALL_CSV)
rain_wide = rain_df.pivot(index="district", columns="year", values="anomaly_pct").reset_index()
rain_wide.columns = ["ADM2_NAME"] + [f"anomaly_{y}" for y in rain_wide.columns[1:]]

merged = districts.merge(rain_wide, on="ADM2_NAME", how="left")

all_values = pd.concat([merged[f"anomaly_{y}"] for y in YEARS])
vmin, vmax = all_values.min(), all_values.max()

cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

ncols = 4  # wrap into a grid instead of one long row
nrows = math.ceil(len(YEARS) / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 5 * nrows))
axes = axes.flatten()

for ax, year in zip(axes, YEARS):
    col = f"anomaly_{year}"
    merged.plot(column=col, cmap=cmap, norm=norm, ax=ax, edgecolor="black", linewidth=0.8)
    for _, row in merged.iterrows():
        c = row.geometry.centroid
        ax.annotate(f"{row[col]:.0f}%", xy=(c.x, c.y), ha="center", fontsize=8)
    ax.set_title(f"{year} — Rainfall anomaly", fontsize=13, pad=10)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
for ax in axes[len(YEARS):]:
    ax.set_visible(False)

fig.subplots_adjust(wspace=0.3, hspace=0.35, top=0.90, bottom=0.08, left=0.05, right=0.9)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
fig.colorbar(sm, cax=cbar_ax, label="Rainfall anomaly (%)")

fig.suptitle("Marathwada rainfall anomaly by district (% departure from regional 20-yr normal)", fontsize=14, y=0.98)
fig.savefig(OUTPUT_PLOT, dpi=300, bbox_inches="tight")
plt.show()