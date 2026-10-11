# out-of-sample test on 2001-2014 with the 2015-2023 methods frozen
#
# Nothing is re-tuned here. The drought rule (CHIRPS Jun-Dec z < -0.5 against 2001-2020), the
# alarm rule (two consecutive composites below z = -3 from 1 July, z against the normal years
# of the same period, leaving the year itself out), the cropland weighting, the NDVI dating and
# the lag metrics are exactly the ones used for 2015-2023. The 2001-2014 years are standardised
# against the normal years of 2001-2014 only, so nothing from 2015-2023 enters the test.
#
# Inputs (2001-2014):
#   data/raw/GOSIF_YYYYDDD.tif.gz               python src/acquisition/download_gosif_new_years.py 2001 2014
#   data/raw/vi_obsdate_2001_2014.csv           Code Editor: gee_vi_obsdate_CODE_EDITOR.js with 2001-2014
#   data/raw/vi_obsdate_by_district_2001_2014.csv
#   data/external/cropland_fraction/cropland_fraction_YYYY.tif   gee_cropland_fraction_CODE_EDITOR.js
#
# Usage:
#   python src/analysis/out_of_sample_2001_2014.py           # extract SIF (once) and run the test
#   python src/analysis/out_of_sample_2001_2014.py --check   # run the same code on 2015-2023 and
#                                                            # compare with the main results
# The SIF extraction repeats clip_gosif.py + aggregate_sif.py + district_lag_analysis.py in memory;
# on the first run it also re-extracts 2015 and checks that it matches the main pipeline exactly.

import gzip
import os
import sys

import numpy as np
import pandas as pd

FIRST, LAST = 2001, 2014
DOYS = list(range(153, 362, 8))
START_DOY = 182
THRESHOLDS = [-1.0, -1.5, -2.0, -3.0]
MAIN_THR = -3.0
LAG_THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]
BASELINE = (2001, 2020)
OUT = "data/processed"
SIF_REGION = f"{OUT}/oos_sif_region_{FIRST}_{LAST}.csv"
SIF_DISTRICT = f"{OUT}/oos_sif_district_{FIRST}_{LAST}.csv"
VI_REGION = f"data/raw/vi_obsdate_{FIRST}_{LAST}.csv"
VI_DISTRICT = f"data/raw/vi_obsdate_by_district_{FIRST}_{LAST}.csv"


# ---------------------------------------------------------------- SIF extraction (needs rasterio)

def extract_sif(years):
    import geopandas as gpd
    import rasterio
    from affine import Affine
    from rasterio.features import geometry_mask
    from rasterio.io import MemoryFile
    from rasterio.mask import mask

    boundary = gpd.read_file("data/raw/marathwada_boundary_polygon.geojson")
    boundary = boundary.set_crs("EPSG:4326") if boundary.crs is None else boundary.to_crs("EPSG:4326")
    geometry = [boundary.geometry.union_all()]
    gdf = gpd.read_file("data/raw/marathwada_districts_separate.geojson")
    gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf.to_crs("EPSG:4326")
    gdf["district"] = gdf["ADM2_NAME"].str.strip()

    def source(year, doy):
        for d in ["data/raw", "data/external"]:
            for ext in [".tif", ".tif.gz"]:
                p = os.path.join(d, f"GOSIF_{year}{doy:03d}{ext}")
                if os.path.exists(p):
                    return p
        raise FileNotFoundError(f"GOSIF_{year}{doy:03d} not found (run download_gosif_new_years.py)")

    reg, dis, masks = [], [], {}
    for year in years:
        with rasterio.open(f"data/external/cropland_fraction/cropland_fraction_{year}.tif") as fsrc:
            frac_all, ftr = fsrc.read().astype("float64"), fsrc.transform
        for doy in DOYS:
            path = source(year, doy)
            opener = gzip.open if path.endswith(".gz") else open
            with opener(path, "rb") as f:
                raw = f.read()
            with MemoryFile(raw) as mem, mem.open() as src:
                meta = src.meta.copy()
                t = src.transform
                if (round(t.c, 6), round(t.f, 6)) != (-180.0, 90.0):
                    if abs(t.c - (-180.0 - t.a / 2)) < 1e-6 and abs(t.f - 90.0) < 1e-6:
                        meta["transform"] = Affine(t.a, t.b, -180.0, t.d, t.e, t.f)
                    else:
                        raise ValueError(f"{path}: unexpected grid origin ({t.c}, {t.f})")
                data = src.read(1)
            with MemoryFile() as mem2:
                with mem2.open(**meta) as dst:
                    dst.write(data, 1)
                with mem2.open() as fixed:
                    out_image, out_tr = mask(fixed, geometry, crop=True, nodata=-1, filled=True)
            sif = out_image[0].astype("float64")
            sif = np.where(sif == -1, np.nan, sif)
            sif = np.where(np.isin(sif, [32766, 32767]), np.nan, sif) * 0.0001
            shape = sif.shape
            dx, dy = (out_tr.c - ftr.c) / ftr.a, (out_tr.f - ftr.f) / ftr.e
            if abs(dx - round(dx)) > 1e-6 or abs(dy - round(dy)) > 1e-6:
                raise ValueError(f"{year}: SIF and cropland-fraction grids are offset by part of a pixel")
            r0, c0 = int(round(dy)), int(round(dx))
            frac = np.nan_to_num(frac_all[:, r0:r0 + shape[0], c0:c0 + shape[1]])
            if frac.shape[1:] != shape:
                raise ValueError(f"{year}: cropland window {frac.shape[1:]} != SIF raster {shape}")
            valid = ~np.isnan(sif)
            sif0 = np.where(valid, sif, 0.0)
            w = np.where(valid, frac[0], 0.0)
            reg.append({"year": year, "doy": doy, "mean_sif": sif0[valid].mean() if valid.any() else np.nan,
                        "mean_sif_crop1214": (sif0 * w).sum() / w.sum()})
            key = (out_tr.c, out_tr.f, shape)
            if key not in masks:
                masks[key] = {d: ~geometry_mask([g], out_shape=shape, transform=out_tr)
                              for d, g in zip(gdf["district"], gdf.geometry)}
            for d, inside in masks[key].items():
                wd = np.where(valid & inside, frac[0], 0.0)
                dis.append({"year": year, "doy": doy, "district": d,
                            "mean_sif": (sif0 * wd).sum() / wd.sum() if wd.sum() > 0 else np.nan})
        print(f"  SIF {year}: {len(DOYS)} composites")
    return pd.DataFrame(reg), pd.DataFrame(dis)


# ---------------------------------------------------------------- the frozen analysis

def crossing(t, v, th):
    for i in range(len(v) - 1):
        if v[i] >= th and v[i + 1] < th:
            return t[i] + (v[i] - th) / (v[i] - v[i + 1]) * (t[i + 1] - t[i])
    return np.nan


def scale(v, how):
    v = np.asarray(v, float)
    if how == "season":
        return (v - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v))
    ip = int(np.nanargmax(v))
    lo = np.nanmin(v[ip:])
    return (v - lo) / (v[ip] - lo)


def lag(t_lead, v_lead, t_lag, v_lag, how):
    """mean over thresholds of (crossing date of the second series - crossing date of the first)"""
    a = scale(v_lead, how)
    b = np.interp(t_lead, t_lag, scale(v_lag, how), left=np.nan, right=np.nan)
    pa, pb = t_lead[np.nanargmax(a)], t_lead[np.nanargmax(b)]
    out = np.array([crossing(t_lead[t_lead >= pb], b[t_lead >= pb], th) -
                    crossing(t_lead[t_lead >= pa], a[t_lead >= pa], th) for th in LAG_THRESHOLDS])
    return np.nanmean(out) if np.isfinite(out).any() else np.nan


def first_alarm(doys, z, thr):
    for i in range(len(doys) - 1):
        if doys[i] >= START_DOY and z[i] < thr and z[i + 1] < thr:
            return doys[i] + 3.5
    return np.nan


def anomaly(table, year, normal_years):
    ref = table.loc[[y for y in normal_years if y != year]]
    return ((table.loc[year] - ref.mean()) / ref.std(ddof=1)).values


def rainfall_classes(years):
    tot = pd.read_csv("data/raw/chirps_seasonal_totals_1981_2023.csv")
    base = tot[tot["year"].between(*BASELINE)]
    clim = base.groupby("unit")["rainfall_mm"].agg(["mean", "std"])
    t = tot[tot["year"].isin(years)].join(clim, on="unit")
    t["z"] = (t["rainfall_mm"] - t["mean"]) / t["std"]
    region = t[t["unit"] == "Marathwada"].set_index("year")["z"]
    district = t[t["unit"] != "Marathwada"].rename(columns={"unit": "district"})
    return region, {(r.district, r.year) for r in district.itertuples() if r.z < -0.5}


def regional_table(sif_reg, vi_reg, sif_col):
    """SIF and NDVI/NIRv on the SIF composite dates (centre = start + 3.5), as in compare_sif_ndvi.py"""
    rows = []
    for y, s in sif_reg.groupby("year"):
        s = s.sort_values("doy")
        v = vi_reg[vi_reg["year"] == y].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
        t = s["doy"].values + 3.5
        rows.append(pd.DataFrame({"year": y, "doy": s["doy"].values, "t": t, "SIF": s[sif_col].values,
                                  "NDVI": np.interp(t, v["mean_obs_doy"], v["mean_ndvi"], left=np.nan, right=np.nan)}))
    return pd.concat(rows)


def analyse(sif_reg, sif_dis, vi_reg, vi_dis, years, sif_col, label):
    region_z, drought_d = rainfall_classes(years)
    drought = {y for y in years if region_z.loc[y] < -0.5}
    normals = [y for y in years if y not in drought]
    print(f"\n=== {label}: {len(years)} years, drought years (CHIRPS z < -0.5): {sorted(drought)}")
    print("    rainfall z: " + ", ".join(f"{y} {region_z.loc[y]:+.2f}" for y in years))

    # --- H4, region
    rt = regional_table(sif_reg, vi_reg, sif_col)
    tabs = {v: rt.pivot(index="year", columns="doy", values=v) for v in ["SIF", "NDVI"]}
    doys = tabs["SIF"].columns.values
    reg_rows = []
    for y in years:
        r = {"year": y, "is_drought": y in drought, "rain_z": region_z.loc[y]}
        for v in ["SIF", "NDVI"]:
            z = anomaly(tabs[v], y, normals)
            for thr in THRESHOLDS:
                r[f"{v}_alarm_{thr}"] = first_alarm(doys, z, thr)
        reg_rows.append(r)
    R = pd.DataFrame(reg_rows)
    print("\n  REGION, drought alarms (day of year of the composite centre; '-' = none):")
    for thr in THRESHOLDS:
        d, n = R[R.is_drought], R[~R.is_drought]
        s_first = ((d[f"SIF_alarm_{thr}"] < d[f"NDVI_alarm_{thr}"]) |
                   (d[f"SIF_alarm_{thr}"].notna() & d[f"NDVI_alarm_{thr}"].isna())).sum()
        n_first = ((d[f"NDVI_alarm_{thr}"] < d[f"SIF_alarm_{thr}"]) |
                   (d[f"NDVI_alarm_{thr}"].notna() & d[f"SIF_alarm_{thr}"].isna())).sum()
        same = (d[f"SIF_alarm_{thr}"] == d[f"NDVI_alarm_{thr}"]).sum()
        print(f"    z < {thr:<5} drought flagged SIF {d[f'SIF_alarm_{thr}'].notna().sum()}/{len(d)}, "
              f"NDVI {d[f'NDVI_alarm_{thr}'].notna().sum()}/{len(d)} | first: SIF {s_first}, same {same}, "
              f"NDVI {n_first} | false alarms SIF {n[f'SIF_alarm_{thr}'].notna().sum()}/{len(n)}, "
              f"NDVI {n[f'NDVI_alarm_{thr}'].notna().sum()}/{len(n)}")
    for _, r in R[R.is_drought].iterrows():
        print(f"    {int(r.year)}: SIF {r[f'SIF_alarm_{MAIN_THR}']}, NDVI {r[f'NDVI_alarm_{MAIN_THR}']}")

    # --- H4, districts (each district's own rainfall baseline)
    drows = []
    for (d, y), g in sif_dis.groupby(["district", "year"]):
        g = g.sort_values("doy")
        n = vi_dis[(vi_dis["district"] == d) & (vi_dis["year"] == y)].dropna(
            subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
        nd = np.interp(g["doy"].values + 3.5, n["mean_obs_doy"], n["mean_ndvi"], left=np.nan, right=np.nan)
        drows += [{"district": d, "year": y, "doy": a, "SIF": b, "NDVI": c} for a, b, c in zip(g["doy"], g["mean_sif"], nd)]
    dist = pd.DataFrame(drows)
    dtabs = {v: dist.pivot_table(index=["district", "year"], columns="doy", values=v) for v in ["SIF", "NDVI"]}
    ddoys = dtabs["SIF"].columns.values
    D = []
    for (d, y) in dtabs["SIF"].index:
        nrm = [yy for yy in years if (d, yy) not in drought_d]
        r = {"district": d, "year": y, "is_drought": (d, y) in drought_d}
        for v in ["SIF", "NDVI"]:
            z = anomaly(dtabs[v].loc[d], y, nrm)
            for thr in THRESHOLDS:
                r[f"{v}_alarm_{thr}"] = first_alarm(ddoys, z, thr)
        D.append(r)
    D = pd.DataFrame(D)
    print(f"\n  DISTRICTS (own rainfall baseline): {int(D.is_drought.sum())} drought, {int((~D.is_drought).sum())} normal district-years")
    dsum = []
    for thr in THRESHOLDS:
        dd, nn = D[D.is_drought], D[~D.is_drought]
        both = dd.dropna(subset=[f"SIF_alarm_{thr}", f"NDVI_alarm_{thr}"])
        lead = both[f"NDVI_alarm_{thr}"] - both[f"SIF_alarm_{thr}"]
        rec = {"period": label, "threshold": thr, "n_drought": len(dd), "n_normal": len(nn),
               "hit_SIF": int(dd[f"SIF_alarm_{thr}"].notna().sum()), "hit_NDVI": int(dd[f"NDVI_alarm_{thr}"].notna().sum()),
               "false_SIF": int(nn[f"SIF_alarm_{thr}"].notna().sum()), "false_NDVI": int(nn[f"NDVI_alarm_{thr}"].notna().sum()),
               "both_flagged": len(both), "SIF_earlier": int((lead > 0).sum()), "same": int((lead == 0).sum()),
               "NDVI_earlier": int((lead < 0).sum())}
        dsum.append(rec)
        print(f"    z < {thr:<5} flagged SIF {rec['hit_SIF']}, NDVI {rec['hit_NDVI']} of {len(dd)} | false alarms SIF "
              f"{rec['false_SIF']}, NDVI {rec['false_NDVI']} of {len(nn)} | both {len(both)}: SIF earlier "
              f"{rec['SIF_earlier']}, same {rec['same']}, NDVI earlier {rec['NDVI_earlier']}")

    # --- seasonal lags, region
    lrows = []
    for y in years:
        s = rt[rt["year"] == y].sort_values("t")
        v = vi_reg[vi_reg["year"] == y].dropna(subset=["mean_ndvi", "mean_obs_doy"]).sort_values("mean_obs_doy")
        ts, ss, tv = s["t"].values, s["SIF"].values, v["mean_obs_doy"].values
        rec = {"year": y, "is_drought": y in drought}
        for how in ["season", "decline"]:
            rec[f"SIF_vs_NDVI_{how}"] = lag(ts, ss, tv, v["mean_ndvi"].values, how)
            if "mean_nirv" in v:
                rec[f"SIF_vs_NIRv_{how}"] = lag(ts, ss, tv, v["mean_nirv"].values, how)
                rec[f"NIRv_vs_NDVI_{how}"] = lag(tv, v["mean_nirv"].values, tv, v["mean_ndvi"].values, how)
        lrows.append(rec)
    L = pd.DataFrame(lrows)
    print("\n  REGION, seasonal lag in days (> 0 = first-named series declines first):")
    print(L.round(1).to_string(index=False))
    for c in [c for c in L.columns if "_vs_" in c]:
        print(f"    {c:22s} first in {(L[c] > 0).sum()}/{L[c].notna().sum()} years, mean {L[c].mean():+.1f} d"
              f" (drought {L.loc[L.is_drought, c].mean():+.1f}, normal {L.loc[~L.is_drought, c].mean():+.1f})")
    return R, pd.DataFrame(dsum), L, D


def main():
    check = "--check" in sys.argv
    if check:
        years = list(range(2015, 2024))
        sif_reg = pd.read_csv(f"{OUT}/marathwada_sif_timeseries.csv")
        sif_dis = pd.read_csv(f"{OUT}/sif_timeseries_by_district.csv")
        vi_reg = pd.read_csv("data/raw/vi_obsdate_2015_2023.csv")
        vi_dis = pd.read_csv("data/raw/vi_obsdate_by_district_2015_2023.csv")
        vi_dis["district"] = vi_dis["district"].str.strip()
        R, Ds, L, _ = analyse(sif_reg, sif_dis, vi_reg, vi_dis, years, "mean_sif_crop1214", "CHECK 2015-2023")
        main_r = pd.read_csv(f"{OUT}/drought_signal_region.csv").set_index("year")
        main_l = pd.read_csv(f"{OUT}/normalisation_sensitivity_region.csv").set_index("year")
        dr = max(np.nanmax(np.abs(R.set_index("year")[c] - main_r[c])) for c in R.columns if "_alarm_" in c)
        dl = np.nanmax(np.abs(L.set_index("year")["SIF_vs_NDVI_season"] - main_l["lag_season"]))
        dd = np.nanmax(np.abs(L.set_index("year")["SIF_vs_NDVI_decline"] - main_l["lag_decline"]))
        print(f"\nCHECK against the main pipeline: max |alarm difference| {dr:.4f} d, "
              f"max |season lag difference| {dl:.4f} d, max |decline lag difference| {dd:.4f} d")
        return

    years = list(range(FIRST, LAST + 1))
    missing = [p for p in [VI_REGION, VI_DISTRICT] if not os.path.exists(p)]
    missing += [f"cropland_fraction_{y}.tif" for y in years
                if not os.path.exists(f"data/external/cropland_fraction/cropland_fraction_{y}.tif")]
    if missing:
        print(f"Inputs missing, skipping the out-of-sample test: {missing[:5]}")
        sys.exit(0)

    if not (os.path.exists(SIF_REGION) and os.path.exists(SIF_DISTRICT)):
        print("Extracting SIF; first re-extracting 2015 to check against the main pipeline ...")
        r15, d15 = extract_sif([2015])
        main_r = pd.read_csv(f"{OUT}/marathwada_sif_timeseries.csv")
        main_d = pd.read_csv(f"{OUT}/sif_timeseries_by_district.csv")
        a = r15.merge(main_r[main_r.year == 2015][["year", "doy", "mean_sif_crop1214"]], on=["year", "doy"], suffixes=("", "_main"))
        b = d15.merge(main_d[main_d.year == 2015], on=["year", "doy", "district"], suffixes=("", "_main"))
        ea = (a["mean_sif_crop1214"] - a["mean_sif_crop1214_main"]).abs().max()
        eb = (b["mean_sif"] - b["mean_sif_main"]).abs().max()
        print(f"  2015 check: max |difference| region {ea:.2e}, districts {eb:.2e} "
              f"({len(a)} and {len(b)} values compared)")
        if not (len(a) == len(DOYS) and ea < 1e-9 and eb < 1e-9):
            raise SystemExit("The re-extracted 2015 SIF does not match the main pipeline; stopping.")
        sif_reg, sif_dis = extract_sif(years)
        sif_reg.to_csv(SIF_REGION, index=False)
        sif_dis.to_csv(SIF_DISTRICT, index=False)
    sif_reg, sif_dis = pd.read_csv(SIF_REGION), pd.read_csv(SIF_DISTRICT)
    vi_reg, vi_dis = pd.read_csv(VI_REGION), pd.read_csv(VI_DISTRICT)
    vi_dis["district"] = vi_dis["district"].str.strip()

    R, Ds, L, D = analyse(sif_reg, sif_dis, vi_reg, vi_dis, years, "mean_sif_crop1214", f"OUT-OF-SAMPLE {FIRST}-{LAST}")
    R.to_csv(f"{OUT}/oos_drought_signal_region.csv", index=False)
    D.to_csv(f"{OUT}/oos_drought_signal_district.csv", index=False)
    Ds.to_csv(f"{OUT}/oos_drought_signal_district_summary.csv", index=False)
    L.to_csv(f"{OUT}/oos_seasonal_lag_region.csv", index=False)
    print(f"\nSaved {OUT}/oos_*.csv")


if __name__ == "__main__":
    main()
