# GREEN ALIBI — Testing the Fluorescence Advantage

**Testing whether Solar-Induced Fluorescence catches agricultural drought stress in Marathwada, Maharashtra before NDVI can — and whether drought severity actually makes that head-start bigger — across eight growing seasons.**

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint-B7410E.svg)](https://eartharxiv.org/repository/view/14813/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21762501.svg)](https://doi.org/10.5281/zenodo.21762501)

## Live Dashboard

**[View the interactive dashboard →](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`GA_Executive_Summary.md`](./GA_Executive_Summary.md) / [`.pdf`](./GA_Executive_Summary.pdf) | One-page snapshot — project overview, question, method, headline finding, robustness checklist, and links (start here) |
| [`Policy_Brief.pdf`](./Policy_Brief.pdf) | Non-technical brief for a policy audience — the drought-declaration/PMFBY problem, what was found, and the policy implication |
| [`GA_Research_Paper.md`](./GA_Research_Paper.md) | Formal academic paper — physical basis, methodology, results, discussion, limitations |
| [`GA_Development_Log.md`](./GA_Development_Log.md) | Full technical development log — every bug, boundary correction, and methodology iteration |

## Interactive Maps & Plots

Interactive district-level maps and headline charts are hosted via GitHub Pages:

**Maps**
- [SIF by District](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/maps/marathwada_sif_by_district.html)
- [Rainfall Anomaly by District](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/maps/marathwada_rainfall_by_district.html)

**Plots**
- [Seasonal SIF vs. NDVI Trajectories](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/plots/seasonal_trajectories.html)
- [SIF-to-NDVI Lag by Threshold](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/plots/lag_by_threshold.html)
- [Bootstrap Confidence Intervals on Lag](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/plots/bootstrap_lag_ci.html)

*(All five are also embedded together on the dedicated Interactive Maps & Plots page in the live dashboard; the two maps are additionally embedded individually on the Spatial SIF Analysis and Rainfall Validation pages.)*

GREEN ALIBI is a geospatial test of whether there's a measurable difference in how timely India's official drought designation is compared to signals captured from space, such as Solar-Induced Fluorescence (SIF), an indicator of photosynthetic activity — and how those signals stack up against the drought designation that crop-insurance payouts under the Pradhan Mantri Fasal Bima Yojana (PMFBY) currently depend on. SIF is grounded in the plant's internal process of energy-partitioning for photosynthesis, which gives it a theoretical head start over NDVI: NDVI only registers a change once the plant's structure has already begun to visibly deteriorate, whereas SIF tracks the drop in photosynthetic efficiency directly. The premise is tested directly in this project with GOSIF v2 fluorescence data and MODIS NDVI, arranged by growing season, where only the 2015 and 2018 growing seasons are classified as drought years based on CHIRPS rainfall data independently. Originally this study was to span 3 years (2015, 2018, 2020); 5 additional years were added after an earlier pass of this project's documentation identified sample size as a limiting factor.

No compromises: all results are presented as obtained, including one hypothesis in this report (H3: drought severity amplifies the SIF–NDVI lag) that the data doesn't support.

---

## What This Project Does

- Separately determines the study region for Marathwada, using precise district-level boundaries (not a rectangular bounding box) from FAO GAUL 2015, with a diagnostic boundary-overlay process.
- Creates a GOSIF v2 SIF raster matched to exact district polygons, and extracts MODIS NDVI for the same clipped, cropland-masked, cloud-screened polygons using Google Earth Engine.
- Calculates a quantitative SIF-to-NDVI decline lag (in days) at 5 seasonal decline thresholds every year, using a linear-interpolation crossing-date estimation approach, and compares that against a time-lagged cross-correlation approach — both with bootstrap confidence intervals characterising the precision of the lag estimates.
- Independently validates the drought/normal year classification against 20 years of CHIRPS rainfall data (2001-2020) at both the regional and district level.
- Tests spatial correlation between SIF stress and rainfall deficit at the district level using Pearson/Spearman correlation, not just visual inspection.
- Checks the accuracy of SIF- and NDVI-based stress-onset timing against the one officially declared drought date available (Maharashtra, 2018), to validate the study's policy motivation independently of rainfall-deficit data.
- Presents all results on an 11-page Streamlit dashboard, including two pages explaining the physics of photosynthesis and reflectance, and a page bringing together both interactive maps.

## Key Findings

SIF's post-peak drop preceded NDVI's post-peak drop in seven of the eight years (2015, 2016, 2017, 2019, 2020, 2022, 2023) under the threshold-crossing method — consistent with its physical basis as a more immediate stress signal. A second, methodologically distinct cross-correlation check gives a more mixed picture, and only does so honestly because of a bug fix: the cross-correlation and bootstrap scripts originally searched only non-negative lags, making it impossible for either to ever report NDVI leading SIF regardless of the data. Fixed and rerun, cross-correlation shows SIF clearly leading in 4 years, a tie in 1 (2020), and NDVI clearly leading in 3 (2018, 2022, 2023) — 2 of those (2022, 2023) backed by a bootstrap where 99%+ of replicates land below zero. Every method agrees 2018 breaks the SIF-leads pattern: a marginally negative threshold-crossing lag, a clearly negative cross-correlation lag (−4 days), and 87.4% of bootstrap replicates landing below zero.

Validating against the same 20-year CHIRPS baseline (2001-2020) via rainfall-anomaly validation (§4.4), only two of the eight study years fall below the drought threshold — 2015 at −21.5% and 2018 at −18.3% — while the five years added during the sample expansion all sit within roughly one standard deviation of normal. In hindsight, the original three-year sample — two-thirds of which were drought years — was considerably more drought-heavy than Marathwada's actual eight-year climate record.

Similar to the original 3-year study, mean threshold-crossing lag was smaller in the two drought years (7.6 days) than in the six normal years (15.0 days) — this data does not support H3. The exact year-to-year ranking is itself sensitive to the method used, and for 2022/2023, so is the direction itself (see Research Paper §4.6); the bootstrap check (§4.7) finds 24 of the 28 pairwise comparisons among this sample's eight years aren't statistically distinguishable from noise, but the remaining 4 cleanly separate the strongest SIF-leads years from the strongest NDVI-leads years.

The drought years are well established from independent rainfall data, and the deficiency isn't uniformly distributed across the region either — regional anomalies range from −21.5% (2015) to +36.8% (2022) relative to the 20-year normal. The 2018 deficit was concentrated in the western districts (Aurangabad −37.3% and Bid −38.0%), while eastern districts experienced a surplus (Nanded +14.7%) — a west-to-east gradient reproduced independently at the district level. A Moran's I diagnostic (§4.8) reveals significant spatial clustering of rainfall in all 8 years, while SIF's own spatial clustering is significant in only 4 of 8 years.

The actual district-level correlation between rainfall and SIF is r = 0.567 (p < 0.0001) and Spearman ρ = 0.551 (p < 0.0001), across 64 district-years (8 districts × 8 years) — both substantially weaker than the original 3-year sample's r = 0.837 (p < 0.0001). This drop is reported precisely because it contradicts rather than confirms the original correlation: it's evidence that the original figure was inflated by that smaller sample's composition.

Both the SIF and NDVI thresholds are crossed roughly 7-8 weeks before the drought was officially declared by the Maharashtra government (31 October 2018), as the chart below shows. After fixing a district-naming bug found during the sample expansion (§3.2), NDVI actually crosses its threshold about five days before SIF in 2018 specifically — the reverse of the original finding, and consistent with 2018 being this study's one exception throughout (§4.9).

Full methodology, physical basis, and limitations are documented in `GA_Research_Paper.md`.

## Repository Structure

```text
GREEN_ALIBI/
├── app.py                              # Streamlit dashboard home page
├── pages/                              # 11-page dashboard (chronological order)
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
│   └── 10_Findings_and_Conclusion.py
├── utils/
│   └── style.py                        # Shared dashboard theme (navy/magenta/pink/teal)
├── src/
│   ├── acquisition/                    # GEE + GOSIF data-acquisition scripts (scripted and executed for all 8 study years)
│   ├── analysis/                       # Clipping, zonal stats, lag calc, rainfall, bootstrap CI, Moran's I, RQ3
│   └── visualization/                  # Static maps + Folium interactive maps
├── data/
│   ├── raw/                             # GOSIF, NDVI, rainfall, boundary data (gitignored)
│   ├── external/                        # Public-record reference data (official drought-declaration dates)
│   └── processed/                       # District-level SIF, rainfall, lag, and bootstrap/spatial-diagnostic CSVs
├── outputs/
│   ├── figures/                          # All static figures (spatial maps, charts, physics diagrams)
│   └── interactive_maps/
│       ├── maps/                          # Folium HTML maps (SIF + rainfall by district)
│       └── plots/                         # Plotly HTML charts (seasonal trajectories, lag analysis)
├── GA_Research_Paper.md                 # Formal academic research paper
├── GA_Development_Log.md                # Full technical development log
└── requirements.txt
```

## Tech Stack

Python · Rasterio · GeoPandas · NumPy / Pandas · Matplotlib · Folium · Branca · Streamlit · Google Earth Engine

## Data Sources

| Dataset | Provider |
|---|---|
| Solar-Induced Fluorescence | GOSIF v2 (Global Ecology Group, University of New Hampshire) |
| NDVI | MODIS MOD13Q1 (via Google Earth Engine) |
| Land Cover / Cropland Mask | MODIS MCD12Q1, IGBP classification (via Google Earth Engine) |
| Precipitation | CHIRPS Daily (UCSB-CHG, via Google Earth Engine) |
| Administrative Boundaries | FAO GAUL 2015, Level 2 (via Google Earth Engine) |

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/GREEN_ALIBI.git
cd GREEN_ALIBI
pip install -r requirements.txt
streamlit run app.py
```

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for citation metadata.

---

*This project's full development process — including every boundary correction, debugging session, and methodology iteration — is documented in `GA_Development_Log.md` for full transparency and reproducibility.*