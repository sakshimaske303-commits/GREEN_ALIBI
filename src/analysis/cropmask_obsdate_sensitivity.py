# cropland mask and NDVI observation-date sensitivity

import glob
import os
import re

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import from_bounds

CLIPPED_DIR = "data/processed/clipped"
FRAC_DIR = "data/external/cropland_fraction"
NDVI_OBS_CSV = "data/raw/ndvi_obsdate_2015_2023.csv"
SIF_OUT = "data/processed/marathwada_sif_timeseries_cropland.csv"
OUT_CSV = "data/processed/cropmask_obsdate_sensitivity.csv"
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT_YEARS = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])

rows = []
frac_cache = {}
for path in sorted(glob.glob(os.path.join(CLIPPED_DIR, "GOSIF_*_clipped.tif"))):
    m = re.search(r"GOSIF_(\d{4})(\d{3})_clipped\.tif", os.path.basename(path))
    year, doy = int(m.group(1)), int(m.group(2))
    with rasterio.open(path) as src:
        sif = src.read(1).astype("float64")
        sif_transform, sif_bounds, shape = src.transform, src.bounds, src.shape

    fpath = os.path.join(FRAC_DIR, f"cropland_fraction_{year}.tif")
    with rasterio.open(fpath) as fsrc:
        dx = (sif_transform.c - fsrc.transform.c) / fsrc.transform.a
        dy = (sif_transform.f - fsrc.transform.f) / fsrc.transform.e
        if abs(dx - round(dx)) > 1e-6 or abs(dy - round(dy)) > 1e-6:
            raise ValueError(f"{os.path.basename(path)}: SIF grid and cropland-fraction grid are "
                             f"offset by a fraction of a pixel ({dx:.3f}, {dy:.3f})")
        win = from_bounds(*sif_bounds, transform=fsrc.transform).round_offsets().round_lengths()
        frac = fsrc.read(window=win).astype("float64")
    if frac.shape[1:] != shape:
        raise ValueError(f"{os.path.basename(path)}: window shape {frac.shape[1:]} != SIF shape {shape}")
    f1214, f12 = frac[0], frac[1]

    valid = ~np.isnan(sif)
    rec = {"year": year, "doy": doy, "mean_sif_all": np.nanmean(sif)}
    for name, f in [("1214", f1214), ("12", f12)]:
        f = np.where(np.isnan(f), 0.0, f)
        w = np.where(valid, f, 0.0)
        rec[f"mean_sif_crop{name}"] = np.nansum(np.where(valid, sif, 0.0) * w) / w.sum() if w.sum() > 0 else np.nan
        rec[f"crop{name}_weight_sum"] = w.sum()
    rec["mean_cropland_fraction_1214"] = f1214[valid].mean()
    rows.append(rec)

sif = pd.DataFrame(rows).sort_values(["year", "doy"]).reset_index(drop=True)
sif.to_csv(SIF_OUT, index=False)
print("Cropland-weighted SIF saved to", SIF_OUT)
print("Mean cropland fraction (12+14) over valid SIF pixels, by year:")
print(sif.groupby("year")["mean_cropland_fraction_1214"].mean().round(3).to_string())

ndvi_obs = pd.read_csv(NDVI_OBS_CSV).sort_values(["year", "doy_start"]).reset_index(drop=True)
ndvi_obs["offset_days"] = ndvi_obs["mean_obs_doy"] - ndvi_obs["doy_start"]
print("\nNDVI actual observation day minus composite start day (days):")
print(ndvi_obs["offset_days"].describe().round(2).to_string())

old = pd.read_csv("data/raw/marathwada_ndvi_mod13q1_timeseries_8years.csv")
chk = ndvi_obs.merge(old, left_on=["year", "doy_start"], right_on=["year", "doy"], how="inner")
print(f"Sanity check vs main NDVI file: {len(chk)} matched composites, "
      f"max |NDVI difference| = {(chk['mean_ndvi_x'] - chk['mean_ndvi_y']).abs().max():.6f}")


def norm(x):
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def crossing(doys, vals, t):
    for i in range(len(vals) - 1):
        v1, v2 = vals[i], vals[i + 1]
        if np.isnan(v1) or np.isnan(v2):
            continue
        if v1 >= t and v2 < t:
            return doys[i] + (v1 - t) / (v1 - v2) * (doys[i + 1] - doys[i])
    return np.nan


def threshold_lags(sub):
    sub = sub.sort_values("t").reset_index(drop=True)
    s, n, t = sub["sif"].values, sub["ndvi"].values, sub["t"].values
    ps, pn = t[np.nanargmax(s)], t[np.nanargmax(n)]
    out = {}
    for th in THRESHOLDS:
        a = crossing(t[t >= ps], s[t >= ps], th)
        b = crossing(t[t >= pn], n[t >= pn], th)
        out[th] = (a, b, b - a)
    return out


def xcorr_lag(sub):
    sub = sub.sort_values("t").reset_index(drop=True)
    s, n, t = sub["sif"].values, sub["ndvi"].values, sub["t"].values
    keep = (t >= t[np.nanargmax(s)]) & ~np.isnan(s) & ~np.isnan(n)
    t, s, n = t[keep], s[keep], n[keep]
    grid = np.arange(t.min(), t.max() + 1)
    sd, nd = np.interp(grid, t, s), np.interp(grid, t, n)
    sd, nd = sd - sd.mean(), nd - nd.mean()
    ml = int(len(grid) / 4)
    lags = np.arange(-ml, ml + 1)
    cs = []
    for L in lags:
        if L > 0:
            cs.append(np.corrcoef(sd[:-L], nd[L:])[0, 1])
        elif L < 0:
            cs.append(np.corrcoef(sd[-L:], nd[:L])[0, 1])
        else:
            cs.append(np.corrcoef(sd, nd)[0, 1])
    i = int(np.argmax(cs))
    return int(lags[i]), abs(lags[i]) == ml


def build(year, sif_col, ndvi_mode):
    s = sif[sif["year"] == year].sort_values("doy")
    n = ndvi_obs[ndvi_obs["year"] == year].sort_values("doy_start")
    if ndvi_mode == "window":
        df = pd.merge_asof(s[["doy", sif_col]], n[["doy_start", "mean_ndvi"]].rename(columns={"doy_start": "doy"}),
                           on="doy", direction="backward")
        return pd.DataFrame({"t": df["doy"], "sif": norm(df[sif_col].values), "ndvi": norm(df["mean_ndvi"].values)})
    tc = s["doy"].values + 3.5
    nd = np.interp(tc, n["mean_obs_doy"].values, norm(n["mean_ndvi"].values), left=np.nan, right=np.nan)
    return pd.DataFrame({"t": tc, "sif": norm(s[sif_col].values), "ndvi": nd})


VARIANTS = {
    "V0_all_window": ("mean_sif_all", "window"),
    "V1_crop1214_window": ("mean_sif_crop1214", "window"),
    "V2_all_obsdate": ("mean_sif_all", "obsdate"),
    "V3_crop1214_obsdate": ("mean_sif_crop1214", "obsdate"),
    "V4_crop12_obsdate": ("mean_sif_crop12", "obsdate"),
}

records = []
for vname, (col, mode) in VARIANTS.items():
    for year in sorted(sif["year"].unique()):
        df = build(year, col, mode)
        tl = threshold_lags(df)
        lags = [v[2] for v in tl.values() if not np.isnan(v[2])]
        xl, pinned = xcorr_lag(df)
        records.append({
            "variant": vname, "year": year, "is_drought_year": year in DROUGHT_YEARS,
            "mean_threshold_lag": np.mean(lags), "n_thresholds": len(lags),
            "sif_cross_0.9": tl[0.9][0], "ndvi_cross_0.9": tl[0.9][1], "lag_0.9": tl[0.9][2],
            "xcorr_lag": xl, "xcorr_at_search_edge": pinned,
        })

res = pd.DataFrame(records)
res.to_csv(OUT_CSV, index=False)

print("\nMean threshold-crossing lag (days) by variant:")
print(res.pivot(index="year", columns="variant", values="mean_threshold_lag").round(1).to_string())
print("\nCross-correlation lag (days) by variant (* = at search edge):")
xc = res.assign(v=res["xcorr_lag"].astype(str) + np.where(res["xcorr_at_search_edge"], "*", ""))
print(xc.pivot(index="year", columns="variant", values="v").to_string())
print("\nDrought vs normal mean threshold lag:")
g = res.groupby(["variant", "is_drought_year"])["mean_threshold_lag"].mean().unstack().round(1)
g.columns = ["normal", "drought"]
print(g.to_string())
print("\n2018, 0.9 threshold crossing day (SIF / NDVI):")
print(res[res["year"] == 2018][["variant", "sif_cross_0.9", "ndvi_cross_0.9", "lag_0.9"]].round(1).to_string(index=False))
print(f"\nSaved {OUT_CSV}")
