# GREEN ALIBI
### Testing Whether Fluorescence Signals Agricultural Drought Earlier than NDVI

Executive Summary · DOI: 10.5281/zenodo.21762501 · Sakshi D. Maske

## Project Overview

I built GREEN ALIBI to turn a physical hunch into a testable claim. Solar-Induced Fluorescence (SIF) is tied to photosynthesis, so it is often expected to register crop stress before NDVI, which responds once canopy damage is visible. India's drought-management process, and the PMFBY crop-insurance payouts tied to it, lean on rainfall deficits and NDVI. If SIF really gave earlier warning, that could matter for how quickly relief reaches farmers. I tested the idea over the eight districts of Marathwada, Maharashtra, across nine Kharif seasons (2015–2023), and kept two questions apart that are often treated as one. The main question: does SIF depart from its normal-year range before NDVI does in a drought year? The secondary one: does SIF's normal seasonal decline start before NDVI's? The answer to the first is no. The answer to the second depends mostly on how the decline is measured. I then applied every method unchanged to 2001–2014 as an out-of-sample test.

## The Questions

- **RQ1 (main):** In drought years, does SIF depart from its normal-year range before NDVI does? (H4)
- **RQ1b:** Does SIF's post-peak seasonal decline begin before NDVI's? (H1)
- **RQ2:** Does the SIF–NDVI lag differ between districts, and does drought widen it? (H2, H3)
- **RQ3:** How do satellite drought signals time against an approximation of India's rainfall-based Trigger-1 and the official 2015 and 2018 declarations?

## The Method

- **Data:** GOSIF v2 SIF (0.05°, 8-day), weighted by each cell's cropland fraction (MODIS MCD12Q1 classes 12 and 14); MODIS MOD13Q1 NDVI (250 m), quality- and cropland-masked, each composite dated by its pixels' observation day; CHIRPS rainfall as the single rainfall source (1981–2023, baseline 2001–2020). Window: 1 June – 27 December.
- **Drought years:** rainfall z-score below −0.5. Only 2015 and 2018 qualify regionally, under four baselines and every cut-off from −0.3 to −0.75. Against each district's own baseline, 15 of 72 district-years are drought years.
- **Drought signal (main test):** each year's SIF and NDVI standardised against normal years; an alarm is two consecutive composites below a z threshold from 1 July. z < −3 is the only threshold with no false alarm in any normal year at regional scale.
- **Seasonal lead:** threshold-crossing lag at five decline thresholds, with each curve scaled two ways (over the whole season, and from peak to post-peak minimum), plus a double-logistic fit and whole-curve cross-correlation; moving-block bootstrap intervals; region and all 72 district-years.
- **Independent check:** TROPOMI SIF (TROPOSIF v2.1, 2018–2020), a direct retrieval not built from MODIS reflectance.
- **Out-of-sample test:** the same methods, unchanged, on 2001–2014 (five more drought years: 2001, 2002, 2003, 2004, 2014), with anomalies standardised against the normal years of 2001–2014 only.
- **Policy timing:** alarms compared with an approximate rainfall Trigger-1 (deficit > 25% plus a dry spell of at least 21 days between 1 July and 30 September) and with the declaration dates.

## The Findings

**SIF is not an earlier drought alarm than NDVI (H4 not supported).** At z < −3, SIF and NDVI both flagged 2015 on 24 August; in 2018 NDVI flagged on 25 September and SIF on 3 October. Across the 15 drought district-years, SIF flagged 12 and NDVI 13; where both did, they coincided in 6, NDVI was earlier in 5 and SIF in 1. At looser thresholds NDVI was earlier in most cases (13 of 15 at z < −1.5). SIF had slightly fewer false alarms (2 vs 4 among 57 normal district-years).

**The same answer out of sample (2001–2014).** With the methods frozen, the 40 drought district-years of 2001–2014 gave the same district picture: where both indices flagged one, NDVI was earlier in 17 of 22 at z < −1.5 and in all 13 at z < −2; SIF was earlier in 1 and 0. Regionally the vegetation anomalies were weaker, and the result leaned slightly towards SIF: at z < −3 SIF flagged 2001 and 2002, NDVI only 2002 (same date). Over both periods SIF flagged four of seven drought years at z < −3 and NDVI three, and where both did they coincided twice and NDVI was earlier once.

**SIF's apparent seasonal lead depends on normalisation.** Scaled over the whole season, SIF crossed every decline threshold first in all nine years and all 72 district-years. But after the monsoon NDVI stays well above its pre-season level while SIF does not, so this scaling delays NDVI's crossings by construction. Scaled from peak to post-peak minimum, the lead shrinks and disappears in three years:

| Year | Rainfall anomaly | Drought? | Season-scaled lag (days) | Decline-scaled lag (days) | Cross-corr. lag (days) |
|---|---|---|---|---|---|
| 2015 | −21.5% | Yes | +21.7 | +9.6 | +10 |
| 2016 | +9.4% | No | +34.2 | +13.4 | +12 |
| 2017 | −1.1% | No | +28.5 | +10.6 | +14 |
| 2018 | −18.4% | Yes | +8.0 | +3.5 | +4 |
| 2019 | +13.3% | No | +25.4 | −5.5 | 0 |
| 2020 | +29.0% | No | +27.1 | +8.8 | +9 |
| 2021 | +17.3% | No | +20.3 | −1.2 | +20 |
| 2022 | +36.7% | No | +11.8 | −1.0 | −1 |
| 2023 | −3.8% | No | +11.1 | +0.4 | −3 |

Cross-correlation, which does not depend on scaling, agrees more with the decline-scaled lag. TROPOMI put SIF first in all three of its years under both scalings. MODIS NIRv and EVI, from the same composites, also lead NDVI by as much as SIF does (NIRv: 9/9 years, +22.8 days season-scaled, +9.9 decline-scaled), and SIF does not lead NIRv (decline-scaled, first in 0 of 9 years). The remaining lead is a property of NDVI, not of fluorescence. In 2001–2014 the same holds: SIF led NDVI in all 14 years season-scaled (+27.4 days) and NIRv by almost as much (+26.6), and decline-scaled NIRv declined before SIF in 11 of 14 years.

**No district differences once scaling is matched (H2 not supported).** Season-scaled, the lag differs between districts (Friedman p = 0.043); decline-scaled, it does not (p = 0.97; district means 2.9–5.6 days). **Drought does not widen the lag (H3 not supported):** season-scaled, drought years averaged 14.8 days against 22.6; decline-scaled, 6.5 against 3.6 — with two drought years, neither difference means much. In 2001–2014, with five drought years, the lead was again not larger in drought (+28.3 against +26.9 days season-scaled).

## Validation & Robustness Checklist

✓ Out-of-sample test on 2001–2014 with every method unchanged

✓ Independent SIF retrieval (TROPOMI, 2018–2020)

✓ Comparison with MODIS EVI and NIRv from the same composites

✓ Rainfall trigger evaluated per CHIRPS pixel as well as on averaged rainfall

✓ Two normalisations, a double-logistic fit and cross-correlation for the seasonal lag

✓ Moving-block bootstrap intervals for threshold-crossing lags; case bootstrap for cross-correlation

✓ District-level replication across 72 district-years, drought classified against each district's own baseline

✓ Drought classification stable across four rainfall baselines and cut-offs −0.3 to −0.75

✓ NDVI quality-coverage check: lag direction unchanged when composites under 25% clear-pixel coverage are dropped (2022 reverses at a 50% cut-off)

✓ Moran's I and year-clustered / fixed-effects tests for district non-independence

✓ Crop-yield check against official district statistics (drought years −1.08 vs normal +0.07; p = 0.15)

✓ Full pipeline reruns from one script (`run_all.py`)

! SIF is not an earlier drought alarm than NDVI (H4)

! The seasonal lead is largely a normalisation effect; no district differences (H2) and no drought widening (H3)

## Limitation

Only two drought years regionally in 2015–2023 (2015, 2018); the 2001–2014 test adds five, but with weaker vegetation anomalies, so few seasons reach the strict alarm threshold. Decline-scaled leads are mostly shorter than the 16-day NDVI sampling interval. The thresholds were chosen during the study, so the analysis is exploratory. GOSIF uses MODIS reflectance as a predictor; TROPOMI removes that dependence but covers only 2018–2020, and for 2001–2014 GOSIF is predicted outside its OCO-2 training period. Results are regional or district averages at about 5 km over a mixed cropland mask, and districts are spatially clustered. Trigger-1 is approximated on district-averaged rainfall and per CHIRPS pixel, not per taluka. Several data-handling errors in the first preprint are corrected and documented in the Development Log.

## Real World Relevance

The rainfall trigger, as approximated here, never fired for the region and fired in only 2 of 15 drought district-years (Aurangabad and Bid, 2018). Evaluated per CHIRPS pixel, it reached 25% of a district's area only in Aurangabad and Bid 2018 and Bid 2017 (a normal year), and in 2015 it fired in at most 7% of any district. Its deficit component alone fired as often in normal years as in drought years. Where it fired, NDVI's alarm was at least as early as SIF's. Both alarms preceded the 2015 declaration by 52.5 days and the 2018 final declaration by 27.5 (SIF) and 35.5 (NDVI) days, but a declaration follows field verification, so a satellite signal precedes it almost by construction. Satellite vegetation anomalies could add lead time to a rainfall-led trigger; this study gives no reason to prefer SIF over the NDVI already in use.

---

GitHub: [github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI) | Live Dashboard: [greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21762501](https://doi.org/10.5281/zenodo.21762501)

**Sakshi D. Maske**, Independent Geospatial Researcher
