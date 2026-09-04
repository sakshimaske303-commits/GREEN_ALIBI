# GREEN ALIBI — Policy Brief

**Can satellite fluorescence data speed up drought relief for Marathwada's farmers?**

Sakshi D. Maske · Independent Geospatial Researcher

---

## The Problem

India's drought declaration and PMFBY crop-insurance payout process relies mainly on rainfall records and NDVI, a satellite index that measures how "green" a crop canopy looks. Both indicators register stress only after visible physical damage has already occurred — by which point the growing season's window for meaningful relief is closing. In Marathwada, Maharashtra, this delay has repeatedly meant drought relief and insurance payouts arriving well after farmers most needed them.

## What This Study Tested

Solar-Induced Fluorescence (SIF) is a satellite-derived signal grounded in the plant's internal photosynthetic process, not its outward appearance. Because photosynthetic efficiency changes before canopy greenness does, SIF should register drought stress earlier than NDVI. This study tested that premise directly and quantitatively — using GOSIF v2 and cloud-screened MODIS NDVI over Marathwada's eight districts, across eight growing seasons (2015–2023, excluding 2021), independently cross-validated against CHIRPS rainfall data. Two of these eight years (2015, 2018) meet this study's own rainfall-anomaly drought threshold; the other six are normal-to-wet monsoon years.

## What Was Found

**SIF leads NDVI in most, but not all, years.** In seven of the eight years studied, SIF's seasonal decline began before NDVI's under the main method used. A second, methodologically distinct check (cross-correlation) agrees in most years but not all: after a search-space bug in the original code was found and fixed — it had been coded to only ever look one direction, so it could never have caught NDVI leading SIF even if the data showed it — the corrected check shows SIF leading in four years, essentially tied in one, and NDVI leading in three (2018, 2022, 2023). **2018 is a genuine exception under every method used**: NDVI actually crosses the key stress threshold slightly *before* SIF that year. This is reported directly rather than averaged away, and the code bug itself is disclosed in full in `GA_Development_Log.md` (Entry 17) rather than quietly patched.

**The exact size of the lead varies by year, and is often a few days, not weeks.** Mean threshold-crossing lags range from about 4 to 24 days depending on the year, with 2018 slightly negative. The two lag-estimation methods agree on direction in most years but not all (2022 and 2023 disagree too), and not always on the exact size or year-to-year ranking.

**The bigger opportunity is elsewhere.** Comparing 2018's satellite signals against the actual date Maharashtra's government officially declared drought (31 October 2018) shows both SIF *and* NDVI crossed their stress thresholds roughly **seven to eight weeks** earlier than the official declaration — even though 2018 is the one year where SIF's edge over NDVI itself disappears. The satellite-versus-declaration gap is real and large regardless of which index is used; SIF's edge over NDVI is a smaller, year-dependent refinement on top of that.

**Drought severity does not simply make the lag bigger.** A natural hypothesis — that more severe drought produces a larger SIF-NDVI gap — was tested directly and was **not supported**, at more than double the original sample size: the two drought years averaged a smaller lag (7.6 days) than the six normal years (15.0 days). This negative result is reported directly, not adjusted or hidden.

**The stress pattern lines up with rainfall independently, though more moderately than an earlier, smaller sample suggested.** District-level SIF stress and rainfall deficit are significantly correlated (Pearson r = 0.567, p < 0.001, across 64 district-year observations), and this correspondence is checked for spatial artifacts via a Moran's I diagnostic: rainfall's spatial clustering is a consistent, year-independent feature (significant in all 8 years), while SIF's spatial clustering is present in only half the years (4 of 8) — a genuine, honestly-reported nuance rather than a uniform result.

## The Policy Implication

PMFBY assessment already incorporates satellite imagery for loss estimation — the operational infrastructure for a satellite-triggered early-warning system already exists in principle. This study's evidence points toward a two-part opportunity, in order of scale:

1. **Larger opportunity:** shortening the roughly seven-to-eight-week gap between when satellite data (of any kind, SIF or NDVI) already shows stress onset and when the official declaration process catches up.
2. **Smaller, additional refinement:** SIF's physiological lead over NDVI, layered on top of that larger improvement — present in most years studied, but not a guarantee in every single season.

## What This Study Does Not Yet Establish

This is an eight-year proof-of-concept, not an operational system. It has not been validated against ground-level crop yield or crop-loss data; it covers one region; the eight years remain unbalanced toward normal conditions (2 drought years versus 6 normal); 2018's exception to the central finding is not yet explained by any available covariate; and GOSIF (the SIF product used) is itself partly modeled from MODIS data, so it is not fully independent of the NDVI it is compared against. These limitations, along with several others, are reported in full in `GA_Research_Paper.md`.

---

*Full methodology, statistical detail, and complete limitations: `GA_Research_Paper.md`. Full development history, including every correction made along the way: `GA_Development_Log.md`.*
