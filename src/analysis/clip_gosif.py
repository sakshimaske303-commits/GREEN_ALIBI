# clip GOSIF files to Marathwada

import glob
import gzip
import os
import re

import geopandas as gpd
import numpy as np
import rasterio
from affine import Affine
from rasterio.io import MemoryFile
from rasterio.mask import mask

SOURCE_DIRS = ["data/raw", "data/external"]
OUTPUT_DIR = "data/processed/clipped"
BOUNDARY_PATH = "data/raw/marathwada_boundary_polygon.geojson"
YEARS = range(2015, 2024)
DOYS = range(153, 362, 8)
SCALE_FACTOR = 0.0001
FILL_VALUES = [32766, 32767]
STANDARD_ORIGIN = (-180.0, 90.0)

os.makedirs(OUTPUT_DIR, exist_ok=True)
boundary = gpd.read_file(BOUNDARY_PATH)
boundary = boundary.set_crs("EPSG:4326") if boundary.crs is None else boundary.to_crs("EPSG:4326")
geometry = [boundary.geometry.union_all()]

sources = {}
for d in SOURCE_DIRS:
    for path in glob.glob(os.path.join(d, "GOSIF_*.tif*")):
        m = re.fullmatch(r"GOSIF_(\d{4})(\d{3})\.tif(\.gz)?", os.path.basename(path))
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        if key[0] in YEARS and key[1] in DOYS and (key not in sources or not path.endswith(".gz")):
            sources[key] = path
missing = [(y, d) for y in YEARS for d in DOYS if (y, d) not in sources]
if missing:
    raise FileNotFoundError(f"{len(missing)} GOSIF 8-day files missing, e.g. {missing[:5]} "
                            "(run src/acquisition/download_gosif_new_years.py)")
print(f"Found all {len(sources)} GOSIF 8-day files ({len(YEARS)} years x {len(DOYS)} composites)")

fixed = set()
for (year, doy), path in sorted(sources.items()):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rb") as f:
        raw = f.read()
    with MemoryFile(raw) as mem, mem.open() as src:
        meta = src.meta.copy()
        t = src.transform
        if (round(t.c, 6), round(t.f, 6)) != STANDARD_ORIGIN:
            if abs(t.c - (STANDARD_ORIGIN[0] - t.a / 2)) < 1e-6 and abs(t.f - STANDARD_ORIGIN[1]) < 1e-6:
                meta["transform"] = Affine(t.a, t.b, STANDARD_ORIGIN[0], t.d, t.e, t.f)
                fixed.add(year)
            else:
                raise ValueError(f"{path}: unexpected grid origin ({t.c}, {t.f})")
        data = src.read(1)
    with MemoryFile() as mem2:
        with mem2.open(**meta) as dst:
            dst.write(data, 1)
        with mem2.open() as fixed_src:
            out_image, out_transform = mask(fixed_src, geometry, crop=True, nodata=-1, filled=True)

    arr = out_image[0].astype("float64")
    arr = np.where(arr == -1, np.nan, arr)
    arr = np.where(np.isin(arr, FILL_VALUES), np.nan, arr) * SCALE_FACTOR
    out_meta = {"driver": "GTiff", "height": arr.shape[0], "width": arr.shape[1], "count": 1,
                "crs": meta["crs"], "transform": out_transform, "dtype": "float64", "nodata": np.nan}
    out_path = os.path.join(OUTPUT_DIR, f"GOSIF_{year}{doy:03d}_clipped.tif")
    with rasterio.open(out_path, "w", **out_meta) as dst:
        dst.write(arr, 1)

print(f"Header origin corrected (-180.025 -> -180.0) for: {sorted(fixed) or 'none'}")
print(f"Done -- {len(sources)} files clipped to the precise 8-district boundary into {OUTPUT_DIR}")
