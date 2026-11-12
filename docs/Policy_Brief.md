# GREEN ALIBI — Policy Brief
### Drought Triggers and Who Carries a Missed Drought

**Can satellite fluorescence data speed up drought relief for Marathwada's farmers?**

Sakshi D. Maske

---

> **Correction in version 2.2.0: the rainfall trigger.** Earlier versions used my own approximation of the rainfall trigger, which was much stricter than the Manual for Drought Management and flagged only 2 of 15 drought district-years. The trigger now follows the Manual's rule, and the results below use it. The SIF–NDVI comparison, the main result, does not use the trigger and is unchanged.

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

**The Manual's rainfall trigger was early and precise, but missed half the droughts.** I coded the rainfall-based Trigger-1 as India's Manual for Drought Management defines it: a dry spell of four standard weeks after the monsoon's normal onset, each with less than half the normal weekly rain, or very low (scanty) rainfall, or a very low standardised precipitation index. For Marathwada as a whole it fired on 22 July 2015, about five weeks before both satellite alarms, and missed 2018. Across districts it flagged 7 of the 15 drought district-years (10 when applied to each rainfall pixel) and fired in only one of 57 normal ones. Wherever a satellite alarm also fired, the trigger came first, by a median of about three and a half weeks (SIF) to five weeks (NDVI). Most of its misses came in 2018, when the drought built up late in the season. One setting moves all of this: if a dry spell counts after three weeks instead of four, which the Manual allows on light soils, the trigger catches 14 of the 15 droughts but also fires in 26 normal district-years.

**Satellite alarms came before the declarations,** by 52.5 days in 2015 and by 27.5 (SIF) to 35.5 (NDVI) days for the final 2018 declaration. This gap is expected, because the declaration comes after field verification, so it should not be read as satellites "beating" the system. The rainfall trigger is the fairer comparison, and it came first.

**The drought classification matches harvests.** Official crop-yield statistics show lower Kharif yields in the two drought years (Yield Anomaly Index −1.08 vs +0.07), in the expected direction, though not statistically significant with only two drought years (yield data before 2015 were not used for this check).

## The Policy Implication

PMFBY already uses satellite imagery for loss assessment, so the basic infrastructure exists. What this study supports is narrow:

1. **Let the vegetation index raise a drought flag on its own, not only confirm a rainfall flag.** The satellite alarms did not come earlier than the Manual's rainfall trigger. But NDVI flagged seven of the eight drought district-years the trigger missed, and a rule that lets either signal raise the flag caught 14 of 15 with no more false alarms than NDVI alone. Today the Manual lets the vegetation index only confirm what rainfall has flagged. This applies to NDVI as much as to SIF.
2. **The dry-spell rule deserves as much scrutiny as the satellite index.** Whether a dry spell is counted as three or four weeks changes which droughts are recognised far more than the choice between SIF and NDVI.
3. **There is no case here for replacing or supplementing NDVI with SIF for drought warning.** In drought years SIF and NDVI raised the alarm within about eight days of each other, with no consistent winner, and SIF's apparent seasonal head start is mostly an artefact of how NDVI's decline is measured. SIF's slightly lower false-alarm count is the only consistent advantage seen, and it held in both periods.

## Extension: Combining the Signals, What the Errors Cost, and Other Systems

*Added after the preprint; it uses only results already in the study (paper, Appendix A).*

India's Manual uses the signals in a sequence: rainfall first, then impact indicators such as the vegetation index, then field verification. So the vegetation index can only confirm what rainfall has flagged. Scored on the same 72 district-years, the Manual's rainfall trigger flagged 7 of 15 drought district-years (10 per pixel) with one false alarm; NDVI on its own flagged 13 with 4; and rainfall trigger OR NDVI flagged 14, also with 4. Rules that wait for a 25% rainfall deficit flagged only 7 or 8, mainly because the deficit missed Aurangabad 2015 and four of the six drought district-years of 2018. Requiring SIF to confirm NDVI halved the false alarms (2 against 4), but the gain was smaller with NDVI taken as observed and cost detections in the milder droughts of 2001–2014 (2 of 40 against 6). In those milder years the rainfall trigger flagged 11 of 40, more than any satellite rule.

Other systems give the satellite signal different powers. The EU's Combined Drought Indicator uses the same rainfall-first order but only for early warning; Spain's river-basin drought plans use a similar sequence of indices to trigger water measures. The U.S. Livestock Forage Disaster Program pays by county from weekly Drought Monitor ratings, and Kenya's Livestock Insurance Program pays out on an NDVI-based forage index alone, which is fast but leaves basis risk with the herder. In Hood's (1983) terms, satellite data in India's system is a tool of information (nodality), not of authority. In this study the Manual's rainfall trigger flagged 7 to 10 of the 15 rainfall-defined drought district-years and NDVI alone 13, but because those droughts are themselves defined by rainfall, this shows how far the indicators agree, not which one is right; whether the index should gain authority of its own is a design choice it can inform but not settle.

**What the errors cost.** Valued as relief at the SDRF rainfed rate (₹8,500 per hectare), the Manual's rainfall trigger would have withheld about ₹4,200 crore from the eight drought district-years it missed (about ₹2,700 crore per pixel), out of a loss of about ₹25,450 crore of Kharif output in the 15, and paid about ₹560 crore in its one false alarm. Letting NDVI raise the flag as well cuts relief withheld to about ₹530 crore, for about ₹2,300 crore paid in four normal district-years. That combined rule is the cheapest whenever a rupee withheld from a drought-hit district weighs between about 1.2 and 7.9 times a rupee paid in a normal year; at lower weights the rainfall trigger on its own or SIF at a strict threshold is cheaper, and a rule that waits for a rainfall deficit is the cheapest only if a rupee withheld counts for less than about two-fifths of a rupee paid in a normal year. The weight is a value choice. Moving the alarm threshold changes the cost far more than swapping NDVI for SIF.

**Three orders of change.** In Hall's (1993) terms, changing a threshold is a first-order change, adding SIF or changing how signals are combined is second order, and letting a satellite index pay out without field verification, as in Kenya's and Spain's livestock insurance, would change the goal itself, from compensating verified loss to paying fast against an index. This study finds the settings, the alarm threshold and the length of a dry spell, to be the levers with the largest consequences, gives no case for adding SIF, supports letting the vegetation index raise a flag alongside the rainfall trigger (a second-order change), and can inform but not settle the third-order choice.

## What This Study Does Not Yet Establish

This is a single-region study. The main period (2015–2023) has only two drought years; the earlier test (2001–2014) adds five, but most were mild, so the strictest alarm comparisons still rest on few seasons. The thresholds were chosen during the analysis, so the results are exploratory. The SIF product used (GOSIF) is partly modelled from the same MODIS data as NDVI; the independent TROPOMI check covers only 2018–2020. All results are district or regional averages at about 5 km, not individual farms or crops. The rainfall trigger follows the Manual's rule but only approximates a taluka-level procedure: it is computed on averaged rainfall and on each rainfall pixel, with one onset date for the region, and its result depends on how the weeks are counted. Testing whether any satellite index should formally feed into drought triggers would need direct SIF measurements over more drought seasons, finer-scale data and crop-specific checks.

---

*Full methodology, statistical detail, and complete limitations: `GA_Research_Paper.md`. Full development history: `GA_Development_Log.md`.*
