import numpy as np
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt

YEARS = [2015, 2018, 2020]
DOY = 273
CLIPPED_DIR = "data/processed/clipped"
BOUNDARY_PATH = "data/raw/marathwada_boundary_polygon.geojson"

# --- Load precise boundary (for overlay) ---
boundary = gpd.read_file(BOUNDARY_PATH)
if boundary.crs is None:
    boundary = boundary.set_crs("EPSG:4326")
elif boundary.crs.to_epsg() != 4326:
    boundary = boundary.to_crs("EPSG:4326")

# --- Load the three rasters, keeping each one's own true (cropped) bounds ---
arrays = {}
bounds_by_year = {}
for year in YEARS:
    path = f"{CLIPPED_DIR}/GOSIF_{year}{DOY:03d}_clipped.tif"  # apni actual filename se match kar
    with rasterio.open(path) as src:
        data = src.read(1)
        arrays[year] = data
        bounds_by_year[year] = src.bounds

# --- Shared color scale across all 3 years ---
all_valid = np.concatenate([arrays[y][~np.isnan(arrays[y])].ravel() for y in YEARS])
vmin, vmax = np.nanpercentile(all_valid, [2, 98])

# --- Plot ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

ims = []
for ax, year in zip(axes, YEARS):
    b = bounds_by_year[year]
    im = ax.imshow(arrays[year], cmap="RdYlGn", vmin=vmin, vmax=vmax,
                    extent=[b.left, b.right, b.bottom, b.top])
    boundary.boundary.plot(ax=ax, color="black", linewidth=0.8)  # <-- asli Marathwada outline
    ax.set_title(f"{year} — DOY {DOY}", fontsize=13, pad=10)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ims.append(im)

fig.subplots_adjust(wspace=0.3, top=0.85, bottom=0.15, left=0.05, right=0.9)

cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
fig.colorbar(ims[-1], cax=cbar_ax, label="SIF (mW/m²/sr/nm)")

fig.suptitle(f"Solar-Induced Fluorescence — Marathwada (precise boundary) — DOY {DOY}", fontsize=15, y=0.98)

fig.savefig("outputs/figures/sif_spatial_comparison_doy273_v2.png", dpi=300, bbox_inches="tight")
plt.show()