# GOSIF grid origin shift check

import glob
import gzip
import os
import re
import shutil
import tempfile

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.features import geometry_mask

CLIPPED = "data/processed/clipped"
FRAC = "data/external/cropland_fraction"
YEARS = [2021, 2022]
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]


def read_gz(path):
    with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
        with gzip.open(path, "rb") as f:
            shutil.copyfileobj(f, tmp)
    with rasterio.open(tmp.name) as src:
        arr, origin = src.read(1), src.transform.c
    os.remove(tmp.name)
    return arr, origin


if os.path.exists("data/raw/GOSIF_2020273.tif.gz") and os.path.exists("data/raw/GOSIF_2022273.tif.gz"):
    a, oa = read_gz("data/raw/GOSIF_2020273.tif.gz")
    b, ob = read_gz("data/raw/GOSIF_2022273.tif.gz")
    print(f"Step 1: header origin 2020 = {oa}, 2022 = {ob}")
    for code, name in [(32767, "water"), (32766, "non-vegetated")]:
        ma, mb = a == code, b == code
        same = int((ma != mb).sum())
        east = int((np.roll(mb, 1, axis=1) != ma).sum())
        west = int((np.roll(mb, -1, axis=1) != ma).sum())
        print(f"  {name:14s} mask: pixels that differ from 2020 -- same index: {same:,} | "
              f"moved one column east: {east:,} | one column west: {west:,}")
    print("  -> masks match by array index: the data are on the standard grid; "
          "only the header origin (-180.025) is wrong.\n")
else:
    print("Step 1 skipped (raw 2020/2022 DOY 273 .tif.gz not found)\n")

with rasterio.open(os.path.join(CLIPPED, "GOSIF_2021273_clipped.tif")) as _s:
    _phase = round((_s.transform.c / _s.transform.a) % 1, 3)
if _phase in (0.0, 1.0):
    print("Step 2 skipped: the 2021/2022 clipped rasters are already on the standard grid "
          "(clip_gosif.py corrects the header). The before/after comparison made while they were "
          "still shifted is kept in data/processed/gosif_grid_shift_check.csv.")
    raise SystemExit(0)

region = gpd.read_file("data/raw/marathwada_boundary_polygon.geojson").to_crs("EPSG:4326").geometry.union_all()
gdf = gpd.read_file("data/raw/marathwada_districts_separate.geojson").to_crs("EPSG:4326")
gdf["district"] = gdf["ADM2_NAME"].str.strip()


def frac_on(transform, shape, year, corrected):
    with rasterio.open(os.path.join(FRAC, f"cropland_fraction_{year}.tif")) as f:
        full = np.nan_to_num(f.read(1).astype("float64"))
        ft = f.transform
    if corrected:
        full = (full[:, :-1] + full[:, 1:]) / 2
        ft = Affine(ft.a, 0, ft.c + ft.a / 2, 0, ft.e, ft.f)
    c0 = int(round((transform.c - ft.c) / ft.a))
    r0 = int(round((transform.f - ft.f) / ft.e))
    out = full[r0:r0 + shape[0], c0:c0 + shape[1]]
    assert out.shape == shape, (out.shape, shape)
    return out


def weighted(sif, frac, inside):
    w = np.where(~np.isnan(sif) & inside, frac, 0.0)
    return (np.where(np.isnan(sif), 0.0, sif) * w).sum() / w.sum() if w.sum() > 0 else np.nan


rows, edge = [], {}
for year in YEARS:
    for path in sorted(glob.glob(os.path.join(CLIPPED, f"GOSIF_{year}*_clipped.tif"))):
        doy = int(re.search(r"GOSIF_\d{4}(\d{3})_", path).group(1))
        with rasterio.open(path) as src:
            sif, t_old, shape = src.read(1).astype("float64"), src.transform, src.shape
        t_new = Affine(t_old.a, 0, t_old.c + t_old.a / 2, 0, t_old.e, t_old.f)
        for version, t, corr in [("current", t_old, False), ("corrected", t_new, True)]:
            fr = frac_on(t, shape, year, corr)
            reg_in = ~geometry_mask([region], out_shape=shape, transform=t)
            rows.append({"version": version, "year": year, "doy": doy, "district": "Marathwada",
                         "mean_sif": weighted(sif, fr, reg_in)})
            for d, g in zip(gdf["district"], gdf.geometry):
                inside = ~geometry_mask([g], out_shape=shape, transform=t)
                rows.append({"version": version, "year": year, "doy": doy, "district": d,
                             "mean_sif": weighted(sif, fr, inside)})
        if year not in edge:
            old_in = ~geometry_mask([region], out_shape=shape, transform=t_old)
            new_in = ~geometry_mask([region], out_shape=shape, transform=t_new)
            edge[year] = (int(old_in.sum()), int((old_in & ~new_in).sum()), int((new_in & ~old_in).sum()))
s = pd.DataFrame(rows)
for y, (n, dropped, missing) in edge.items():
    print(f"{y}: {n} pixels inside the region in the current version; correcting the position drops "
          f"{dropped} that fall outside, and {missing} true-inside pixels were cut off at clipping "
          f"(lost -- the clipped file has no value for them)")

cur_reg = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
cur_reg = cur_reg[cur_reg["year"].isin(YEARS)][["year", "sif_start_doy", "mean_sif"]]
chk = s[(s["version"] == "current") & (s["district"] == "Marathwada")].merge(
    cur_reg, left_on=["year", "doy"], right_on=["year", "sif_start_doy"], suffixes=("", "_pipe"))
cur_d = pd.read_csv("data/processed/sif_timeseries_by_district.csv")
chk_d = s[(s["version"] == "current") & (s["district"] != "Marathwada")].merge(
    cur_d, on=["year", "doy", "district"], suffixes=("", "_pipe"))
print(f"Reproduction check (current version vs pipeline): region max |diff| = "
      f"{(chk['mean_sif'] - chk['mean_sif_pipe']).abs().max():.2e}, district max |diff| = "
      f"{(chk_d['mean_sif'] - chk_d['mean_sif_pipe']).abs().max():.2e}\n")


def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def crossing(doys, vals, t):
    for i in range(len(vals) - 1):
        v1, v2 = vals[i], vals[i + 1]
        if v1 >= t and v2 < t:
            return doys[i] + (v1 - t) / (v1 - v2) * (doys[i + 1] - doys[i])
    return np.nan


def lags_for(sv, n):
    sv = sv.sort_values("doy")
    n = n.dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
    t = sv["doy"].values + 3.5
    sn = minmax(sv["mean_sif"].values)
    nn = np.interp(t, n["mean_obs_doy"].values, minmax(n["mean_ndvi"].values), left=np.nan, right=np.nan)
    ps, pn = t[np.nanargmax(sn)], t[np.nanargmax(nn)]
    th = []
    for thr in THRESHOLDS:
        a = crossing(t[t >= ps], sn[t >= ps], thr)
        b = crossing(t[t >= pn], nn[t >= pn], thr)
        if not (np.isnan(a) or np.isnan(b)):
            th.append(b - a)
    keep = (t >= ps) & ~np.isnan(nn)
    tt, ss, nd = t[keep], sn[keep], nn[keep]
    grid = np.arange(tt.min(), tt.max() + 1)
    sd, ndd = np.interp(grid, tt, ss), np.interp(grid, tt, nd)
    sd, ndd = sd - sd.mean(), ndd - ndd.mean()
    ml = int(len(grid) / 4)
    lags = np.arange(-ml, ml + 1)
    cs = [np.corrcoef(sd[:-L], ndd[L:])[0, 1] if L > 0 else
          np.corrcoef(sd[-L:], ndd[:L])[0, 1] if L < 0 else np.corrcoef(sd, ndd)[0, 1] for L in lags]
    return (np.mean(th) if th else np.nan), int(lags[int(np.argmax(cs))])


ndvi_r = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv")
ndvi_d = pd.read_csv("data/raw/ndvi_obsdate_by_district_2015_2023.csv")
ndvi_d["district"] = ndvi_d["district"].str.strip()
out = []
for (v, y, d), sv in s.groupby(["version", "year", "district"]):
    n = ndvi_r[ndvi_r["year"] == y] if d == "Marathwada" else ndvi_d[(ndvi_d["year"] == y) & (ndvi_d["district"] == d)]
    tl, xl = lags_for(sv, n)
    out.append({"version": v, "year": y, "district": d, "threshold_lag": tl, "xcorr_lag": xl,
                "season_mean_sif": sv["mean_sif"].mean()})
res = pd.DataFrame(out)
wide = res.pivot_table(index=["year", "district"], columns="version",
                       values=["threshold_lag", "xcorr_lag", "season_mean_sif"])
wide.columns = [f"{a}_{b}" for a, b in wide.columns]
wide = wide.reset_index()
wide["threshold_lag_change"] = wide["threshold_lag_corrected"] - wide["threshold_lag_current"]
wide["season_sif_change_pct"] = 100 * (wide["season_mean_sif_corrected"] / wide["season_mean_sif_current"] - 1)
wide.to_csv("data/processed/gosif_grid_shift_check.csv", index=False)

pd.set_option("display.width", 200)
print("Threshold lag (days) and seasonal SIF, current vs corrected position:")
print(wide[["year", "district", "threshold_lag_current", "threshold_lag_corrected", "threshold_lag_change",
            "xcorr_lag_current", "xcorr_lag_corrected", "season_sif_change_pct"]].round(2).to_string(index=False))
dist = wide[wide["district"] != "Marathwada"]
print(f"\nDistrict threshold lag change: mean {dist['threshold_lag_change'].mean():+.2f} d, "
      f"max |change| {dist['threshold_lag_change'].abs().max():.2f} d")
print(f"District seasonal SIF change: max |change| {dist['season_sif_change_pct'].abs().max():.2f}%")
print("\nSaved data/processed/gosif_grid_shift_check.csv")
