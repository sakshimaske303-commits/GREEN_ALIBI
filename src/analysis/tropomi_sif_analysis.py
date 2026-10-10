# TROPOMI SIF cross-check

import glob
import os
import re

import numpy as np
import pandas as pd

RAW_DIR = "data/external/troposif_raw"
BOUNDARY = "data/raw/marathwada_boundary_polygon.geojson"
SOUNDINGS = "data/processed/tropomi_soundings_marathwada.csv.gz"
OUT_COMP = "data/processed/tropomi_8day_composites.csv"
OUT_CMP = "data/processed/tropomi_vs_gosif.csv"
COMP_STARTS = np.arange(153, 362, 8)
MIN_SOUNDINGS = 100
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]
VARIANTS = {
    "main (cf<0.2, cropland, SIF_Corr)": (0.2, True, "sif_corr"),
    "cf<0.5": (0.5, True, "sif_corr"),
    "all land cover": (0.2, False, "sif_corr"),
    "uncorrected SIF_743": (0.2, True, "sif"),
}


def extract():
    import geopandas as gpd
    import netCDF4
    import shapely

    poly = gpd.read_file(BOUNDARY).to_crs("EPSG:4326").geometry.union_all()
    minx, miny, maxx, maxy = poly.bounds
    done = set()
    if os.path.exists(SOUNDINGS):
        done = set(pd.read_csv(SOUNDINGS, usecols=["date"])["date"].unique())
    files = sorted(glob.glob(os.path.join(RAW_DIR, "TROPOSIF_L2B_*.nc")))
    todo = [f for f in files if re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) not in done]
    print(f"Step 1: {len(files)} TROPOSIF files on disk, {len(done)} dates already extracted, {len(todo)} to read")
    for i, f in enumerate(todo, 1):
        d = re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1)
        try:
            ds = netCDF4.Dataset(f)
        except OSError as e:
            print(f"  skip {os.path.basename(f)}: cannot open ({e}) -- probably a partial download")
            continue
        p = ds["PRODUCT"]
        lat, lon = p["latitude"][:], p["longitude"][:]
        box = np.where((lon >= minx) & (lon <= maxx) & (lat >= miny) & (lat <= maxy))[0]
        if len(box):
            inside = shapely.contains_xy(poly, np.asarray(lon[box]), np.asarray(lat[box]))
            idx = box[inside]
        else:
            idx = box
        if len(idx):
            sd, geo, inp = p["SUPPORT_DATA"], p["SUPPORT_DATA"]["GEOLOCATIONS"], p["SUPPORT_DATA"]["INPUT_DATA"]
            df = pd.DataFrame({
                "date": d, "lat": np.asarray(lat[idx]), "lon": np.asarray(lon[idx]),
                "sif": np.ma.filled(p["SIF_743"][idx], np.nan),
                "sif_corr": np.ma.filled(p["SIF_Corr_743"][idx], np.nan),
                "sif_err": np.ma.filled(p["SIF_ERROR_743"][idx], np.nan),
                "cloud_fraction": np.ma.filled(inp["cloud_fraction_L2"][idx], np.nan),
                "land_cover": np.ma.filled(inp["LC_MASK"][idx], -1),
                "sza": np.ma.filled(geo["solar_zenith_angle"][idx], np.nan),
                "vza": np.ma.filled(geo["viewing_zenith_angle"][idx], np.nan),
            })
            df.to_csv(SOUNDINGS, mode="a", header=not os.path.exists(SOUNDINGS), index=False)
        ds.close()
        if i % 25 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)} files read")


def minmax(x):
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def crossing(t, v, th):
    for i in range(len(v) - 1):
        if v[i] >= th and v[i + 1] < th:
            return t[i] + (v[i] - th) / (v[i] - v[i + 1]) * (t[i + 1] - t[i])
    return np.nan


def threshold_lag(t, sif, tn, nd):
    ok = ~np.isnan(sif)
    t, sif = t[ok], sif[ok]
    if len(t) < 8:
        return np.nan
    sn = minmax(sif)
    nn = np.interp(t, tn, minmax(nd), left=np.nan, right=np.nan)
    ps, pn = t[np.nanargmax(sn)], t[np.nanargmax(nn)]
    out = []
    for th in THRESHOLDS:
        a, b = crossing(t[t >= ps], sn[t >= ps], th), crossing(t[t >= pn], nn[t >= pn], th)
        if not (np.isnan(a) or np.isnan(b)):
            out.append(b - a)
    return np.mean(out) if out else np.nan


def composites(s, max_cf, crop_only, var):
    f = s[(s["cloud_fraction"] < max_cf) & (s["sza"] < 70) & s[var].notna()]
    if crop_only:
        f = f[f["land_cover"].isin([12, 14])]
    f = f.assign(year=f["date"].str[:4].astype(int),
                 doy=pd.to_datetime(f["date"]).dt.dayofyear)
    f = f[(f["doy"] >= COMP_STARTS[0]) & (f["doy"] < COMP_STARTS[-1] + 8)]
    f["start"] = COMP_STARTS[np.searchsorted(COMP_STARTS, f["doy"], side="right") - 1]
    c = f.groupby(["year", "start"]).agg(tropomi_sif=(var, "mean"), n=(var, "size"),
                                         days=("date", "nunique")).reset_index()
    c.loc[c["n"] < MIN_SOUNDINGS, "tropomi_sif"] = np.nan
    return c


def analyse():
    s = pd.read_csv(SOUNDINGS)
    s["date"] = s["date"].astype(str)
    print(f"\nStep 2: {len(s):,} soundings inside Marathwada on {s['date'].nunique()} days "
          f"({s['date'].min()} to {s['date'].max()})")
    print(f"  cloud fraction < 0.2: {100 * (s['cloud_fraction'] < 0.2).mean():.0f}% | "
          f"cropland (LC 12/14): {100 * s['land_cover'].isin([12, 14]).mean():.0f}% | "
          f"SZA < 70: {100 * (s['sza'] < 70).mean():.0f}%")

    g = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
    ndvi = pd.read_csv("data/raw/ndvi_obsdate_2015_2023.csv").dropna(subset=["mean_ndvi", "mean_obs_doy"])
    gl = pd.read_csv("data/processed/sif_ndvi_lag_by_threshold.csv").groupby("year")["lag_days"].mean()

    all_comp, rows = [], []
    for vname, (cf, crop, var) in VARIANTS.items():
        c = composites(s, cf, crop, var)
        c["variant"] = vname
        all_comp.append(c)
        for y, cy in c.groupby("year"):
            gy = g[g["year"] == y].set_index("sif_start_doy")["mean_sif"]
            ty = cy.set_index("start")["tropomi_sif"].reindex(gy.index)
            ok = ty.notna()
            if ok.sum() < 8:
                continue
            ny = ndvi[ndvi["year"] == y].sort_values("mean_obs_doy")
            tc = gy.index.values + 3.5
            lag_t = threshold_lag(tc, ty.values, ny["mean_obs_doy"].values, ny["mean_ndvi"].values)
            rows.append({"variant": vname, "year": y, "n_composites": int(ok.sum()),
                         "r_with_gosif": np.corrcoef(ty[ok], gy[ok])[0, 1],
                         "peak_doy_tropomi": ty.idxmax() + 3.5, "peak_doy_gosif": gy.idxmax() + 3.5,
                         "lag_tropomi_vs_ndvi": lag_t, "lag_gosif_vs_ndvi": gl.get(y, np.nan)})
    comp = pd.concat(all_comp)
    comp.to_csv(OUT_COMP, index=False)
    R = pd.DataFrame(rows)
    R.to_csv(OUT_CMP, index=False)

    pd.set_option("display.width", 200)
    print("\nStep 3: TROPOMI vs GOSIF, per year (lag = NDVI crossing minus SIF crossing, days; > 0 = SIF leads)")
    print(R.round(2).to_string(index=False))

    main = comp[comp["variant"] == list(VARIANTS)[0]].pivot(index="start", columns="year", values="tropomi_sif")
    gos = g.pivot(index="sif_start_doy", columns="year", values="mean_sif")
    if 2018 in main.columns and main.shape[1] >= 2:
        others = [y for y in main.columns if y != 2018]
        print(f"\n2018 vs mean of {others} (ratio, Aug-Oct composites), TROPOMI and GOSIF side by side:")
        sel = [d for d in main.index if 213 <= d <= 297]
        t_ratio = main.loc[sel, 2018] / main.loc[sel, others].mean(axis=1)
        g_ratio = gos.loc[sel, 2018] / gos.loc[sel, others].mean(axis=1)
        out = pd.DataFrame({"start_doy": sel, "tropomi_2018_ratio": t_ratio.values, "gosif_2018_ratio": g_ratio.values})
        print(out.round(2).to_string(index=False))
        ok = out.dropna()
        if len(ok) >= 3:
            print(f"  r between the two ratio series = {np.corrcoef(ok['tropomi_2018_ratio'], ok['gosif_2018_ratio'])[0, 1]:.2f}")
    print(f"\nSaved {OUT_COMP} and {OUT_CMP}")


if __name__ == "__main__":
    # the raw TROPOSIF files (~100 GB) are not in the repository; without them the
    # analysis runs from the extracted soundings file that is
    if glob.glob(os.path.join(RAW_DIR, "TROPOSIF_L2B_*.nc")):
        extract()
    else:
        print(f"No raw TROPOSIF files in {RAW_DIR}; using the extracted soundings in {SOUNDINGS}")
    analyse()
