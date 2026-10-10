# TROPOMI SIF cross-check (district level)

import os
import re
import time
import calendar
from datetime import date

import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

BASE_URL = "http://ftp.sron.nl/open-access-data-2/TROPOMI/tropomi/sif/v2.1/l2b/"
DOWNLOAD_DIR = "data/external/troposif_raw"
BOUNDARY_PATH = "data/raw/marathwada_boundary_polygon.geojson"
OUT_CSV = "data/processed/tropomi_sif_marathwada_daily.csv"

# default 2018-2020; pass a range to download more years, e.g.
#   python src/analysis/tropomi_sif_crosscheck.py 2018 2023
# (check first which years exist under BASE_URL; each year is tens of GB)
import sys as _sys
STUDY_YEARS = (list(range(int(_sys.argv[1]), int(_sys.argv[2]) + 1)) if len(_sys.argv) == 3
               else [2018, 2019, 2020])
SEASON_START, SEASON_END = (6, 1), (12, 27)

NC_GROUP = "PRODUCT"
SIF_VAR_CANDIDATES = ["SIF_Corr_743", "SIF_743", "sif743", "SIF", "sif"]
LAT_VAR_CANDIDATES = ["latitude", "lat", "Latitude"]
LON_VAR_CANDIDATES = ["longitude", "lon", "Longitude"]

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def get_with_retry(url, attempts=3, backoff_seconds=5, **kwargs):
    last_exc = None
    for attempt in range(1, attempts + 1):
        try:
            return requests.get(url, **kwargs)
        except requests.exceptions.RequestException as e:
            last_exc = e
            if attempt < attempts:
                print(f"  connection hiccup ({e.__class__.__name__}), retrying in {backoff_seconds}s "
                      f"({attempt}/{attempts})...")
                time.sleep(backoff_seconds)
    raise last_exc


def list_links(url):
    resp = get_with_retry(url, timeout=60)
    resp.raise_for_status()
    return re.findall(r'href="([^"?/][^"]*)"', resp.text)


def discover_files_for_year(year):
    candidates = []
    top_links = list_links(BASE_URL)
    year_str = str(year)

    if f"{year_str}/" in top_links:
        month_links = list_links(BASE_URL + f"{year_str}/")
        for m in month_links:
            if m.endswith("/"):
                candidates += [f"{year_str}/{m}{f}" for f in list_links(BASE_URL + f"{year_str}/{m}") if f.endswith(".nc")]
            elif m.endswith(".nc"):
                candidates.append(f"{year_str}/{m}")
    else:
        candidates += [f for f in top_links if f.endswith(".nc") and year_str in f]

    return candidates


def file_date_from_name(fname):
    m = re.search(r"(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})", fname)
    if not m:
        return None
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        return date(y, mo, d)
    except ValueError:
        return None


def in_season(d, year):
    start = date(year, *SEASON_START)
    end = date(year, *SEASON_END)
    return start <= d <= end


def pick_var(ds, candidates, kind):
    for c in candidates:
        if c in ds.variables:
            return c
    print(f"\nCouldn't auto-match a {kind} variable from {candidates}.")
    print(f"Variables actually in this file: {list(ds.variables.keys())}")
    raise KeyError(f"Add the correct {kind} variable name to {kind.upper()}_VAR_CANDIDATES above and rerun.")


def main():
    import xarray as xr

    boundary = gpd.read_file(BOUNDARY_PATH)
    if boundary.crs is None:
        boundary = boundary.set_crs("EPSG:4326")
    elif boundary.crs.to_epsg() != 4326:
        boundary = boundary.to_crs("EPSG:4326")
    marathwada_poly = boundary.geometry.union_all()
    minx, miny, maxx, maxy = marathwada_poly.bounds

    sif_var = lat_var = lon_var = None

    done_dates = set()
    daily_rows = []
    if os.path.exists(OUT_CSV):
        prior = pd.read_csv(OUT_CSV)
        daily_rows = prior.to_dict("records")
        done_dates = set(prior["date"])
        print(f"Resuming from {OUT_CSV}: {len(done_dates)} day(s) already done, skipping those.")

    for year in STUDY_YEARS:
        print(f"\nDiscovering TROPOSIF files for {year}...")
        try:
            all_files = discover_files_for_year(year)
        except requests.RequestException as e:
            print(f"Could not reach {BASE_URL} ({e}). Check your internet connection and that")
            print("ftp.sron.nl isn't blocked by a firewall/VPN, then rerun.")
            return

        season_files_all = [f for f in all_files if (d := file_date_from_name(f)) and in_season(d, year)]
        season_files = [f for f in season_files_all if file_date_from_name(f).isoformat() not in done_dates]
        print(f"{len(all_files)} files listed for {year}, {len(season_files_all)} fall in the Jun 1 - Dec 27 "
              f"season window, {len(season_files)} left to process this run (already-done days skipped)")
        if all_files and not season_files_all:
            print("  0 matched -- printing the first 5 raw filenames so the date pattern can be checked:")
            for f in all_files[:5]:
                print("   ", f)
            continue
        if not season_files:
            print(f"  All of {year}'s season days are already done, nothing left to fetch for this year.")
            continue

        for relpath in season_files:
            fname = os.path.basename(relpath)
            local_path = os.path.join(DOWNLOAD_DIR, fname)
            if not os.path.exists(local_path):
                try:
                    r = get_with_retry(BASE_URL + relpath, timeout=120)
                except requests.exceptions.RequestException as e:
                    print(f"  skip {fname} after retries ({e.__class__.__name__}) -- rerun this script "
                          f"later to pick it up, everything up to here is already saved")
                    continue
                if r.status_code != 200:
                    print(f"  skip {fname}: HTTP {r.status_code}")
                    continue
                with open(local_path, "wb") as f:
                    f.write(r.content)

            try:
                ds = xr.open_dataset(local_path, group=NC_GROUP)
            except Exception as e:
                print(f"  skip {fname}: couldn't open ({e})")
                continue

            if sif_var is None:
                sif_var = pick_var(ds, SIF_VAR_CANDIDATES, "sif")
                lat_var = pick_var(ds, LAT_VAR_CANDIDATES, "lat")
                lon_var = pick_var(ds, LON_VAR_CANDIDATES, "lon")
                print(f"Using variables: sif={sif_var}, lat={lat_var}, lon={lon_var}")

            lats = ds[lat_var].values.ravel()
            lons = ds[lon_var].values.ravel()
            sifs = ds[sif_var].values.ravel()
            ds.close()

            bbox_mask = (lons >= minx) & (lons <= maxx) & (lats >= miny) & (lats <= maxy)
            if not bbox_mask.any():
                continue
            pts = gpd.GeoSeries(
                [Point(xy) for xy in zip(lons[bbox_mask], lats[bbox_mask])], crs="EPSG:4326"
            )
            inside = pts.within(marathwada_poly)
            matched_sif = sifs[bbox_mask][inside.values]
            matched_sif = matched_sif[~np.isnan(matched_sif)]
            if len(matched_sif) == 0:
                continue

            d = file_date_from_name(fname)
            daily_rows.append({
                "date": d.isoformat(), "year": year, "doy": d.timetuple().tm_yday,
                "mean_tropomi_sif": float(np.mean(matched_sif)),
                "n_soundings": int(len(matched_sif)),
            })
            print(f"  {fname}: {len(matched_sif)} soundings inside Marathwada, mean SIF={np.mean(matched_sif):.4f}")

            pd.DataFrame(daily_rows).sort_values("date").to_csv(OUT_CSV, index=False)

    if not daily_rows:
        print("\nNo matching soundings found inside the Marathwada boundary for any study year.")
        print("This can genuinely happen -- TROPOMI's ~7x3.5 km footprint is coarser than")
        print("GOSIF's 0.05 deg grid, and cloud/quality filtering in the L2B product already")
        print("drops a lot of soundings before you ever get here. If this is empty, that's a")
        print("real finding to report (TROPOMI's usable sample over this specific region is")
        print("too sparse for a meaningful comparison), not necessarily a bug in this script.")
        return

    daily_df = pd.DataFrame(daily_rows).sort_values("date")
    daily_df.to_csv(OUT_CSV, index=False)
    print(f"\nSaved {len(daily_df)} daily district-mean TROPOMI SIF values to {OUT_CSV}")

    try:
        gosif = pd.read_csv("data/processed/sif_rainfall_district_merged.csv")
        gosif_yearly = gosif.groupby("year")["mean_sif"].mean()
        tropomi_yearly = daily_df.groupby("year")["mean_tropomi_sif"].mean()
        print("\nYear-mean comparison (different products, different units/scaling --")
        print("compare RELATIVE year-to-year pattern, not absolute values):")
        for year in STUDY_YEARS:
            g = gosif_yearly.get(year, float("nan"))
            t = tropomi_yearly.get(year, float("nan"))
            print(f"  {year}: GOSIF mean_sif={g:.4f}   TROPOMI mean_sif={t:.4f}")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    main()
