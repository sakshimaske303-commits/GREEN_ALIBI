"""
One-off cleanup script for files that are no longer used by anything in this
repository but are still sitting on disk. Run this once from the repo root:

    python cleanup_stale_files.py

By default it only prints what it would delete. Pass --delete to actually
remove the files.

What this removes, and why:

1. data/processed/clipped/GOSIF_<year><doy>.tif (no suffix) and their
   .tif.aux.xml sidecars, for 2015/2018/2020 — these are the original
   rectangular-window GOSIF clips from before the boundary-precision fix
   (see GA_Development_Log.md, Entry 4 and Entry 11). Every current script
   reads only the *_clipped.tif files (the polygon-masked output), so these
   plain-named originals are dead weight left over from a stale glob-pattern
   bug that briefly caused aggregate_sif.py to read the wrong ones. Keeping
   them around risks that exact bug resurfacing in any future script that
   globs this folder loosely.

2. outputs/figures/imgg1.png, idk.jpeg, theme.jpeg — image files sitting in
   the figures folder that no dashboard page, script, or document actually
   references. Confirmed via a full-repository grep before listing them here.
"""

import argparse
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

STALE_GOSIF_RE = re.compile(r"^GOSIF_\d{7}\.tif$")
STALE_AUX_RE = re.compile(r"^GOSIF_\d{7}\.tif\.aux\.xml$")

CLIPPED_DIR = os.path.join(ROOT, "data", "processed", "clipped")

ORPHANED_FIGURES = [
    os.path.join(ROOT, "outputs", "figures", "imgg1.png"),
    os.path.join(ROOT, "outputs", "figures", "idk.jpeg"),
    os.path.join(ROOT, "outputs", "figures", "theme.jpeg"),
]


def find_stale_gosif_files():
    if not os.path.isdir(CLIPPED_DIR):
        return []
    stale = []
    for name in os.listdir(CLIPPED_DIR):
        if STALE_GOSIF_RE.match(name) or STALE_AUX_RE.match(name):
            stale.append(os.path.join(CLIPPED_DIR, name))
    return sorted(stale)


def find_orphaned_figures():
    return [p for p in ORPHANED_FIGURES if os.path.exists(p)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--delete", action="store_true",
        help="Actually delete the files. Without this flag, only lists them."
    )
    args = parser.parse_args()

    stale_gosif = find_stale_gosif_files()
    orphaned_figs = find_orphaned_figures()
    all_targets = stale_gosif + orphaned_figs

    if not all_targets:
        print("Nothing to clean up — no stale or orphaned files found.")
        return

    print(f"Stale pre-boundary-fix GOSIF clips: {len(stale_gosif)} file(s)")
    for p in stale_gosif:
        print(f"  {os.path.relpath(p, ROOT)}")

    print(f"\nOrphaned figure files: {len(orphaned_figs)} file(s)")
    for p in orphaned_figs:
        print(f"  {os.path.relpath(p, ROOT)}")

    if not args.delete:
        print(f"\n{len(all_targets)} file(s) total. Re-run with --delete to remove them.")
        return

    removed = 0
    for p in all_targets:
        try:
            os.remove(p)
            removed += 1
        except OSError as e:
            print(f"Could not remove {p}: {e}")

    print(f"\nRemoved {removed} of {len(all_targets)} file(s).")


if __name__ == "__main__":
    main()
