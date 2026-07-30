import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

YEARS = [2015, 2018, 2020]
DISTRICTS_PATH = "data/raw/marathwada_districts_separate.geojson"
SIF_CSV = "data/processed/sif_by_district.csv"
OUTPUT_PLOT = "outputs/figures/sif_by_district_static.png"

districts = gpd.read_file(DISTRICTS_PATH)
if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")
elif districts.crs.to_epsg() != 4326:
    districts = districts.to_crs("EPSG:4326")

sif_df = pd.read_csv(SIF_CSV)
sif_wide = sif_df.pivot(index="district", columns="year", values="mean_sif").reset_index()
sif_wide.columns = ["ADM2_NAME"] + [f"sif_{y}" for y in sif_wide.columns[1:]]

merged = districts.merge(sif_wide, on="ADM2_NAME", how="left")

all_values = pd.concat([merged[f"sif_{y}"] for y in YEARS])
vmin, vmax = all_values.min(), all_values.max()

cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, year in zip(axes, YEARS):
    col = f"sif_{year}"
    merged.plot(column=col, cmap=cmap, norm=norm, ax=ax, edgecolor="black", linewidth=0.8)
    for _, row in merged.iterrows():
        c = row.geometry.centroid
        ax.annotate(f"{row[col]:.3f}", xy=(c.x, c.y), ha="center", fontsize=8)
    ax.set_title(f"{year} — Mean SIF", fontsize=13, pad=12)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

fig.subplots_adjust(wspace=0.3, top=0.85, bottom=0.15, left=0.05, right=0.9)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
fig.colorbar(sm, cax=cbar_ax, label="Mean SIF (DOY 273)")

fig.suptitle("Marathwada mean SIF by district (DOY 273)", fontsize=14, y=0.98)
fig.savefig(OUTPUT_PLOT, dpi=300, bbox_inches="tight")
plt.show()