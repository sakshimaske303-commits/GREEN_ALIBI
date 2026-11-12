# GREEN ALIBI
### Drought Triggers and Who Carries a Missed Drought

Executive Summary · Sakshi D. Maske

## The policy question

In India, drought relief passes through a chain of rules: a rainfall trigger, then impact indicators such as NDVI, then a field check. Each link is a policy instrument with a threshold, and each threshold decides who carries the error when the rule gets it wrong: the farmer whose drought is missed, or the budget that pays out in a normal year. GREEN ALIBI asks whether a newer satellite signal, solar-induced fluorescence (SIF), would move that chain earlier, and what the design of the rules does to who is protected.

## What I found

- **The new sensor did not help.** SIF did not warn of drought earlier than NDVI in Marathwada (8 districts, 2015–2023), and rerunning every method unchanged on 2001–2014 gave the same answer. Most of SIF's apparent seasonal lead comes from how the curves are scaled.
- **The rule matters more than the sensor.** I coded India's rainfall Trigger-1 as the Manual for Drought Management defines it. It flagged 7 of 15 drought district-years (10 per pixel) with one false alarm, weeks before the satellite alarms wherever both fired, and NDVI flagged seven of the eight it missed. Counting a dry spell as three weeks instead of four, which the Manual allows on light soils, the trigger flags 14 but also 26 normal district-years. The definition of a dry spell decides which droughts get recognised far more than the choice between SIF and NDVI.
- **Thresholds move the money.** Pricing each error as relief at the SDRF rate, moving the alarm threshold shifts costs far more than swapping NDVI for SIF. How much a missed drought should weigh against a false alarm is a value judgement the data cannot make for the government.
- **Other systems give satellites more power.** I compared India with the EU's Combined Drought Indicator, Spain's drought plans and pasture insurance, the U.S. Livestock Forage Disaster Program and Kenya's livestock insurance. In Hood's terms, India uses satellite data as information (nodality); in the others it can trigger money directly. Letting a satellite index pay out without a field check would be a change of goals, a third-order change in Hall's sense, and evidence alone cannot settle it.

> **Correction in version 2.2.0: Trigger-1.** Earlier versions used my own approximation of Trigger-1 (a rainfall deficit over 25% plus 21 consecutive days each under 2.5 mm), which is much stricter than the Manual's rule and flagged only 2 of 15 drought district-years. Trigger-1 now follows the Manual (a dry spell of four standard weeks after the normal onset date, each below 50% of normal weekly rainfall, or scanty rainfall, or SPI below −1.5), and the policy timing and the policy extension were rerun with it. The SIF–NDVI comparison, the main result, does not use the trigger and is unchanged.

## About the Project

Solar-Induced Fluorescence (SIF) is linked to photosynthesis, so many people expect it to show crop stress before NDVI, which changes only when the canopy is already damaged. In India, drought declarations, which release relief, depend mainly on rainfall deficits and NDVI; PMFBY crop-insurance claims are settled mainly from crop-cutting yield estimates, not from drought declarations. If SIF gave an earlier warning, relief could reach farmers sooner. I tested this idea in the eight districts of Marathwada, Maharashtra, over nine Kharif seasons (2015–2023). I asked two separate questions. The main one: in a drought year, does SIF move away from its normal-year range before NDVI does? The second one: does SIF's normal end-of-season decline start before NDVI's? For the first question the answer is no. The two drought alarms came within one 8-day composite of each other, and neither index was first every time. For the second question, the answer depends mostly on how the decline is measured. I then ran every method again, without changes, on 2001–2014 as an out-of-sample test.

## Questions

- **RQ1 (main):** In drought years, does SIF move away from its normal-year range before NDVI does? (H4)
- **RQ1b:** Does SIF's decline after the seasonal peak start before NDVI's? (H1)
- **RQ2:** Does the SIF–NDVI lag differ between districts, and does drought widen it? (H2, H3)
- **RQ3:** How do satellite drought signals time against India's rainfall-based Trigger-1 and the official 2015 and 2018 declarations?

## Method

- **Data:** GOSIF v2 SIF (0.05°, 8-day), weighted by how much of each cell is cropland (MODIS MCD12Q1 classes 12 and 14). MODIS MOD13Q1 NDVI (250 m), with bad-quality and non-cropland pixels removed, and each composite dated by the day its pixels were observed. CHIRPS as the only rainfall source (1981–2023, baseline 2001–2020). Time window: 1 June – 27 December.
- **Drought years:** rainfall z-score below −0.5. For the whole region only 2015 and 2018 qualify. This is true under four baselines, and with the main 2001–2020 baseline it holds for every cut-off from −0.3 to −0.75. Against each district's own baseline, 15 of 72 district-years are drought years.
- **Drought alarm (main test):** I compared each year's SIF and NDVI with the normal years. An alarm is two composites in a row below a z threshold, starting from 1 July. For the region, z < −3 is the only threshold with no alarm in any normal year. I also repeated the test using the observed NDVI values in place of NDVI interpolated onto the SIF dates.
- **Seasonal lead:** the lag between SIF and NDVI crossing five decline thresholds. Each curve was scaled in two ways: over the whole season, and from the peak to the low point after the peak. I also used a double-logistic fit, cross-correlation over the post-peak decline, and moving-block bootstrap intervals, for the region and all 72 district-years.
- **Independent check:** TROPOMI SIF (TROPOSIF v2.1, 2018–2020), which is measured directly and does not use MODIS reflectance, compared with NDVI, EVI and NIRv.
- **Out-of-sample test:** the same methods with no changes on 2001–2014, which has five more drought years (2001, 2002, 2003, 2004, 2014). Anomalies here are compared only with the normal years of 2001–2014.
- **Policy timing:** I compared the alarms with the rainfall Trigger-1, coded as the Manual defines it (a dry spell of four standard weeks from the week of 18–24 June, each below 50% of normal weekly rainfall, or scanty rainfall, or SPI below −1.5), on district-average rainfall and in every CHIRPS pixel, and with the official declaration dates.

## Findings

**Main question (H4): not supported.** SIF did not give a clearly earlier drought alarm than NDVI. At z < −3, both flagged 2015 on 24 August. In 2018 NDVI flagged on 25 September and SIF on 3 October, eight days later. There were 15 drought district-years. SIF flagged 12 and NDVI 13. Where both flagged, SIF was earlier in 7, they were on the same date in 2, and NDVI was earlier in 3. In 11 of these 12, the gap was eight days or less. At looser thresholds NDVI was earlier more often (9 against 2 at z < −1.5). NDVI comes only every 16 days, so a gap of eight days is too small to trust. The order also changes with how NDVI is dated. When I used only the NDVI already observed on each date, SIF came first in both regional drought years and in 8 of 12 district-years. SIF gave slightly fewer false alarms (2 against 4, out of 57 normal district-years).

**2001–2014 gives the same answer.** I kept every method the same. Across the 40 drought district-years of 2001–2014, the picture was the same as before. Where both indices flagged a district-year at z < −1.5, SIF was earlier in 5 of 22, NDVI in 6, and 11 were on the same date. At z < −2 the numbers were 0, 6 and 7 of 13. For the whole region the vegetation anomalies were weaker, and the result leaned a little towards SIF. At z < −3 SIF flagged 2001 and 2002, and NDVI flagged only 2002, on the same date. Over both periods together, SIF flagged four of seven drought years at z < −3 and NDVI three. Where both flagged, they were on the same date twice and NDVI was earlier once.

**The seasonal lead (H1) depends on scaling.** When each curve is scaled over the whole season, SIF crossed every decline threshold first in all nine years and all 72 district-years. But after the monsoon NDVI stays well above its pre-season level and SIF does not. This makes NDVI cross the thresholds later, just because of the scaling. When each curve is scaled from its peak to its low point after the peak, the lead gets smaller and is gone in three years:

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

Cross-correlation does not depend on scaling, and it agrees more with the second scaling. MODIS NIRv and EVI, from the same composites, also come before NDVI by about as much as GOSIF does (NIRv: 9 of 9 years, +22.8 days season-scaled, +9.9 decline-scaled). GOSIF does not come before NIRv (decline-scaled, first in 0 of 9 years). So for GOSIF the remaining lead comes from NDVI itself, which is partly expected since GOSIF is built from MODIS reflectance. TROPOMI does not use MODIS data. It put SIF before NDVI in all three of its years under both scalings, and also before NIRv (by 1–13 days). Three years are too few to call this a fluorescence lead, and I leave that question open. 2001–2014 shows the same thing. Season-scaled, SIF came before NDVI in all 14 years (+27.4 days) and NIRv by almost the same (+26.6). Decline-scaled, NIRv declined before SIF in 11 of 14 years.

**Districts (H2): not supported.** Season-scaled, the lag differs between districts (Friedman p = 0.043). Decline-scaled, it does not (p = 0.97; district means 2.9–5.6 days).

**Drought and the lag (H3): not supported.** Season-scaled, drought years averaged 14.8 days against 22.6 in normal years. Decline-scaled, it was 6.5 against 3.6. With only two drought years, these differences do not tell us much. In 2001–2014, with five drought years, the lead was again not larger in drought years (+28.3 against +26.9 days season-scaled).

## Checks I Ran

- Ran every method again on 2001–2014 with no changes
- Compared with a second SIF product (TROPOMI, 2018–2020), also against NIRv and EVI
- Repeated the alarm test with observed NDVI in place of interpolated NDVI
- Compared with MODIS EVI and NIRv from the same composites
- Ran the rainfall trigger in every CHIRPS pixel as well as on district-average rainfall, with a three-week dry spell, with weeks counted from July, and on 2001–2014
- Measured the seasonal lag in four ways: two scalings, a double-logistic fit and cross-correlation
- Bootstrap intervals for all lags (moving-block for threshold crossing, case resampling for cross-correlation)
- Repeated the analysis for all 72 district-years, with drought judged against each district's own rainfall
- Checked the drought years with four rainfall baselines (and cut-offs from −0.3 to −0.75 with the main baseline)
- Checked NDVI cloud cover: the lag direction stays the same when composites with under 25% clear pixels are removed (2022 flips with a 50% cut-off)
- Moran's I, plus year-clustered and fixed-effects tests, because nearby districts are not independent
- Checked against official district crop yields (drought years −1.08 vs normal +0.07; p = 0.15)
- The whole pipeline runs from one script (`run_all.py`)

None of these checks changed the two main answers: SIF was not a clearly earlier drought alarm than NDVI (H4), with the alarms mostly eight days apart or less, and GOSIF's seasonal lead comes mostly from the scaling and from NDVI itself, with no district differences (H2) and no larger lag in drought years (H3).

## Limitations

For the whole region there were only two drought years in 2015–2023 (2015, 2018). The 2001–2014 test adds five, but their vegetation anomalies were weaker, so few seasons reach the strict alarm threshold. Most decline-scaled leads and most gaps between the SIF and NDVI alarms are shorter than NDVI's 16-day sampling. I chose the thresholds during the study, so the analysis is exploratory. GOSIF uses MODIS reflectance as an input. TROPOMI does not, but it covers only 2018–2020, and for 2001–2014 GOSIF is predicted outside its OCO-2 training period. All results are regional or district averages at about 5 km over a mixed cropland mask, and nearby districts are similar to each other. I computed Trigger-1 on district-average rainfall and per CHIRPS pixel, with one onset date for the region, while the state applies it per taluka; its result depends on the dry-spell length and on how the weeks are aligned. The first preprint had several data-handling errors. They are fixed here and listed in the Development Log.

## What This Means for Drought Policy

Coded as the Manual defines it, the rainfall trigger fired for the whole region on 22 July 2015, about five weeks before both satellite alarms and 86 days before the declaration, and in no other year of 2015–2023, including 2018. At district level it flagged 7 of 15 drought district-years (six districts in 2015, Aurangabad in 2018) and one of 57 normal ones (Aurangabad 2023). Run in each CHIRPS pixel, it covered at least a quarter of the district in 10 drought district-years and the same one normal one. Wherever a satellite alarm also fired, the trigger came first: SIF by a median of 25.5 days and NDVI by 33.5 days. Its weakness is coverage: it missed eight drought district-years, five of them in the late-building 2018 drought, and NDVI flagged seven of those eight. So in this region the vegetation index is most useful as a second route to a drought flag, not as an earlier warning. With a three-week dry spell the trigger flags 14 droughts but also 26 normal district-years. Both satellite alarms came 52.5 days before the 2015 declaration, and 27.5 (SIF) and 35.5 (NDVI) days before the 2018 final declaration; because a declaration comes only after field checks, a satellite signal will nearly always come before it. This study gives no reason to choose GOSIF SIF over the NDVI that is already used.

## Policy Extension: Trigger Design, Its Costs and Other Systems

After the preprint I added Appendix A to the paper. It uses only alarm and trigger dates already in the study and changes no main result.

**Combining the signals.** India's Manual uses rainfall as a gate: the vegetation index is looked at only after Trigger-1 fires, and field verification decides. I scored combined rules on the same 72 district-years. The Manual's Trigger-1 flagged 7 (10 per pixel), all by 30 September, with one false alarm. NDVI on its own flagged 13 with 4 false alarms. Letting either raise the flag, Trigger-1 OR NDVI, flagged 14 with no more false alarms than NDVI (4). Rules that wait for a 25% rainfall deficit flagged only 7 or 8. I do not read the misses as droughts the Manual misses: the 15 droughts are themselves defined by rainfall, so the gaps are between indicators. Requiring SIF to confirm NDVI halved the false alarms (2 against 4) but did not hold up in 2001–2014, where it flagged 2 of 40 milder drought district-years against 6 for NDVI alone. In those years the rainfall trigger flagged 11 of 40.

**What the errors cost.** I valued each error as the relief it moves, at the SDRF rainfed rate of ₹8,500 per hectare: relief withheld when a drought is missed, relief paid when a normal year is flagged. The 15 drought district-years lost about ₹25,450 crore of Kharif output at 2022–23 support prices; relief at the SDRF rate would have covered 31% of it, and the Manual's rainfall trigger would have withheld ₹4,177 crore from the eight it missed (₹2,657 crore per pixel), while its one false alarm paid ₹562 crore. Adding NDVI as a second route cuts relief withheld to ₹526 crore. Trigger-1 OR NDVI is the cheapest rule whenever a rupee withheld from a drought-hit district weighs between about 1.2 and 7.9 times a rupee paid in a normal year (2.3 to 7.7 if only flags by 30 September count); the per-pixel trigger alone is cheapest at lower weights if only flags by 30 September count. A rule that waits for the rainfall deficit is the cheapest only if a rupee withheld counts for less than about two-fifths of a rupee paid in a normal year. Setting that weight is a value judgement. Moving the alarm threshold changes the cost far more than swapping NDVI for SIF.

**Other systems.** I compared India's design with the EU Combined Drought Indicator, Spain's river-basin drought plans and pasture-loss insurance, the U.S. Livestock Forage Disaster Program and the Kenya Livestock Insurance Program. The EU indicator and the Spanish basin plans use sequences of indices for warning and water measures; the U.S., Kenyan and Spanish insurance schemes pay directly against an index, and leave basis risk with the farmer. In Hood's (1983) terms, satellite data in India's system is a tool of information, not of authority.

**Three orders of change.** In Hall's (1993) terms, changing a threshold is a first-order change, adding SIF or changing how signals combine is second order, and letting a satellite index pay out without field verification would be third order, a change of goal from compensating verified loss to paying fast against an index. My results speak to the first two; the third is a political choice that this study can inform but not settle.

---

GitHub: [github.com/sakshimaske303-commits/GREEN_ALIBI](https://github.com/sakshimaske303-commits/GREEN_ALIBI) | Live Dashboard: [greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app](https://greenalibi-bzs2wvod5fflqh7dfe2cf4.streamlit.app)

**Sakshi D. Maske**
