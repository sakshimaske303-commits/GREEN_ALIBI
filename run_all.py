# runs the full pipeline in order

import argparse
import datetime
import importlib.metadata as md
import os
import platform
import subprocess
import sys
import time

ACQUIRE = [
    "src/acquisition/gee_cropland_fraction_and_ndvi_obsdates.py",
    "src/acquisition/gee_district_ndvi_and_rain_timing.py",
    "src/acquisition/gee_rainfall_seasonal_totals_1981_2023.py",
]
ANALYSIS = [
    "src/analysis/clip_gosif.py",
    "src/analysis/aggregate_sif.py",
    "src/analysis/rainfall_analysis.py",
    "src/analysis/rainfall_by_district_analysis.py",
    "src/analysis/compare_sif_ndvi.py",
    "src/analysis/lag_analysis.py",
    "src/analysis/cross_correlation_lag.py",
    "src/analysis/bootstrap_lag_uncertainty.py",
    "src/analysis/final_summary.py",
    "src/analysis/h3_continuous_severity.py",
    "src/analysis/rq3_official_declaration_comparison.py",
    "src/analysis/zonal_stats_sif.py",
    "src/analysis/sif_rainfall_correlation.py",
    "src/analysis/district_climatology_anomaly.py",
    "src/analysis/spatial_autocorrelation.py",
    "src/analysis/sensitivity_checks.py",
    "src/analysis/cropmask_obsdate_sensitivity.py",
    "src/analysis/district_lag_analysis.py",
    "src/analysis/district_seasonal_sif.py",
    "src/analysis/rain_timing_analysis.py",
    "src/analysis/crop_yield_validation.py",
    "src/analysis/crop_yield_sensitivity.py",
    "src/analysis/baseline_sensitivity.py",
    "src/analysis/lag_uncertainty_check.py",
    "src/analysis/drought_signal_analysis.py",
    "src/analysis/rainfall_trigger_comparison.py",
    "src/analysis/method_dependence.py",
    "src/analysis/gosif_grid_shift_check.py",
]
FIGURES = [
    "src/analysis/check_boundary_overlay.py",
    "src/visualization/map_sif_spatial.py",
    "src/visualization/map_sif_by_district_static.py",
    "src/visualization/map_rainfall_spatial_static.py",
    "src/visualization/map_combined_sif_rainfall.py",
    "src/visualization/plot_sif_rainfall_correlation.py",
    "src/visualization/plot_spatial_autocorrelation.py",
    "src/visualization/plot_bootstrap_lag_ci.py",
    "src/visualization/plot_crop_yield_validation.py",
    "src/visualization/build_folium_map.py",
    "src/visualization/build_folium_rainfall_map.py",
    "src/visualization/build_interactive_plots.py",
    "src/visualization/make_graphical_abstract.py",
    "fig3_study_area_map.py",
]
REQUIRED_INPUTS = [
    "data/raw/marathwada_boundary_polygon.geojson",
    "data/raw/marathwada_districts_separate.geojson",
    "data/raw/ndvi_obsdate_2015_2023.csv",
    "data/raw/ndvi_obsdate_by_district_2015_2023.csv",
    "data/raw/chirps_seasonal_totals_1981_2023.csv",
    "data/raw/chirps_daily_region_2001_2023.csv",
    "data/raw/chirps_daily_by_district_2015_2023.csv",
    "data/raw/marathwada_ndvi_mod13q1_timeseries_8years.csv",
    "data/external/extracted/crop-wise-area-production-yield.csv",
    "data/external/official_drought_declarations.csv",
] + [f"data/external/cropland_fraction/cropland_fraction_{y}.tif" for y in range(2015, 2024)]
PACKAGES = ["numpy", "pandas", "scipy", "statsmodels", "rasterio", "geopandas", "shapely", "affine",
            "libpysal", "esda", "matplotlib", "folium", "plotly", "earthengine-api", "geemap"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acquire", action="store_true", help="re-run the Earth Engine exports first")
    ap.add_argument("--from", dest="start", help="start at the script whose name contains this")
    ap.add_argument("--no-figures", action="store_true")
    args = ap.parse_args()

    steps = (ACQUIRE if args.acquire else []) + ANALYSIS + ([] if args.no_figures else FIGURES)
    if args.start:
        hits = [i for i, s in enumerate(steps) if args.start in s]
        if not hits:
            sys.exit(f"No step matches '{args.start}'")
        steps = steps[hits[0]:]

    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/interactive_maps/maps", exist_ok=True)
    os.makedirs("outputs/interactive_maps/plots", exist_ok=True)
    log = open("outputs/run_log.txt", "w", encoding="utf-8")

    def out(msg=""):
        print(msg)
        log.write(msg + "\n")
        log.flush()

    out(f"GREEN ALIBI pipeline run, {datetime.datetime.now():%Y-%m-%d %H:%M}")
    out(f"Python {platform.python_version()} on {platform.platform()}")
    for p in PACKAGES:
        try:
            out(f"  {p} {md.version(p)}")
        except md.PackageNotFoundError:
            out(f"  {p} (not installed)")

    produced_by_acquire = ("ndvi_obsdate", "chirps_", "cropland_fraction")
    need = [f for f in REQUIRED_INPUTS if not (args.acquire and any(k in f for k in produced_by_acquire))]
    if not os.path.exists("data/external/extracted/crop-wise-area-production-yield.csv") and \
            os.path.exists("data/external/Crop_Wise_Area_Production_Yield.zip"):
        need.remove("data/external/extracted/crop-wise-area-production-yield.csv")
    if True:
        missing = [f for f in need if not os.path.exists(f)]
        if missing:
            out("\nMissing inputs (run with --acquire, or see each file's producing script):")
            for f in missing:
                out(f"  {f}")
            sys.exit(1)

    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    t_all = time.time()
    for i, script in enumerate(steps, 1):
        if not os.path.exists(script):
            out(f"\n[{i}/{len(steps)}] SKIP {script} (file not found)")
            continue
        out(f"\n[{i}/{len(steps)}] {script}")
        t = time.time()
        r = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, encoding="utf-8")
        log.write(r.stdout)
        log.write(r.stderr)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            print(r.stderr[-3000:])
            out(f"FAILED ({r.returncode}) after {time.time() - t:.0f}s -- stopping. "
                f"Fix it, then: python run_all.py --from {os.path.basename(script)[:-3]}")
            sys.exit(r.returncode)
        out(f"  ok ({time.time() - t:.0f}s)")
    out(f"\nAll {len(steps)} steps finished in {(time.time() - t_all) / 60:.1f} min. Full output: outputs/run_log.txt")


if __name__ == "__main__":
    main()
