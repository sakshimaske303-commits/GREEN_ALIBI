import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Findings & Conclusion — GREEN ALIBI", page_icon="📝", layout="wide")
apply_custom_style()

st.title("📝 Key Findings, Limitations & Conclusion")

st.markdown("""
I kept two questions apart that are often treated as one. **(a)** In a drought year, does
SIF depart from its normal-year range before NDVI does? This is the main question, because
only it would make SIF a better drought alarm. **(b)** Does SIF's normal seasonal decline
start before NDVI's?
""")

section_divider()

st.header("(a) Drought-Specific Alarm: SIF Is Not Earlier")

st.image("outputs/figures/drought_signal_anomaly_curves.png", use_container_width=True)
styled_caption(
    "Standardised SIF and NDVI anomalies relative to normal years, by composite date; "
    "2015 red, 2018 orange, normal years grey; dashed line = alarm threshold z = −3."
)

st.markdown("""
I standardised each year's SIF and NDVI against the normal years at each composite date
(z-score) and set an alarm at the first date from 1 July with two consecutive composites
below a threshold. At the regional scale, z < −3 is the only threshold at which neither
index raises an alarm in any normal year, so it is the main alarm threshold. District-years
are classified against each district's own rainfall record.
""")

st.warning("""
**H4 — not supported.**

- **Region (z < −3):** in 2015 SIF and NDVI both raised the alarm on 24 August. In 2018
  NDVI did so on 25 September and SIF on 3 October, eight days later.
- **Districts (15 drought, 57 normal district-years, z < −3):** SIF flagged 12 and NDVI 13
  of the 15 drought district-years. False alarms: SIF 2, NDVI 4. Where both flagged, they
  coincided in 6, NDVI was earlier in 5 and SIF in 1.
- **Looser thresholds:** at z < −1.5 NDVI was earlier in 13 of 15; at z < −2, in 10 of 14.
- **AUC by date:** both separate drought from normal district-years from 23 July (AUC ≥ 0.75).
  SIF's AUC is slightly higher until early August, NDVI's from 24 August to 19 October.

SIF's only edge is slightly fewer false alarms; it does not give an earlier drought alarm.
""")

section_divider()

st.header("(b) Seasonal Decline: Mostly a Scaling Effect")

st.image("outputs/figures/normalisation_sensitivity.png", use_container_width=True)
styled_caption("Regional SIF–NDVI lag by year: season-scaled, decline-scaled, and double-logistic end of season.")

st.info("""
**H1 — depends on how the decline is measured.** Scaled from each year's seasonal minimum
to its peak, SIF crossed every decline threshold first in all nine years: 21.7 days (2015),
34.2 (2016), 28.5 (2017), 8.0 (2018), 25.4 (2019), 27.1 (2020), 20.3 (2021), 11.8 (2022)
and 11.1 (2023), and in all 72 district-years. But after the monsoon NDVI stays well above
its pre-season level (0.23–0.59 on that scale, against 0.00–0.28 for SIF), so its crossings
are delayed by construction. Scaled from peak to post-peak minimum, the lag is 9.6, 13.4,
10.6, 3.5, −5.5, 8.8, −1.2, −1.0 and 0.4 days: SIF first in six years, NDVI in 2019, 2021
and 2022.
""")

st.info("""
**Cross-correlation and TROPOMI.** Whole-curve cross-correlation, which does not depend on
scaling, gives 10, 12, 14, 4, 0, 9, 20, −1 and −3 days, closer to the decline-scaled
estimate. TROPOMI SIF (2018–2020), not built from MODIS reflectance, put SIF first in all
three years under both scalings (decline-scaled 10.4, 10.3 and 27.7 days), so a small lead
may remain.
""")

st.image("outputs/figures/district_lag_by_year.png", use_container_width=True)
styled_caption("Season-scaled SIF–NDVI lag by district and year.")

st.warning("""
**H2 — not supported.** Season-scaled, the lag differs between districts (Friedman
p = 0.043). Decline-scaled, it does not (p = 0.97; district means 2.9–5.6 days), so the
apparent district differences come from how far NDVI stays up after the season.
""")

st.warning("""
**H3 (exploratory) — not supported.** Drought did not widen the lag: drought years averaged
14.8 days against 22.6 for normal years season-scaled, and 6.5 against 3.6 decline-scaled.
With two drought years neither difference means much.
""")

section_divider()

st.header("RQ3: Rainfall Trigger and Declarations")

st.image("outputs/figures/rq3_declaration_timeline.png", use_container_width=True)
styled_caption("2015 and 2018: satellite drought alarms (z < −3), the rainfall trigger and the declaration dates.")

st.info("""
**Rainfall Trigger-1 (approximation).** I approximated the Manual for Drought Management
(2016) Trigger-1 as cumulative rainfall since 1 June more than 25% below normal plus a dry
spell of at least 21 days between 1 July and 30 September. On averaged rainfall it never
fired for the region. At district level it fired in 2 of 15 drought district-years
(Aurangabad and Bid, 2018) and one normal one (Bid 2017). In Aurangabad, NDVI's alarm came
23.5 days and SIF's 15.5 days before the trigger; in Bid both came at the same time.
""")

st.info("""
**Official declarations.** The z < −3 alarms came 52.5 days before the 2015 declaration
(reported 16 October) for both indices; 27.5 days (SIF) and 35.5 days (NDVI) before the
2018 final declaration (31 October); and 19.5 and 27.5 days before the 2018 first-stage
declaration (23 October).
""")

st.warning("""
A declaration comes at the end of a sequence of triggers that ends in field verification of
crop damage, so a satellite signal will precede it almost by construction. The more
meaningful benchmark is the rainfall trigger, and there NDVI's anomaly was at least as early
as SIF's in both cases where it fired.
""")

section_divider()

st.header("Study at a Glance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("H4 SIF earlier drought alarm", "Not supported")
with c2:
    st.metric("SIF first, decline-scaled", "6 / 9 years")
with c3:
    st.metric("SIF first, season-scaled", "9 / 9 years")
with c4:
    st.metric("Rainfall-defined drought years", "2 / 9")

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("H2 district differences", "Not supported")
with c6:
    st.metric("H3 drought widens lag", "Not supported")
with c7:
    st.metric("Trigger-1 fired (drought district-years)", "2 / 15")
with c8:
    st.metric("Alarms before final declarations", "27–53 days")

section_divider()

st.header("Limitations")

st.markdown("""
- **Two drought years.** Only 2015 and 2018 meet the regional drought criterion, under every
  baseline and cut-off from −0.3 to −0.75. Extending the record to 2001–2014 would add at
  least five drought years.
- **Normalisation dependence.** The seasonal lead depends on how each curve is scaled; the
  double-logistic fits that could give a third estimate are unstable at 8- and 16-day sampling.
- **Lag size and sampling.** GOSIF is 8-day and MOD13Q1 16-day; decline-scaled leads are
  mostly shorter than the NDVI sampling interval.
- **NDVI coverage.** Many monsoon NDVI composites rest on few clear pixels; the lag direction
  does not change when they are dropped.
- **Post-hoc thresholds.** The decline thresholds, the drought cut-off (z < −0.5) and the
  alarm threshold (z < −3) were chosen during the study. The analysis is exploratory.
- **GOSIF–MODIS dependence.** GOSIF uses MODIS reflectance as a predictor. TROPOMI removes
  this only for 2018–2020, with one drought year.
- **Spatial scale.** All results are regional or district averages at about 5 km over a mixed
  cropland mask; they do not describe individual crops or fields.
- **District non-independence.** District observations are spatially clustered. With
  district and year fixed effects, SIF does not track rainfall anomaly (p = 0.37).
- **Rainfall trigger approximation.** My Trigger-1 is computed on averaged rainfall, not per
  taluka or per pixel.
- **Declarations.** I found only three declaration dates; the 2015 date is the date it was
  reported. Declarations follow field verification, so they are structurally late.
- **Yield data.** One end-of-season number per district-crop, ending in 2022-23 (drought
  −1.08 vs. normal +0.07, p = 0.15).

This version corrects five data-handling errors in the first preprint and adds the
normalisation check, own-district drought baselines, a monsoon-only dry-spell window for the
trigger and a block bootstrap; the full pipeline reruns from `run_all.py`.
""")

section_divider()

st.header("Conclusion")

st.markdown("""
Across nine Kharif seasons in Marathwada, GOSIF SIF did not flag agricultural drought earlier
than NDVI. Compared with their own normal-year behaviour, the two raised the alarm on the
same date in 2015, NDVI was first in 2018, and across drought district-years they most often
coincided, with NDVI earlier at looser thresholds.

SIF's normal seasonal decline appears to start well before NDVI's when each curve is scaled
over the whole season, but most of that lead comes from NDVI not returning to its pre-season
level after the monsoon. Measured over each curve's own decline, or by cross-correlation, the
lead is small and absent in about a third of the years.

So my conclusion is negative on the question I started from. In this region and dataset,
SIF is not an earlier drought alarm than NDVI. Satellite vegetation anomalies may add lead
time to a rainfall-led trigger, but I found no evidence that SIF would add more than NDVI
already does. Testing that properly would need more drought years, direct SIF retrievals over
more seasons, and a comparison with other reflectance indices.
""")

st.markdown("""
---
*GREEN ALIBI — an independent satellite-verification study, Marathwada, Maharashtra.*
""")

styled_caption("GREEN ALIBI — Findings, Limitations & Conclusion")
