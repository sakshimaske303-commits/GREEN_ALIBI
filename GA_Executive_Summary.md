# GREEN ALIBI
### Testing Whether Fluorescence Catches Drought Stress Before the Eye Can See It

Executive Summary · DOI: 10.5281/zenodo.21762501 · Sakshi D. Maske

## Project Overview

I built GREEN ALIBI to turn a physical hunch into a testable, falsifiable claim: Solar-Induced Fluorescence should catch drought stress before NDVI does, because it tracks a drop in photosynthetic efficiency right away. It does not wait for a leaf's structure to visibly break down. Right now, policy just assumes NDVI is the faster signal, without ever putting that to the test. India's drought declaration process, and the PMFBY crop insurance payout mechanism riding on it, lean on NDVI because it's the established indicator. Nobody has shown proof that it's the fastest one; if SIF really has a physical head start, that gap translates directly into how quickly a stressed farmer gets paid. A single hypothesis felt too thin for this, so I framed the work around 4 research questions: does SIF lead NDVI at all, is that lag geographically consistent, how does it line up against the one official drought declaration I could verify, and is it large enough to matter for insurance timelines? A solid early warning case needs more than 1 line of evidence behind it. The project started as a 3 year pilot (2015, 2018, 2020), and I extended it to 9 growing seasons because 3 years alone did not feel like enough to trust. I reran the full pipeline against the larger sample from scratch: acquisition, boundary definition, lag calculation, all of it. I did not simply bolt new numbers onto old code. That expansion also turned up the biggest finding of all: the original 3 year sample turned out to be 2/3 drought years, far more drought heavy than Marathwada's actual 9 year climate record, exactly the kind of thing a small sample tends to hide. What follows is the result of that harder test, H3 not holding up and 2018 stubbornly refusing to fit the pattern included.

## The Question

India's official drought declaration process, and the PMFBY crop insurance payout mechanism that depends on it, rely substantially on NDVI. NDVI is a reflectance signal that only changes once a plant's structure has already begun to visibly degrade. Solar-Induced Fluorescence (SIF) is grounded in a more direct physical process: a drop in photosynthetic efficiency, before outward greenness changes. Does that physical head start show up at all as a measurable time lag in the satellite record? Does drought severity make that lag bigger, as hypothesized?

## The Method

8 districts of Marathwada, Maharashtra were tested across 9 growing seasons (2015–2023), using GOSIF v2 fluorescence data and cloud screened MODIS NDVI. The study started with 3 years (2015, 2018, 2020); 5 more (2016, 2017, 2019, 2022, 2023) got added to fix the original small sample limitation, and 2021 was added last, its raw SIF data tracked down and processed by hand after the rest of the expansion was already done. The SIF to NDVI decline lag was calculated 2 methodologically distinct ways (not independent — both run on the same underlying SIF/NDVI series, just different math): threshold crossing (linear interpolation at 5 seasonal decline thresholds) and time lagged cross correlation, with 2,000 replicate bootstrap confidence intervals quantifying precision. Rainfall anomaly validation against a 20 year CHIRPS climatology found only 2 of the 9 years (2015, 2018) meet the drought threshold this project set. The other 6 normal years all sit within roughly 1 standard deviation of normal.

## The Finding

SIF's decline precedes NDVI's in 8 of the 9 years under the threshold crossing method. A second, methodologically distinct cross correlation check gives a more mixed picture. A coding mistake affected this result at first: the cross correlation and bootstrap scripts originally searched only non negative lags, so they could never have reported NDVI leading SIF no matter what the data showed. Once that got corrected and rerun, cross correlation shows SIF ahead in 5 years, tied in 1, and NDVI ahead in 3 (2018, 2022, 2023). 2 of those (2022, 2023) are backed by a bootstrap where 99%+ of replicates land below zero. 2018 stands apart as an exception that every method agrees on: its threshold crossing lag is marginally negative, its cross correlation lag is negative too (−4 days), and 87.4% of its bootstrap replicates land below zero. Drought severity still doesn't amplify the threshold crossing lag. The 2 drought years averaged a smaller lag (7.6 days) than the 7 normal years (15.1 days), the same direction as the original 3 year study, now confirmed at nearly triple the sample size.

| Year | Rainfall Anomaly | Threshold Crossing Lag | Cross Corr. Lag |
|---|---|---|---|
| 2015 (drought) | −21.5% | 16.3 days | 4 days |
| 2016 (normal) | +9.5% | 23.8 days | 2 days |
| 2017 (normal) | −1.1% | 21.6 days | 27 days |
| 2018 (drought) | −18.3% | −1.1 days | −4 days |
| 2019 (normal) | +13.3% | 17.2 days | 18 days |
| 2020 (normal) | +29.1% | 20.6 days | 0 days |
| 2021 (normal) | +17.4% | 13.1 days | 14 days |
| 2022 (normal) | +36.8% | 5.1 days | −9 days |
| 2023 (normal) | −3.7% | 4.2 days | −10 days |

H1 (SIF leads NDVI) holds up under threshold crossing in most years, but the cross correlation check, after its bug fix, agrees only on 6 of the 9 years, is an exact tie in 1 (2020), and finds the opposite direction on 2 (2022, 2023) — 2018 is not a reversal between methods, since both threshold crossing and cross correlation independently land on a (marginally, in threshold crossing's case) negative lag there. That disagreement between methods stands as it is, without smoothing it over. H3 (drought amplifies the lag) doesn't survive this test either. This negative result now holds at n = 9 years, up from the earlier n = 3.

## Validation & Robustness Checklist

✓ 2 methodologically distinct lag estimation methods (threshold crossing + cross correlation)

✓ Bootstrap confidence intervals (2,000 replicates per year, all 9 years)

✓ Independent rainfall validation (CHIRPS, 20 year climatological baseline)

✓ Moran's I spatial autocorrelation check (effective sample size given, per year)

✓ Cross referenced against the actual government drought declaration date (2018)

✓ Sample expanded from 3 to 9 years, an actual fix carried out in the work, beyond simply naming the limitation

! H3 (drought amplifies lag) does not hold up in the data

! 2018 breaks the H1 pattern under every single method used here

! Cross correlation and bootstrap both had a coding mistake at first (it searched non negative lags only), fixed and rerun before publishing. See Development Log Entry 17

! Exact year to year ranking is flagged as method sensitive and weak, and for 2022/2023, even the direction of the result is weak too

## Limitation

Only 2 of the 9 years fall under the drought threshold this project set, so the comparison between drought and normal years stays an uneven 2 versus 7 split. Every lag value comes from just 14–18 post peak satellite observations per year, which is why confidence intervals run wide. 32 of the 36 possible pairwise comparisons between years' intervals overlap, meaning most of the exact year to year ranking isn't statistically distinguishable from noise even at 9 years (the 4 pairs that do separate cleanly split the strongest SIF leads years from the strongest NDVI leads years). The SIF rainfall spatial correlation (Pearson r = 0.531, p < 0.0001, n = 72 district years) holds up, though it is noticeably weaker than the r = 0.837 the smaller, drought heavy 3 year sample originally produced. A Moran's I diagnostic also finds SIF's own spatial clustering significant in only 4 of 9 years, against rainfall's, significant in all 9. One coding mistake sat inside the cross correlation and bootstrap scripts too: the lag search only ever checked one direction. This got caught and corrected before publishing, and it mattered, because it changed the actual result (Development Log, Entry 17). The newest year, 2021, was added afterward, once its raw SIF rasters were downloaded and processed separately (Development Log, Entry 20) — it lands squarely in the normal-year range on every check, though its own bootstrap confidence in SIF leading is close to a coin flip rather than strong.

## Real World Relevance

Comparing 2018's SIF and NDVI decline onset against Maharashtra's official drought declaration (31 October 2018) shows both satellite indicators beating the official declaration by roughly 7 to 8 weeks. Once the district boundary naming mistake got caught and corrected during the sample expansion, NDVI now crosses its threshold about 5 days before SIF in 2018, the reverse of the original finding, and in line with 2018 being the one exception throughout. For a rainfall deficit prone farming region, the bigger, more dependable opportunity is satellite based monitoring of either kind arriving 7 or more weeks ahead of the current process, and SIF's own edge over NDVI is a smaller extra bonus on top, one that depends on the year and will not always show up.

---

GitHub: [github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI) | Live Dashboard: [greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21762501](https://doi.org/10.5281/zenodo.21762501)

**Sakshi D. Maske**, Independent Geospatial Researcher
