# GREEN ALIBI
### Testing Whether Fluorescence Catches Drought Stress Before the Eye Can See It

Executive Summary · DOI: 10.5281/zenodo.21762501 · Sakshi D. Maske

## Project Overview

I built GREEN ALIBI to turn a physical hunch — that Solar-Induced Fluorescence should catch drought stress before NDVI does, because it tracks a drop in photosynthetic efficiency directly instead of waiting for a leaf's structure to visibly break down — into a testable, falsifiable claim rather than something policy just assumes. India's drought-declaration process, and the PMFBY crop-insurance payout mechanism riding on it, lean on NDVI because it's the established indicator, not because anyone has actually shown it's the fastest one; if SIF really has a physical head start, that gap translates directly into how quickly a stressed farmer gets paid. I framed the work around three research questions instead of a single hypothesis — does SIF actually lead NDVI, is that lag geographically consistent, and how does SIF-based stress timing relate to independently measured rainfall deficit across drought and normal years — because a genuine early-warning case needs more than one line of evidence behind it. The project started as a three-year pilot (2015, 2018, 2020), and I extended it to eight growing seasons specifically because three years wasn't enough to trust, re-running the full pipeline — acquisition, boundary definition, lag calculation — against the larger sample instead of just bolting new numbers onto old code. That expansion also surfaced this study's most important finding about itself: the original three-year sample turned out to be two-thirds drought years, far more drought-heavy than Marathwada's actual eight-year climate record, exactly the kind of thing a small sample tends to hide. What follows is the result of that harder test, H3 not holding up and 2018 stubbornly refusing to fit the pattern included.

## The Question

India's official drought-declaration process, and the PMFBY crop-insurance payout mechanism that depends on it, rely substantially on NDVI — a reflectance signal that only changes once a plant's structure has already begun to visibly degrade. Solar-Induced Fluorescence (SIF) is grounded in a more direct physical process: a drop in photosynthetic efficiency, before outward greenness changes. Does that physical head-start actually show up as a measurable time lag on real satellite data — and does drought severity make that lag bigger, as hypothesized?

## The Method

Eight districts of Marathwada, Maharashtra were tested across eight growing seasons (2015–2023, excluding 2021), using GOSIF v2 fluorescence data and cloud-screened MODIS NDVI. The study started with three years (2015, 2018, 2020); five more (2016, 2017, 2019, 2022, 2023) were added later specifically to fix the original small-sample limitation. The SIF-to-NDVI decline lag was calculated two independent ways — threshold-crossing (linear-interpolation at 5 seasonal decline thresholds) and time-lagged cross-correlation — with 2,000-replicate bootstrap confidence intervals quantifying precision. Rainfall-anomaly validation against a 20-year CHIRPS climatology found only 2 of the 8 years (2015, 2018) actually meet this study's own drought threshold — the other 5 added years all sit within roughly one standard deviation of normal.

## The Finding

SIF's decline precedes NDVI's in 7 of the 8 years under the threshold-crossing method. A second, methodologically distinct cross-correlation check gives a more mixed picture — and this section itself was rewritten after fixing a real bug: the cross-correlation and bootstrap scripts originally searched only non-negative lags, so they could never have reported NDVI leading SIF no matter what the data showed. Once fixed and rerun, cross-correlation shows SIF clearly leading in 4 years, a tie in 1, and NDVI clearly leading in 3 (2018, 2022, 2023) — 2 of those (2022, 2023) backed by a bootstrap where 99%+ of replicates land below zero. 2018 is a genuine, multiply-confirmed exception across every method: its threshold-crossing lag is marginally negative, its cross-correlation lag is clearly negative (−4 days), and 87.4% of its bootstrap replicates land below zero. Drought severity still doesn't amplify the threshold-crossing lag: the two drought years averaged a smaller lag (7.6 days) than the six normal years (15.0 days) — the same direction as the original 3-year study, now confirmed at more than double the sample size.

| Year | Rainfall Anomaly | Threshold-Crossing Lag | Cross-Corr. Lag |
|---|---|---|---|
| 2015 (drought) | −21.5% | 16.3 days | 4 days |
| 2016 (normal) | +9.5% | 23.8 days | 2 days |
| 2017 (normal) | −1.1% | 21.6 days | 27 days |
| 2018 (drought) | −18.3% | −1.1 days | −4 days |
| 2019 (normal) | +13.3% | 17.2 days | 18 days |
| 2020 (normal) | +29.1% | 20.6 days | 0 days |
| 2022 (normal) | +36.8% | 5.1 days | −9 days |
| 2023 (normal) | −3.7% | 4.2 days | −10 days |

H1 (SIF leads NDVI) holds up under threshold-crossing in most years, but the cross-correlation check — after its bug fix — agrees only on 5 of the 8 years and finds the opposite direction on 3 (2018, 2022, 2023). That disagreement between methods is now reported as a real finding, not smoothed over. H3 (drought amplifies the lag) is reported plainly as not supported — a real non-result, confirmed at n = 8 years rather than just n = 3.

## Validation & Robustness Checklist

✓ Two methodologically distinct lag-estimation methods (threshold-crossing + cross-correlation)

✓ Bootstrap confidence intervals (2,000 replicates per year, all 8 years)

✓ Independent rainfall validation (CHIRPS, 20-year climatological baseline)

✓ Moran's I spatial-autocorrelation check (effective sample size disclosed, per year)

✓ Cross-referenced against the real government drought-declaration date (2018)

✓ Sample expanded from 3 to 8 years — a real, executed fix, not just a stated limitation

! H3 (drought amplifies lag) — honestly reported as not supported

! 2018 is a consistent exception to H1 across every method — reported, not hidden

! Cross-correlation and bootstrap both had a real search-space bug (non-negative lags only) — found, fixed, and rerun before publishing; see Development Log Entry 17

! Exact year-to-year ranking flagged as method-sensitive, not robust — and for 2022/2023, so is the direction

## Honest Limitation

Only 2 of 8 years meet this study's own drought threshold, so the drought-vs-normal comparison stays a 2-versus-6 split, not a balanced one. Every lag value is a point estimate from just 14–18 post-peak satellite observations per year, so confidence intervals run wide — 24 of the 28 possible pairwise comparisons between years' intervals overlap, meaning most of the exact year-to-year ranking isn't statistically distinguishable from noise even at 8 years (the 4 pairs that do come apart cleanly separate the strongest SIF-leads years from the strongest NDVI-leads years). The SIF-rainfall spatial correlation (Pearson r = 0.567, p < 0.0001, n = 64 district-years) is real but noticeably weaker than the r = 0.837 the smaller, drought-heavy 3-year sample originally produced, and a Moran's I diagnostic finds SIF's own spatial clustering significant in only 4 of 8 years, against rainfall's, significant in all 8. A real bug in the cross-correlation and bootstrap scripts — a lag search that only ever looked one direction — was found and fixed before this paper went out; it's disclosed in full rather than quietly patched, because it changed a real finding (Development Log, Entry 17).

## Real-World Relevance

Comparing 2018's SIF and NDVI decline onset against Maharashtra's official drought declaration (31 October 2018) shows both satellite indicators beating the official declaration by roughly seven to eight weeks. After a district-boundary naming bug was found and fixed during the sample expansion, NDVI now crosses its threshold about five days before SIF in 2018 specifically — the reverse of the original finding, and in line with 2018 being this study's one exception throughout. For a rainfall-deficit-prone farming region, the bigger, more dependable opportunity is satellite-based monitoring of either kind arriving seven-plus weeks ahead of the current process, with SIF's own edge over NDVI a smaller, year-dependent bonus on top — not a guaranteed one.

---

GitHub: [github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI) | Live Dashboard: [greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21762501](https://doi.org/10.5281/zenodo.21762501)

**Sakshi D. Maske** — Independent Geospatial Researcher
