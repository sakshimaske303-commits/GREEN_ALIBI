# H4 with a direct SIF retrieval: does TROPOMI SIF leave its normal-year range before NDVI?
#
# drought_signal_analysis.py tests H4 with GOSIF, which is predicted from MODIS EVI and
# reanalysis weather and so cannot carry a fluorescence signal independent of greenness.
# This repeats the same anomaly-alarm logic with TROPOMI (TROPOSIF) 8-day composites for
# whatever years are available in data/processed/tropomi_8day_composites.csv.
#
# With only 2018-2020 the normal-year reference is two years (2019, 2020), so the z-scores
# are not meaningful yet; the script prints a warning until at least four normal years are
# present. Extend the TROPOMI years (tropomi_sif_crosscheck.py / tropomi_sif_analysis.py)
# before interpreting the output.

import numpy as np
import pandas as pd

THRESHOLDS = [-1.0, -1.5, -2.0, -3.0]
START_DOY = 182
MIN_NORMAL_YEARS = 4

rain = pd.read_csv("data/processed/rainfall_anomaly_summary.csv")
DROUGHT = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])
tc = pd.read_csv("data/processed/tropomi_8day_composites.csv")
tc = tc[tc["variant"].str.startswith("main")]
trop = tc.pivot(index="year", columns="start", values="tropomi_sif")
m = pd.read_csv("data/processed/marathwada_sif_ndvi_merged.csv")
ndvi = m.pivot(index="year", columns="sif_start_doy", values="mean_ndvi").loc[trop.index, trop.columns]
gosif = m.pivot(index="year", columns="sif_start_doy", values="mean_sif").loc[trop.index, trop.columns]
DOYS = trop.columns.values
years = list(trop.index)
normals = [y for y in years if y not in DROUGHT]

if len(normals) < MIN_NORMAL_YEARS:
    print(f"WARNING: only {len(normals)} normal year(s) with TROPOMI data ({normals}); the anomaly reference "
          f"needs at least {MIN_NORMAL_YEARS}. Results below are illustrative only.\n")


def first_alarm(z, thr):
    for i in range(len(DOYS) - 1):
        if DOYS[i] >= START_DOY and z[i] < thr and z[i + 1] < thr:
            return DOYS[i] + 3.5
    return np.nan


rows = []
for y in years:
    ref = [r for r in normals if r != y]
    if len(ref) < 2:
        continue
    rec = {"year": y, "is_drought": y in DROUGHT, "n_reference_years": len(ref)}
    for name, tab in [("TROPOMI", trop), ("GOSIF", gosif), ("NDVI", ndvi)]:
        z = ((tab.loc[y] - tab.loc[ref].mean()) / tab.loc[ref].std(ddof=1)).values
        for thr in THRESHOLDS:
            rec[f"{name}_alarm_{thr}"] = first_alarm(z, thr)
    rows.append(rec)
R = pd.DataFrame(rows)
R.to_csv("data/processed/tropomi_drought_signal.csv", index=False)
print(R.to_string(index=False))
print("\nSaved data/processed/tropomi_drought_signal.csv")
