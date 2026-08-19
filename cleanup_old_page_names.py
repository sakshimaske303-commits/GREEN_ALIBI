"""Removes the old emoji-named page files in GREEN_ALIBI/pages/, now that
each one has a clean re-saved copy without the emoji in the filename.
Dry-run by default, prints what it'd remove; pass --delete to actually remove.

Run from the GREEN_ALIBI folder:
    python cleanup_old_page_names.py
    python cleanup_old_page_names.py --delete
"""
import os
import sys

OLD_FILES = [
    "pages/1_\U0001F30D_Study_Area.py",
    "pages/10_\U0001F4DD_Findings_and_Conclusion.py",
    "pages/2_\U0001F52C_Fluorescence_Physics.py",
    "pages/3_\U0001F52C_NDVI_Physics.py",
    "pages/4_\U0001F6F0️_Data_and_Methodology.py",
    "pages/5_\U0001F4C8_Seasonal_Trajectories.py",
    "pages/6_\U0001F4CA_Lag_Analysis.py",
    "pages/7_\U0001F5FA️_Spatial_SIF_Analysis.py",
    "pages/8_\U0001F327️_Rainfall_Validation.py",
    "pages/9_\U0001F517_Combined_Comparison.py",
    "pages/9_\U0001F5FA️_Interactive_Maps.py",
]

delete = "--delete" in sys.argv

for rel_path in OLD_FILES:
    if os.path.exists(rel_path):
        if delete:
            os.remove(rel_path)
            print(f"Deleted: {rel_path}")
        else:
            print(f"Would delete: {rel_path}")
    else:
        print(f"Not found (already gone?): {rel_path}")

if not delete:
    print("\nDry run only -- re-run with --delete to actually remove these files.")
