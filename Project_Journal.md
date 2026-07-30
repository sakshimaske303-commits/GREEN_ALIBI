# GREEN ALIBI — Project Journal

## 1. Project Overview

GREEN ALIBI is an independent satellite-based verification study examining whether Solar-Induced Fluorescence (SIF) — a physical proxy for photosynthetic activity — registers vegetation and crop drought stress earlier than the Normalized Difference Vegetation Index (NDVI), the reflectance-based greenness metric that underlies much of India's current drought-monitoring and crop-insurance assessment framework. The study is situated in the Marathwada region of Maharashtra, an area with a well-documented recent history of recurring agricultural drought, and evaluates satellite data across three growing seasons: 2015 and 2018 (both documented drought years) and 2020 (a comparatively normal monsoon year), used as a baseline for comparison.

## 2. Scientific Rationale

NDVI is a reflectance-based index, derived from how much visible and near-infrared light a leaf's surface reflects. Reflectance changes only once a plant's internal structure has already begun to visibly degrade — thinning leaves, reduced chlorophyll content, canopy stress. SIF is grounded in a more direct physical mechanism: when a leaf absorbs sunlight for photosynthesis, a small fraction of the absorbed energy is not converted into chemical energy but is instead re-emitted as fluorescence, a process governed by the quantum yield of photosynthesis. Under physiological stress, photosynthetic efficiency declines before outward greenness does, and this is expected to register as a measurable change in fluorescence emission ahead of any NDVI decline. NDVI, in this framing, reflects a plant's outward appearance, while SIF reflects the underlying physiological state.

India's drought declaration process, and the crop-insurance payout mechanism under the Pradhan Mantri Fasal Bima Yojana (PMFBY) that depends on it, relies substantially on rainfall-deficit and NDVI-based assessment — both indicators that are known to respond only after visible crop stress has already set in. Delayed drought recognition translates directly into delayed insurance payouts, at the point when affected farmers most need them. This project treats the existence and size of a SIF-NDVI lag as an empirical, testable question rather than an assumption, with the intent of establishing whether such a lag — if present and sufficiently large — could constitute a physics-based case for an earlier-warning indicator than those currently used in policy.

## 3. Research Questions and Hypotheses

**Research Questions:**

RQ1: Does SIF decline measurably earlier than NDVI during documented drought-onset periods in the study region?

RQ2: Is the SIF–NDVI lag, where it exists, consistent across different districts, or does it vary meaningfully by geography?

RQ3: How does the timing of SIF-based stress onset compare against official drought-declaration timelines for the same districts and years?

RQ4: Does the observed SIF–NDVI lag translate into a practically meaningful early-warning window relevant to crop-insurance and drought-relief timelines?

**Hypotheses:**

H1: SIF declines significantly before NDVI during a given drought episode, consistent with fluorescence capturing a drop in photosynthetic efficiency ahead of any visible, reflectance-based greenness loss.

H2: The magnitude and timing of SIF–NDVI divergence is not uniform across the study region, varying with local geography and rainfall regime.

H3: Drought severity, as measured independently through rainfall deficit, amplifies the size of the SIF–NDVI lag.

## 4. Study Region and Data Sources

The study region comprises the eight districts constituting Marathwada — Chhatrapati Sambhajinagar (Aurangabad), Jalna, Parbhani, Hingoli, Nanded, Beed, Latur, and Dharashiv (Osmanabad) — selected for its recurring, well-documented drought history. Three growing seasons were analyzed: June 1 through December 31 of 2015, 2018, and 2020.

Four independent datasets were used:

- **SIF:** GOSIF v2, a global 0.05° 8-day solar-induced fluorescence product (Li & Xiao, 2019), distributed by the Global Ecology Group at the University of New Hampshire.
- **NDVI:** MODIS MOD13Q1, a 16-day, 250 m Vegetation Index product incorporating a Maximum-Value-Composite cloud-suppression algorithm, accessed via Google Earth Engine.
- **Land cover:** MODIS MCD12Q1 (IGBP classification), used to construct a cropland mask (classes 12 and 14) restricting analysis to agricultural pixels.
- **Precipitation:** CHIRPS daily rainfall, accessed via Google Earth Engine, used both for the three study years and for a twenty-year (2001–2020) climatological baseline.

## 5. Methodology

### 5.1 SIF Acquisition and Processing

Sixty 8-day GOSIF GeoTIFF files (twenty per study year) were acquired for the June–December window. Each file was clipped to the Marathwada study region, with a scale factor of 0.0001 applied to convert raw digital values to physical SIF units, and GOSIF's fill-value codes (32766 for water, 32767 for non-vegetated or missing data) masked prior to any averaging. A regional daily/8-day mean SIF value was then computed for each date, alongside a valid-pixel-fraction quality metric.

### 5.2 NDVI Acquisition and Processing

NDVI was extracted via Google Earth Engine using MOD13Q1, filtered by its native `SummaryQA` band (retaining only good- and marginal-quality pixels) and restricted to cropland pixels via the MCD12Q1-derived mask. An initial extraction using raw MOD09Q1 reflectance without quality filtering produced a physically implausible time series (single-period swings inconsistent with vegetation phenology), traced to cloud and cloud-shadow contamination during the monsoon-season observation window; the pipeline was rebuilt around the cloud-screened MOD13Q1 product to resolve this.

### 5.3 Boundary Definition

The initial study-region boundary was defined as a rectangular bounding box (75.0–78.5°E, 17.5–20.5°N). Subsequent visual verification in Google Earth Engine identified that this rectangle extended beyond Marathwada into neighboring Telangana districts (Nizamabad, Bidar, Adilabad) and into Solapur and Yavatmal, both outside the study region and subject to different rainfall regimes. The boundary definition was corrected to the precise union of the eight Marathwada districts, sourced from the FAO GAUL 2015 level-2 administrative boundary dataset. A subsequent naming-convention discrepancy (Beed district being stored under the earlier spelling "Bid" in the 2015-vintage dataset) was identified and corrected, with an explicit district-count check added to the extraction pipeline to guard against similar silent omissions. Both the SIF clipping pipeline (using polygon-based raster masking) and the NDVI extraction pipeline were subsequently rebuilt against this precise boundary, and the full analysis chain was re-executed.

### 5.4 Temporal Alignment and Lag Calculation

SIF (8-day) and NDVI (16-day) series were merged per year using nearest-date matching. A quantitative lag metric was constructed by computing, for each year, the day-of-year at which each series (normalized 0–1 within year) crossed a series of decline thresholds (90%, 80%, 70%, 60%, and 50% of seasonal peak), via linear interpolation between observed dates. The lag at each threshold was defined as the difference between the NDVI crossing date and the corresponding SIF crossing date.

### 5.5 Spatial Analysis

District-level and pixel-level spatial comparisons were constructed for a representative day-of-year (273) across all three study years, using the precise administrative boundary for masking. Per-district zonal statistics (mean SIF, mean rainfall anomaly) were computed by masking each dataset to individual district polygons.

### 5.6 Rainfall Validation

CHIRPS precipitation totals for the June–December window were computed for the three study years and for a twenty-year (2001–2020) climatological period, establishing a measured baseline against which each study year's rainfall anomaly (percentage departure, z-score) was calculated. This was extended to the district level, using the region-wide climatological mean as a shared reference baseline across all eight districts.

## 6. Development Process and Quality Assurance

Several methodological issues were identified and resolved over the course of the analysis, each addressed before proceeding rather than deferred:

- An initial NDVI extraction lacked cloud/cloud-shadow quality filtering, producing an implausibly noisy time series; resolved by switching from raw MOD09Q1 reflectance to the cloud-screened MOD13Q1 product with explicit QA-band masking.
- An Earth Engine geometry-transform error, caused by clipping a multi-resolution composite image, was resolved by removing a redundant clip operation, since region-restriction was already handled by the reducer's geometry parameter.
- A plot-labeling error incorrectly identified 2018 as a normal monsoon year rather than a drought year; corrected via explicit set-membership logic rather than single-year conditional checks.
- An initial visual assessment of the SIF-NDVI lag suggested a materially larger lag in drought years than in the normal year; on rigorous recalculation using a percentage-of-peak threshold method, this specific claim was not supported and was withdrawn in favor of the more limited, defensible finding that SIF's decline precedes NDVI's decline generally, across all three years studied.
- The initial study-region boundary (a rectangular bounding box) was found, on visual inspection, to include areas outside Marathwada with differing rainfall regimes; the boundary was corrected to a precise administrative polygon (FAO GAUL level-2), with a subsequent naming-convention gap (Beed vs. "Bid") identified and corrected via an explicit feature-count verification step added to the extraction pipeline.
- Following the boundary correction, a spatial verification map that appeared visually unchanged prompted a dedicated diagnostic check (overlaying the true boundary polygon directly on the raster output) to confirm, independently of visual impression, that the underlying masking had in fact been corrected; this confirmed the raster data was correctly masked, and identified the visualization script itself — not the underlying data — as the remaining unupdated component.
- A rainfall-validation step confirmed the drought/normal classification used throughout the study via independently measured precipitation deficit (2015: −21.5%, 2018: −18.3%, 2020: +29.1%, relative to a twenty-year climatological normal), while also revealing that the magnitude of rainfall deficit did not correspond in a simple way to the magnitude of the SIF-NDVI lag between the two drought years, a limitation reported directly rather than resolved artificially.

## 7. Key Findings

1. SIF's post-peak seasonal decline consistently precedes NDVI's decline across all three study years (2015, 2018, 2020), supporting the core premise that SIF is a more temporally responsive indicator of physiological change than NDVI.
2. The hypothesis that drought conditions amplify the SIF-NDVI lag (H3) is not supported by this dataset. Mean lag across resolved thresholds was 24.2 days (2015, drought), 5.1 days (2018, drought), and 25.5 days (2020, normal) — the two drought years averaging a smaller lag (14.6 days) than the normal year (25.5 days).
3. The two documented drought years (2015, 2018) differ substantially from each other in SIF-NDVI lag behavior, indicating that a binary drought/non-drought classification does not adequately characterize inter-annual variation relevant to this analysis.
4. District-level spatial analysis identifies a consistent low-SIF zone concentrated in the western and southwestern districts (Aurangabad, Bid, Latur, Osmanabad) during both drought years, corresponding spatially with the districts showing the largest rainfall deficits in the same years.
5. Rainfall deficit was found to be spatially uneven within Marathwada during both drought years, particularly in 2018, where the eastern districts (Nanded, Hingoli) recorded near-normal or above-normal rainfall despite a region-wide deficit of 18.3%.

## 8. Limitations

- The sample size (three years: two drought, one normal) is small, and the two drought years differ substantially from one another, limiting the extent to which any drought/normal comparison can be generalized.
- The observed spatial correspondence between rainfall deficit and SIF stress is a visual, physically-motivated consistency check rather than a formal statistical correlation or regression analysis.
- The low-SIF spatial zones identified have not been validated against ground-level crop-stress reporting; the observed pattern is consistent with known Marathwada drought geography but has not been independently confirmed.
- District-level rainfall anomaly was computed relative to a single region-wide climatological baseline rather than a per-district climatology, which was not computed due to the additional data-processing scope required.

