import numpy as np
import pandas as pd
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]
DOY = 273
CLIPPED_DIR = "data/processed/clipped"
BOUNDARY_PATH = "data/raw/marathwada_boundary_polygon.geojson"
DISTRICTS_PATH = "data/raw/marathwada_districts_separate.geojson"
RAINFALL_CSV = "data/processed/rainfall_anomaly_by_district.csv"
OUTPUT_PLOT = "outputs/figures/combined_sif_rainfall_comparison.png"

# --- SIF rasters ---
boundary = gpd.read_file(BOUNDARY_PATH)
if boundary.crs is None:
    boundary = boundary.set_crs("EPSG:4326")
elif boundary.crs.to_epsg() != 4326:
    boundary = boundary.to_crs("EPSG:4326")

sif_arrays, sif_bounds = {}, {}
for year in YEARS:
    path = f"{CLIPPED_DIR}/GOSIF_{year}{DOY:03d}_clipped.tif"
    with rasterio.open(path) as src:
        sif_arrays[year] = src.read(1)
        sif_bounds[year] = src.bounds

sif_all_valid = np.concatenate([sif_arrays[y][~np.isnan(sif_arrays[y])].ravel() for y in YEARS])
sif_vmin, sif_vmax = np.nanpercentile(sif_all_valid, [2, 98])

# --- Rainfall by district ---
districts = gpd.read_file(DISTRICTS_PATH)
if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")
elif districts.crs.to_epsg() != 4326:
    districts = districts.to_crs("EPSG:4326")

rain_df = pd.read_csv(RAINFALL_CSV)
rain_wide = rain_df.pivot(index="district", columns="year", values="anomaly_pct").reset_index()
rain_wide.columns = ["ADM2_NAME"] + [f"anomaly_{y}" for y in rain_wide.columns[1:]]
merged = districts.merge(rain_wide, on="ADM2_NAME", how="left")

rain_all_values = pd.concat([merged[f"anomaly_{y}"] for y in YEARS])
rain_norm = mcolors.Normalize(vmin=rain_all_values.min(), vmax=rain_all_values.max())

# --- Combined 2-row figure: SIF on top, rainfall below ---
fig, axes = plt.subplots(2, len(YEARS), figsize=(4.2 * len(YEARS), 11))

for col_idx, year in enumerate(YEARS):
    ax_sif = axes[0, col_idx]
    b = sif_bounds[year]
    im_sif = ax_sif.imshow(sif_arrays[year], cmap="RdYlGn", vmin=sif_vmin, vmax=sif_vmax,
                            extent=[b.left, b.right, b.bottom, b.top])
    boundary.boundary.plot(ax=ax_sif, color="black", linewidth=0.8)
    ax_sif.set_title(f"{year} — SIF (DOY {DOY})", fontsize=12)
    ax_sif.set_xlabel("Longitude")
    if col_idx == 0:
        ax_sif.set_ylabel("Latitude")

    ax_rain = axes[1, col_idx]
    rain_col = f"anomaly_{year}"
    merged.plot(column=rain_col, cmap="RdYlGn", norm=rain_norm, ax=ax_rain, edgecolor="black", linewidth=0.8)
    ax_rain.set_title(f"{year} — Rainfall anomaly", fontsize=12)
    ax_rain.set_xlabel("Longitude")
    if col_idx == 0:
        ax_rain.set_ylabel("Latitude")

fig.subplots_adjust(wspace=0.3, hspace=0.35, top=0.92, bottom=0.08, left=0.06, right=0.88)

sif_cbar_ax = fig.add_axes([0.90, 0.53, 0.02, 0.35])
fig.colorbar(im_sif, cax=sif_cbar_ax, label="SIF")

rain_sm = plt.cm.ScalarMappable(cmap="RdYlGn", norm=rain_norm)
rain_sm._A = []
rain_cbar_ax = fig.add_axes([0.90, 0.10, 0.02, 0.35])
fig.colorbar(rain_sm, cax=rain_cbar_ax, label="Rainfall anomaly (%)")

fig.suptitle("SIF stress vs rainfall deficit — Marathwada, 8 years (2015-2023)", fontsize=15, y=0.97)
fig.savefig(OUTPUT_PLOT, dpi=300, bbox_inches="tight")
plt.show()