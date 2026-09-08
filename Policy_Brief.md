# GREEN ALIBI — Policy Brief

**Can satellite fluorescence data speed up drought relief for Marathwada's farmers?**

Sakshi D. Maske · Independent Geospatial Researcher

---

## The Problem

India's drought declaration and PMFBY crop-insurance payout process mainly depends on rainfall records and NDVI, a satellite index that shows how "green" a crop canopy looks. Both of these only pick up stress after real physical damage has already happened to the crop, and by then the growing season's window for meaningful relief is closing. In Marathwada, Maharashtra, this delay has meant drought relief and insurance payouts keep arriving late, well after farmers needed them the most.

## What This Study Tested

Solar-Induced Fluorescence (SIF) is a satellite signal that comes from the plant's own photosynthesis process, not how it looks from outside. Photosynthetic efficiency changes before a crop's green color does, so SIF should pick up drought stress earlier than NDVI. This study tested that idea directly, using GOSIF v2 and cloud-screened MODIS NDVI over Marathwada's 8 districts, across 8 growing seasons (2015–2023, skipping 2021), and checked it independently against CHIRPS rainfall data. 2 of these 8 years (2015, 2018) meet this study's own rainfall-anomaly drought threshold; the other 6 are normal-to-wet monsoon years.

## What Was Found

SIF leads NDVI in most years, but not all of them. In 7 of the 8 years studied, SIF's seasonal decline started before NDVI's, under the main method used. A second, different check (cross-correlation) agrees for most years but not all. A bug in the original code turned up here too: it had been written to only ever look in 1 direction, so it could never have shown NDVI leading SIF even if the data actually said so. Once fixed, the corrected check shows SIF leading in 4 years, basically tied in 1, and NDVI leading in 3 (2018, 2022, 2023). 2018 is an exception under every method used: NDVI actually crosses the key stress threshold slightly *before* SIF that year. This is reported directly, not smoothed over, and the code bug itself is written out in full in `GA_Development_Log.md` (Entry 17), not quietly patched and left unmentioned.

The size of the lead changes year to year, and it's often just a few days, not weeks. Mean threshold-crossing lags range from about 4 to 24 days depending on the year, with 2018 slightly negative. The 2 lag-estimation methods agree on direction for most years but not all (2022 and 2023 disagree too), and they don't always agree on the exact size or which year ranks where.

The bigger opportunity is somewhere else. Comparing 2018's satellite signals against the actual date Maharashtra's government officially declared drought (31 October 2018) shows both SIF *and* NDVI crossed their stress thresholds roughly 7 to 8 weeks earlier than the official declaration, even in 2018, the one year where SIF's edge over NDVI itself disappears. This satellite-versus-declaration gap is real and large no matter which index is used. SIF's edge over NDVI is just a smaller, year-dependent extra on top of that.

Drought severity does not simply make the lag bigger. The natural idea here was that a more severe drought would produce a bigger SIF-NDVI gap. This was tested directly, at more than double the original sample size, and it did not hold up: the 2 drought years averaged a smaller lag (7.6 days) than the 6 normal years (15.0 days). This negative result is reported directly, not adjusted or hidden.

The stress pattern lines up with rainfall on its own, though more weakly than an earlier, smaller sample had suggested. District-level SIF stress and rainfall deficit are significantly correlated (Pearson r = 0.567, p < 0.001, across 64 district-year observations), and this was also checked for spatial artifacts using a Moran's I diagnostic. Rainfall's spatial clustering shows up consistently every year (significant in all 8 years), while SIF's spatial clustering only shows up in half the years (4 of 8). This is a real, mixed result, not a uniform one.

## The Policy Implication

PMFBY assessment already uses satellite imagery for loss estimation, so the basic setup for a satellite-triggered early-warning system already exists in principle. This study's evidence points toward a 2-part opportunity, in order of size:

1. **Bigger opportunity:** shortening the roughly 7-to-8-week gap between when satellite data (of any kind, SIF or NDVI) already shows stress starting, and when the official declaration process catches up.
2. **Smaller, extra refinement:** SIF's lead over NDVI, on top of that bigger improvement, present in most years studied, but not guaranteed every single season.

## What This Study Does Not Yet Establish

This is an 8-year proof-of-concept, not a working operational system. It has not been checked against real crop yield or crop-loss data on the ground; it covers just 1 region; the 8 years are still unbalanced toward normal conditions (2 drought years versus 6 normal); 2018's exception to the main finding isn't explained yet by anything checked so far; and GOSIF (the SIF product used) is itself partly modeled from MODIS data, so it isn't fully separate from the NDVI it's being compared against. These limits, and a few more, are reported in full in `GA_Research_Paper.md`.

---

*Full methodology, statistical detail, and complete limitations: `GA_Research_Paper.md`. Full development history, including every correction made along the way: `GA_Development_Log.md`.*
