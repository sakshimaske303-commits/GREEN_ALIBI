# 🌿 GREEN ALIBI — Testing the Fluorescence Advantage

**Testing whether Solar-Induced Fluorescence catches agricultural drought stress in Marathwada, Maharashtra before NDVI can — and whether drought severity actually makes that head-start bigger — across eight growing seasons.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21762501.svg)](https://doi.org/10.5281/zenodo.21762501)

## 🔗 Live Dashboard

**[View the interactive dashboard →](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app/)**

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| ⚡ [`GA_Executive_Summary.pdf`](./GA_Executive_Summary.pdf) | One-page snapshot — question, method, headline finding, robustness checklist, and links (fastest overview) |
| 📘 [`GA_Project_Report.md`](./GA_Project_Report.md) | Polished project summary — methodology, findings, conclusions (start here) |
| 📗 [`GA_Research_Paper.md`](./GA_Research_Paper.md) | Formal academic paper — physical basis, methodology, results, discussion, limitations |
| 📙 [`GA_Development_Log.md`](./GA_Development_Log.md) | Full technical development log — every bug, boundary correction, and methodology iteration |

## 🗺️ Interactive Maps

Interactive district-level maps are hosted via GitHub Pages:

- [SIF by District](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/maps/marathwada_sif_by_district.html)
- [Rainfall Anomaly by District](https://sakshimaske303-commits.github.io/GREEN_ALIBI/outputs/interactive_maps/maps/marathwada_rainfall_by_district.html)

*(Both maps are also embedded individually in the live dashboard's Spatial SIF Analysis and Rainfall Validation pages, and together in one place on the dedicated Interactive Maps page.)*

GREEN ALIBI is a geospatial framework testing whether Solar-Induced Fluorescence (SIF) — a satellite-derived proxy for photosynthetic activity — registers vegetation stress measurably earlier than the Normalized Difference Vegetation Index (NDVI), the reflectance-based indicator that currently underpins India's drought declaration and PMFBY crop-insurance payout process. Where NDVI only changes once a plant's internal structure has already begun to visibly degrade, SIF is grounded in the plant's photosynthetic energy-partitioning process itself, making it a physically earlier signal in principle. This project tests that premise directly, using GOSIF v2 fluorescence data and cloud-screened MODIS NDVI over Marathwada's eight districts across eight growing seasons (2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023) — of which only 2015 and 2018 turn out to meet this study's own rainfall-anomaly drought threshold — cross-validated independently against CHIRPS rainfall data. The study originally covered three years (2015, 2018, 2020); five more were added in a later expansion pass specifically to address the small-sample limitation flagged in every earlier version of this project's own documentation.

Built on a **"no compromises"** standard — every result is reported exactly as it came out, including a hypothesis (H3: drought severity amplifies the SIF–NDVI lag) that this study's own data does not support.

---

## 📊 What This Project Does

- Defines the Marathwada study region using precise FAO GAUL 2015 district-level boundaries (not a rectangular bounding box), independently verified via a boundary-overlay diagnostic
- Clips GOSIF v2 SIF rasters to the exact district polygon using `rasterio.mask`, and extracts cloud-screened, cropland-masked MODIS NDVI over the same boundary via Google Earth Engine
- Calculates a quantitative SIF-to-NDVI decline lag (days) at five seasonal decline thresholds, per year, using linear-interpolation crossing-date estimation, cross-checked against an independent time-lagged cross-correlation method — with bootstrap confidence intervals quantifying how precise those lag estimates actually are
- Independently validates the drought/normal year classification using CHIRPS rainfall data against a 20-year (2001–2020) climatological baseline, region-wide and by district
- Cross-references spatial SIF stress patterns against spatial rainfall deficit patterns at the district level, confirmed via Pearson/Spearman correlation and a Moran's I spatial-autocorrelation diagnostic (not just a visual check)
- Compares SIF- and NDVI-based stress-onset timing against the one well-documented official government drought-declaration date available (2018), to ground the study's policy motivation in an actual institutional timeline rather than rainfall deficit alone
- Presents all findings through an 11-page Streamlit dashboard, including two dedicated pages explaining the underlying photosynthesis and reflectance physics and one dedicated page consolidating both interactive maps

## 🔬 Key Findings

**SIF's decline precedes NDVI's in seven of the eight years studied — 2018 is a genuine, replicated exception.** Across 2015, 2016, 2017, 2019, 2020, 2022, and 2023, SIF's post-peak seasonal decline preceded NDVI's, supporting SIF's physical basis as a more temporally responsive stress indicator — corroborated in direction by an independent cross-correlation method and shown via bootstrap resampling to never favor NDVI leading SIF in any year (100% of resampled replicates, every year). 2018 alone shows a marginally negative threshold-crossing lag, a zero cross-correlation lag, and a bootstrap interval with only 8.1% of replicates favoring a positive lag — three independent methods agreeing that 2018 specifically does not fit the general pattern.

**Only 2 of the 8 years actually meet this study's own drought threshold.** Rainfall-anomaly validation (§4.4) finds only 2015 (−21.5%) and 2018 (−18.3%) fall below the drought threshold used throughout this study; the five newly added years (2016, 2017, 2019, 2022, 2023) are all within roughly one standard deviation of normal. The original 3-year sample being two-thirds drought years was, in hindsight, considerably more drought-heavy than Marathwada's typical 8-year climate record — a finding about sample representativeness in its own right.

**Drought severity does not amplify the lag — confirmed at more than double the original sample size.** Mean lag was smaller in the two drought years (7.6 days) than in the six normal years (15.0 days), the same direction reported in the original 3-year study. H3 is explicitly reported as not supported by this data. The exact inter-annual ranking is method-sensitive (see Research Paper §4.6) and, per the bootstrap check (§4.7), not statistically distinguishable between any of the 28 possible year-pairs at this sample size.

**Rainfall independently confirms the drought years, and the deficit isn't spatially uniform.** Regional rainfall departed −21.5% (2015) to +36.8% (2022) from a 20-year normal across the 8 years. At the district level, 2018's deficit was concentrated in the west (Aurangabad −37.3%, Bid −38.0%) while eastern districts recorded surpluses (Nanded +14.7%) — a west-to-east gradient reproduced independently in the SIF signal itself. A Moran's I diagnostic (§4.8) finds rainfall's spatial clustering significant in all 8 years, but SIF's spatial clustering significant in only 4 of 8 — a more qualified result than the original 3-year study.

**District-level SIF-rainfall correlation is real but weaker than the original 3-year estimate suggested.** Across all 64 district-year observations (8 districts × 8 years), Pearson r = 0.567, Spearman ρ = 0.551, both p < 0.0001 — still strongly significant, but down from r = 0.837 in the original, smaller, drought-heavy 3-year sample. This drop is reported directly as evidence the original correlation was inflated by sample composition, not as a contradiction.

**The satellite-vs-NDVI edge is real but small next to the satellite-vs-official-process gap — and its direction for 2018 reversed after a boundary fix.** Comparing 2018's SIF and NDVI decline onset against the Maharashtra government's official drought declaration (31 October 2018) shows both satellite indicators leading the official declaration by roughly seven to eight weeks. Notably, after correcting a district-boundary naming bug found during the sample-size expansion (§3.2), NDVI now crosses its threshold about five days *before* SIF in 2018 — the reverse of what the original study reported — consistent with 2018 being this study's one exception throughout (§4.9).

Full methodology, physical basis, and limitations are documented in `GA_Research_Paper.md`.

## 🗂️ Repository Structure

```text
GREEN_ALIBI/
├── app.py                              # Streamlit dashboard home page
├── pages/                              # 11-page dashboard (chronological order)
│   ├── 1_🌍_Study_Area.py
│   ├── 2_🔬_Fluorescence_Physics.py
│   ├── 3_🔬_NDVI_Physics.py
│   ├── 4_🛰️_Data_and_Methodology.py
│   ├── 5_📈_Seasonal_Trajectories.py
│   ├── 6_📊_Lag_Analysis.py
│   ├── 7_🗺️_Spatial_SIF_Analysis.py
│   ├── 8_🌧️_Rainfall_Validation.py
│   ├── 9_🔗_Combined_Comparison.py
│   ├── 9_🗺️_Interactive_Maps.py
│   └── 10_📝_Findings_and_Conclusion.py
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
│   └── interactive_maps/maps/            # Folium HTML maps (SIF + rainfall by district)
├── GA_Research_Paper.md                 # Formal academic research paper
├── GA_Development_Log.md                # Full technical development log
└── requirements.txt
```

## 🛠️ Tech Stack

Python · Rasterio · GeoPandas · NumPy / Pandas · Matplotlib · Folium · Branca · Streamlit · Google Earth Engine

## 📚 Data Sources

| Dataset | Provider |
|---|---|
| Solar-Induced Fluorescence | GOSIF v2 (Global Ecology Group, University of New Hampshire) |
| NDVI | MODIS MOD13Q1 (via Google Earth Engine) |
| Land Cover / Cropland Mask | MODIS MCD12Q1, IGBP classification (via Google Earth Engine) |
| Precipitation | CHIRPS Daily (UCSB-CHG, via Google Earth Engine) |
| Administrative Boundaries | FAO GAUL 2015, Level 2 (via Google Earth Engine) |

## ▶️ Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/GREEN_ALIBI.git
cd GREEN_ALIBI
pip install -r requirements.txt
streamlit run app.py
```

## 👤 Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## 📜 License

This project is licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for citation metadata.

---

*This project's full development process — including every boundary correction, debugging session, and methodology iteration — is documented in `GA_Development_Log.md` for full transparency and reproducibility.*