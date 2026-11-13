# GREEN ALIBI: Drought Triggers and Who Carries a Missed Drought

Sakshi D. Maske

Nagpur, Maharashtra, India

ORCID: [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

Corresponding author: [sakshimaske303@gmail.com](mailto:sakshimaske303@gmail.com)

## Highlights

- In drought years, GOSIF SIF and NDVI dropped below normal at almost the same time, within one 8-day composite.
- Neither index came first every time, in 2015–2023 or in 2001–2014.
- SIF's seasonal lead over NDVI changes a lot with how each curve is scaled.
- MODIS NIRv also declines before NDVI, by about as much as GOSIF; TROPOMI SIF declined slightly before NIRv in 2018–2020.
- Reconstructed from India's Manual for Drought Management on CHIRPS rainfall, Trigger-1 came weeks before the satellite alarms wherever both fired and never fired in a 2015–2022 district-year without a poor harvest, but it flagged only 7 of the 18 poor-harvest district-years (10 per pixel); NDVI flagged 13, and the two together 14.
- The official 2018 declaration covered talukas in four districts the reconstruction missed, and a three-week instead of four-week dry spell takes the trigger from 7 to 14 of 15 drought district-years and from 1 to 26 false alarms: what a rainfall trigger recognises depends on its data, scale and settings far more than on the choice between GOSIF and NDVI.

## Abstract

Drought relief in India passes through a chain of rules: a rainfall trigger, impact indicators such as NDVI, and a field check, and each threshold in that chain decides who carries the cost of an error. Solar-Induced Fluorescence (SIF) is linked to photosynthesis, so many expect it to show drought stress earlier than NDVI. I tested this in the eight districts of Marathwada, Maharashtra, over nine Kharif seasons (2015–2023). I compared cropland-weighted GOSIF SIF with MODIS NDVI, with each NDVI value dated to the day the pixel was observed. My main question was whether SIF drops below its normal-year range earlier than NDVI in a drought year. I compared each year with the normal years, and in most cases the two alarms came within one 8-day composite of each other. For the whole region, both crossed z < −3 on the same date in 2015, and NDVI was eight days earlier in 2018. There were 15 drought district-years (each district judged against its own rainfall record). SIF flagged 12 of them and NDVI 13. Where both flagged, SIF was earlier in 7, they were on the same date in 2, and NDVI was earlier in 3. All but one of these differences were one composite or less. At looser thresholds NDVI was earlier more often. NDVI comes only every 16 days, so the direction of a one-composite difference depends on how NDVI is placed in time. When I used only the NDVI already observed on each date, SIF came first in both regional drought years and in 8 of the 12 district-years. My second question was whether SIF's normal end-of-season decline starts before NDVI's. When each year is scaled from its seasonal minimum to its peak, SIF crossed the decline thresholds first in all nine years (8.0–34.2 days) and in all 72 district-years. But in this region NDVI stays above its pre-season level after the monsoon, and this scaling pushes NDVI's crossings later. When each curve is scaled from its peak to its own post-peak minimum, the lead becomes −5.5 to +13.4 days, SIF is first in only six years, and the differences between districts go away (Friedman p = 0.97). MODIS NIRv and EVI also declined before NDVI, by about as much as GOSIF SIF. Under the second scaling, GOSIF did not decline before NIRv in any of the nine years. GOSIF is built partly from MODIS reflectance, so this is partly expected. TROPOMI SIF (2018–2020) is a direct measurement. It declined before NDVI under both scalings and before NIRv in all three years, by 1–13 days. Only 2015 and 2018 were drought years by rainfall, and the lead was not larger in those years. I then ran the same methods, without changes, on 2001–2014, which has five more drought years, and got much the same picture. At district level the two alarms were again mostly on the same date or one composite apart, in both directions (at z < −1.5, SIF earlier in 5 of 22 drought district-years flagged by both, same date in 11, NDVI earlier in 6). For the region, SIF flagged two of the five drought years at z < −3 and NDVI one, and the seasonal lead again matched NIRv's. I also reconstructed the rainfall-based Trigger-1 of the Manual for Drought Management on CHIRPS rainfall. For the region it fired on 22 July 2015, about five weeks before both satellite alarms, and not in 2018. It flagged 7 of the 15 drought district-years (10 when applied in each rainfall pixel) with one false alarm in 57 normal district-years, and wherever a satellite alarm also fired, the trigger came first; with the three-week dry spell the Manual allows on light soils, it flagged 14 and 26 normal ones. Scored against crop loss instead of rainfall, it flagged 7 of the 18 district-years with a poor Kharif harvest and none of the other 46, NDVI 13, and the two together 14. The official 2018 declaration covered talukas in four districts the reconstruction missed, so these misses describe the rule run on gridded rainfall over districts and pixels, not the state's taluka-level procedure. At the sampling available, GOSIF SIF does not give a clearly earlier drought alarm than NDVI. Most of GOSIF's seasonal lead comes from the way NDVI's decline is measured. The small lead of TROPOMI SIF over NIRv needs more years to test.

**Correction in version 2.2.0: Trigger-1.** Earlier versions approximated Trigger-1 as a rainfall deficit over 25% plus 21 consecutive days each under 2.5 mm, which is much stricter than the Manual's rule, and reported that it rarely fired. In this version Trigger-1 follows the Manual's rule: a dry spell of four consecutive standard meteorological weeks after the normal onset date, each with less than 50% of normal weekly rainfall, or scanty rainfall (60% or more below normal), or SPI below −1.5 (Section 3.10). RQ3 and Appendix A were rerun with it, and the trigger is now also scored against IMD's deficient class and against crop loss and compared with the 2018 declaration list. The SIF–NDVI comparison, the main result, does not use the trigger and is unchanged.

## 1. Introduction

### 1.1 Motivation

NDVI measures how much red and near-infrared light a crop canopy reflects. It changes when leaf area, canopy structure or chlorophyll content change. SIF comes from a different process: when a leaf absorbs sunlight, it gives off a small part of that energy as fluorescence, and the size of this part depends on how the leaf is using the light. Under stress, photosynthesis can slow down before the leaves lose their green colour. In theory, then, SIF should show stress before NDVI. This study tests whether this shows up as a measurable difference in timing in the satellite products available today.

In India, drought declarations, which release relief, depend mainly on rainfall deficit and NDVI, while PMFBY crop-insurance claims are settled mainly from crop-cutting yield estimates (Ministry of Agriculture & Farmers Welfare, 2016a, 2016b; Down To Earth, 2025). When people call SIF an earlier indicator, they can mean two different things. The first is that SIF starts its normal end-of-season decline before NDVI. The second is that, in a drought year, SIF moves away from its normal-year values before NDVI does. Only the second would make SIF a better drought alarm. I test both questions separately, and the second one is my main question.

The question matters beyond remote sensing. A drought trigger is a policy instrument: it sets a threshold, links it to a payment, and so decides whose losses count. If a better signal arrives, the design question is where in the chain it should sit, whether it should confirm a drought or declare one, and how its errors should be weighed. Appendix A takes this up by pricing errors as relief, comparing India's design with four other systems, and classifying possible reforms with Hood's (1983) tools of government and Hall's (1993) orders of policy change.

### 1.2 Previous Work and Research Gap

Satellite SIF does respond to drought. GOME-2 and OCO-2 SIF fell during the 2011–2014 droughts in Texas and California, together with gross primary production (Sun et al., 2015). In India's Indo-Gangetic Plains, GOME-2 SIF showed the effect of heat stress on winter wheat earlier than reflectance-based indices (Song et al., 2018). It is less clear whether SIF responds *before* greenness. Several studies find that, at canopy scale, much of the SIF signal follows absorbed light and canopy structure more than fluorescence yield (Yoshida et al., 2015; Dechant et al., 2020). Because of this, SIF and a structural index like NIRv (Badgley et al., 2017) can move together. Reviews of SIF and plant stress (Mohammed et al., 2019; Porcar-Castell et al., 2014) say that early stress detection is possible only if the yield signal can be separated from these structural effects.

Most studies of SIF lead times compare seasonal curves, or compare SIF and vegetation-index anomalies over large areas using coarse SIF data. Few studies test, at the district scale used for drought declarations, whether a SIF *anomaly* comes before an NDVI anomaly in drought years that were identified independently. Few also check how much a "seasonal lead" changes with the way each curve is normalised. This is a known problem in phenology work (Zhang et al., 2003; Jönsson & Eklundh, 2004), because NDVI and other reflectance indices saturate over dense canopies and do not return to the same baseline after the season (Huete et al., 2002). This study looks at both problems at the district level, where Indian drought declarations are made.

### 1.3 Physical Basis of Solar-Induced Fluorescence

When a leaf absorbs photosynthetically active radiation, the energy is split between three pathways: photochemistry (Φ_P), non-photochemical quenching or heat dissipation (Φ_NPQ), and chlorophyll fluorescence (Φ_F):

Φ_P + Φ_NPQ + Φ_F = 1

When a crop has enough water, most of the absorbed energy goes to photochemistry, and a small and fairly stable share comes out as fluorescence. Under drought or heat stress, photochemistry slows down and heat dissipation increases. The fluorescence yield changes during this process, before the canopy structure changes (Porcar-Castell et al., 2014).

The signal measured by a satellite is

SIF = APAR × Φ_F × f_esc

Here APAR is the absorbed photosynthetically active radiation, Φ_F is the fluorescence quantum yield and f_esc is the share of emitted light that escapes the canopy. APAR and f_esc both depend on canopy structure, so a large part of the change in canopy SIF can come from structure and only a smaller part from Φ_F (Dechant et al., 2020). Instruments such as GOME-2, OCO-2 and TROPOMI measure SIF in Fraunhofer lines, where the weak fluorescence can be separated from reflected sunlight. GOSIF, my main SIF source, is not a direct measurement. It is a statistical product built from OCO-2 soundings, MODIS reflectance and weather reanalysis data (Li & Xiao, 2019). TROPOMI SIF, which I use as an independent check, is a direct measurement.

### 1.4 Physical Basis of NDVI

NDVI comes from surface reflectance in the red and near-infrared bands:

NDVI = (NIR − RED) / (NIR + RED)

Chlorophyll absorbs red light strongly, so healthy leaves reflect little red light. Inside the leaf, the spongy mesophyll, where air spaces meet cell walls, scatters near-infrared light strongly. A dense and healthy canopy therefore has a big difference between red and near-infrared reflectance and a high NDVI. When the canopy thins or dries, this difference becomes smaller. Over dense canopies NDVI saturates (Huete et al., 2002), so it can stay close to its peak even when leaf area is already going down. I removed cloud and cloud-shadow pixels using MOD13Q1's `SummaryQA` flag (Section 3.1).

### 1.5 Research Questions and Hypotheses

**Table 1.** Research questions, hypotheses and where they are tested.

| Research question | Hypothesis | Section |
|---|---|---|
| RQ1 (main): In drought years, does SIF depart from its normal-year range before NDVI does? | H4: SIF's drought anomaly precedes NDVI's. | 3.9, 3.14, 4.2, 4.11 |
| RQ1b: Does SIF's normal post-peak decline begin before NDVI's? | H1: SIF's seasonal decline begins before NDVI's. | 3.4, 4.3–4.6, 4.11 |
| RQ2: Does the SIF–NDVI lag differ between districts and with drought? | H2: the lag differs between districts. H3 (exploratory): drought widens the lag. | 3.8, 4.7, 4.11 |
| RQ3: How do satellite drought signals time against the rainfall Trigger-1 and the 2015 and 2018 declarations? | — (descriptive) | 3.10, 4.9 |

H3 is exploratory because only two of the nine years (2015, 2018) meet the drought criterion (Section 3.5). The 2001–2014 out-of-sample test adds five more (Section 4.11).

## 2. Study Area

The study covers all eight districts of Marathwada, Maharashtra: Chhatrapati Sambhajinagar (Aurangabad), Jalna, Parbhani, Hingoli, Nanded, Beed (called "Bid" in the FAO GAUL dataset used for the boundaries (FAO, 2015); see Section 3.2), Latur, and Dharashiv (Osmanabad). I chose this region because it has a long history of agricultural drought. Most farming here is rain-fed Kharif cropping (soybean, cotton, pulses, sorghum) during the June–September monsoon.

![Figure 1](../outputs/figures/figure3_study_area_map.png)

**Figure 1.** Study area: the eight districts of Marathwada, Maharashtra, India, with district boundaries and names.

## 3. Data and Methodology

### 3.1 Data Sources

All analyses use the 1 June – 27 December window (day-of-year 153–361) of nine years, 2015–2023. The out-of-sample test in Section 3.14 uses the same window in 2001–2014.

- **SIF (main):** GOSIF v2, a global 0.05°, 8-day solar-induced fluorescence product (Li & Xiao, 2019), distributed by the Global Ecology Group, University of New Hampshire.
- **SIF (independent check):** TROPOSIF v2.1 Level-2B daily soundings from Sentinel-5P TROPOMI (Guanter et al., 2021), for 2018–2020.
- **NDVI:** MODIS MOD13Q1 (Didan, 2021), 16-day, 250 m, via Google Earth Engine, including its per-pixel `DayOfYear` band (the day each pixel's value was observed).
- **Land cover:** MODIS MCD12Q1 (Friedl & Sulla-Menashe, 2022), IGBP classes 12 (cropland) and 14 (cropland/natural vegetation mosaic).
- **Precipitation:** CHIRPS daily rainfall (Funk et al., 2015), via Google Earth Engine: seasonal totals for 1981–2023 at region and district level, and daily series for the region (2001–2023) and districts (2015–2023); for the rainfall trigger, daily rainfall in every 0.05° pixel from 1 June to 30 September, 1981–2023. Every rainfall anomaly in this study comes from this one series.
- **Crop yields:** district-season-crop Area/Production/Yield statistics (Ministry of Agriculture & Farmers Welfare, 2024), Kharif season, 1997-98 to 2022-23.
- **Official declarations:** the 2015 Maharashtra drought declaration (reported 16 October 2015; India.com/ANI, 2015), the 2018 first-stage declaration of a drought-like situation (23 October 2018; Deccan Herald, 2018), and the 2018 final Kharif drought declaration (31 October 2018; Zee News, 2018; Economic and Political Weekly, 2018).

Three things about these datasets affect how the results should be read. First, GOSIF is trained on OCO-2 SIF, with MODIS reflectance (including EVI) and MERRA-2 reanalysis as inputs (Li & Xiao, 2019). MOD13Q1 NDVI also comes from MODIS reflectance, so GOSIF and NDVI are not fully independent. This is why I added the TROPOMI check (Section 3.11). Second, the GOSIF grid is 0.05° (about 5 km), much coarser than the 250 m of MOD13Q1. All comparisons are therefore at regional or district scale and say nothing about single fields. Third, class 14 is a mix of cropland and natural vegetation, so "cropland" here means a mixed farming landscape. Classes 12 and 14 together cover about 96–97% of the cells in the study area.

### 3.2 Boundary Definition and Verification

The study boundary comes from the FAO GAUL 2015 level-2 dataset. I selected the eight Marathwada districts and merged them into one polygon, and used this polygon for both the SIF clipping and the NDVI extraction. When I overlaid the polygon on a clipped SIF raster, data remained only inside the district outlines (Figure 2).

![Figure 2](../outputs/figures/boundary_overlay_check.png)

**Figure 2.** Verification of boundary masking: clipped SIF data (color) overlaid with the Marathwada district boundary (blue outline).

### 3.3 Processing Pipeline

**SIF.** GOSIF GeoTIFFs were clipped to the study boundary, scaled by GOSIF's 0.0001 factor, and masked for fill values (32767 water, 32766 snow/ice or barren). Each 0.05° cell was weighted by its cropland fraction, which is the share of MCD12Q1 pixels in classes 12 or 14 inside that cell, computed in Earth Engine on the GOSIF grid. Each 8-day composite is dated at its middle (start day + 3.5).

**NDVI.** I kept MOD13Q1 pixels only where `SummaryQA` shows good or marginal quality and where MCD12Q1 marks the pixel as cropland. A 16-day MOD13Q1 value can come from any day in its window, so I dated each composite by the mean of its pixels' `DayOfYear` values instead of its start date. Each year's NDVI series was normalised on its own observations and then linearly interpolated onto the SIF composite dates. During the monsoon many NDVI composites have few clear pixels. In 23 of 117 regional composites, under 25% of cropland pixels pass the quality screen. Removing these composites does not change the direction of any year's lag. With a stricter 50% cut-off, the 2022 lag becomes negative (−6.2 days; Supplementary Figure S1).

### 3.4 Seasonal Lag Calculation

I rescaled each year's SIF and NDVI series to 0–1. Then, by linear interpolation, I found the day-of-year on which each series first fell below each decline threshold after its peak (0.9, 0.8, 0.7, 0.6, 0.5). The lag at each threshold is the NDVI crossing date minus the SIF crossing date (positive means SIF first). A year's lag is the mean over the thresholds it reaches. I used two rescalings:

- **Season range** (the original method): 0 at the year's seasonal minimum, 1 at its peak. The minimum is usually the pre-monsoon value in June.
- **Decline range**: 0 at the minimum *after* the peak, 1 at the peak, so each series is measured over its own decline.

Both give the same result if both series go back to their pre-season level at the end of the season. If one series does not, the season-range scaling makes it cross every threshold later, because its post-season low point sits partway up the scale. I also fitted an asymmetric double-logistic curve to each series and used the end-of-season inflection date as a third estimate. These fits are unstable with 8- and 16-day data, so I report them only as a sensitivity check (Supplementary Figure S2).

To check whether a remaining lead comes from NDVI itself and has nothing to do with fluorescence, I repeated the same threshold-crossing comparison with two other MOD13Q1 reflectance indices from the same composites, with the same quality and cropland masks. These are EVI and NIRv (NDVI × near-infrared reflectance), which tracks canopy structure and absorbed light (Badgley et al., 2017). I compared SIF with each index, and compared EVI and NIRv with NDVI on their shared observation dates.

### 3.5 Rainfall Anomaly and Drought Classification

For each year I compared the seasonal CHIRPS total (1 June – 26 December) with the 2001–2020 mean and standard deviation, which gives a percentage anomaly and a z-score. A year counts as a drought year when its z-score is below −0.5. June–September totals give the same two drought years. District-years were classified against each district's own 2001–2020 baseline (main) and, as a check, against the regional baseline. The 2001–2020 baseline includes six of the study years, so I repeated the regional classification with three other baselines (2001–2014, 1981–2014, 1991–2020).

### 3.6 Cross-Correlation Lag

As an estimate that does not depend on scale, I used time-lagged cross-correlation over the post-peak decline, starting from SIF's peak. Both series were interpolated to daily values, their means were removed, and they were cross-correlated at shifts from −N/4 to +N/4 days, where N is the length of the decline window. The shift that gives the highest correlation between SIF(t) and NDVI(t + lag) is that year's estimate (positive means SIF first). Correlation does not change with scaling, so the choice of normalisation does not affect this estimate.

### 3.7 Uncertainty

For cross-correlation, I resampled each year's observations 2,000 times and repeated the same search. The 2.5th and 97.5th percentiles give a 95% interval. For threshold-crossing, I smoothed each series (Savitzky–Golay, window 5, order 2), resampled the residuals in moving blocks of three composites (to keep their autocorrelation), added them back to the smooth curve 2,000 times, and recomputed the lag each time. The replicates were centred on the reported lag and not on the lag of the smoothed curve. A leave-one-observation-out jackknife gives a second view. I also combined the per-year draws into an interval for the drought-minus-normal difference. This interval shows measurement uncertainty only and leaves out year-to-year variation.

### 3.8 District-Level Lag (H2, H3)

The same lags were computed for every district-year (8 × 9 = 72). I tested whether the lag differs between districts with a two-way ANOVA (district and year effects) and a Friedman test across the nine years, and compared drought and normal district-years with Welch's t-test.

### 3.9 Drought-Specific Anomaly Signal (H4)

A seasonal lag tells us when each index starts its normal decline. It does not tell us when the index moves away from normal. For each composite date, I standardised each year's SIF (and NDVI) value against the normal years on that date, leaving the year itself out: z = (x − mean of normal years) / s.d. of normal years. For each threshold (−0.5, −1, −1.5, −2, −3), a year's alarm date is the first composite from 1 July at which z stays below the threshold for two composites in a row. For the region, z < −3 is the only threshold where neither index gives an alarm in any normal year, so I use it as the main alarm threshold. I applied the same steps to the 72 district-years: 15 drought and 57 normal against each district's own rainfall baseline (main), and 17 and 55 against the regional baseline (sensitivity). I also measured, date by date, how well each index separates drought from normal district-years, using the area under the ROC curve (AUC). District-years in the same year share the same weather, so the AUCs are only descriptive.

NDVI is placed on the SIF dates by linear interpolation between its observation days. This means the NDVI value on a date already includes part of the next observation, which can be up to about 16 days later. To see how much this matters, I repeated the alarm test using, on each SIF date, the last NDVI value observed by the end of that SIF composite. SIF composites and interpolated NDVI are both 8 days apart, so I count alarm differences of 8 days or less as within one composite.

### 3.10 Rainfall Trigger and Declaration Dates (RQ3)

India's Manual for Drought Management (Ministry of Agriculture & Farmers Welfare, 2016a) begins drought assessment with Trigger-1, which combines rainfall deviation, SPI and dry spells (its Trigger-1 table; the 2020 update keeps the same dry-spell definition). A dry spell sets the trigger off whatever the deficit. Without one, the rainfall must be scanty (60% or more below normal) or SPI below −1.5. The Manual defines a dry spell as consecutive weeks after the due date of monsoon onset, each with less than 50% of normal weekly rainfall, usually four weeks and up to three on light soils. I coded the rule in this way. Weeks are IMD standard meteorological weeks, counted from the first full week after the normal onset date, which is about 15 June for the region (12 June at Ahmednagar and 15 June at Nagpur; India Meteorological Department, 2020); that is the week of 18–24 June. I first counted seven-day blocks from 15 June; the result moved when the blocks were shifted, so I switched to standard weeks after seeing this, and I report the block version as a check. The normal is the 2001–2020 mean for each day. The deficit since 1 June and SPI are assessed at the end of July, August and September; SPI is the rainfall since 1 June against a gamma distribution fitted to 1981–2020 (McKee et al., 1993). The trigger date is the first date on which any of the three conditions is met. In the main version a dry spell is four weeks; as checks I used three weeks, and weeks counted only from July (from the week of 2–8 July). The state applies the trigger at taluka level, so I applied it to district-average rainfall and also in every 0.05° CHIRPS pixel, each pixel against its own normal and SPI, and recorded for each district-year the share of pixels where it was met and the first date that share reached 25% and 50%. Both versions only approximate the taluka-level procedure, and both use CHIRPS, a gridded satellite and gauge product, where the state uses rain-gauge data, so they reconstruct the rule, not the official outcome. Fatima and Udmale (2026) map Trigger-1 conditions across Maharashtra's sub-districts for 2001–2023 with several SPI time scales and dry-spell thresholds; here I use one version of the rule to time it against satellite alarms. I computed the trigger for 2001–2023, so it can also be scored on the out-of-sample years. My earlier approximation (a deficit over 25% plus 21 consecutive days each under 2.5 mm) and the deficit on its own are kept for comparison. I compared the satellite alarm dates with the trigger date and with the three declaration dates. Because the 15 drought district-years are defined by a lenient rainfall anomaly, I also scored the trigger and the satellite alarms against two other definitions: IMD's deficient class (June–September rainfall 20% or more below the district's 2001–2020 mean) and crop loss (a Kharif Yield Anomaly Index below −0.5, Section 3.13, for 2015–2022), and compared the district-years it missed with the talukas declared in 2018 (`src/analysis/trigger_truth_check.py`).

### 3.11 Independent Check with TROPOMI SIF

I kept TROPOSIF soundings over Marathwada (1 June – 27 December, 2018–2020) where cloud fraction < 0.2, solar zenith angle < 70° and the product's land-cover flag is cropland (12 or 14), and averaged them into 8-day composites that match GOSIF's dates. The main variable is SIF_Corr_743 (Guanter et al., 2021). I also ran three variants (cloud fraction < 0.5, all land cover, uncorrected SIF_743). I computed the seasonal lag against NDVI under both rescalings, and in the same way against MODIS EVI and NIRv (Section 3.4).

### 3.12 Method Dependence

I recomputed the regional lag under 40 combinations of choices. SIF was cropland-weighted or unweighted; NDVI was dated by observation day or by compositing window; series were raw or smoothed; and the lag metric was the mean over thresholds, the 0.9, 0.7 or 0.5 threshold alone, or cross-correlation (all with season-range scaling). For each combination I noted whether SIF leads in all nine years, whether drought years have a smaller mean lag than normal years, and whether 2018 has the smallest lag.

### 3.13 Spatial Autocorrelation and Crop-Yield Check

I computed Moran's I every year for district SIF and rainfall anomaly, using Queen-contiguity weights (9,999 permutations). For the yield check, I took every district-crop pair with at least 10 of the 26 Kharif seasons, converted its yields to z-scores against its own mean and standard deviation, and averaged them into a Yield Anomaly Index for each district-year and each region-year (n = 8 region-years, because the yield data end in 2022-23).

### 3.14 Out-of-Sample Test, 2001–2014

After I finished the 2015–2023 analysis, I ran it again on 2001–2014, the GOSIF years before the study period, without changing anything. The drought rule, the alarm rule and its thresholds, the cropland weighting (with each year's MCD12Q1 map), the NDVI quality screen and observation-day dating, and both lag scalings are the same as in Sections 3.3–3.9. I did not re-tune anything on the new years. Anomalies are standardised against the normal years of 2001–2014 only, so no vegetation data from 2015–2023 is used in this test. Drought years are still defined against the 2001–2020 rainfall baseline, as in the main analysis. Before extracting the new years, I extracted 2015 again with the same code, and it matched the main series exactly (largest difference about 10⁻¹⁶). TROPOMI does not cover these years, and I did not repeat the district-level lag tests (H2).

## 4. Results

### 4.1 Rainfall and Drought Years

![Figure 3](../outputs/figures/rainfall_anomaly_2015_2023.png)

**Figure 3.** Regional June–December rainfall anomaly (% departure from the 2001–2020 mean), 2015–2023, with z-scores; dark red = drought years (z < −0.5).

The 2001–2020 mean is 826.8 mm (σ = 158.9 mm). Against it, the nine years were 649.0 mm in 2015 (−21.5%, z = −1.12); 904.7 mm in 2016 (+9.4%, z = 0.49); 817.4 mm in 2017 (−1.1%, z = −0.06); 674.9 mm in 2018 (−18.4%, z = −0.96); 936.3 mm in 2019 (+13.3%, z = 0.69); 1066.5 mm in 2020 (+29.0%, z = 1.51); 970.0 mm in 2021 (+17.3%, z = 0.90); 1130.3 mm in 2022 (+36.7%, z = 1.91, the wettest season since 1981); and 795.3 mm in 2023 (−3.8%, z = −0.20). Only 2015 and 2018 meet the drought criterion, and this is true under all four baselines. With the 2001–2020 baseline it holds for every cut-off from −0.3 to −0.75; at −1.0 only 2015 remains. With the 1981–2014 baseline, 2018 (z = −0.65) drops out at cut-offs of −0.7 and below. 2023 is a borderline year. Its seasonal total is close to normal, but August had only 51 mm (z = −2.52), and Maharashtra declared drought in 40 talukas on 31 October 2023 (Morung Express/IANS, 2023). By the same rule, 2001, 2002, 2003, 2004 and 2014 are also drought years, and Section 4.11 uses them as an out-of-sample test.

![Figure 4](../outputs/figures/rainfall_anomaly_by_district_static.png)

**Figure 4.** Rainfall anomaly by district (% departure from the regional 2001–2020 mean), 2015–2023.

The rainfall deficit was not the same everywhere. In 2018, Bid (−38.0%), Aurangabad (−37.3%) and Osmanabad (−33.9%) had the largest deficits, while Hingoli (+10.2%) and Nanded (+14.6%) got more rain than normal. In 2015, Osmanabad (−36.4%) had the largest deficit, and Hingoli (−8.0%) and Nanded (−7.1%) the smallest. Against each district's own baseline, 15 district-years are drought years: all eight districts in 2015, six in 2018 (all except Hingoli and Nanded), and Jalna in 2023. The count is 12 to 17 under the other baselines. The z < −0.5 cut-off is lenient (about 10% below normal for the region): 9 of the 15 had June–September rainfall within the band IMD calls normal (−19% to +19%), which is why Section 4.9 also uses a stricter rainfall definition and crop loss.

### 4.2 Is There a Drought-Specific SIF Advantage? (H4)

![Figure 5](../outputs/figures/drought_signal_anomaly_curves.png)

**Figure 5.** Standardised SIF and NDVI anomalies relative to normal years, by composite date; 2015 red, 2018 orange, normal years grey. The dashed line marks the alarm threshold z = −3; the dotted vertical lines mark the 2015 declaration and the 2018 final declaration.

For the region at z < −3, SIF and NDVI both gave the 2015 alarm on 24 August. In 2018 NDVI gave it on 25 September and SIF on 3 October, one composite (eight days) later. At z < −1, SIF came first in both drought years (by 8 days in 2015 and 32 in 2018). But at that threshold each index also gave alarms in five of the seven normal years, so this threshold cannot tell drought seasons from normal ones. In 2018 both indices reached their lowest anomaly on the same composite (11 October), and NDVI dropped further (z = −12.6 vs −7.9).

**Table 2.** Drought alarms in district-years, own-district rainfall baseline (15 drought, 57 normal district-years).

| Threshold | Drought flagged, SIF | Drought flagged, NDVI | False alarms, SIF | False alarms, NDVI | Both flagged | SIF earlier | Same date | NDVI earlier | Within one composite |
|---|---|---|---|---|---|---|---|---|---|
| z < −1.5 | 15 | 15 | 22 | 24 | 15 | 2 | 4 | 9 | 9 |
| z < −2 | 14 | 15 | 11 | 12 | 14 | 4 | 4 | 6 | 9 |
| z < −3 | 12 | 13 | 2 | 4 | 12 | 7 | 2 | 3 | 11 |

At the main threshold, SIF was earlier in 7 of the 12 drought district-years flagged by both, they were on the same date in 2, and NDVI was earlier in 3. In 11 of the 12, the gap was one composite or less. At looser thresholds NDVI was earlier more often (9 against 2 at z < −1.5, 6 against 4 at z < −2), again mostly by one composite (Table 2). SIF had slightly fewer false alarms. With the regional baseline instead (17 drought district-years), both flag 12 at z < −3; SIF is earlier in 5, the same in 4 and later in 3. The date-by-date AUC shows SIF separating drought from normal district-years from 23 July (AUC 0.80) and NDVI from 31 July (0.76). SIF's AUC is higher from 15 to 31 July and again on 24 August–1 September. NDVI's is higher in late June–early July (when both are near 0.5) and on 8–16 August. From 9 September to 20 November the two differ by about 0.02 at most, and by up to 0.06 in late November and early December.

These gaps are about as long as the sampling interval of the data, or shorter, and their direction changes with how NDVI is placed in time (Section 3.9). When I used only the NDVI observed by the end of each SIF composite, SIF came first at z < −3 in both regional drought years (by 8 days each) and in 8 of the 12 district-years flagged by both (same date in 3, NDVI earlier in 1).

H4 is therefore not supported in the way I set out to test it. With the time resolution of these data, GOSIF SIF did not give a drought alarm that was earlier every time, and NDVI did not either. The two alarms were usually one composite apart or less, their order changed with the NDVI dating, and the only steady difference was that SIF gave slightly fewer false alarms.

### 4.3 Seasonal SIF–NDVI Trajectories

![Figure 6](../outputs/figures/sif_vs_ndvi_seasonal_v2.png)

**Figure 6.** Normalised cropland-weighted SIF and NDVI (at observation day) seasonal trajectories, Marathwada, 2015–2023 (season-range scaling). Open squares mark NDVI composites in which fewer than 25% of cropland pixels passed the quality screen.

With season-range scaling, SIF's post-peak decline seems to start before NDVI's in all nine years, and NDVI stays near its peak for longer. Figure 6 also shows why the scaling is important. By late December SIF is back close to its June level (0.00–0.28 on the season scale), but NDVI is still higher (0.23–0.59). After the monsoon NDVI stays well above its pre-monsoon level, probably because of leftover vegetation, Rabi sowing and weeds on fallow land.

### 4.4 Threshold-Crossing Lag and Its Dependence on Normalisation

![Figure 7](../outputs/figures/sif_ndvi_lag_by_threshold.png)

**Figure 7.** SIF-to-NDVI decline lag (days), by decline threshold and year (season-range scaling).

With season-range scaling, the lag was 21.7 days (2015), 34.2 (2016), 28.5 (2017), 8.0 (2018), 25.4 (2019), 27.1 (2020), 20.3 (2021), 11.8 (2022) and 11.1 (2023). All of them are positive, and the lag gets bigger at deeper thresholds (Figure 7). The moving-block bootstrap puts every year above zero (95% intervals: 2015 [16.3, 30.4]; 2016 [12.5, 39.6]; 2017 [17.5, 32.5]; 2018 [2.8, 16.1]; 2019 [8.9, 33.0]; 2020 [18.6, 34.4]; 2021 [4.0, 25.2]; 2022 [5.3, 14.9]; 2023 [7.6, 16.6]). In 8 of the 36 pairs of years, the intervals do not overlap.

![Figure 8](../outputs/figures/normalisation_sensitivity.png)

**Figure 8.** Regional SIF–NDVI lag by year under season-range scaling, decline-range scaling, and the double-logistic end-of-season date.

This lead depends on the scaling. When each series is scaled from its peak to its own post-peak minimum, the lag becomes 9.6 (2015), 13.4 (2016), 10.6 (2017), 3.5 (2018), −5.5 (2019), 8.8 (2020), −1.2 (2021), −1.0 (2022) and 0.4 (2023) days. SIF is first in six years, by 0.4–13.4 days, and NDVI is first by 1–6 days in 2019, 2021 and 2022 (Figure 8). The double-logistic end-of-season date gives lags from −30 to +41 days with no clear direction, and the fits are unstable (Supplementary Figure S2). The lead shrinks most in the years when NDVI's post-season level sits much higher than SIF's. Across the nine years, this gap (on the season scale) and the difference between the two lags correlate at r = 0.67.

**Table 3.** Regional results by year and method.

| Year | Drought? | Season-range lag (days) | Block-bootstrap 95% interval | Decline-range lag (days) | Cross-correlation lag (days) | Cross-correlation 95% interval |
|---|---|---|---|---|---|---|
| 2015 | Yes | +21.7 | [16.3, 30.4] | +9.6 | +10 | [6, 13] |
| 2016 | No | +34.2 | [12.5, 39.6] | +13.4 | +12 | [8, 15] |
| 2017 | No | +28.5 | [17.5, 32.5] | +10.6 | +14 | [−20, 28] |
| 2018 | Yes | +8.0 | [2.8, 16.1] | +3.5 | +4 | [0, 6] |
| 2019 | No | +25.4 | [8.9, 33.0] | −5.5 | 0 | [−20, 24] |
| 2020 | No | +27.1 | [18.6, 34.4] | +8.8 | +9 | [−28, 28] |
| 2021 | No | +20.3 | [4.0, 25.2] | −1.2 | +20 | [−4, 30] |
| 2022 | No | +11.8 | [5.3, 14.9] | −1.0 | −1 | [−5, 3] |
| 2023 | No | +11.1 | [7.6, 16.6] | +0.4 | −3 | [−10, 0] |

### 4.5 Cross-Correlation and Its Uncertainty

![Figure 9](../outputs/figures/cross_correlation_lag.png)

**Figure 9.** Cross-correlation between SIF and NDVI as a function of the lag applied to NDVI, by year. Black markers show the correlation-maximising lag; a negative lag means NDVI leads SIF.

Cross-correlation does not depend on scaling. The shift with the highest correlation was 10 days (2015), 12 (2016), 14 (2017), 4 (2018), 0 (2019), 9 (2020), 20 (2021), −1 (2022) and −3 (2023), with peak correlations of 0.979–0.998. The correlation curves are very flat. Even at zero shift the correlation is already 0.975–0.993, so the best shift is hard to pin down.

![Figure 10](../outputs/figures/cross_correlation_lag_bootstrap_ci.png)

**Figure 10.** Cross-correlation lag point estimates with 95% bootstrap intervals (case resampling, 2,000 replicates per year), labelled with the percentage of replicates showing a SIF lead.

The 95% intervals lie fully on the SIF-lead side only in 2015 and 2016. In 2018 the interval touches zero, and in 2023 it leans towards NDVI (Table 3). Cross-correlation and the decline-range lag mostly agree. Both put 2015 and 2016 among the clearest SIF leads, and both find no lead in 2019, 2022 and 2023. These two methods point to a small SIF lead that changes from year to year. They do not support the steady three-week lead of the season-range method.

### 4.6 Independent Check with TROPOMI SIF

**Table 4.** TROPOMI (TROPOSIF v2.1) versus GOSIF, 2018–2020. Lags are NDVI crossing minus SIF crossing (days).

| Year | Composites | r (TROPOMI vs GOSIF) | Peak DOY TROPOMI | Peak DOY GOSIF | Season-range lag, TROPOMI | Season-range lag, GOSIF | Decline-range lag, TROPOMI | Decline-range lag, GOSIF |
|---|---|---|---|---|---|---|---|---|
| 2018 | 26 | 0.91 | 244.5 | 236.5 | 12.8 | 8.0 | 10.4 | 3.5 |
| 2019 | 26 | 0.97 | 252.5 | 260.5 | 43.8 | 25.4 | 10.3 | −5.5 |
| 2020 | 26 | 0.97 | 212.5 | 236.5 | 45.3 | 27.1 | 27.7 | 8.8 |

Of 630,091 soundings inside Marathwada on 540 days, 53% passed the cloud filter. TROPOMI follows GOSIF's seasonal curve closely (r = 0.91–0.97). It also puts SIF's decline before NDVI's in all three years under both scalings, though by different amounts. The four TROPOMI variants agree (season-range lags 10.8–45.9 days, none negative). In 2020 TROPOMI peaks earlier than GOSIF and its lead is larger, so the size of the lead differs between the two products. Both products show the 2018 drop compared with 2019–2020 (correlation of the two ratio series, August–October, r = 0.91). With only two normal TROPOMI years, I could not yet run a useful TROPOMI version of the H4 anomaly test.

**Other reflectance indices.** EVI and NIRv, from the same MOD13Q1 composites, also declined before NDVI. NIRv did so in all nine years (mean +22.8 days season-scaled, +9.9 days decline-scaled), and EVI in nine and eight years (+17.1 and +7.7 days). These leads are as large as SIF's (+20.9 and +4.3 days). When compared directly, GOSIF did not decline before NIRv. It was first in 4 of 9 years season-scaled (mean −1.8 days) and in none decline-scaled (mean −6.1 days). For GOSIF, then, NIRv, an index of canopy structure and absorbed light, has the same lead over NDVI, and this lead comes from NDVI's late decline. GOSIF itself is predicted from MODIS reflectance (Section 3.1), so some agreement with NIRv is expected. TROPOMI does not use MODIS data. It declined before NIRv in all three of its years, by 5.4, 7.8 and 13.1 days season-scaled and 4.6, 1.2 and 12.5 days decline-scaled (2018–2020), and before EVI by 3.0–20.8 days. Across the four TROPOMI variants it came first against NIRv in 23 of 24 year-and-scaling cases. Three years, with only one drought year, are not enough to show a lead that comes from fluorescence itself. Still, with these results I cannot say that all of SIF's lead is an NDVI effect.

### 4.7 Method Dependence and District-Level Lags (H2, H3)

Across the 40 combinations of Section 3.12 (all season-range), SIF leads in all nine years in all 8 mean-threshold combinations, in 4 of 8 at the 0.9 threshold, and in none of the 8 cross-correlation combinations. Using unweighted SIF and NDVI paired by window changes individual years' mean lag by −2.5 to +2.6 days. Cropland weighting changes lags by at most 0.2 days. These choices matter much less than the scaling.

![Figure 11](../outputs/figures/district_lag_by_year.png)

**Figure 11.** Season-range SIF–NDVI lag by district and year.

With season-range scaling, SIF's decline came first in all 72 district-years (median 17.7 days, range 2.4–43.6). The district effect is significant in the Friedman test (χ² = 14.5, p = 0.043) and borderline in the two-way ANOVA (p = 0.055). With decline-range scaling, SIF is first in 52 of 72 district-years (median 2.3 days, range −8.1 to 19.9), district means range only from 2.9 to 5.6 days, and the Friedman test finds no district effect (p = 0.97). H2 is therefore not supported. The district differences under the first scaling come from how high NDVI stays after the season in each district.

H3 is not supported either. For the region, drought years had a smaller season-range lag than normal years (14.8 vs 22.6 days) and a slightly larger decline-range lag (6.5 vs 3.6 days). With two drought years, neither difference can be interpreted. The block-bootstrap drought-minus-normal difference for the season-range lag is −7.8 days, with a measurement-only interval of [−9.9, +1.8]. At district level (own baseline), drought district-years average 14.8 vs 19.5 days (season range, Welch p = 0.080) and 5.8 vs 3.4 days (decline range, p = 0.13).

### 4.8 Spatial SIF Pattern and Spatial Autocorrelation

![Figure 12](../outputs/figures/sif_spatial_comparison_doy273_v2.png)

**Figure 12.** Spatial SIF distribution, day-of-year 273, 2015–2023.

![Figure 13](../outputs/figures/sif_by_district_static.png)

**Figure 13.** Mean SIF by district, day-of-year 273, 2015–2023.

Osmanabad has the lowest district SIF on day-of-year 273 in eight of nine years; in 2018 Bid (0.143) is lower than Osmanabad (0.151). The highest-SIF district varies: Aurangabad in five years, Nanded in two (2015, 2018), Jalna and Parbhani in one each.

![Figure 14](../outputs/figures/sif_rainfall_correlation_scatter.png)

**Figure 14.** District-level SIF (day-of-year 273) against rainfall anomaly, 72 district-years.

District SIF and rainfall anomaly are correlated across the 72 district-years (day-of-year 273: Pearson r = 0.53, Spearman ρ = 0.51, both p < 0.0001; p = 0.01 with standard errors clustered by year and a t-distribution for the nine clusters). Season-mean SIF has a stronger correlation (r = 0.74), also within years (r = 0.66). With district and year fixed effects, the relationship is not significant (p = 0.37 for season-mean SIF). SIF and rainfall move together across years and across districts, but SIF does not reliably follow a district's change from its own average in a given year.

![Figure 15](../outputs/figures/spatial_autocorrelation_morans_i.png)

**Figure 15.** Moran's I for district SIF (day-of-year 273) and rainfall anomaly, by year (* = p < 0.05).

Rainfall anomaly is spatially clustered in all nine years (Moran's I 0.26–0.56). Day-of-year-273 SIF is clustered in four years, and season-mean SIF in all nine (I = 0.29–0.54). District observations are therefore not independent, and the clustered and fixed-effects results above are the ones to rely on.

### 4.9 Satellite Signals, the Rainfall Trigger and Official Declarations (RQ3)

![Figure 16](../outputs/figures/rq3_declaration_timeline.png)

**Figure 16.** Timeline of the 2015 and 2018 seasons: SIF and NDVI drought alarms (z < −3), the regional rainfall Trigger-1 (22 July 2015; it did not fire in 2018), the declaration dates, and, faintly, the seasonal 0.9 crossings.

**Rainfall trigger.** For the region, Trigger-1 fired on 22 July 2015, after four dry weeks from 25 June, and in no other year of 2015–2023, including 2018. At district level it flagged 7 of the 15 drought district-years: six districts in 2015 (Bid, Hingoli, Latur, Nanded, Osmanabad and Parbhani, all on 22 July) and Aurangabad in 2018 (12 August). It missed Aurangabad and Jalna in 2015, Bid, Jalna, Latur, Osmanabad and Parbhani in 2018, and Jalna in 2023. It fired in one normal district-year, Aurangabad 2023 (2 September). In 2015–2023 the dry spell set it off every time. Scanty rainfall never set it off in any year; SPI below −1.5 did only in 2001–2014. Applied in each CHIRPS pixel, it was met over at least 25% of the district in 10 drought district-years, adding Jalna 2015 (43% of the district) and Jalna and Parbhani 2018 (34% and 32%), and in the same one normal district-year (Aurangabad 2023, 65%). In 2018 it covered 64% of Aurangabad but 0–16% of Bid, Latur and Osmanabad. Where the trigger and a satellite alarm both fired in a drought district-year, the trigger always came first: the SIF alarm by 17.5–36.5 days (median 25.5, five district-years) and the NDVI alarm by 25.5–137.5 days (median 33.5, six district-years). In Hingoli 2015 neither satellite alarm fired in the season, and in Nanded 2015 SIF's never fired and NDVI's came on 6 December. The result depends on how a dry spell is counted. With three dry weeks, which the Manual allows on light soils, the trigger flagged 14 drought district-years but also 26 normal ones. With the weeks counted only from July, it flagged 6 and 1. With seven-day blocks counted from 15 June in place of the standard weeks, the four-week rule flagged 10 and 7. My earlier approximation flagged 2 and 1, and the deficit over 25% on its own 10 and 18. In the 2001–2014 out-of-sample years the trigger flagged 11 of the 40 drought district-years (18 per pixel), with 5 (7) false alarms in 72 normal district-years; the NDVI alarm at z < −3 flagged 6 with one false alarm.

**Which droughts the trigger missed.** Seven of the eight drought district-years the district-average trigger missed had June–September rainfall less than 20% below their 2001–2020 mean, inside the band IMD calls normal; only Bid 2018 (−24%) was deficient. Against IMD's deficient class (June–September 20% or more below normal), the trigger flagged 5 of the 6 district-years with 3 false alarms in 66, and NDVI all 6 with 11. Against crop loss (a Kharif Yield Anomaly Index below −0.5, 18 of the 64 district-years of 2015–2022), the trigger flagged 7 (10 per pixel) and fired in none of the other 46; NDVI flagged 13 with 2 false alarms, SIF 12 with 2, and Trigger-1 OR NDVI 14 with 2. Every missed drought district-year with yield data had a poor harvest (index −0.56 to −1.31). The state's own process saw more than my reconstruction. The final declaration of 31 October 2018 listed severe drought in 11 talukas of Bid, 7 of Jalna, 7 of Osmanabad and 6 of Parbhani, and moderate drought in one taluka of Latur (Punekar News, 2018), all district-years in which the CHIRPS trigger did not fire. So these are not droughts the Manual misses. They show what the rule recognises when it is run on gridded rainfall over districts and 5 km pixels instead of taluka rain gauges, and that the vegetation index recovers most of what that version misses.

**Declarations.** The drought alarms (z < −3) of both indices came 52.5 days before the 2015 declaration (16 October). They came 27.5 (SIF) and 35.5 (NDVI) days before the 2018 final declaration (31 October), and 19.5 and 27.5 days before the 2018 first-stage declaration (23 October). The seasonal 0.9 crossings (Figure 16, faint) happen at about the same time every year. They show the normal start of the decline and say nothing about drought. The 2015 declaration was made under Maharashtra's paisewari system, for villages where the crop value was below 50 paise in the rupee (Business Standard/PTI, 2015), before the 2016 Manual, so the 2015 trigger date shows what the Manual's rule would have given, not what the state used.

Under the Manual for Drought Management, a declaration comes only after a series of triggers that ends with field checks of crop damage (Ministry of Agriculture & Farmers Welfare, 2016a). Because of this, a satellite signal will nearly always come before the declaration, and the rainfall trigger is a more useful point of comparison. For the region in 2015 the trigger came 33.5 days before both satellite alarms and 86 days before the declaration. In this region the vegetation alarms do not warn earlier than the rainfall trigger. What they add is coverage: NDVI flagged seven of the eight drought district-years that the district-average trigger missed, all but Jalna 2023.

### 4.10 Crop-Yield Check

![Figure 17](../outputs/figures/crop_yield_anomaly_by_year.png)

**Figure 17.** Marathwada Kharif Yield Anomaly Index by year (points per year and group means), with rainfall anomaly.

The Yield Anomaly Index (127 district-crop pairs, 16 crops) follows rainfall closely (r = 0.93, p = 0.0009, n = 8). Its correlation with season-mean (June–December) regional SIF is r = 0.88 (p = 0.004). It is r = 0.80–0.85 (p = 0.007–0.017) in versions without zero yields and outliers, area-weighted, detrended and with major crops only. With day-of-year-273 SIF alone it is r = 0.67 (p = 0.071). At district level, with district and year fixed effects, the yield index is linked to season-mean SIF only marginally (p ≈ 0.04–0.08 across versions, with standard errors clustered by district and a t-distribution for the eight clusters). The two drought years had a mean index of −1.08 against +0.07 for the six normal years with data (Welch p = 0.15). Harvests were lower in the drought years, as expected, but the difference is not significant with only two drought years. This check supports the drought classification. It does not tell us anything about timing within the season.

### 4.11 Out-of-Sample Test, 2001–2014

Five of the fourteen years are drought years under the same rule: 2001 (z = −0.52, just past the cut-off), 2002 (−1.27), 2003 (−1.01), 2004 (−1.35) and 2014 (−1.12). Against each district's own baseline, 40 of the 112 district-years are drought district-years. The vegetation anomalies in these years were weaker than in 2015 and 2018. At z < −3, which again gave no alarm in any of the nine normal years, SIF flagged two of the five drought years and NDVI one (Table 5).

**Table 5.** Out-of-sample drought alarms, 2001–2014, with all methods unchanged. Region: 5 drought and 9 normal years. Districts (own rainfall baseline): 40 drought and 72 normal district-years. "First" counts a year in which only one index raised the alarm as that index being first.

| Threshold | Region: drought flagged, SIF / NDVI | Region: first SIF / same / NDVI | Region: false alarms, SIF / NDVI | Districts: drought flagged, SIF / NDVI | Districts: false alarms, SIF / NDVI | Districts, both flagged: SIF earlier / same / NDVI earlier |
|---|---|---|---|---|---|---|
| z < −1 | 5 / 5 | 3 / 1 / 1 | 5 / 6 | 38 / 38 | 40 / 42 | 15 / 9 / 13 |
| z < −1.5 | 5 / 4 | 4 / 1 / 0 | 2 / 3 | 25 / 25 | 16 / 25 | 5 / 11 / 6 |
| z < −2 | 2 / 3 | 2 / 0 / 1 | 2 / 1 | 14 / 21 | 7 / 12 | 0 / 7 / 6 |
| z < −3 | 2 / 1 | 1 / 1 / 0 | 0 / 0 | 3 / 6 | 0 / 1 | 0 / 1 / 1 |

For the region, the out-of-sample years lean towards SIF. At z < −3, SIF flagged 2001 (17 September) and 2002 (25 September), and NDVI flagged only 2002, on the same date. At z < −1.5, SIF was first in four drought years and NDVI in none, with one tie. SIF was earlier by 8 days in 2001 and 2002 and by 64 days in 2014, and in 2004 NDVI did not reach the threshold. SIF also gave fewer false alarms at that threshold (2 against 3 of the 9 normal years).

At district level, where the sample is eight times larger, the results look like those of 2015–2023, and neither index is first every time. At every threshold NDVI flagged as many drought district-years as SIF, or more. Where both flagged a district-year, SIF was earlier in 15 of 37 at z < −1, NDVI in 13, and 9 were on the same date. At z < −1.5 the counts were 5, 6 and 11, and at z < −2 they were 0, 6 and 7. At z < −1.5, 17 of the 22 differences were one composite or less. SIF again gave fewer false alarms (16 against 25 at z < −1.5; 7 against 12 at z < −2). At z < −3 only two drought district-years were flagged by both, one on the same date and one with NDVI earlier. The regional series is an average of districts that differ in timing and in their normal-year spread, so regional and district alarms do not have to agree.

Taking both periods together, there are seven drought years for the region and 55 drought district-years. SIF flagged four of the drought years at z < −3 and NDVI three. Where both flagged, they were on the same date twice and NDVI was earlier once. Among the drought district-years flagged by both, SIF was earlier in 7 of 37 at z < −1.5, NDVI in 15, and 15 were on the same date. At z < −3, SIF was earlier in 7 of 14, NDVI in 4, and 3 were on the same date. So H4 is still not supported: neither index is earlier every time and most differences are one composite, even though in 2001–2014 the regional series gave SIF a small advantage.

**Table 6.** Regional seasonal lags in both periods (days; > 0 means the first-named series declines first). "First" is the number of years in which the first-named series declined first.

| Comparison | Scaling | 2015–2023: first | 2015–2023: mean | 2001–2014: first | 2001–2014: mean | 2001–2014: drought / normal mean |
|---|---|---|---|---|---|---|
| SIF vs NDVI | Season range | 9 of 9 | +20.9 | 14 of 14 | +27.4 | +28.3 / +26.9 |
| SIF vs NDVI | Decline range | 6 of 9 | +4.3 | 13 of 14 | +8.3 | +7.6 / +8.6 |
| NIRv vs NDVI | Season range | 9 of 9 | +22.8 | 14 of 14 | +26.6 | +28.9 / +25.3 |
| NIRv vs NDVI | Decline range | 9 of 9 | +9.9 | 14 of 14 | +13.8 | +17.8 / +11.5 |
| SIF vs NIRv | Season range | 4 of 9 | −1.8 | 10 of 14 | +1.9 | +0.2 / +2.9 |
| SIF vs NIRv | Decline range | 0 of 9 | −6.1 | 3 of 14 | −6.4 | −12.4 / −3.0 |

The seasonal results repeat (Table 6). Season-scaled, SIF declined before NDVI in all 14 years (mean +27.4 days), and NIRv did almost exactly the same (+26.6 days). Decline-scaled, SIF was first in 13 years (+8.3 days), but NIRv's lead over NDVI was bigger (+13.8 days), and NIRv declined before SIF in 11 of the 14 years (mean −6.4 days). Again a reflectance index has the same lead over NDVI. The lead is also not larger in drought years (season-scaled +28.3 against +26.9 days; decline-scaled +7.6 against +8.6), so H3 is not supported with five drought years either.

## 5. Discussion

I did not find what I expected for my main question. When each index is compared with its own normal years, GOSIF SIF does not give a consistently earlier drought alarm than NDVI in Marathwada. For the region, the alarms came on the same date in 2015, and NDVI was one composite earlier in 2018. In the drought district-years the gap between them was mostly zero or eight days. SIF was more often first at the strictest threshold, and NDVI at the looser ones. A gap of one 8-day composite is shorter than NDVI's 16-day sampling, and the order flips when I use the observed NDVI values in place of interpolated ones. With this data I cannot tell which index moves first. H4 is not supported.

The out-of-sample test on 2001–2014, with every method kept the same, mostly gives the same picture. At district level, with 40 more drought district-years, the alarms were again mostly on the same date or one composite apart, in both directions. The seasonal lead again matched NIRv's and did not grow in drought years. The regional alarms leaned towards SIF. SIF flagged one drought year (2001) in which NDVI did not reach the strict threshold, and SIF was first in four of five years at a looser threshold. The regional series alone cannot answer the question, and over 2001–2023 as a whole I see no consistent SIF advantage. Also, GOSIF is trained on OCO-2 soundings, which start in September 2014, so for 2001–2014 GOSIF is a prediction outside its training period.

My second result, that SIF's seasonal decline starts before NDVI's, depends on how the decline is measured. When each curve is scaled over the whole season, SIF crosses every threshold first, in every year and every district-year. But in this region NDVI does not go back to its pre-monsoon level after the season, while SIF mostly does. On the season scale, NDVI's decline is measured against a low point it never reaches, so it crosses each threshold later. When each series is scaled over its own decline, the lead shrinks to 0–13 days and disappears in three years. The district differences disappear too, and cross-correlation, which does not depend on scaling, agrees with the smaller estimate. The other reflectance indices help explain the GOSIF lead that remains. NIRv and EVI, from the same MODIS composites, lead NDVI by as much as GOSIF does, and GOSIF does not lead NIRv. For GOSIF, the lead therefore comes from NDVI itself, which saturates over dense canopy and returns slowly to its pre-season level. TROPOMI, which does not use MODIS reflectance, declined before NIRv in all three of its years, by 1–13 days. A small lead that comes from fluorescence is still possible, but three years, with one drought year, cannot show it.

Both results fit the idea that, at 5 km and 8- to 16-day resolution, GOSIF behaves mostly like a greenness and absorbed-light signal. GOSIF is predicted from MODIS EVI and reanalysis weather (Li & Xiao, 2019), and canopy SIF is driven mainly by APAR and structure (Dechant et al., 2020). It would be strange if GOSIF carried a separate early stress signal, and the NIRv result shows that at these scales it does not. Whether direct SIF measurements carry such a signal is still unknown. The TROPOMI lead over NIRv is small and based on three years, and the next step is to test more TROPOMI years.

For policy, the rainfall trigger is a better point of comparison than the declaration. As reconstructed here, the trigger is precise and early: it fired in one of 57 normal district-years and in none of the 46 district-years of 2015–2022 without a poor harvest, and in every drought district-year where a satellite alarm also fired, it came first, by weeks. Its weakness is coverage. It missed eight of the 15 rainfall-defined drought district-years, five of them in 2018, when the drought built up late in the season, and 11 of the 18 poor harvests; NDVI flagged most of them. The official 2018 declaration covered four of the districts it missed, so the gap belongs to the reconstruction: a rule run on gridded rainfall over districts and pixels recognises less than the state's taluka-level procedure with gauges and field inputs. That is itself the policy finding. The same rule recognises different droughts depending on the rainfall data, the spatial unit and its settings: with a three-week dry spell instead of four it flags 14 of 15 but fires in 26 normal district-years, and how the weeks are aligned matters too. In this study these choices decide more about which droughts are recognised than the choice of satellite index does, and the vegetation index adds most as a second route to a drought flag for losses a rainfall rule does not see, rather than as a confirmation of a rainfall flag (the only role the Manual gives it) or as an earlier warning (Appendix A). None of this gives a reason to choose GOSIF SIF over the NDVI that is already in use.

## 6. Limitations

- **Few drought years.** Only 2015 and 2018 meet the regional drought criterion in 2015–2023. The 2001–2014 test adds five more, but their vegetation anomalies were weaker, so at the strict alarm threshold it adds only two flagged drought years. Regional drought-versus-normal comparisons still rest on few seasons, and district-years within one season are not independent.
- **Normalisation dependence.** The seasonal lead depends on how each series is scaled (Section 4.4). The double-logistic fits that could provide a third, model-based estimate are unstable with the available sampling.
- **Lag size and sampling.** GOSIF is 8-day and MOD13Q1 16-day; decline-range leads are mostly smaller than the NDVI sampling interval.
- **Alarm timing resolution.** The SIF and NDVI drought alarms mostly differ by one 8-day composite or not at all, and the direction of that difference depends on whether NDVI is interpolated between observations or taken as observed (Section 4.2).
- **NDVI coverage.** Many monsoon NDVI composites have few clear pixels. The lag direction does not change when composites under 25% coverage are removed, but with a 50% cut-off it reverses in 2022 (Supplementary Figure S1). The timing of single composites is uncertain.
- **Post-hoc thresholds.** The decline thresholds, the drought cut-off (z < −0.5) and the alarm threshold (z < −3) were chosen during this study. I report sensitivity checks, and the 2001–2014 test uses the same values without change to guard against tuning, but the analysis is still exploratory.
- **Retrospective measures.** Both lag measures need the whole season, and the anomaly alarms use normal years that include later years. They compare timing after the season is over and cannot be used as they are for early warning.
- **GOSIF–MODIS dependence.** GOSIF uses MODIS reflectance as a predictor, which also makes its agreement with NIRv partly expected. TROPOMI removes this only for 2018–2020, with one drought year and two normal years. For 2001–2014, GOSIF is predicted outside the OCO-2 period it was trained on.
- **Spatial scale.** All results are regional or district averages at about 5 km over a mixed cropland mask. They do not describe single crops or fields.
- **Rainfall trigger reconstruction.** Trigger-1 is applied by the state per taluka with rain-gauge data and field inputs; here it follows the Manual's rule but is computed from CHIRPS on district-averaged rainfall and per pixel, with one onset date for the region (standard weeks from 18 June) and the deficit and SPI assessed only at month ends. I checked it against the official outcome only through the 2018 district counts, and the 2018 declaration covered four districts it missed. Its result depends on the dry-spell length (three or four weeks), on when the weeks start and on how they are aligned (seven-day blocks from 15 June in place of standard weeks give 10 of 15 drought district-years and 7 false alarms); I chose standard weeks after seeing that the blocks moved the result, and I report each.
- **Drought definition.** The 15 drought district-years come from a lenient rainfall anomaly (z < −0.5 over June–December); 9 of them had June–September rainfall within IMD's normal band, and the count is 12 to 17 under other baselines. I therefore also score the trigger against IMD's deficient class and against crop loss (Section 4.9).
- **Declarations.** I found only three declaration dates, and for 2015 I used the date it was reported. The 2015 declaration was made under the paisewari system, before the 2016 Manual. A declaration comes after field checks, so satellite signals will almost always come before it.
- **Alarm construction and inference.** Two consecutive 8-day GOSIF composites are separate retrievals, while consecutive NDVI values interpolated from a 16-day product can share one observation, so the persistence rule is not identical for the two indices. The z-scores rest on six to eight normal years, so z < −3 does not mean the same tail probability on every date. Clustered tests use a t-distribution with one degree of freedom fewer than the number of clusters; with eight or nine clusters the district yield–SIF link is marginal.
- **Yield data.** Yield is one end-of-season number per district-crop, ends in 2022-23, and includes some crops grown partly outside the Kharif season. Cotton lint production is labelled in tonnes in the source, but its values are plausible only as bales, so I treat it as bales.

## 7. Conclusion

Across nine Kharif seasons in Marathwada, GOSIF SIF did not flag agricultural drought clearly earlier than NDVI. Compared with their own normal years, the two indices gave the alarm on the same date in 2015, and NDVI one composite earlier in 2018. In the drought district-years they were mostly within eight days of each other, and which one came first depended on how I dated NDVI. When I applied the same tests unchanged to 2001–2014, the district results were the same, and the seasonal lead was again shared with NIRv. Only the regional alarms leaned slightly towards SIF.

When each curve is scaled over the whole season, SIF's normal decline seems to start well before NDVI's. Most of this lead comes from NDVI not going back to its pre-season level after the monsoon. When I measure over each series' own decline, or use cross-correlation, the lead is small, changes from year to year, and is missing in about a third of the years. MODIS NIRv and EVI also lead NDVI by as much as GOSIF does, so for GOSIF the remaining lead comes from NDVI. TROPOMI SIF led NIRv slightly in its three years, so a small lead from fluorescence itself is still possible.

For Marathwada and the data I used, GOSIF SIF is not an earlier drought alarm than NDVI at the time resolution available. The Manual's rainfall trigger, reconstructed on CHIRPS, flagged fewer droughts than NDVI, but earlier wherever both fired and with almost no false alarms; scored against crop loss, it flagged 7 of 18 poor harvests and NDVI 13. The official 2018 declaration recognised droughts my reconstruction missed, which shows how much a trigger's reach depends on the rainfall data and the scale at which it is run. Here a vegetation index is most useful as a second route to a drought flag, not as an earlier warning, and whether a dry spell is counted as three or four weeks changes which droughts are flagged far more than the choice between GOSIF and NDVI. This study shows no sign that GOSIF SIF would add more than NDVI already does. A proper test needs direct SIF measurements over more drought seasons, and vegetation data that comes more often than every 16 days.

## Revision Note

This version fixes five data-handling errors in the first preprint. NDVI dates were one day early and were matched to the nearest date, which made every lag about eight days shorter. The cross-correlation search could not return negative lags. The 2021 and 2022 GOSIF files had a half-pixel longitude offset. One district name did not match ("Beed" vs "Bid"). Two different rainfall sources were used for different anomalies. Compared with the previous version, this version also makes the drought-anomaly test (H4) the main question; adds the decline-range normalisation and double-logistic checks (Section 4.4), which change how the seasonal lead and H2 are read; classifies district drought against each district's own rainfall baseline; counts Trigger-1 dry spells only during the monsoon; uses a moving-block bootstrap centred on the reported lag; adds the NDVI coverage check; compares SIF with MODIS EVI and NIRv; runs Trigger-1 per CHIRPS pixel; and runs all methods unchanged on 2001–2014 as an out-of-sample test. A final check found an alignment error in the district alarm comparison that dated every district NDVI alarm one composite (8 days) too early. I fixed it and added the NDVI-dating check (Section 3.9) and the TROPOMI–NIRv comparison (Section 4.6). GA_Development_Log.md records every change. Appendix A, added after the preprint, scores combined drought-trigger rules on the same district-years, values their errors in rupees of relief, compares the Indian trigger design with four other systems and classifies the proposed changes by order of policy change; it does not change any result in the main text. Version 2.1.0 corrects how the policy appendix is described: my Trigger-1 approximation is much stricter than the Manual's dry spell, so its results describe my rule and not the Manual's, and the claim that a rainfall gate hides about half the droughts is withdrawn. It also corrects two facts (PMFBY claims are settled mainly from crop-cutting yield estimates; the U.S. Livestock Forage Disaster Program needs 8 consecutive weeks of D2) and adds the declarations to the paper. Version 2.2.0 replaces my Trigger-1 approximation with the Manual's own rule (a dry spell of four consecutive standard meteorological weeks after the normal onset date, each with less than 50% of normal weekly rainfall, or scanty rainfall (60% or more below normal), or SPI below −1.5), computed from daily CHIRPS rainfall in every pixel for 1981–2023, reruns RQ3 and Appendix A, and also scores Trigger-1 on 2001–2014. The trigger now flags 7 of 15 drought district-years (10 per pixel) instead of 2, before the satellite alarms wherever both fired, with one false alarm. This version also scores the trigger against IMD's deficient class and crop loss, compares its misses with the 2018 declaration, notes that 2015 was declared under the paisewari system, and reports clustered tests with a small-sample t-distribution; the SIF–NDVI results do not change. From version 2.2.0 the paper carries the project's title; earlier versions, including the EarthArXiv preprint, were titled "Testing the Fluorescence Advantage: Does Solar-Induced Fluorescence Signal Agricultural Drought Earlier than NDVI in Marathwada, India?"

## Supplementary Figures

![Figure S1](../outputs/figures/ndvi_coverage.png)

**Figure S1.** Share of cropland NDVI pixels passing the quality screen in each regional composite, and the regional season-range lag when composites below 10%, 25% or 50% coverage are excluded.

![Figure S2](../outputs/figures/normalisation_sensitivity_fits.png)

**Figure S2.** Asymmetric double-logistic fits to the regional SIF and NDVI series, by year, with the fitted end-of-season dates.

## Appendix A. Policy Extension: Combined Trigger Rules, the Cost of Their Errors and Other Drought Systems

*Added after the EarthArXiv preprint. This appendix uses only alarm and trigger dates already produced in this study. It does not change any result in the main text.*

### A.1 Why combine signals

The main text scores each signal on its own: the rainfall trigger, the NDVI anomaly and the SIF anomaly. The Manual for Drought Management does not use them on their own. It uses them in a sequence (Ministry of Agriculture & Farmers Welfare, 2016a). Trigger-1 is based on rainfall deviation, SPI and dry spells. Only if it is set off do states look at impact indicators (Trigger-2) in four groups: crop area sown, remote sensing (VCI or NDVI deviation), soil moisture and hydrology. States choose three of the four, and the drought is moderate or severe depending on how many of them are in the moderate or severe class. Field verification (Trigger-3) follows in a random 10% of affected villages, where an estimated crop loss of 33% or more counts as drought and more than 50% as severe drought. The state then declares drought by notification, for Kharif by 30 October.

In this design the satellite vegetation index can only confirm a drought that rainfall has already flagged. Reconstructed from the Manual on CHIRPS, the rainfall step flagged fewer drought district-years than NDVI, but earlier and with one false alarm (Section 4.9). So I asked a policy-design question that the data can answer directly: which combination of the three signals catches the most drought district-years with the fewest false alarms, and how early?

### A.2 Method

I used the same 72 district-years as in Sections 4.2 and 4.9 (15 drought and 57 normal, each district against its own rainfall record), the same satellite alarms (z < −3 for two composites in a row) and the same rainfall trigger dates. Every rule fires on a date:

- **Single signals:** the Manual's Trigger-1 on district-average rainfall; Trigger-1 when it has been met in 25% of a district's CHIRPS pixels; a rainfall deficit over 25% since 1 June, checked daily from 1 July (not the Manual's rule, which needs scanty rainfall when there is no dry spell); the NDVI anomaly; the SIF anomaly.
- **AND rules** fire when the last of their signals has fired (deficit AND NDVI, deficit AND SIF, NDVI AND SIF).
- **A sequence rule** fires when the NDVI alarm comes on or after the rainfall deficit, which is the order the Manual uses (deficit, then NDVI confirms).
- **OR rules** fire with the first signal (NDVI OR SIF, Trigger-1 OR NDVI).
- **A 2-of-3 rule** fires on the date the second of deficit, NDVI and SIF fires.

For each rule I counted the drought district-years flagged, the false alarms in normal district-years, how many drought district-years were flagged by 30 September (the end of the monsoon window used for the dry-spell rule), and the median alarm date. I repeated the scoring with NDVI taken as observed instead of interpolated (Section 3.9), and for the satellite-only rules on the 2001–2014 district-years (Section 3.14). The deficit rule and the rules built on it can be scored only for 2015–2023, where the district daily rainfall from Earth Engine is available; Trigger-1, computed from the daily CHIRPS pixel stacks, is scored in both periods. The script is `src/analysis/trigger_rule_comparison.py`, and the figure is made by `src/visualization/plot_trigger_rules.py`.

### A.3 Results

**Table A1.** Trigger rules scored on 72 district-years, 2015–2023 (satellite alarms at z < −3, own-district rainfall baseline).

| Rule | Drought flagged (of 15) | False alarms (of 57) | Flagged by 30 Sep | Median alarm date |
|---|---|---|---|---|
| Rainfall Trigger-1 (district average) | 7 | 1 | 7 | 22 Jul |
| Rainfall Trigger-1 (25% of pixels) | 10 | 1 | 10 | 22 Jul |
| Rainfall deficit > 25% alone | 10 | 18 | 9 | 16 Jul |
| NDVI anomaly | 13 | 4 | 9 | 17 Sep |
| SIF anomaly | 12 | 2 | 9 | 13 Sep |
| Deficit AND NDVI | 8 | 2 | 6 | 5 Sep |
| Deficit AND SIF | 7 | 0 | 6 | 24 Aug |
| Deficit, then NDVI confirms | 7 | 2 | 6 | 24 Aug |
| NDVI AND SIF | 12 | 2 | 9 | 17 Sep |
| NDVI OR SIF | 13 | 4 | 9 | 17 Sep |
| Trigger-1 OR NDVI | 14 | 4 | 11 | 30 Aug |
| 2 of 3: deficit, NDVI, SIF | 13 | 4 | 9 | 17 Sep |

![Figure A1](../outputs/figures/trigger_rule_comparison.png)
*Figure A1. Drought district-years flagged (left; dark part = flagged by 30 September) and false alarms in normal district-years (right) for each rule, 2015–2023.*

The Manual's Trigger-1 flagged 7 drought district-years on district-average rainfall and 10 per pixel, all by 30 September with a median date of 22 July, and fired in one normal district-year. NDVI on its own flagged 13 of 15 with 4 false alarms, and every satellite rule missed Hingoli 2015 and Jalna 2023. Trigger-1 OR NDVI, which lets either signal raise the flag, flagged 14, missing only Jalna 2023, with no more false alarms than NDVI alone, because the trigger's one false alarm (Aurangabad 2023) was a false alarm for NDVI too. The deficit alone flagged Hingoli 2015 and Jalna 2023, but with 18 false alarms.

The rules that need the rainfall deficit (deficit AND NDVI, deficit AND SIF, deficit then NDVI) flagged only 7 or 8 of 15. The deficit rule missed Aurangabad 2015 and four of the six drought district-years of 2018 (Jalna, Latur, Osmanabad, Parbhani), so any rule that waits for it misses them too. The rules that did fire fired earlier than the satellite rules (median 24 August to 5 September), and deficit AND SIF had no false alarm. A gate on the deficit limits detection to what the deficit can see. The Manual's own gate is mostly the dry spell, which flagged 7 to 10 of the 15, but I would not read the remaining misses as droughts the Manual misses either. The drought district-years are themselves defined by rainfall, the deficit rule is checked every day from 1 July (so many of its false alarms are just a late monsoon onset), and some of the drought district-years it missed had small seasonal deficits. What the counts show is two rainfall definitions and NDVI disagreeing.

Asking SIF to confirm NDVI did halve the false alarms (from 4 to 2) without losing any drought flagged by 30 September (9 in both). The one extra miss, Nanded 2015, was flagged by NDVI only on 6 December. But the gain does not survive two checks: with NDVI taken as observed, NDVI alone has 3 false alarms against 2 for NDVI AND SIF. In 2001–2014, requiring both indices flagged 2 of 40 drought district-years against 6 for NDVI alone, while NDVI alone had a single false alarm (Table A2). Where droughts are mild, confirmation costs detections.

No satellite rule at z < −3 flagged more than 9 of the 15 drought district-years by 30 September, against 7 to 10 for the Manual's Trigger-1 and 11 for Trigger-1 OR NDVI, and the strict z < −3 threshold caught at most 7 of the 40 milder drought district-years of 2001–2014. In those years Trigger-1 flagged 11 (18 per pixel), but with 5 (7) false alarms against one for NDVI. The alarm threshold is itself a policy choice between missed droughts and false alarms, and these data only describe its consequences at one level.

**Table A2.** Sensitivity of the rules.

| Rule | 2015–2023, NDVI as observed: drought (of 15) / false (of 57) | 2001–2014: drought (of 40) / false (of 72) |
|---|---|---|
| NDVI anomaly | 13 / 3 | 6 / 1 |
| SIF anomaly | 12 / 2 | 3 / 0 |
| NDVI AND SIF | 12 / 2 | 2 / 0 |
| NDVI OR SIF | 13 / 3 | 7 / 1 |
| Rainfall Trigger-1 (district average) | 7 / 1 | 11 / 5 |
| Rainfall Trigger-1 (25% of pixels) | 10 / 1 | 18 / 7 |
| Trigger-1 OR NDVI | 14 / 3 | 16 / 6 |

The counts above depend on what is called a drought. Scored against crop loss (a Kharif Yield Anomaly Index below −0.5; 18 of the 64 district-years of 2015–2022), Trigger-1 flagged 7 (10 per pixel) with no false alarm, NDVI 13 with 2, SIF 12 with 2, and Trigger-1 OR NDVI 14 with 2. Against IMD's deficient class (6 district-years), Trigger-1 flagged 5 with 3 false alarms and NDVI 6 with 11. The pattern that matters for design holds on the impact-based definition: the rainfall rule is precise but sees only part of the loss, and letting NDVI raise a flag recovers most of the rest (Section 4.9; `data/processed/trigger_truth_check.csv`).

### A.4 What the errors cost

Counting errors treats a missed drought in a large district like one in a small district, and it leaves open how a missed drought should weigh against a false alarm. To put both errors in one unit, I valued them in rupees, as the relief they move.

For relief I used the SDRF/NDRF input subsidy for rainfed crops with a crop loss of 33% or more, ₹8,500 per hectare (norms for 2022–23 to 2025–26; Ministry of Home Affairs, 2022), on each district's mean Kharif sown area for 2015–2022 (Ministry of Agriculture & Farmers Welfare, 2024). In a drought district-year that a rule misses, this is relief withheld; in a normal district-year in which the rule fires, it is relief paid where there was no drought. Both are upper bounds, because relief goes only to farmers with a verified loss of 33% or more and to at most 2 ha per farmer. For scale I also valued the crop loss in each drought district-year: the shortfall of each Kharif crop's yield below its mean in that district's normal years of 2015–2022, times the area sown, at the 2022–23 Minimum Support Prices (Directorate of Economics & Statistics, 2025). The nine priced crops cover 98.9% of the Kharif area. Cotton lint production is labelled in tonnes in the source, but its values are plausible only as bales, so I treated it as bales and converted at about 5 quintals of seed cotton per bale. District yields for 2023 are not yet published, so the loss for Jalna 2023 is imputed from the mean loss per hectare of the other drought district-years.

A rule's weighted cost is w × relief withheld + relief paid in normal years. The weight w says how much a rupee that fails to reach a drought-hit district counts against a rupee paid where there was no drought: at w = 1 only the budget counts, and w > 1 gives priority to drought-hit farmers. This is the logic of the cost–loss model for weather warnings (Murphy, 1977), with relief in place of protective action. Rather than choose w, I report the range of w over which each rule has the lowest cost. I scored the rules of Table A1, and the NDVI, SIF and NDVI AND SIF rules at z < −1.5, −2 and −3, counting a drought as flagged at any date and, separately, only if flagged by 30 September. The script is `src/analysis/trigger_cost_analysis.py`, and Figure A2 is made by `src/visualization/plot_trigger_costs.py`.

**Table A4.** The cost of each rule's errors, 2015–2023 (₹ crore; relief at ₹8,500/ha; drought flagged at any date). Selected rules; all are in `data/processed/trigger_cost_comparison.csv`.

| Rule | Drought flagged (of 15) / false alarms (of 57) | Relief withheld in missed droughts | Relief paid in normal years | Crop loss in missed droughts |
|---|---|---|---|---|
| Rainfall Trigger-1 (district average) | 7 / 1 | 4,177 | 562 | 12,795 |
| Rainfall Trigger-1 (25% of pixels) | 10 / 1 | 2,657 | 562 | 7,898 |
| Trigger-1 OR NDVI, z < −3 | 14 / 4 | 526 | 2,336 | 1,707 |
| Rainfall deficit > 25% alone | 10 / 18 | 2,435 | 9,757 | 5,989 |
| NDVI anomaly, z < −1.5 | 15 / 24 | 0 | 12,725 | 0 |
| NDVI anomaly, z < −2 | 15 / 12 | 0 | 6,492 | 0 |
| NDVI AND SIF, z < −2 | 14 / 7 | 526 | 3,811 | 1,707 |
| NDVI anomaly, z < −3 | 13 / 4 | 889 | 2,336 | 2,904 |
| SIF anomaly, z < −3 (same as NDVI AND SIF) | 12 / 2 | 1,595 | 1,068 | 5,110 |
| Deficit, then NDVI confirms | 7 / 2 | 3,886 | 1,268 | 9,687 |
| Deficit AND SIF | 7 / 0 | 4,030 | 0 | 11,100 |

**Table A5.** The rule with the lowest weighted cost, by the weight w on relief withheld from drought-hit districts.

| w | Drought flagged at any date | w | Drought flagged by 30 September |
|---|---|---|---|
| below 0.41 | Deficit AND SIF | below 0.30 | Deficit AND SIF |
| 0.41–0.47 | Rainfall Trigger-1 (25% of pixels) | 0.30–2.26 | Rainfall Trigger-1 (25% of pixels) |
| 0.48–1.18 | SIF anomaly, z < −3 | 2.27–7.71 | Trigger-1 OR NDVI, z < −3 |
| 1.19–7.89 | Trigger-1 OR NDVI, z < −3 | 7.72 and above | NDVI anomaly, z < −1.5 |
| 7.90 and above | NDVI anomaly, z < −2 | | |

![Figure A2](../outputs/figures/trigger_cost_frontier.png)
*Figure A2. Relief withheld in missed drought district-years against relief paid in normal district-years, for each rule, 2015–2023 (left: drought flagged at any date; right: only by 30 September). The dashed line joins the rules with the lowest weighted cost for some weight w.*

Start with the scale. The 15 drought district-years lost about ₹25,450 crore of Kharif output at 2022–23 prices. Relief at the SDRF rate would have covered ₹7,843 crore of it (31%). If relief followed the reconstructed Trigger-1 on district-average rainfall alone, the eight it missed would receive none: ₹4,177 crore at the SDRF rate, and half of the crop loss (₹12,795 crore) fell in district-years it did not flag. Per pixel it missed five: ₹2,657 crore withheld and 31% of the crop loss (₹7,898 crore). Its one false alarm paid ₹562 crore. Letting NDVI raise the flag as well (Trigger-1 OR NDVI) cuts relief withheld to ₹526 crore and the crop loss in missed droughts to ₹1,707 crore (7%), for ₹2,336 crore paid in four normal district-years. These are the amounts each rule would move, not money that was withheld: in 2018 the state declared drought in talukas of five of the eight (Section 4.9). Relief is a transfer, not a social cost, and under the Manual a Trigger-1 false alarm leads to Trigger-2 and field verification, so its real cost is mostly verification effort, which I do not model.

Trigger-1 OR NDVI is the cheapest rule over most of the range of weights: for w from 1.19 to 7.89 when a flag at any date counts, and from 2.27 to 7.71 when only flags by 30 September count. When only flags by 30 September count and w is lower (0.30–2.26), the per-pixel Trigger-1 on its own is cheapest, because its single false alarm keeps relief paid in normal years low. A gate that waits for the deficit is the cheapest only when a rupee that fails to reach a drought-hit district counts for less than about a third to two-fifths of a rupee paid in a normal year (w below 0.41, or 0.30 by 30 September).

Which rule is cheapest depends on w, and choosing w is a value judgement that the data cannot make. Among the satellite rules alone, SIF at z < −3 is cheapest at low weights because of its two fewer false alarms, and NDVI at z < −3 and then z < −2 at higher ones; with the rainfall trigger in the comparison, SIF on its own stays the cheapest only for w between about 0.5 and 1.2 when a flag at any date counts. SIF's advantage rests on few events: in the checks of Table A2 it kept one false alarm fewer than NDVI, but in 2001–2014 it flagged half as many drought district-years (3 against 6 of 40).

Moving the threshold changes the cost more than changing the index. Going from NDVI at z < −3 to z < −2 cuts relief withheld from ₹889 crore to nothing and raises relief paid in normal years from ₹2,336 to ₹6,492 crore. Swapping NDVI for SIF at z < −3 moves the two by ₹706 and ₹1,268 crore. The threshold is a setting of the instrument, the index is the instrument itself (A.6).

### A.5 How other systems use vegetation signals

To put the Indian design in context, I compared it with four systems that use satellite vegetation or drought information in drought decisions, one of them in an EU member state. They differ in what the signal is allowed to decide, which is what matters for who carries each kind of error.

**Table A3.** Drought triggers in India and four other systems.

| | India: Manual for Drought Management | EU: European Drought Observatory, Combined Drought Indicator | USA: U.S. Drought Monitor and the Livestock Forage Disaster Program | Kenya: Kenya Livestock Insurance Program | Spain: river-basin drought plans and pasture-loss insurance |
|---|---|---|---|---|---|
| Signals | Rainfall deviation, SPI and dry spells; then three of crop sown area, VCI or NDVI deviation, soil moisture and hydrology; then field verification | SPI-1 and SPI-3, modelled soil moisture anomaly, fAPAR anomaly | Weekly county drought ratings from D0 to D4 | NDVI-based index of forage availability over the season, against its historical average | Plans: a prolonged-drought index from precipitation or natural flows, and a scarcity index from reservoir storage, flows and groundwater. Insurance: NDVI per homogeneous pasture zone, for each ten-day period, against its historical mean |
| Logic | Sequence: rainfall gate, then impact indicators, then field check | Sequence: Watch (rainfall deficit), Warning (plus soil moisture), Alert (plus vegetation) | Fixed schedule: 8 consecutive weeks of D2 gives one monthly payment, more severe or longer drought gives up to five | Vegetation index alone triggers the payout | Plans: index thresholds move each unit from normal to pre-alert, alert and emergency, each stage with set measures. Insurance: NDVI alone; payment below the mean minus 0.7 or 1.5 standard deviations (standard option) |
| What it decides | State declaration and relief (SDRF/NDRF) | Monitoring and early warning only; no payments | Payments to livestock producers | Insurance payouts to pastoralists | Plans: water-allocation measures, and less demanding ecological flows in a prolonged drought. Insurance: payouts to livestock farmers, premiums subsidised by ENESA |
| Unit | Village, block, taluka or district, as notified | 5 km grid | County | Insurance unit within a county | Plans: territorial unit within a river basin. Insurance: homogeneous pasture zone |
| Who carries a missed drought | Farmers, until field verification catches up | No direct payment at stake | Producers in counties rated below the threshold | Pastoralists whose forage loss the index does not see | Plans: water users in the unit. Insurance: livestock farmers whose pasture loss the zone index does not see |
| Source | Ministry of Agriculture & Farmers Welfare (2016a) | Sepulcre-Canto et al. (2012); Copernicus European Drought Observatory (n.d.) | USDA Farm Service Agency (n.d.) | WOCAT (n.d.) | Estrela (2017); Ministerio de Agricultura, Pesca y Alimentación (2020) |

The EU indicator uses the same order as India, rainfall first and vegetation last, but it decides nothing about money. The U.S. and Kenyan programmes, and Spain's pasture insurance, tie payments to a satellite or expert rating directly, with no field verification step, which makes them fast but means that the index error falls on the farmer or herder whose field the index does not represent (basis risk). My results do not show which design is better. In Marathwada, the Manual's rainfall trigger flagged 7 to 10 of the 15 rainfall-defined drought district-years, before NDVI wherever both fired, and NDVI flagged 13; letting either signal raise the flag caught 14. A gate that waits for a 25% deficit flagged 7 or 8. Since those droughts come from a rainfall definition, the comparison says more about how the indicators agree than about which one is right.

Spain, an EU member state, uses both designs side by side, for different goals. Its river-basin drought plans follow a sequence of indices, like the EU indicator, and the measures they trigger concern water: in a prolonged drought, less demanding ecological flows and a justified temporary deterioration of water bodies; under scarcity, the measures set for each stage from pre-alert to emergency (Estrela, 2017). For livestock farmers, the pasture-loss insurance pays out on NDVI alone, starting below the zone's historical mean minus 0.7 standard deviations in the standard option (Ministerio de Agricultura, Pesca y Alimentación, 2020). That threshold is far looser than the z < −3 used here. In Marathwada, NDVI at z < −1.5 flagged all 15 drought district-years but also 24 of 57 normal ones (Table A4), a trade that is never the cheapest when a flag at any date counts, and is the cheapest only at a weight on missed droughts of about 7.7 or more when only flags by 30 September count. The two thresholds are not strictly comparable, since my baseline uses only normal years and needs two composites in a row.

In the classification of policy tools by Hood (1983), India's drought response uses all four types: information (nodality) in the satellite and rainfall monitoring, authority in the Manual's trigger rules and the state notification, treasure in SDRF/NDRF relief and PMFBY payouts, and organisation in the district drought contingency cells and the field verification teams. The satellite signals in this study enter only through nodality. Whether they should also gain authority, by triggering a decision as in the U.S., Kenyan and Spanish insurance programmes, is the policy question this study can inform but not settle. A closer analogue to that change is public relief rather than insurance: Kenya's Hunger Safety Net Programme scales up emergency cash transfers in the arid counties it covers when the Vegetation Condition Index crosses pre-agreed severe or extreme thresholds in any sub-county, paying a fixed share of registered households (50% or 75%) the following month without a field check (Fitzgibbon, 2016). There, a vegetation index already has authority over relief, which is what letting NDVI raise a drought flag would move India towards.

### A.6 Three orders of policy change

Hall (1993) distinguishes three orders of policy change: the settings of existing instruments (first order), the instruments themselves (second order), and the goals behind them (third order). The proposals in and around this study fall into all three.

- **First order: settings.** The alarm threshold (z < −3 or −2), the dry-spell length (three or four weeks) and the weeks from which it is counted, and whether the trigger is computed on district averages or per pixel. Here, first-order changes move the results most: three dry weeks instead of four take the rainfall trigger from 7 to 14 of the drought district-years and from 1 to 26 false alarms (Section 4.9), and the alarm threshold moves the cost of errors more than the choice of index (A.4).
- **Second order: instruments and how they are combined.** Adding SIF, or replacing the rainfall gate with an OR or 2-of-3 rule. The evidence is against adding SIF for earlier warning (Section 4.2) and against a gate on the rainfall deficit in front of the vegetation index (A.3, A.4). It favours a different change of instrument: letting the vegetation index raise a drought flag on its own as well as after the rainfall trigger. Trigger-1 OR NDVI caught 14 of the 15 drought district-years with no more false alarms than NDVI alone, and 14 of the 18 poor harvests, and it is the cheapest rule over most weights.
- **Third order: the goal.** India's drought response aims to compensate verified loss: the satellite index informs and field verification decides. The U.S., Kenyan and Spanish insurance programmes aim to pay quickly against an index, and accept that some will be paid without a loss and others not paid despite one. Giving a satellite index authority in India would be a third-order change.

This study can inform the third-order question with how often and how early an index would have been right, and what its errors would have cost. It cannot settle that question, because in Hall's account a change of goals does not follow from technical evidence alone; it comes out of a contest over the goals themselves.

### A.7 Limitations of this extension

The rules are scored on the same 72 district-years, in which only two drought seasons (2015 and 2018) supply 14 of the 15 drought cases, and district-years within one season are not independent. The satellite alarms are retrospective, because their normal years include later years (Section 6). The rainfall trigger follows the Manual's rule but is a CHIRPS reconstruction computed on district-average rainfall and per pixel, not per taluka with gauge data and field inputs, with one onset date for the region, and the Trigger-2 categories other than vegetation are not modelled; the 2018 declaration covered districts it missed. Its results depend on the dry-spell length and on how the weeks are aligned (Section 4.9). The costs in A.4 apply a flat relief rate to each district's whole Kharif area, which overstates both errors, since relief goes only to farmers with a verified loss of 33% or more and to at most 2 ha each. They leave out PMFBY payouts, which scale with the insured loss, and the cost of field verification. Crop losses are valued at one year's support prices, cotton through an approximate conversion, and the 2023 loss is imputed. The cost model treats each rule as the final decision, while under the Manual a rainfall flag is checked by Trigger-2 and field verification, and relief values are transfers, not social costs. I leave the weight w open on purpose: the results show where the cheapest rule switches, and which weight is right is for policy to decide. The comparison in A.5 describes how each system is designed on paper; I did not test how well any of them performs.

## Declarations

### Author contributions

Sakshi D. Maske: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review and editing, Visualization. This is a single-author study.

### Funding

This research received no external funding. I covered all costs myself.

### Competing interests

I declare no competing interests.

### Ethics approval

Not applicable. This study did not involve human participants, animals, or personal data of any kind.

### Data availability

All input datasets are publicly available from their original providers: GOSIF v2 (Global Ecology Group, University of New Hampshire); TROPOSIF v2.1 from Sentinel-5P TROPOMI; MODIS MOD13Q1 and MCD12Q1 and CHIRPS daily rainfall, accessed through Google Earth Engine; FAO GAUL 2015 district boundaries; district crop-yield statistics from the Ministry of Agriculture & Farmers Welfare; and drought declaration dates from the news sources cited in the paper. Processed data used in the analysis are in the repository: [https://github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI). An interactive dashboard of the results is at [https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app).

### Code availability and reproducibility

All analysis code is in the repository. The full pipeline runs from `run_all.py`, which records the Python and package versions and stops on any failure. The GOSIF files must first be downloaded once with the included download script. The MODIS, CHIRPS and cropland exports were made in Google Earth Engine; re-running those exports requires an Earth Engine account, and the exported files used in the analysis are included in the repository.

### Analysis transparency

The decline thresholds, the drought cut-off (z < −0.5) and the alarm threshold (z < −3) were chosen during this study, not fixed in advance, and the analysis is exploratory. I report results across the full range of thresholds and scalings. As a guard against tuning, I applied every method unchanged to 2001–2014, which adds five drought years, and report that test separately from the main 2015–2023 results.

### Corrections and version history

The current version corrects five data-handling errors in my first preprint: NDVI dates were one day early and matched to the nearest date, which shortened every lag by about eight days; the cross-correlation search could not return negative lags; the 2021 and 2022 GOSIF files had a half-pixel longitude offset; one district name did not match ("Beed" vs "Bid"); and two different rainfall sources were used for different anomalies. A final check found and fixed an alignment error that dated every district NDVI alarm one composite (8 days) too early. Each error, its effect and the fix are recorded in `GA_Development_Log.md`. Version 2.2.0 corrects the rainfall trigger. My earlier approximation of Trigger-1 (a rainfall deficit over 25% plus 21 consecutive days each under 2.5 mm) was much stricter than the Manual's rule and flagged only 2 of 15 drought district-years. It is replaced by the Manual's rule (a dry spell of four consecutive standard meteorological weeks after the normal onset date, each with less than 50% of normal weekly rainfall, or scanty rainfall (60% or more below normal), or SPI below −1.5), computed on district-average rainfall and in every CHIRPS pixel, and RQ3 and Appendix A were rerun with it. The same version scores the trigger against IMD's deficient class and crop loss, compares its misses with the 2018 declaration list, and reports clustered tests with a small-sample t-distribution, which makes the district yield–SIF link marginal (p ≈ 0.04–0.08 instead of 0.015–0.040). The SIF–NDVI comparison does not use the trigger and is not affected.

### Use of AI tools

I used Claude (Anthropic), an AI assistant, at several points in this project. Most of that help was checking: whether the numbers quoted in the paper, executive summary, policy brief, README and dashboard matched my output files, from the seasonal lags and the drought-alarm counts to the 2001–2014 out-of-sample test and the TROPOMI comparison. When a script failed or returned something I could not explain, I sometimes used it to help trace the problem in my Python code. I wrote the paper and the other documents myself; I used it to point out sentences that were unclear or too technical, places where something seemed to be missing, and punctuation errors, and I decided what to change. I also used it for the layout of the project pages. It did not download or process the GOSIF, MODIS, CHIRPS or TROPOMI data, run the analysis or produce the results. The research questions, the study design, the decision to separate the seasonal lead from the drought alarm and to make the alarm the main question, and the interpretation are my own. I checked every suggestion before using it and take full responsibility for the content.

### Licence and citation

The code, documentation and paper are released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). Citation metadata are in `CITATION.cff`.

## References

Badgley, G., Field, C. B., & Berry, J. A. (2017). Canopy near-infrared reflectance and terrestrial photosynthesis. *Science Advances*, 3(3), e1602244. [https://doi.org/10.1126/sciadv.1602244](https://doi.org/10.1126/sciadv.1602244)

Business Standard / PTI. (2015, October 16). *14,708 villages in Maha declared drought-hit*. [https://www.business-standard.com/article/pti-stories/14-708-villages-in-maha-declared-drought-hit-115101601357_1.html](https://www.business-standard.com/article/pti-stories/14-708-villages-in-maha-declared-drought-hit-115101601357_1.html)

Copernicus European Drought Observatory. (n.d.). *Combined Drought Indicator (CDI)* [Factsheet]. European Commission, Joint Research Centre. [https://drought.emergency.copernicus.eu/data/factsheets/factsheet_combinedDroughtIndicator.pdf](https://drought.emergency.copernicus.eu/data/factsheets/factsheet_combinedDroughtIndicator.pdf)

Deccan Herald. (2018, October 23). *Drought-like situation declared in 180 tehsils*. [https://www.deccanherald.com/india/drought-situation-declared-180-699467.html](https://www.deccanherald.com/india/drought-situation-declared-180-699467.html)

Dechant, B., Ryu, Y., Badgley, G., Zeng, Y., Berry, J. A., Zhang, Y., Goulas, Y., Li, Z., Zhang, Q., Kang, M., Li, J., & Moya, I. (2020). Canopy structure explains the relationship between photosynthesis and sun-induced chlorophyll fluorescence in crops. *Remote Sensing of Environment*, 241, 111733. [https://doi.org/10.1016/j.rse.2020.111733](https://doi.org/10.1016/j.rse.2020.111733)

Didan, K. (2021). *MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid V061* [Data set]. NASA EOSDIS Land Processes Distributed Active Archive Center. [https://doi.org/10.5067/MODIS/MOD13Q1.061](https://doi.org/10.5067/MODIS/MOD13Q1.061)

Directorate of Economics & Statistics, Ministry of Agriculture & Farmers Welfare, Government of India. (2025). *Minimum Support Prices (MSP) statement* [As on 12.12.2025]. [https://desagri.gov.in/wp-content/uploads/2025/12/MSP-Statement_English_As-on-12.12.2025.pdf](https://desagri.gov.in/wp-content/uploads/2025/12/MSP-Statement_English_As-on-12.12.2025.pdf)

Down To Earth. (2025). *When crop insurance fails farmers: Why India's PMFBY scheme needs urgent reform*. [https://www.downtoearth.org.in/agriculture/when-crop-insurance-fails-farmers-pmfby-needs-a-rethink](https://www.downtoearth.org.in/agriculture/when-crop-insurance-fails-farmers-pmfby-needs-a-rethink)

Economic and Political Weekly. (2018). Drought in Maharashtra [Editorial]. *Economic and Political Weekly*, 53(48). [https://www.epw.in/journal/2018/48/editorials/drought-maharashtra.html](https://www.epw.in/journal/2018/48/editorials/drought-maharashtra.html)

Estrela, T. (2017). *Aspectos básicos de los Planes Especiales de Sequía* [Presentation]. Confederación Hidrográfica del Júcar. [https://www.chj.es/es-es/ciudadano/participacion_publica/Documents/PES%202017/Teodoro_Estrela_Presentacion_Aspectos_Basicos_PES.pdf](https://www.chj.es/es-es/ciudadano/participacion_publica/Documents/PES%202017/Teodoro_Estrela_Presentacion_Aspectos_Basicos_PES.pdf)

Fatima, S., & Udmale, P. D. (2026). *Drought (trigger-1) assessment in Maharashtra at sub-district level in the 21st century using multiple SPI and dry spell combinations* (EGU26-721). EGU General Assembly 2026, Vienna. [https://meetingorganizer.copernicus.org/EGU26/EGU26-721.html](https://meetingorganizer.copernicus.org/EGU26/EGU26-721.html)

Fitzgibbon, C. (2016, February 23). *Shock-responsive social protection in practice: Kenya's experience in scaling up cash transfers*. Humanitarian Practice Network. [https://odihpn.org/blog/shock-responsive-social-protection-in-practice-kenyas-experience-in-scaling-up-cash-transfers/](https://odihpn.org/blog/shock-responsive-social-protection-in-practice-kenyas-experience-in-scaling-up-cash-transfers/)

Food and Agriculture Organization of the United Nations (FAO). (2015). *FAO GAUL (Global Administrative Unit Layers): Global Administrative Unit Layers 2015, Level 2* [Data set]. Google Earth Engine Data Catalog. [https://developers.google.com/earth-engine/datasets/catalog/FAO_GAUL_2015_level2](https://developers.google.com/earth-engine/datasets/catalog/FAO_GAUL_2015_level2)

Friedl, M., & Sulla-Menashe, D. (2022). *MODIS/Terra+Aqua Land Cover Type Yearly L3 Global 500m SIN Grid V061* [Data set]. NASA EOSDIS Land Processes Distributed Active Archive Center. [https://doi.org/10.5067/MODIS/MCD12Q1.061](https://doi.org/10.5067/MODIS/MCD12Q1.061)

Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A., & Michaelsen, J. (2015). The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes. *Scientific Data*, 2, Article 150066. [https://doi.org/10.1038/sdata.2015.66](https://doi.org/10.1038/sdata.2015.66)

Guanter, L., Bacour, C., Schneider, A., Aben, I., van Kempen, T. A., Maignan, F., Retscher, C., Köhler, P., Frankenberg, C., Joiner, J., & Zhang, Y. (2021). The TROPOSIF global sun-induced fluorescence dataset from the Sentinel-5P TROPOMI mission. *Earth System Science Data*, 13, 5423–5440. [https://doi.org/10.5194/essd-13-5423-2021](https://doi.org/10.5194/essd-13-5423-2021)

Hall, P. A. (1993). Policy paradigms, social learning, and the state: The case of economic policymaking in Britain. *Comparative Politics*, 25(3), 275–296. [https://doi.org/10.2307/422246](https://doi.org/10.2307/422246)

Hood, C. (1983). *The Tools of Government*. Macmillan.

Huete, A., Didan, K., Miura, T., Rodriguez, E. P., Gao, X., & Ferreira, L. G. (2002). Overview of the radiometric and biophysical performance of the MODIS vegetation indices. *Remote Sensing of Environment*, 83(1–2), 195–213. [https://doi.org/10.1016/S0034-4257(02)00096-2](https://doi.org/10.1016/S0034-4257(02)00096-2)

India Meteorological Department. (2020). *New normal dates of onset/progress and withdrawal of southwest monsoon* [Press release]. [https://mausam.imd.gov.in/backend/assets/press_release_pdf/IMD_Press_release_new_onset_and_withdrawal_dates%28Final%29.pdf](https://mausam.imd.gov.in/backend/assets/press_release_pdf/IMD_Press_release_new_onset_and_withdrawal_dates%28Final%29.pdf)

India.com / ANI. (2015, October 16). *Maharashtra: Drought declared in 14,708 villages*. [https://www.india.com/news/india/maharashtra-drought-declared-in-14708-villages-state-government-waves-off-school-students-fees-637146/](https://www.india.com/news/india/maharashtra-drought-declared-in-14708-villages-state-government-waves-off-school-students-fees-637146/)

Jönsson, P., & Eklundh, L. (2004). TIMESAT—a program for analyzing time-series of satellite sensor data. *Computers & Geosciences*, 30(8), 833–845. [https://doi.org/10.1016/j.cageo.2004.05.006](https://doi.org/10.1016/j.cageo.2004.05.006)

Li, X., & Xiao, J. (2019). A global, 0.05-degree product of solar-induced chlorophyll fluorescence derived from OCO-2, MODIS, and reanalysis data. *Remote Sensing*, 11(5), 517. [https://doi.org/10.3390/rs11050517](https://doi.org/10.3390/rs11050517)

McKee, T. B., Doesken, N. J., & Kleist, J. (1993). The relationship of drought frequency and duration to time scales. In *Proceedings of the 8th Conference on Applied Climatology* (pp. 179–184). American Meteorological Society.

Ministerio de Agricultura, Pesca y Alimentación, Entidad Estatal de Seguros Agrarios (ENESA). (2020). *Seguro de compensación por pérdida de pastos* [Information note]. [https://servicio.mapa.gob.es/en/enesa/publicaciones/notapastos-mapa2020_je_tcm38-542028.pdf](https://servicio.mapa.gob.es/en/enesa/publicaciones/notapastos-mapa2020_je_tcm38-542028.pdf)

Ministry of Agriculture & Farmers Welfare, Government of India. (2016a). *Manual for Drought Management*. Department of Agriculture, Cooperation & Farmers Welfare, New Delhi.

Ministry of Agriculture & Farmers Welfare, Government of India. (2016b). *Pradhan Mantri Fasal Bima Yojana (PMFBY)*. Retrieved from [https://pmfby.gov.in](https://pmfby.gov.in)

Ministry of Agriculture & Farmers Welfare, Government of India. (2024). *Crop Wise Area Production Yield* [Data set]. India Data Portal. [https://indiadataportal.com/p/area-production-yield-apy](https://indiadataportal.com/p/area-production-yield-apy)

Ministry of Home Affairs, Government of India. (2022). *Items and norms of assistance from the State Disaster Response Fund (SDRF) and National Disaster Response Fund (NDRF), 2022-23 to 2025-26*. [https://kokrajhar.assam.gov.in/sites/default/files/public_utility/Revised%20SDRF%20Norms%20%26%20Assistance.pdf](https://kokrajhar.assam.gov.in/sites/default/files/public_utility/Revised%20SDRF%20Norms%20%26%20Assistance.pdf)

Mohammed, G. H., Colombo, R., Middleton, E. M., Rascher, U., van der Tol, C., Nedbal, L., Goulas, Y., Pérez-Priego, O., Damm, A., Meroni, M., Joiner, J., Cogliati, S., Verhoef, W., Malenovský, Z., Gastellu-Etchegorry, J.-P., Miller, J. R., Guanter, L., Moreno, J., Moya, I., … Zarco-Tejada, P. J. (2019). Remote sensing of solar-induced chlorophyll fluorescence (SIF) in vegetation: 50 years of progress. *Remote Sensing of Environment*, 231, 111177. [https://doi.org/10.1016/j.rse.2019.04.030](https://doi.org/10.1016/j.rse.2019.04.030)

Morung Express / IANS. (2023, October 31). *Maharashtra declares drought in 40 talukas*.

Murphy, A. H. (1977). The value of climatological, categorical and probabilistic forecasts in the cost-loss ratio situation. *Monthly Weather Review*, 105(7), 803–816. [https://doi.org/10.1175/1520-0493(1977)105<0803:TVOCCA>2.0.CO;2](https://doi.org/10.1175/1520-0493(1977)105<0803:TVOCCA>2.0.CO;2)

Porcar-Castell, A., Tyystjärvi, E., Atherton, J., van der Tol, C., Flexas, J., Pfündel, E. E., Moreno, J., Frankenberg, C., & Berry, J. A. (2014). Linking chlorophyll a fluorescence to photosynthesis for remote sensing applications: mechanisms and challenges. *Journal of Experimental Botany*, 65(15), 4065–4095. [https://doi.org/10.1093/jxb/eru191](https://doi.org/10.1093/jxb/eru191)

Punekar News. (2018, October 31). *Severe drought hits 112 talukas of Maharashtra*. [https://www.punekarnews.in/?p=30530](https://www.punekarnews.in/?p=30530)

Sepulcre-Canto, G., Horion, S., Singleton, A., Carrao, H., & Vogt, J. (2012). Development of a Combined Drought Indicator to detect agricultural drought in Europe. *Natural Hazards and Earth System Sciences*, 12(11), 3519–3531. [https://doi.org/10.5194/nhess-12-3519-2012](https://doi.org/10.5194/nhess-12-3519-2012)

Song, L., Guanter, L., Guan, K., You, L., Huete, A., Ju, W., & Zhang, Y. (2018). Satellite sun-induced chlorophyll fluorescence detects early response of winter wheat to heat stress in the Indian Indo-Gangetic Plains. *Global Change Biology*, 24(9), 4023–4037. [https://doi.org/10.1111/gcb.14302](https://doi.org/10.1111/gcb.14302)

Sun, Y., Fu, R., Dickinson, R., Joiner, J., Frankenberg, C., Gu, L., Xia, Y., & Fernando, N. (2015). Drought onset mechanisms revealed by satellite solar-induced chlorophyll fluorescence: Insights from two contrasting extreme events. *Journal of Geophysical Research: Biogeosciences*, 120(11), 2427–2440. [https://doi.org/10.1002/2015JG003150](https://doi.org/10.1002/2015JG003150)

USDA Farm Service Agency. (n.d.). *Livestock Forage Disaster Program (LFP)*. [https://www.fsa.usda.gov/resources/disaster-recovery/livestock-forage-disaster-program-lfp](https://www.fsa.usda.gov/resources/disaster-recovery/livestock-forage-disaster-program-lfp)

WOCAT. (n.d.). *Kenya Livestock Insurance Program (KLIP)* [Approach]. WOCAT Global SLM Database. [https://qcat.wocat.net/wocat/approaches/view/approaches_3283](https://qcat.wocat.net/wocat/approaches/view/approaches_3283)

Yoshida, Y., Joiner, J., Tucker, C., Berry, J., Lee, J.-E., Walker, G., Reichle, R., Koster, R., Lyapustin, A., & Wang, Y. (2015). The 2010 Russian drought impact on satellite measurements of solar-induced chlorophyll fluorescence: Insights from modeling and comparisons with parameters derived from satellite reflectances. *Remote Sensing of Environment*, 166, 163–177. [https://doi.org/10.1016/j.rse.2015.06.008](https://doi.org/10.1016/j.rse.2015.06.008)

Zee News. (2018, October 31). *Maharashtra declares drought in 151 talukas in 26 districts*. [https://zeenews.india.com/india/maharashtra-declares-drought-in-151-talukas-in-26-districts-2152281.html](https://zeenews.india.com/india/maharashtra-declares-drought-in-151-talukas-in-26-districts-2152281.html)

Zhang, X., Friedl, M. A., Schaaf, C. B., Strahler, A. H., Hodges, J. C. F., Gao, F., Reed, B. C., & Huete, A. (2003). Monitoring vegetation phenology using MODIS. *Remote Sensing of Environment*, 84(3), 471–475. [https://doi.org/10.1016/S0034-4257(02)00135-9](https://doi.org/10.1016/S0034-4257(02)00135-9)
