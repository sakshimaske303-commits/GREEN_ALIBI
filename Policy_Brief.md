# GREEN ALIBI — Policy Brief

**Can satellite fluorescence data speed up drought relief for Marathwada's farmers?**

Sakshi D. Maske · Independent Geospatial Researcher

---

## The Problem

India's drought declaration and PMFBY crop-insurance payout process relies mainly on rainfall records and NDVI, a satellite index that measures how "green" a crop canopy looks. Both indicators register stress only after visible physical damage has already occurred — by which point the growing season's window for meaningful relief is closing. In Marathwada, Maharashtra, this delay has repeatedly meant drought relief and insurance payouts arriving well after farmers most needed them.

## What This Study Tested

Solar-Induced Fluorescence (SIF) is a satellite-derived signal grounded in the plant's internal photosynthetic process, not its outward appearance. Because photosynthetic efficiency changes before canopy greenness does, SIF should register drought stress earlier than NDVI. This study tested that premise directly and quantitatively — using GOSIF v2 and cloud-screened MODIS NDVI over Marathwada's eight districts, across two drought years (2015, 2018) and one normal monsoon year (2020), independently cross-validated against CHIRPS rainfall data.

## What Was Found

**SIF leads NDVI, consistently.** Across all three years studied, SIF's seasonal decline began before NDVI's — confirmed by two independent statistical methods, and shown by bootstrap resampling to hold in every resampled scenario tested (100% of 2,000 replicates per year found a non-negative SIF lead).

**The exact size of that lead is a few days, not weeks.** In 2018, SIF crossed a key stress threshold three to four days before NDVI did.

**The bigger opportunity is elsewhere.** Comparing 2018's satellite signals against the actual date Maharashtra's government officially declared drought (31 October 2018) shows both SIF *and* NDVI crossed their stress thresholds roughly **seven weeks** earlier than the official declaration. The three-to-four-day SIF-versus-NDVI edge is real, but it is small next to this much larger, seven-week gap between any satellite signal and the current institutional process.

**Drought severity does not simply make the lag bigger.** A natural hypothesis — that more severe drought produces a larger SIF-NDVI gap — was tested directly and was **not supported**: the two drought years behaved quite differently from each other, and the normal year showed the largest average lag of the three. This negative result is reported directly, not adjusted or hidden.

**The stress pattern lines up with rainfall independently.** District-level SIF stress and rainfall deficit are strongly and significantly correlated (Pearson r = 0.837, p < 0.001), and this correspondence is confirmed to be spatially real via a Moran's I diagnostic, not a byproduct of neighboring districts simply sharing weather.

## The Policy Implication

PMFBY assessment already incorporates satellite imagery for loss estimation — the operational infrastructure for a satellite-triggered early-warning system already exists in principle. This study's evidence points toward a two-part opportunity, in order of scale:

1. **Larger opportunity:** shortening the roughly seven-week gap between when satellite data (of any kind, SIF or NDVI) already shows stress onset and when the official declaration process catches up.
2. **Smaller, additional refinement:** SIF's few-day physiological lead over NDVI, layered on top of that larger improvement.

## What This Study Does Not Yet Establish

This is a three-year proof-of-concept, not an operational system. It has not been validated against ground-level crop yield or crop-loss data; it covers one region; and GOSIF (the SIF product used) is itself partly modeled from MODIS data, so it is not fully independent of the NDVI it is compared against. These limitations, along with several others, are reported in full in `Research_Paper.md`.

---

*Full methodology, statistical detail, and complete limitations: `Research_Paper.md`. Full development history, including every correction made along the way: `Development_Log.md`.*
