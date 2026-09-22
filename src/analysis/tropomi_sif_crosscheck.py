"""Tier-3 extension #3: an independent SIF cross-check using TROPOMI
(Sentinel-5P) data instead of GOSIF, so the paper's core SIF signal isn't
resting on one single SIF product. Unlike the two scripts above, this one
does NOT need Google Earth Engine or any account/login at all -- TROPOSIF
(the specific TROPOMI SIF product used here) is published as free, open,
no-registration netCDF files over plain HTTP by SRON (the Dutch institute
that runs it): http://ftp.sron.nl/open-access-data-2/TROPOMI/tropomi/sif/v2.1/l2b/
Source/method paper: Guanter et al. 2021, ESSD, "The TROPOSIF global
sun-induced fluorescence dataset from the Sentinel-5P TROPOMI mission".

READ THIS BEFORE RUNNING -- one real, hard limitation, not a maybe:
TROPOSIF v2.1's public L2B files only cover May 2018 through March 2021.
That means this cross-check can ONLY ever compare against 3 of this study's
8 years -- 2018, 2019, and 2020 (2015-2017, 2022, and 2023 are simply not
covered by TROPOMI at all, which only launched in 2017). This is not a
temporary access restriction, it's the satellite record itself, so don't
spend time trying to make it cover more years than that -- 3 of 8 is the
real, honest scope of what this check can be. Still directly useful though:
2018 is this study's most closely examined and most consistently anomalous
year across the paper (Sections 4.2, 4.6, 4.7, 4.9), so an independent SIF
product actually landing squarely on that year is a genuinely useful check.

I haven't been able to test-run this end to end yet -- the exact folder/file
naming pattern on the download host isn't confirmed, so this script
DISCOVERS filenames at runtime by reading the directory listing pages,
rather than guessing a hardcoded pattern that might be wrong. Same story for
the SIF variable's exact name inside each netCDF file -- I don't have a
sample file open right now to confirm "SIF_743" is really the field name
TROPOSIF v2.1 uses, so the script prints every variable name it finds in the
first file it opens; if the auto-pick below doesn't find a match, check that
printed list and edit SIF_VAR_CANDIDATES accordingly.

Needs: pip install xarray netCDF4 requests geopandas shapely (--break-system-packages)
Run from the project root: python src/analysis/tropomi_sif_crosscheck.py
"""

import os
import re
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

# TROPOSIF only actually covers these study years (see docstring) -- same
# Jun 1 - Dec 27 Kharif-season window the rest of this study uses
STUDY_YEARS = [2018, 2019, 2020]
SEASON_START, SEASON_END = (6, 1), (12, 27)

SIF_VAR_CANDIDATES = ["SIF_743", "sif743", "SIF_Corr_743", "SIF", "sif"]
LAT_VAR_CANDIDATES = ["lat", "latitude", "Latitude"]
LON_VAR_CANDIDATES = ["lon", "longitude", "Longitude"]

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def list_links(url):
    """Parse an Apache/nginx-style directory-listing page for href links."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return re.findall(r'href="([^"?/][^"]*)"', resp.text)


def discover_files_for_year(year):
    """The exact folder layout (flat, or split by year/month) isn't known
    ahead of time -- try a same-name subfolder first, fall back to filtering
    the top-level listing by year if there's no subfolder."""
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
    """Pull a YYYYMMDD date out of the filename, wherever it sits, tolerating
    optional separators between the year/month/day (e.g. 20180601,
    2018-06-01, 2018_06_01) -- the first version of this only matched 8
    consecutive digits with no separator at all, which is why it found 0
    matches against real TROPOSIF filenames that use dashes."""
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

    sif_var = lat_var = lon_var = None  # resolved from the first file opened
    daily_rows = []

    for year in STUDY_YEARS:
        print(f"\nDiscovering TROPOSIF files for {year}...")
        try:
            all_files = discover_files_for_year(year)
        except requests.RequestException as e:
            print(f"Could not reach {BASE_URL} ({e}). Check your internet connection and that")
            print("ftp.sron.nl isn't blocked by a firewall/VPN, then rerun.")
            return

        season_files = [f for f in all_files if (d := file_date_from_name(f)) and in_season(d, year)]
        print(f"{len(all_files)} files listed for {year}, {len(season_files)} fall in the Jun 1 - Dec 27 season window")
        if all_files and not season_files:
            print("  0 matched -- printing the first 5 raw filenames so the date pattern can be checked:")
            for f in all_files[:5]:
                print("   ", f)
            continue

        for relpath in season_files:
            fname = os.path.basename(relpath)
            local_path = os.path.join(DOWNLOAD_DIR, fname)
            if not os.path.exists(local_path):
                r = requests.get(BASE_URL + relpath, timeout=120)
                if r.status_code != 200:
                    print(f"  skip {fname}: HTTP {r.status_code}")
                    continue
                with open(local_path, "wb") as f:
                    f.write(r.content)

            try:
                ds = xr.open_dataset(local_path)
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

            # cheap bbox pre-filter before the more expensive exact polygon test
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

    # quick comparison against this study's own GOSIF-derived mean SIF per year
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
