# GREEN ALIBI: Declarations

**Testing the Fluorescence Advantage: Does Solar-Induced Fluorescence Signal Agricultural Drought Earlier than NDVI in Marathwada, India?**

Sakshi D. Maske · Independent Geospatial Researcher · ORCID [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

Version 1.2.0  
Preprint: EarthArXiv, DOI [10.31223/X5CN58](https://doi.org/10.31223/X5CN58) · Archive: Zenodo, DOI [10.5281/zenodo.21762500](https://doi.org/10.5281/zenodo.21762500) · Code and data: [github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI)

## Use of AI tools

I used Claude (Anthropic), an AI assistant, at several points in this project. Most of that help was checking: whether the numbers quoted in the paper, executive summary, policy brief, README and dashboard matched my output files, from the seasonal lags and the drought-alarm counts to the 2001–2014 out-of-sample test and the TROPOMI comparison. When a script failed or returned something I could not explain, I sometimes used it to help trace the problem in my Python code. I wrote the paper and the other documents myself; I used it to point out sentences that were unclear or too technical, places where something seemed to be missing, and punctuation errors, and I decided what to change. I also used it for the layout of the project pages. It did not download or process the GOSIF, MODIS, CHIRPS or TROPOMI data, run the analysis or produce the results. The research questions, the study design, the decision to separate the seasonal lead from the drought alarm and to make the alarm the main question, and the interpretation are my own. I checked every suggestion before using it and take full responsibility for the content.

The two explanatory illustrations on the Signal Physics page of the dashboard were made with an AI image-generation tool. They are visual aids only and are not data or results of this study.

## Highlights

- In drought years, SIF and NDVI dropped below normal at almost the same time, within one 8-day composite.
- Neither index came first every time, in 2015–2023 or in 2001–2014.
- SIF's seasonal lead over NDVI changes a lot with how each curve is scaled.
- MODIS NIRv also declines before NDVI, by about as much as GOSIF; TROPOMI SIF declined slightly before NIRv in 2018–2020.
- My approximation of India's rainfall Trigger-1 rarely fired in the drought years, but it is much stricter than the Manual's own rule (see Corrections and version history).

## Author contributions (CRediT)

Sakshi D. Maske: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review and editing, Visualization. This is a single-author study.

## Funding

This research received no external funding. I covered all costs myself.

## Competing interests

I declare no competing interests.

## Ethics

Not applicable. This study did not involve human participants, animals, or personal data of any kind.

## Data availability

All input datasets are publicly available from their original providers: GOSIF v2 (Global Ecology Group, University of New Hampshire); TROPOSIF v2.1 from Sentinel-5P TROPOMI; MODIS MOD13Q1 and MCD12Q1 and CHIRPS daily rainfall, accessed through Google Earth Engine; FAO GAUL 2015 district boundaries; district crop-yield statistics from the Ministry of Agriculture & Farmers Welfare; and drought declaration dates from the news sources cited in the paper. Processed data used in the analysis are in the repository.

## Code availability and reproducibility

All analysis code is in the repository. The full pipeline runs from `run_all.py`, which records the Python and package versions and stops on any failure. The GOSIF files must first be downloaded once with the included download script. The MODIS, CHIRPS and cropland exports were made in Google Earth Engine; re-running those exports requires an Earth Engine account, and the exported files used in the analysis are included in the repository.

## Analysis transparency

The decline thresholds, the drought cut-off (z < −0.5) and the alarm threshold (z < −3) were chosen during this study, not fixed in advance, and the analysis is exploratory. I report results across the full range of thresholds and scalings. As a guard against tuning, I applied every method unchanged to 2001–2014, which adds five drought years, and report that test separately from the main 2015–2023 results.

## Corrections and version history

The current version corrects five data-handling errors in my first preprint: NDVI dates were one day early and matched to the nearest date, which shortened every lag by about eight days; the cross-correlation search could not return negative lags; the 2021 and 2022 GOSIF files had a half-pixel longitude offset; one district name did not match ("Beed" vs "Bid"); and two different rainfall sources were used for different anomalies. A final check found and fixed an alignment error that dated every district NDVI alarm one composite (8 days) too early. Each error, its effect and the fix are recorded in `GA_Development_Log.md`. The policy appendix also has a correction in progress: my approximation of Trigger-1 (a rainfall deficit over 25% plus 21 consecutive days each under 2.5 mm) is much stricter than the Manual's dry spell (3–4 consecutive weeks, each below 50% of normal weekly rainfall), so I am re-specifying it and will rerun RQ3 and Appendix A. The SIF–NDVI comparison does not use the trigger and is not affected.

## Licence and citation

The code, documentation and paper are released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). Citation metadata are in `CITATION.cff`.
