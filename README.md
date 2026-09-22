# GREEN ALIBI: Testing the Fluorescence Advantage

**Testing whether Solar-Induced Fluorescence catches agricultural drought stress in Marathwada, Maharashtra before NDVI can, and whether drought severity makes that head start bigger, across 9 growing seasons.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21762501.svg)](https://doi.org/10.5281/zenodo.21762501)

## Live Dashboard

**[View the interactive dashboard →](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`GA_Executive_Summary.md`](./GA_Executive_Summary.md) / [`.pdf`](./GA_Executive_Summary.pdf) | 1 page snapshot: project overview, question, method, headline finding, robustness checklist, and links (start here) |
| [`Policy_Brief.pdf`](./Policy_Brief.pdf) | Non technical brief for a policy audience: the drought declaration/PMFBY problem, what was found, and the policy implication |
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

GREEN ALIBI is a geospatial test of whether there's a measurable difference in how timely India's official drought designation is compared to signals captured from space, such as Solar-Induced Fluorescence (SIF), an indicator of photosynthetic activity. It also checks how those signals stack up against the drought designation that crop insurance payouts under the Pradhan Mantri Fasal Bima Yojana (PMFBY) currently depend on. SIF is grounded in the plant's internal process of energy partitioning for photosynthesis, which gives it a theoretical head start over NDVI: NDVI only registers a change once the plant's structure has already begun to visibly deteriorate, whereas SIF tracks the drop in photosynthetic efficiency directly. The premise gets tested with GOSIF v2 fluorescence data and MODIS NDVI, arranged by growing season, where only the 2015 and 2018 growing seasons are classified as drought years based on CHIRPS rainfall data independently. The plan first covered 3 years (2015, 2018, 2020); 5 additional years (2016, 2017, 2019, 2022, 2023) got added after an earlier pass of the documentation found sample size to be a limiting factor, and 2021 was added last, once its raw SIF data was tracked down and processed by hand.

Every result here gets shown as it came out, including 1 hypothesis (H3: drought severity amplifies the SIF to NDVI lag) that the data does not support.

---

## What This Project Does

- Works out the study region for Marathwada on its own, using precise district level boundaries (not a rectangular bounding box) from FAO GAUL 2015, with a diagnostic boundary overlay process.
- Creates a GOSIF v2 SIF raster matched to exact district polygons, and pulls MODIS NDVI for the same clipped, cropland masked, cloud screened polygons using Google Earth Engine.
- Works out a numeric SIF to NDVI decline lag (in days) at 5 seasonal decline thresholds every year, using a linear interpolation crossing date method, then compares that against a time lagged cross correlation method. Both come with bootstrap confidence intervals that show how precise the lag estimates are.
- Independently checks the drought/normal year classification against 20 years of CHIRPS rainfall data (2001-2020) at both the regional and district level.
- Tests spatial correlation between SIF stress and rainfall deficit at the district level using Pearson/Spearman correlation, instead of relying only on visual inspection.
- Checks how accurate SIF based and NDVI based stress onset timing are against the one officially declared drought date available (Maharashtra, 2018), to test the policy angle on its own, separate from rainfall deficit data.
- Shows all results on an 11 page Streamlit dashboard, including 2 pages that explain the physics of photosynthesis and reflectance, and a page that brings together both interactive maps.

## Key Findings

SIF's post peak drop came before NDVI's post peak drop in 8 of the 9 years (2015, 2016, 2017, 2019, 2020, 2021, 2022, 2023) under the threshold crossing method. This fits SIF's physical basis as a faster stress signal. A second, methodologically distinct cross correlation check gives a more mixed picture, and it only shows this properly after a bug fix: the cross correlation and bootstrap scripts originally searched only non negative lags, so neither one could ever report NDVI leading SIF, no matter what the data showed. Once that got fixed and rerun, cross correlation shows SIF ahead in 5 years, tied in 1 (2020), and NDVI ahead in 3 (2018, 2022, 2023). 2 of those (2022, 2023) are backed by a bootstrap where 99%+ of replicates land below zero. Every method agrees that 2018 breaks the SIF leads pattern: a marginally negative threshold crossing lag, a cross correlation lag that is negative too (−4 days), and 87.4% of bootstrap replicates landing below zero.

Checking against the same 20 year CHIRPS baseline (2001-2020) through rainfall anomaly validation (§4.4), only 2 of the 9 years fall below the drought threshold: 2015 at −21.5% and 2018 at −18.3%. The 6 years added during the sample expansion all sit within roughly 1 standard deviation of normal, including 2021, which was folded in last, after its raw GOSIF files were tracked down and processed by hand. Looking back, the original 3 year sample, where 2/3 of the years were drought years, was much more drought heavy than Marathwada's actual 9 year climate record.

Just like the original 3 year study, the mean threshold crossing lag was smaller in the 2 drought years (7.6 days) than in the 7 normal years (15.1 days). This does not support H3. The exact year to year ranking is sensitive to the method used on its own, and for 2022/2023 even the direction changes (see Research Paper §4.6). The bootstrap check (§4.7) finds 32 of the 36 pairwise comparisons among the 9 years aren't statistically distinguishable from noise, but the remaining 4 cleanly separate the strongest SIF leads years from the strongest NDVI leads years.

The drought years are well established from independent rainfall data, and the shortfall is not spread evenly across the region either. Regional anomalies range from −21.5% (2015) to +36.8% (2022) against the 20 year normal. The 2018 deficit sat mostly in the western districts (Aurangabad −37.3% and Bid −38.0%), while eastern districts saw a surplus instead (Nanded +14.7%). This west to east gradient shows up on its own at the district level too. A Moran's I diagnostic (§4.8) finds significant spatial clustering of rainfall in all 9 years, while SIF's own spatial clustering is significant in only 4 of 9 years.

The actual district level correlation between rainfall and SIF comes out to r = 0.531 (p < 0.0001) and Spearman ρ = 0.504 (p < 0.0001), across 72 district years (8 districts × 9 years). Both numbers are much weaker than the original 3 year sample's r = 0.837 (p < 0.0001). This drop matters because it goes against the original correlation instead of backing it up: it shows that the earlier figure was inflated by that smaller sample's makeup.

Both the SIF and NDVI thresholds are crossed roughly 7 to 8 weeks before the drought was officially declared by the Maharashtra government (31 October 2018), as the chart below shows. After fixing a district naming bug found during the sample expansion (§3.2), NDVI crosses its threshold about 5 days before SIF in 2018, the reverse of the original finding, and in line with 2018 being the one exception throughout (§4.9).

Full methodology, physical basis, and limitations are documented in `GA_Research_Paper.md`.

## Repository Structure

```text
GREEN_ALIBI/
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
│   └── style.py                        # Shared dashboard theme (navy/magenta/pink/teal)
├── src/
│   ├── acquisition/                    # GEE + GOSIF data acquisition scripts (scripted and executed for all 9 study years)
│   ├── analysis/                       # Clipping, zonal stats, lag calc, rainfall, bootstrap CI, Moran's I, RQ3
│   └── visualization/                  # Static maps + Folium interactive maps
├── data/
│   ├── raw/                             # GOSIF, NDVI, rainfall, boundary data (gitignored)
│   ├── external/                        # Public record reference data (official drought declaration dates)
│   └── processed/                       # District level SIF, rainfall, lag, and bootstrap/spatial diagnostic CSVs
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

It's licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for citation metadata.

---

*The full development process, including every boundary correction, debugging session, and methodology iteration, is written up in `GA_Development_Log.md` so the whole thing can be checked and rebuilt from scratch.*