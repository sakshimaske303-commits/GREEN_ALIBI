# GREEN ALIBI — Policy Brief

**Can satellite fluorescence data speed up drought relief for Marathwada's farmers?**

Sakshi D. Maske · Independent Geospatial Researcher

---

## The Problem

India's drought-management process, and the PMFBY crop-insurance payouts tied to it, rely mainly on rainfall records and on NDVI, a satellite index of how green a crop canopy looks. Both tend to register drought once crop damage is already visible. Declarations then follow a sequence of triggers that ends in field verification of crop damage, so relief and payouts in Marathwada, Maharashtra, often arrive after the season when farmers needed them.

## What This Study Tested

Solar-Induced Fluorescence (SIF) is a faint glow that plants emit during photosynthesis. Because photosynthesis slows under stress before a crop loses its green colour, SIF is often expected to warn of drought earlier than NDVI. I tested this over Marathwada's eight districts across nine Kharif seasons (2015–2023), using GOSIF SIF, MODIS NDVI and CHIRPS rainfall, with a second, independent SIF product (TROPOMI) as a check for 2018–2020. Only 2015 and 2018 were drought years by rainfall; the other seven were normal to wet.

I asked two separate questions:

1. In a drought year, does SIF move away from its normal-year range before NDVI does? This is the question that tells us whether SIF is a better drought alarm.
2. Does SIF's normal end-of-season decline start before NDVI's?

## What Was Found

**SIF is not an earlier drought alarm than NDVI.** When each index was compared with its own behaviour in normal years, SIF did not flag drought first. In 2015 both raised the alarm on the same date (24 August); in 2018 NDVI was eight days earlier (25 September vs 3 October). Across the 15 district-years that were drought years by each district's own rainfall record, the two indices raised the alarm on the same date in 6, NDVI was earlier in 5 and SIF in 1. SIF had slightly fewer false alarms in normal years (2 against NDVI's 4, out of 57).

**SIF's apparent "head start" in the normal season is mostly a measurement effect.** If each curve is scaled over the whole season, SIF's end-of-season decline seems to start one to five weeks before NDVI's in every year. But after the monsoon, NDVI stays well above its pre-season level while SIF does not, and that alone makes NDVI look later. Measured over each index's own decline, the lead shrinks to at most about two weeks and disappears in three of the nine years.

**The rainfall trigger rarely fired.** I approximated the rainfall-based Trigger-1 from India's Manual for Drought Management (rainfall more than 25% below normal plus a dry spell of at least 21 days during the monsoon). Computed on district-average rainfall, it never fired for Marathwada as a whole and fired in only 2 of 15 drought district-years (Aurangabad and Bid, 2018). In Aurangabad both satellite alarms came first (NDVI 23.5 days, SIF 15.5 days earlier); in Bid they came at the same time as the trigger. The rainfall-deficit part alone fired as often in normal years as in drought years.

**Satellite alarms came before the declarations,** by 52.5 days in 2015 and by 27.5 (SIF) to 35.5 (NDVI) days for the final 2018 declaration. This gap is expected, because the declaration comes after field verification, so it should not be read as satellites "beating" the system. The rainfall trigger is the fairer comparison.

**The drought classification matches harvests.** Official crop-yield statistics show lower Kharif yields in the two drought years (Yield Anomaly Index −1.08 vs +0.07), in the expected direction, though not statistically significant with only two drought years.

## The Policy Implication

PMFBY already uses satellite imagery for loss assessment, so the basic infrastructure exists. What this study supports is narrow:

1. **Satellite vegetation anomalies could add lead time to a rainfall-led trigger.** Where the approximated rainfall trigger fired, standardised vegetation anomalies were often already showing drought. This applies to NDVI as much as to SIF.
2. **There is no case here for replacing or supplementing NDVI with SIF for drought warning.** In drought years NDVI raised the alarm at the same time as SIF or earlier, and SIF's apparent seasonal head start is mostly an artefact of how NDVI's decline is measured. SIF's slightly lower false-alarm count is the only advantage seen, and it rests on very few drought years.

## What This Study Does Not Yet Establish

This is a nine-year, single-region study with only two drought years, so every drought-versus-normal result rests on two seasons. The thresholds were chosen during the analysis, so the results are exploratory. The SIF product used (GOSIF) is partly modelled from the same MODIS data as NDVI; the independent TROPOMI check covers only 2018–2020. All results are district or regional averages at about 5 km, not individual farms or crops. The rainfall trigger used here is an approximation of a taluka-level procedure, computed on averaged rainfall. Testing whether any satellite index should formally feed into drought triggers would need more drought years, finer-scale data and crop-specific checks.

---

*Full methodology, statistical detail, and complete limitations: `GA_Research_Paper.md`. Full development history: `GA_Development_Log.md`.*
