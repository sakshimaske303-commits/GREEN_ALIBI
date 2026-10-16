# GEE: India state outlines (FAO GAUL level 1) for the Figure 3 locator inset
#   python src/acquisition/gee_india_states_for_locator.py

import os
import sys

import ee
import geemap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gee_data_acquisition  # noqa: E402,F401  (initialises Earth Engine)

OUT = "data/external/india_states_gaul_l1.geojson"

states = (ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1")
          .filter(ee.Filter.eq("ADM0_NAME", "India"))
          .select(["ADM1_NAME"]))

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    geemap.ee_export_vector(states, filename=OUT)
    print(f"Saved {OUT}. Next: python fig3_study_area_map.py")
