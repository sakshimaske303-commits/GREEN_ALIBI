# GREEN ALIBI: Testing the Fluorescence Advantage

**Does Solar-Induced Fluorescence signal agricultural drought earlier than NDVI in Marathwada, India? A test across 8 districts and 9 Kharif seasons (2015–2023).**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21762501.svg)](https://doi.org/10.5281/zenodo.21762501)

## Live Dashboard

**[View the interactive dashboard →](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`GA_Executive_Summary.md`](./GA_Executive_Summary.md) | Short snapshot: project overview, questions, method, headline findings, robustness checklist, and links (start here) |
| [`Policy_Brief.md`](./Policy_Brief.md) | Non technical brief for a policy audience: the drought declaration/PMFBY problem, what was found, and the policy implication |
| [`GA_Research_Paper.md`](./GA_Research_Paper.md) | Formal academic paper: physical basis, methodology, results, discussion, limitations |
| [`GA_Development_Log.md`](./GA_Development_Log.md) | Full technical development log: every bug, boundary correction, and methodology iteration |

## Interactive Maps & Plots

Interactive district level maps and headline charts are hosted via GitHub Pages:

**Maps**
- [SIF by District](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/maps/marathwada_sif_by_district.html)
- [Rainfall Anomaly by District](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/maps/marathwada_rainfall_by_district.html)

**Plots**
- [Seasonal SIF vs. NDVI Trajectories](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/plots/seasonal_trajectories.html)
- [SIF to NDVI Lag by Threshold](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/plots/lag_by_threshold.html)
- [Bootstrap Confidence Intervals on Lag](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/plots/bootstrap_lag_ci.html)

*(All 5 are also embedded together on the dedicated Interactive Maps & Plots page in the live dashboard; the 2 maps also show up on their own on the Spatial SIF Analysis and Rainfall Validation pages.)*

India's drought-management process, and the crop-insurance payouts under the Pradhan Mantri Fasal Bima Yojana (PMFBY) tied to it, rest on rainfall deficits and on vegetation indices such as NDVI, which respond once crop damage is visible. Solar-Induced Fluorescence (SIF) is tied to photosynthesis, so it is often expected to respond earlier. GREEN ALIBI is my test of that expectation for the eight districts of Marathwada, Maharashtra. I compare cropland-weighted GOSIF v2 SIF with MODIS NDVI timed to each pixel's observation date, check the result with TROPOMI SIF (a retrieval not built from MODIS reflectance), and keep two questions apart. The main one is whether SIF shows a drought-specific anomaly before NDVI does, which is what would make SIF a better drought alarm; the secondary one is whether SIF's normal seasonal decline starts before NDVI's. Only 2015 and 2018 qualify as drought years on CHIRPS rainfall, so I also ran every test, unchanged, on 2001–2014 (five more drought years) as an out-of-sample check.

The hypotheses the data do not support are reported alongside the rest (H4: SIF departs from normal before NDVI in drought years; H2: the lag differs between districts; H3: drought widens the lag).

---

## What This Project Does

- Builds the Marathwada study region from FAO GAUL 2015 district polygons (not a bounding box) and checks the clipping with a boundary overlay.
- Weights each GOSIF v2 cell by its cropland fraction (MODIS MCD12Q1 classes 12 and 14), and pulls quality- and cropland-masked MODIS MOD13Q1 NDVI in Google Earth Engine, dating each composite by its pixels' actual observation day.
- Measures the SIF-to-NDVI decline lag at 5 thresholds by threshold-crossing, with each curve scaled over the whole season and over its own decline, plus a double-logistic fit and cross-correlation over the post-peak decline, with bootstrap intervals, for the region and all 72 district-years.
- Tests how much the lag depends on analysis choices across 40 method variants, and checks the direction with TROPOMI SIF for 2018–2020, against NDVI, EVI and NIRv.
- Classifies drought years from CHIRPS seasonal rainfall (1981–2023, baseline 2001–2020), checked against three alternative baselines and a range of cut-offs.
- Tests for a drought-specific signal by standardising SIF and NDVI against normal years and comparing alarm dates and ROC AUC, with NDVI both interpolated onto the SIF dates and taken as observed.
- Repeats the drought-alarm and seasonal-lag tests on 2001–2014 with every method frozen, as an out-of-sample test.
- Times satellite alarms against an approximation of the rainfall-based Trigger-1 in India's Manual for Drought Management and against the official 2015 and 2018 drought declarations.
- Checks district-level SIF against rainfall anomaly (with year-clustered and fixed-effects tests), spatial autocorrelation (Moran's I), and official district crop-yield statistics.
- Presents everything in a multi-page Streamlit dashboard, including pages on the physics of fluorescence and reflectance.

## Key Findings

**SIF is not a resolvably earlier drought alarm than NDVI (H4 not supported).** Standardised against normal years, at z < −3 (the only threshold with no regional false alarm), both indices flagged 2015 on 24 August; in 2018 NDVI flagged on 25 September and SIF on 3 October, one composite later. Across the 15 drought district-years (each district against its own rainfall baseline), SIF flagged 12 and NDVI 13; where both did, SIF was earlier in 7, they coincided in 2 and NDVI was earlier in 3, in 11 of 12 cases by at most one composite. At looser thresholds NDVI was earlier more often. These one-composite differences are below NDVI's 16-day sampling and flip with how NDVI is dated (taking NDVI as observed rather than interpolated, SIF is first in both regional drought years and in 8 of 12 district-years). SIF had slightly fewer false alarms (2 vs 4 in 57 normal district-years).

**Out of sample, 2001–2014 (methods unchanged).** Across the 40 drought district-years, where both indices flagged one at z < −1.5, SIF was earlier in 5 of 22, NDVI in 6, and 11 coincided; at z < −2, 0, 6 and 7 of 13. Regionally the anomalies were weaker and leaned slightly towards SIF: at z < −3 SIF flagged 2001 and 2002, NDVI only 2002 (same date). The seasonal lead again matched NIRv's (season-scaled, SIF +27.4 and NIRv +26.6 days over NDVI, 14 of 14 years each) and was not larger in drought years.

**SIF's seasonal lead is mostly a normalisation effect.** Scaled over the whole season, SIF's decline came first in all 9 years (8.0–34.2 days) and all 72 district-years (median 17.7 days). But after the monsoon NDVI stays well above its pre-season level while SIF does not, which delays NDVI's threshold crossings by construction. Scaled from peak to post-peak minimum, the lag is 9.6, 13.4, 10.6, 3.5, −5.5, 8.8, −1.2, −1.0 and 0.4 days (2015–2023): SIF first in 6 years, NDVI first in 2019, 2021 and 2022. Cross-correlation, which does not depend on scaling (10, 12, 14, 4, 0, 9, 20, −1, −3 days), agrees more with the smaller estimate. MODIS NIRv and EVI, from the same composites, also lead NDVI by as much as GOSIF does (NIRv: 9/9 years, +22.8 days season-scaled, +9.9 decline-scaled), and GOSIF does not lead NIRv (decline-scaled, first in 0 of 9 years), so for GOSIF the remaining lead is a property of NDVI. That is partly expected, since GOSIF is predicted from MODIS reflectance. TROPOMI SIF (2018–2020), which is not, put SIF first against NDVI under both scalings and also declined before NIRv in all three years (by 1–13 days), which leaves a small fluorescence-specific lead open.

**No district differences once scaling is matched (H2 not supported).** Season-scaled, the district effect is significant (Friedman p = 0.043); decline-scaled it vanishes (p = 0.97; district means 2.9–5.6 days).

**Drought does not widen the lag (H3 not supported).** Season-scaled, drought years averaged 14.8 days against 22.6; decline-scaled, 6.5 against 3.6. With two drought years neither difference is meaningful; in 2001–2014, with five, the lead was again not larger in drought (+28.3 vs +26.9 days season-scaled).

**Rainfall trigger and declarations (RQ3).** The approximate rainfall Trigger-1 (dry spells counted 1 July – 30 September) never fired for the region and fired in 2 of 15 drought district-years (Aurangabad and Bid, 2018); in Aurangabad both satellite alarms came 15.5 days first; in Bid SIF came 0.5 days and NDVI 8.5 days after it. Evaluated per CHIRPS pixel, it reached 25% of a district's area only in Aurangabad and Bid 2018 and Bid 2017 (a normal year), and in 2015 it fired in at most 7% of any district. Both alarms preceded the 2015 declaration by 52.5 days and the 2018 final declaration by 27.5 (SIF) and 35.5 (NDVI) days, but declarations follow field verification, so satellite signals precede them almost by construction.

**Supporting checks.** District SIF on day-of-year 273 correlates with rainfall anomaly (r = 0.53, p < 0.0001; year-clustered p = 0.001), but not once district and year fixed effects are included (p = 0.37). Rainfall and season-mean SIF are spatially clustered in all 9 years. The crop Yield Anomaly Index tracks rainfall (r = 0.93) and is lower in the drought years (−1.08 vs +0.07, p = 0.15). The lag direction is unchanged when NDVI composites with under 25% clear pixels are excluded (at a 50% cut-off, 2022 reverses).

In short: SIF is not a resolvably earlier drought alarm than NDVI in this dataset, and GOSIF's apparent seasonal head start is largely a property of how NDVI's decline is measured. Satellite vegetation anomalies, NDVI as much as SIF, may add lead time to a rainfall-led trigger. Full methodology, physical basis, and limitations are in `GA_Research_Paper.md`; `GA_Development_Log.md` records every correction and revision.

## Repository Structure

```text
GREEN_ALIBI/
├── run_all.py                          # Runs the full pipeline in order
├── app.py                              # Streamlit dashboard home page
├── pages/                              # 12 page dashboard (chronological order)
│   ├── 01_Study_Area.py
│   ├── 02_Fluorescence_Physics.py
│   ├── 03_NDVI_Physics.py
│   ├── 04_Data_and_Methodology.py
│   ├── 05_Seasonal_Trajectories.py
│   ├── 06_Lag_Analysis.py
│   ├── 07_Spatial_SIF_Analysis.py
│   ├── 08_Rainfall_Validation.py
│   ├── 09_Combined_Comparison.py
│   ├── 09_Interactive_Maps.py
│   ├── 10_Crop_Yield_Validation.py
│   └── 11_Findings_and_Conclusion.py
├── utils/
│   ├── doc_viewer.py
│   └── style.py                        # Shared dashboard theme (navy/magenta/pink/teal)
├── src/
│   ├── acquisition/                    # Earth Engine exports (cropland fraction, NDVI observation dates, CHIRPS) and GOSIF download
│   ├── analysis/                       # All analysis scripts (listed below)
│   └── visualization/                  # Static maps, Folium maps, Plotly charts
├── data/
│   ├── raw/                             # GOSIF, NDVI, rainfall, boundary data
│   ├── external/                        # Cropland fraction rasters, crop-yield statistics, official drought declaration dates
│   └── processed/                       # Regional and district SIF, NDVI, rainfall, lag, and diagnostic CSVs
├── outputs/
│   ├── figures/                          # All static figures (spatial maps, charts, physics diagrams)
│   └── interactive_maps/
│       ├── maps/                          # Folium HTML maps (SIF + rainfall by district)
│       └── plots/                         # Plotly HTML charts (seasonal trajectories, lag analysis)
├── GA_Research_Paper.md                 # Formal academic research paper
├── GA_Development_Log.md                # Full technical development log
└── requirements.txt
```

### Analysis scripts (`src/analysis/`)

| Script | What it does |
|---|---|
| `clip_gosif.py` | Clips GOSIF files to Marathwada |
| `aggregate_sif.py` | Cropland-weighted regional mean SIF per 8-day composite |
| `zonal_stats_sif.py` | District zonal statistics for SIF |
| `district_seasonal_sif.py` | District seasonal SIF series |
| `compare_sif_ndvi.py` | SIF vs NDVI seasonal comparison (NDVI at observation date) |
| `lag_analysis.py` | Threshold-crossing lag, per year |
| `cross_correlation_lag.py` | Cross-correlation lag (searches both directions) |
| `bootstrap_lag_uncertainty.py` | Bootstrap intervals for the cross-correlation lag |
| `lag_uncertainty_check.py` | Residual bootstrap and jackknife for the threshold-crossing lag |
| `final_summary.py` | Final summary table |
| `h3_continuous_severity.py` | H3 as a continuous rainfall-severity test |
| `district_lag_analysis.py` | District-level lag and H2 tests (ANOVA, Friedman) |
| `drought_signal_analysis.py` | Drought-specific anomaly signal: SIF vs NDVI alarm dates and AUC (H4) |
| `alarm_dating_sensitivity.py` | H4 alarm comparison with NDVI interpolated vs taken as observed, both periods, with a one-composite tolerance |
| `rainfall_trigger_comparison.py` | Satellite alarms vs approximate rainfall Trigger-1 (RQ3) |
| `rq3_official_declaration_comparison.py` | Satellite alarms vs official 2015 and 2018 declarations (RQ3) |
| `method_dependence.py` | 40 method variants: which findings depend on which choices |
| `tropomi_sif_analysis.py` | TROPOMI SIF cross-check (regional) |
| `tropomi_sif_crosscheck.py` | TROPOMI SIF cross-check (district level) |
| `rainfall_analysis.py` | Regional seasonal rainfall anomaly (CHIRPS) |
| `rainfall_by_district_analysis.py` | District seasonal rainfall anomaly |
| `district_climatology_anomaly.py` | District rainfall climatology and own-baseline anomalies |
| `baseline_sensitivity.py` | Drought classification under alternative baselines and cut-offs |
| `rain_timing_analysis.py` | Within-season rainfall timing vs lag |
| `sif_rainfall_correlation.py` | District SIF–rainfall correlation (clustered and fixed-effects) |
| `spatial_autocorrelation.py` | Moran's I for SIF and rainfall |
| `sensitivity_checks.py` | Robustness checks |
| `cropmask_obsdate_sensitivity.py` | Cropland-weighting and NDVI observation-date sensitivity |
| `gosif_grid_shift_check.py` | GOSIF grid-origin check for 2021–2022 |
| `crop_yield_validation.py` | Crop Yield Anomaly Index vs rainfall and SIF |
| `crop_yield_sensitivity.py` | Crop-yield check under weighting and cleaning variants |
| `check_boundary_overlay.py` | Boundary overlay figure |
| `normalisation_sensitivity.py` | Lag under season-range vs decline-range scaling and a double-logistic fit (region, districts, TROPOMI) |
| `rainfall_window_sensitivity.py` | Drought classification by Jun–Dec, Jun–Sep and single-month rainfall |
| `ndvi_coverage_check.py` | NDVI quality-pixel coverage per composite and lag with low-coverage composites dropped |
| `tropomi_drought_signal.py` | H4 anomaly test with TROPOMI SIF (illustrative until more TROPOMI years are added) |
| `tropomi_vs_reflectance.py` | TROPOMI SIF seasonal lag against MODIS NDVI, EVI and NIRv, 2018–2020 |
| `vegetation_index_lag.py` | SIF vs NDVI, EVI and NIRv lags (needs `gee_vi_obsdate.py` output) |
| `out_of_sample_2001_2014.py` | Out-of-sample test on 2001–2014 with all 2015–2023 methods frozen (`--check` reruns it on 2015–2023). The extracted 2001–2014 SIF series are kept in `data/processed/oos_sif_*.csv`, so the test reruns without the GOSIF download |
| `rainfall_trigger_pixel.py` | Trigger-1 per CHIRPS pixel, summarised by district (needs `gee_chirps_dryspell_area.py` output) |

## Tech Stack

Python · Rasterio · GeoPandas · NumPy / Pandas · SciPy · statsmodels · libpysal / esda · Matplotlib · Plotly · Folium · Branca · Streamlit · Google Earth Engine

## Data Sources

| Dataset | Provider |
|---|---|
| Solar-Induced Fluorescence (main) | GOSIF v2 (Global Ecology Group, University of New Hampshire) |
| Solar-Induced Fluorescence (independent check) | TROPOSIF v2.1, Sentinel-5P TROPOMI (SRON) |
| NDVI | MODIS MOD13Q1, including its DayOfYear band (via Google Earth Engine) |
| Land Cover / Cropland Mask | MODIS MCD12Q1, IGBP classification (via Google Earth Engine) |
| Precipitation | CHIRPS Daily (UCSB-CHG, via Google Earth Engine) |
| Administrative Boundaries | FAO GAUL 2015, Level 2 (via Google Earth Engine) |
| Crop yields | Ministry of Agriculture & Farmers Welfare, district Area/Production/Yield (India Data Portal) |

## Running Locally

To view the dashboard:

```bash
git clone https://github.com/sakshimaske303-commits/GREEN_ALIBI.git
cd GREEN_ALIBI
pip install -r requirements.txt
streamlit run app.py
```

To rerun the analysis, the whole pipeline runs from one script. The first step clips the raw GOSIF files, which are not in the repository (several GB); download them once with `python src/acquisition/download_gosif_new_years.py 2015 2023` before the first run:

```bash
python run_all.py                    # all analysis scripts, then all figures
python run_all.py --acquire          # rerun the Earth Engine exports first (needs an authenticated Earth Engine account)
python run_all.py --from lag_analysis   # restart from the first script whose name contains this text
python run_all.py --no-figures       # analysis only, skip figures and maps
```

`run_all.py` checks that the required raw inputs exist before starting, stops at the first failing script, and writes a full log to `outputs/run_log.txt`. `tropomi_sif_analysis.py` re-extracts the TROPOSIF soundings only if the raw files are present and otherwise analyses the saved composites; `tropomi_sif_crosscheck.py` (district level) is run separately because it downloads the soundings. Exact package versions from the last full run are in `requirements-lock.txt`.

### Optional extensions (need Earth Engine or a download)

```bash
python src/acquisition/gee_vi_obsdate.py                 # NDVI, EVI and NIRv at observation date -> vegetation_index_lag.py
# (both Earth Engine exports also have Code Editor versions: src/acquisition/*_CODE_EDITOR.js)
python src/acquisition/gee_chirps_dryspell_area.py       # Trigger-1 per CHIRPS pixel -> rainfall_trigger_pixel.py
python src/acquisition/gee_india_states_for_locator.py   # state outlines for the Figure 3 locator inset
python src/acquisition/download_gosif_new_years.py 2001 2014   # earlier GOSIF years (several GB)
```

The scripts that use these outputs skip quietly until the files exist. The raw GOSIF archives and decompressed GeoTIFFs take several GB; only the clipped files are needed after `clip_gosif.py` has run.

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

ORCID: [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

## License

It's licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for citation metadata.

---

*The full development process, including every boundary correction, debugging session, and methodology iteration, is written up in `GA_Development_Log.md` so the whole thing can be checked and rebuilt from scratch.*
