# GREEN ALIBI: Declarations

**GREEN ALIBI: Drought Triggers and Who Carries a Missed Drought**

Sakshi D. Maske · ORCID [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

Version 2.2.0  
Preprint: EarthArXiv, DOI [10.31223/X5CN58](https://doi.org/10.31223/X5CN58) · Archive: Zenodo, DOI [10.5281/zenodo.21762500](https://doi.org/10.5281/zenodo.21762500) · Code and data: [github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI)

## Use of AI tools

I used Claude (Anthropic), an AI assistant, at certain points in this project. Most of that help was checking: whether the numbers quoted in the paper, executive summary, policy brief, README and dashboard matched my output files, from the seasonal lags and the drought-alarm counts to the 2001–2014 out-of-sample test and the TROPOMI comparison. When a script failed or returned something I could not explain, I sometimes used it to help trace the problem in my Python code. I wrote the paper and the other documents myself; I used it to point out sentences that were unclear or too technical, places where something seemed to be missing, and punctuation errors, and I decided what to change. I also used it for the layout of the project pages. It did not download or process the GOSIF, MODIS, CHIRPS or TROPOMI data, run the analysis or produce the results. The research questions, the study design, the decision to separate the seasonal lead from the drought alarm and to make the alarm the main question, and the interpretation are my own. I checked every suggestion before using it and take full responsibility for the content.

The two explanatory illustrations on the Signal Physics page of the dashboard were made with an AI image-generation tool. They are visual aids only and are not data or results of this study.

## Highlights

- In drought years, GOSIF SIF and NDVI dropped below normal at almost the same time, within one 8-day composite.
- Neither index came first every time, in 2015–2023 or in 2001–2014.
- SIF's seasonal lead over NDVI changes a lot with how each curve is scaled.
- MODIS NIRv also declines before NDVI, by about as much as GOSIF; TROPOMI SIF declined slightly before NIRv in 2018–2020.
- Reconstructed from India's Manual for Drought Management on CHIRPS rainfall, Trigger-1 came weeks before the satellite alarms wherever both fired and never fired in a 2015–2022 district-year without a poor harvest, but it flagged only 7 of the 18 poor-harvest district-years (10 per pixel); NDVI flagged 13, and the two together 14.
- The official 2018 declaration covered talukas in four districts the reconstruction missed, and a three-week instead of four-week dry spell takes the trigger from 7 to 14 of 15 drought district-years and from 1 to 26 false alarms: what a rainfall trigger recognises depends on its data, scale and settings far more than on the choice between GOSIF and NDVI.

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

The decline thresholds, the drought cut-off (z < −0.5) and the alarm threshold (z < −3) were chosen during this study, not fixed in advance, and the analysis is exploratory. I report results across the full range of thresholds and scalings. As a guard against tuning, I applied every method unchanged to 2001–2014, which adds five drought years, and report that test separately from the main 2015–2023 results. The alignment of the dry-spell weeks was also chosen after seeing that seven-day blocks moved the trigger's result; both versions are reported. Clustered tests use a small-sample t-distribution.

## Corrections and version history

The current version corrects five data-handling errors in my first preprint: NDVI dates were one day early and matched to the nearest date, which shortened every lag by about eight days; the cross-correlation search could not return negative lags; the 2021 and 2022 GOSIF files had a half-pixel longitude offset; one district name did not match ("Beed" vs "Bid"); and two different rainfall sources were used for different anomalies. A final check found and fixed an alignment error that dated every district NDVI alarm one composite (8 days) too early. Each error, its effect and the fix are recorded in `GA_Development_Log.md`. Version 2.2.0 corrects the rainfall trigger. My earlier approximation of Trigger-1 (a rainfall deficit over 25% plus 21 consecutive days each under 2.5 mm) was much stricter than the Manual's rule and flagged only 2 of 15 drought district-years. It is replaced by the Manual's rule (a dry spell of four consecutive standard meteorological weeks after the normal onset date, each with less than 50% of normal weekly rainfall, or scanty rainfall (60% or more below normal), or SPI below −1.5), reconstructed on CHIRPS district-average rainfall and in every pixel, and RQ3 and Appendix A were rerun with it. The same version scores the trigger against IMD's deficient class and crop loss, compares its misses with the 2018 declaration list, and reports clustered tests with a small-sample t-distribution. The SIF–NDVI comparison does not use the trigger and is not affected.

## Licence and citation

The code, documentation and paper are released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). Citation metadata are in `CITATION.cff`.
