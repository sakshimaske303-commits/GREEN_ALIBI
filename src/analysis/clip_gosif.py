import os
import glob
import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# --- Config ---
RAW_DIR = "data/raw"
OUTPUT_DIR = "data/processed/clipped"
BOUNDARY_PATH = "data/raw/marathwada_boundary_polygon.geojson"
SCALE_FACTOR = 0.0001
FILL_VALUES = [32766, 32767]  # water, non-vegetated/missing

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load the precise Marathwada boundary (8 districts, from GEE FAO GAUL, Bid-fixed) ---
boundary = gpd.read_file(BOUNDARY_PATH)
print(f"Loaded boundary: {len(boundary)} feature(s), CRS: {boundary.crs}")

# GOSIF is in geographic WGS84 (EPSG:4326) — reproject defensively in case
# the GeoJSON export from GEE didn't carry CRS metadata cleanly
if boundary.crs is None:
    boundary = boundary.set_crs("EPSG:4326")
elif boundary.crs.to_epsg() != 4326:
    boundary = boundary.to_crs("EPSG:4326")

geometry = [boundary.geometry.unary_union]  # merge into one polygon for masking

# --- Process each raw GOSIF file ---
raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "GOSIF_*.tif")))
print(f"Found {len(raw_files)} raw GOSIF files to clip.")

for filepath in raw_files:
    filename = os.path.basename(filepath)

    with rasterio.open(filepath) as src:
        # crop=True trims to the polygon's bounding extent;
        # nodata=-1 marks every pixel OUTSIDE the actual district shapes
        # (safe sentinel — raw GOSIF digital numbers are never negative)
        out_image, out_transform = mask(src, geometry, crop=True, nodata=-1, filled=True)
        out_meta = src.meta.copy()

    data = out_image[0].astype("float64")

    # Pixels outside the precise polygon -> NaN
    data = np.where(data == -1, np.nan, data)
    # GOSIF's own fill codes (water / non-vegetated) -> NaN
    data = np.where(np.isin(data, FILL_VALUES), np.nan, data)
    # Apply GOSIF scale factor to get real SIF units
    data = data * SCALE_FACTOR

    out_meta.update({
        "driver": "GTiff",
        "height": data.shape[0],
        "width": data.shape[1],
        "transform": out_transform,
        "dtype": "float64",
        "nodata": np.nan
    })

    out_path = os.path.join(OUTPUT_DIR, filename.replace(".tif", "_clipped.tif"))
    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(data, 1)

    valid_frac = np.sum(~np.isnan(data)) / data.size
    print(f"{filename}: clipped to precise 8-district boundary | valid pixel fraction: {valid_frac:.2%}")

print("Done — all files now clipped to the precise Marathwada boundary (rasterio.mask), not a rectangle.")