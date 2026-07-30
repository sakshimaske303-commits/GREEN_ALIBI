import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt

BOUNDARY_PATH = "data/raw/marathwada_boundary_polygon.geojson"
CLIPPED_FILE = "data/processed/clipped/GOSIF_2020273_clipped.tif"  # apni actual filename se match kar

boundary = gpd.read_file(BOUNDARY_PATH)
if boundary.crs is None:
    boundary = boundary.set_crs("EPSG:4326")
elif boundary.crs.to_epsg() != 4326:
    boundary = boundary.to_crs("EPSG:4326")

with rasterio.open(CLIPPED_FILE) as src:
    data = src.read(1)
    bounds = src.bounds

total_pixels = data.size
valid_pixels = np.sum(~np.isnan(data))
print(f"Total pixels: {total_pixels}")
print(f"Valid (non-NaN) pixels: {valid_pixels}")
print(f"Valid fraction: {valid_pixels/total_pixels:.2%}")

fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(data, cmap="RdYlGn",
                extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])
boundary.boundary.plot(ax=ax, color="blue", linewidth=1.5)
plt.colorbar(im, label="SIF")
ax.set_title("SIF data (color) vs actual Marathwada boundary (blue outline)")
plt.savefig("outputs/figures/boundary_overlay_check.png", dpi=200, bbox_inches="tight")
plt.show()