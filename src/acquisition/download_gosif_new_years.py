# GOSIF v2 8-day download, DOY 153-361
#   python src/acquisition/download_gosif_new_years.py             # 2015-2023
#   python src/acquisition/download_gosif_new_years.py 2001 2014   # any year range (e.g. the 2001-2014 extension)

import gzip
import os
import shutil
import time

import sys

import requests

BASE_URL = "https://data.globalecology.unh.edu/data/GOSIF_v2/8day/"
OUT_DIR = "data/raw"

DOYS = list(range(153, 362, 8))

NEW_YEARS = (list(range(int(sys.argv[1]), int(sys.argv[2]) + 1)) if len(sys.argv) == 3
             else list(range(2015, 2024)))
EXISTING_DIRS = ["data/raw", "data/external"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


def download_one(year, doy):
    filename = f"GOSIF_{year}{doy:03d}.tif.gz"
    gz_path = os.path.join(OUT_DIR, filename)
    tif_path = gz_path[:-3]

    for d in EXISTING_DIRS:
        base = os.path.join(d, filename[:-3])
        if os.path.exists(base) or os.path.exists(base + ".gz"):
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
            with gzip.open(gz_path, "rb") as f_in:
                f_in.read(1024)
            print(f"  {filename}: downloaded ({len(resp.content)/1e6:.1f} MB).")
            return True

        print(f"  {filename}: attempt {attempt} failed (HTTP {resp.status_code})")
        if resp.status_code == 404:
            break
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
