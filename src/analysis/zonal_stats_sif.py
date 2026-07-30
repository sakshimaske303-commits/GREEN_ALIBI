import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask

YEARS = [2015, 2018, 2020]
DOY = 273
CLIPPED_DIR = "data/processed/clipped"
DISTRICTS_PATH = "data/raw/marathwada_districts_separate.geojson"
OUTPUT_CSV = "data/processed/sif_by_district.csv"

# --- Load district-level boundaries (8 separate features, with names) ---
districts = gpd.read_file(DISTRICTS_PATH)
if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")
elif districts.crs.to_epsg() != 4326:
    districts = districts.to_crs("EPSG:4326")

print(f"Loaded {len(districts)} districts: {districts['ADM2_NAME'].tolist()}")

results = []

for year in YEARS:
    raster_path = f"{CLIPPED_DIR}/GOSIF_{year}{DOY:03d}_clipped.tif"  # apni actual filename se match kar

    with rasterio.open(raster_path) as src:
        for _, row in districts.iterrows():
            district_name = row['ADM2_NAME']
            geom = [row.geometry.__geo_interface__]

            out_image, _ = mask(src, geom, crop=True, nodata=np.nan, filled=True)
            data = out_image[0].astype("float64")
            mean_sif = np.nanmean(data)
            valid_frac = np.sum(~np.isnan(data)) / data.size

            results.append({
                "district": district_name,
                "year": year,
                "doy": DOY,
                "mean_sif": mean_sif,
                "valid_pixel_fraction": valid_frac
            })

            print(f"{year} | {district_name}: mean SIF = {mean_sif:.4f} (valid frac: {valid_frac:.1%})")

df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\nSaved district-level SIF stats to {OUTPUT_CSV}")

pivot = df.pivot(index="district", columns="year", values="mean_sif")
print("\nSanity check (mean SIF by district and year):")
print(pivot.round(4))