# GREEN ALIBI — Policy Brief
### Drought Triggers and Who Carries a Missed Drought

**Can satellite fluorescence data speed up drought relief for Marathwada's farmers?**

Sakshi D. Maske · Independent Geospatial Researcher

---

> **Correction in progress: Trigger-1 and the rainfall-gate comparison.** A check of my code showed that my Trigger-1 approximation (rainfall deficit over 25% plus 21 consecutive days each under 2.5 mm) is much stricter than the Manual's dry spell (3–4 consecutive weeks, each below 50% of normal weekly rainfall). Every Trigger-1 result in this project describes my approximation, not the Manual's rule. The comparison of rainfall-gated rules also scores them against drought district-years that are themselves defined by rainfall, so it shows how far the indicators disagree, not droughts that the Manual would miss. I am re-specifying the trigger and will rerun RQ3 and Appendix A. The SIF–NDVI comparison, the main result, does not use the trigger and is not affected.

## The Problem

India's drought-management process relies mainly on rainfall records and on NDVI, a satellite index of how green a crop canopy looks. (PMFBY crop-insurance claims are settled mainly from crop-cutting yield estimates, not from drought declarations.) Both tend to register drought once crop damage is already visible. Declarations then follow a sequence of triggers that ends in field verification of crop damage, so relief and payouts in Marathwada, Maharashtra, often arrive after the season when farmers needed them.

## What This Study Tested

Solar-Induced Fluorescence (SIF) is a faint glow that plants emit during photosynthesis. Because photosynthesis slows under stress before a crop loses its green colour, SIF is often expected to warn of drought earlier than NDVI. I tested this over Marathwada's eight districts across nine Kharif seasons (2015–2023), using GOSIF SIF, MODIS NDVI and CHIRPS rainfall, with a second, independent SIF product (TROPOMI) as a check for 2018–2020. Only 2015 and 2018 were drought years by rainfall; the other seven were normal to wet. To get more drought years, I then repeated every test, without changing anything, on 2001–2014, which has five more drought years.

I asked two separate questions:

1. In a drought year, does SIF move away from its normal-year range before NDVI does? This is the question that decides whether SIF is a better drought alarm.
2. Does SIF's normal end-of-season decline start before NDVI's?

## What Was Found

**SIF is not a clearly earlier drought alarm than NDVI.** When each index was compared with its own behaviour in normal years, the two raised the alarm within about eight days (one 8-day step) of each other. In 2015 both raised the alarm on the same date (24 August); in 2018 NDVI was eight days earlier (25 September vs 3 October). Across the 15 district-years that were drought years by each district's own rainfall record, SIF was earlier in 7, the two were on the same date in 2 and NDVI was earlier in 3, almost always by a single 8-day step. NDVI is only measured every 16 days, so a one-step difference cannot tell which index really moved first. SIF had slightly fewer false alarms in normal years (2 against NDVI's 4, out of 57).

**The earlier years give the same answer.** In 2001–2014, across 40 district-years that were drought years, neither index was consistently first: where both flagged the drought at a moderate threshold, SIF was earlier in 5, NDVI in 6, and 11 were on the same date. For the region as a whole these droughts were milder, and SIF flagged one of them (2001) that NDVI did not at the strictest threshold; in the other flagged year (2002) both raised the alarm on the same date.

**SIF's apparent "head start" in the normal season is mostly a measurement effect.** If each curve is scaled over the whole season, SIF's end-of-season decline seems to start one to five weeks before NDVI's in every year. But after the monsoon, NDVI stays well above its pre-season level while SIF does not, and that alone makes NDVI look later. Measured over each index's own decline, the lead shrinks to at most about two weeks and disappears in three of the nine years. Two other greenness indices from the same satellite (EVI and NIRv) show the same "head start" over NDVI, and the main SIF product is not ahead of them, so most of the head start comes from NDVI. The independent TROPOMI product was slightly ahead of NIRv in its three years, too few to say more.

**My approximation of the rainfall trigger rarely fired.** I approximated the rainfall-based Trigger-1 from India's Manual for Drought Management (rainfall more than 25% below normal plus 21 consecutive days each under 2.5 mm during the monsoon). This is much stricter than the Manual's dry spell (3–4 consecutive weeks, each below 50% of normal weekly rainfall), so these results describe my approximation, and I am re-specifying it. Computed on district-average rainfall, it never fired for Marathwada as a whole and fired in only 2 of 15 drought district-years (Aurangabad and Bid, 2018). In Aurangabad both satellite alarms came 15.5 days before the trigger; in Bid they came at about the same time (SIF half a day after, NDVI about a week after). Applied to each rainfall pixel instead of district averages, the picture is the same: in 2015, the stronger drought year, it fired in at most 7% of any district. The rainfall-deficit part alone fired in more normal district-years than drought ones (18 against 10) and missed the 2018 drought for the region as a whole.

**Satellite alarms came before the declarations,** by 52.5 days in 2015 and by 27.5 (SIF) to 35.5 (NDVI) days for the final 2018 declaration. This gap is expected, because the declaration comes after field verification, so it should not be read as satellites "beating" the system. The rainfall trigger is the fairer comparison.

**The drought classification matches harvests.** Official crop-yield statistics show lower Kharif yields in the two drought years (Yield Anomaly Index −1.08 vs +0.07), in the expected direction, though not statistically significant with only two drought years (yield data before 2015 were not used for this check).

## The Policy Implication

PMFBY already uses satellite imagery for loss assessment, so the basic infrastructure exists. What this study supports is narrow:

1. **Satellite vegetation anomalies could add lead time to a rainfall-led trigger.** Where the approximated rainfall trigger fired, standardised vegetation anomalies were already showing drought or showed it at about the same time. This applies to NDVI as much as to SIF.
2. **There is no case here for replacing or supplementing NDVI with SIF for drought warning.** In drought years SIF and NDVI raised the alarm within about eight days of each other, with no consistent winner, and SIF's apparent seasonal head start is mostly an artefact of how NDVI's decline is measured. SIF's slightly lower false-alarm count is the only consistent advantage seen, and it held in both periods.

## Extension: Combining the Signals, What the Errors Cost, and Other Systems

*Added after the preprint; it uses only results already in the study (paper, Appendix A).*

India's Manual uses the signals in a sequence: rainfall first, then impact indicators such as the vegetation index, then field verification. So the vegetation index can only confirm what rainfall has flagged. Scored on the same 72 district-years, no combined rule flagged more drought district-years than NDVI on its own (13 of 15, 4 false alarms). Rules that wait for the rainfall deficit flagged only 7 or 8 of 15, mainly because the deficit missed Aurangabad 2015 and four of the six drought district-years of 2018. Requiring SIF to confirm NDVI halved the false alarms (2 against 4), but the gain was smaller with NDVI taken as observed and cost detections in the milder droughts of 2001–2014 (2 of 40 against 6). Even the best rules flagged only 9 of the 15 by 30 September.

Other systems give the satellite signal different powers. The EU's Combined Drought Indicator uses the same rainfall-first order but only for early warning; Spain's river-basin drought plans use a similar sequence of indices to trigger water measures. The U.S. Livestock Forage Disaster Program pays by county from weekly Drought Monitor ratings, and Kenya's Livestock Insurance Program pays out on an NDVI-based forage index alone, which is fast but leaves basis risk with the herder. In Hood's (1983) terms, satellite data in India's system is a tool of information (nodality), not of authority. In this study, rules that wait for the rainfall deficit flagged 7–8 of the 15 rainfall-defined drought district-years, against 13 for NDVI alone, but because those droughts are themselves defined by rainfall, this shows how far the indicators disagree, not droughts the Manual would miss; whether the index should gain authority of its own is a design choice it can inform but not settle.

**What the errors cost.** Valued as relief at the SDRF rainfed rate (₹8,500 per hectare), my strict approximation of the rainfall trigger would have withheld about ₹6,600 crore from the 15 drought district-years (to be recomputed with the corrected rule), which lost about ₹25,450 crore of Kharif output. A rule that waits for rainfall is the cheapest only if a rupee withheld from a drought-hit district counts for less than half a rupee paid in a normal year. Which satellite rule is cheapest then depends on that weight, a value choice: SIF at a strict threshold when the budget weighs most (an advantage resting on two false alarms), NDVI at the same threshold when drought-hit farmers count about two to four times as much, and a looser NDVI threshold beyond that. Moving the threshold changes the cost far more than swapping NDVI for SIF.

**Three orders of change.** In Hall's (1993) terms, changing a threshold is a first-order change, adding SIF or changing how signals are combined is second order, and letting a satellite index pay out without field verification, as in Kenya's and Spain's livestock insurance, would change the goal itself, from compensating verified loss to paying fast against an index. This study finds the threshold to be the lever with the largest cost consequences, gives no case for adding SIF, and can inform but not settle the third-order choice.

## What This Study Does Not Yet Establish

This is a single-region study. The main period (2015–2023) has only two drought years; the earlier test (2001–2014) adds five, but most were mild, so the strictest alarm comparisons still rest on few seasons. The thresholds were chosen during the analysis, so the results are exploratory. The SIF product used (GOSIF) is partly modelled from the same MODIS data as NDVI; the independent TROPOMI check covers only 2018–2020. All results are district or regional averages at about 5 km, not individual farms or crops. The rainfall trigger used here is an approximation of a taluka-level procedure, computed on averaged rainfall and on each rainfall pixel. Testing whether any satellite index should formally feed into drought triggers would need direct SIF measurements over more drought seasons, finer-scale data and crop-specific checks.

---

*Full methodology, statistical detail, and complete limitations: `GA_Research_Paper.md`. Full development history: `GA_Development_Log.md`.*
