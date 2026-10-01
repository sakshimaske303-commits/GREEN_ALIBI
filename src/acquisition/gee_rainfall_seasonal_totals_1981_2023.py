# GEE: CHIRPS seasonal totals per district, 1981-2023

import os
import sys

import ee
import geemap
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gee_data_acquisition import marathwada_fc, marathwada_boundary

YEARS = list(range(1981, 2024))
OUT_CSV = "data/raw/chirps_seasonal_totals_1981_2023.csv"
TMP_DIR = "data/raw/_gee_tmp"
SCALE = 5566

districts = marathwada_fc.select(["ADM2_NAME"])


def year_features(year):
    total = (ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
               .filterDate(ee.Date(f"{year}-06-01"), ee.Date(f"{year}-12-27"))
               .sum())
    region = total.reduceRegion(ee.Reducer.mean(), marathwada_boundary, SCALE, maxPixels=1e9)
    region_f = ee.Feature(None, {"year": year, "unit": "Marathwada", "rainfall_mm": region.get("precipitation")})
    dist = total.reduceRegions(collection=districts, reducer=ee.Reducer.mean(), scale=SCALE)
    dist = dist.map(lambda f: ee.Feature(None, {"year": year, "unit": f.get("ADM2_NAME"),
                                                "rainfall_mm": f.get("mean")}))
    return ee.FeatureCollection([region_f]).merge(dist)


if __name__ == "__main__":
    os.makedirs(TMP_DIR, exist_ok=True)
    parts = []
    for i in range(0, len(YEARS), 5):
        chunk = YEARS[i:i + 5]
        fc = ee.FeatureCollection([year_features(y) for y in chunk]).flatten()
        tmp = os.path.join(TMP_DIR, f"seasonal_totals_{chunk[0]}_{chunk[-1]}.csv")
        geemap.ee_export_vector(fc, filename=tmp, verbose=False)
        df = pd.read_csv(tmp)
        parts.append(df[["year", "unit", "rainfall_mm"]])
        print(f"  {chunk[0]}-{chunk[-1]}: {len(df)} rows")
    out = pd.concat(parts, ignore_index=True).sort_values(["unit", "year"])
    out.to_csv(OUT_CSV, index=False)
    print(f"-> saved {OUT_CSV} ({len(out)} rows; expected {len(YEARS) * 9})")
    print("Next: python src/analysis/baseline_sensitivity.py")
