"""
GREEN ALIBI — GOSIF v2 8-day raw data download for the sample-size
expansion (3 years -> 8 years).

Pulls the same GOSIF v2 8-day composite product, same seasonal window
(DOY 153-361, 27 composites/year) and file-naming convention already used
for 2015/2018/2020, for the five new years: 2016, 2017, 2019, 2022, 2023.

Has to run from a normal home/office connection -- the GOSIF server
blocks cloud-hosted IP ranges with a 403.

Usage:
    pip install requests
    python src/acquisition/download_gosif_new_years.py

Downloads ~135 files as .tif.gz into data/raw/, decompresses each to the
matching .tif. Safe to re-run after an interruption -- already-downloaded
files are skipped. ~1.2 GB total.
"""

import gzip
import os
import shutil
import time

import requests

BASE_URL = "https://data.globalecology.unh.edu/data/GOSIF_v2/8day/"
OUT_DIR = "data/raw"

# Same seasonal window already used for 2015/2018/2020 — day-of-year
# 153 through 361 in 8-day steps (27 composites per year, roughly
# early June through late December).
DOYS = list(range(153, 362, 8))

# The five new years agreed for this expansion pass. 2015/2018/2020 are
# intentionally NOT re-downloaded — they're already in data/raw/.
NEW_YEARS = [2016, 2017, 2019, 2022, 2023]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


def download_one(year, doy):
    filename = f"GOSIF_{year}{doy:03d}.tif.gz"
    gz_path = os.path.join(OUT_DIR, filename)
    tif_path = gz_path[:-3]  # strip ".gz"

    if os.path.exists(tif_path):
        print(f"  {filename}: already have the decompressed .tif, skipping.")
        return True

    url = BASE_URL + filename
    for attempt in (1, 2, 3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=120)
        except requests.exceptions.RequestException as e:
            print(f"  {filename}: attempt {attempt} network error ({e})")
            time.sleep(5)
            continue

        if resp.status_code == 200:
            with open(gz_path, "wb") as f:
                f.write(resp.content)
            with gzip.open(gz_path, "rb") as f_in, open(tif_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            print(f"  {filename}: downloaded and decompressed ({len(resp.content)/1e6:.1f} MB).")
            return True

        print(f"  {filename}: attempt {attempt} failed (HTTP {resp.status_code})")
        if resp.status_code == 404:
            break  # no point retrying a genuine 404
        time.sleep(5)

    print(f"  {filename}: FAILED after retries — this composite date may not exist for this year, "
          f"or the server is temporarily unavailable. Continuing with the rest.")
    return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Downloading GOSIF v2 8-day composites for {NEW_YEARS}, DOY {DOYS[0]}-{DOYS[-1]} "
          f"(step 8, {len(DOYS)} composites/year)...\n")

    results = {}
    for year in NEW_YEARS:
        print(f"{year}:")
        ok_count = 0
        for doy in DOYS:
            if download_one(year, doy):
                ok_count += 1
        results[year] = ok_count
        print(f"  -> {ok_count}/{len(DOYS)} composites OK for {year}\n")

    print("Done.")
    for year, ok_count in results.items():
        flag = "" if ok_count == len(DOYS) else "  <-- some composites missing, check log above"
        print(f"  {year}: {ok_count}/{len(DOYS)}{flag}")


if __name__ == "__main__":
    main()
