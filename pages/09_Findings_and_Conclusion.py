import os

import pandas as pd
import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Findings & Conclusion — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Key Findings, Limitations & Conclusion")

st.markdown("""
I kept two questions apart that are often treated as one. **(a)** In a drought year, does
SIF depart from its normal-year range before NDVI does? This is the main question, because
only it would make SIF a better drought alarm. **(b)** Does SIF's normal seasonal decline
start before NDVI's?
""")

section_divider()

st.header("(a) Drought-Specific Alarm: No Resolvable Difference")

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
  NDVI did so on 25 September and SIF on 3 October, one composite (eight days) later.
- **Districts (15 drought, 57 normal district-years, z < −3):** SIF flagged 12 and NDVI 13
  of the 15 drought district-years. False alarms: SIF 2, NDVI 4. Where both flagged, SIF was
  earlier in 7, they coincided in 2 and NDVI was earlier in 3; in 11 of the 12 the difference
  was at most one composite.
- **Looser thresholds:** at z < −1.5 NDVI was earlier in 9 of 15 and SIF in 2; at z < −2,
  NDVI in 6 of 14 and SIF in 4.
- **How NDVI is dated:** NDVI is interpolated onto the 8-day SIF dates from 16-day data. Taking
  only the NDVI already observed on each date instead, SIF was first in both regional drought
  years and in 8 of the 12 district-years. So the direction of a one-composite difference
  depends on a dating choice.
- **AUC by date:** SIF separates drought from normal district-years from 23 July (AUC 0.80),
  NDVI from 31 July (0.76); from 9 September to 20 November the two differ by at most about 0.02
  (up to 0.06 in late November and early December).

Neither index gives a consistently earlier alarm that these data can resolve. SIF's one steady
edge is slightly fewer false alarms.
""")

st.subheader("Out-of-Sample Check, 2001–2014")

st.markdown("""
Two drought years is a thin base, so I ran the same test on 2001–2014 **without changing
anything**: same drought rule, same alarm rule and thresholds, same cropland weighting and NDVI
dating. The anomalies are standardised against the normal years of 2001–2014 only (drought
years still use the 2001–2020 rainfall baseline). Five of those
years are drought years (2001, 2002, 2003, 2004, 2014), and 40 of the 112 district-years.
""")

_REG = "data/processed/oos_drought_signal_region.csv"
_DIS = "data/processed/oos_drought_signal_district_summary.csv"
if os.path.exists(_REG) and os.path.exists(_DIS):
    reg = pd.read_csv(_REG)
    dis = pd.read_csv(_DIS).set_index("threshold")
    rows = []
    for thr in [-1.0, -1.5, -2.0, -3.0]:
        s_col, n_col = f"SIF_alarm_{thr}", f"NDVI_alarm_{thr}"
        d, n = reg[reg["is_drought"]], reg[~reg["is_drought"]]
        s_first = int(((d[s_col] < d[n_col]) | (d[s_col].notna() & d[n_col].isna())).sum())
        n_first = int(((d[n_col] < d[s_col]) | (d[n_col].notna() & d[s_col].isna())).sum())
        same = int((d[s_col] == d[n_col]).sum())
        r = dis.loc[thr]
        rows.append({
            "Threshold": f"z < {thr:g}".replace("-", "−"),
            "Region: drought flagged (SIF / NDVI, of 5)": f"{d[s_col].notna().sum()} / {d[n_col].notna().sum()}",
            "Region: first (SIF / same / NDVI)": f"{s_first} / {same} / {n_first}",
            "Region: false alarms (SIF / NDVI, of 9)": f"{n[s_col].notna().sum()} / {n[n_col].notna().sum()}",
            "Districts: drought flagged (SIF / NDVI, of 40)": f"{int(r.hit_SIF)} / {int(r.hit_NDVI)}",
            "Districts: false alarms (SIF / NDVI, of 72)": f"{int(r.false_SIF)} / {int(r.false_NDVI)}",
            "Districts, both flagged: SIF earlier / same / NDVI earlier":
                f"{int(r.SIF_earlier)} / {int(r.same)} / {int(r.NDVI_earlier)}",
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    styled_caption("Out-of-sample drought alarms, 2001–2014, all methods unchanged. "
                   "'First' counts a year in which only one index raised the alarm as that index being first.")
else:
    st.info("The out-of-sample tables appear here once `out_of_sample_2001_2014.py` has been run.")

st.warning("""
**Districts: the same picture.** Where both indices flagged a drought district-year at
z < −1.5, SIF was earlier in 5 of 22, NDVI in 6, and 11 coincided; at z < −2, 0, 6 and 7 of 13.
SIF again had fewer false alarms.

**Region: slightly towards SIF.** The vegetation anomalies were weaker than in 2015 and 2018.
At z < −3 SIF flagged 2001 (17 September) and 2002 (25 September), NDVI only 2002, on the same
date; no normal year was flagged. At z < −1.5 SIF was first in four drought years and NDVI in none.

**Both periods together:** at z < −3 SIF flagged four of seven drought years and NDVI three;
where both did, they coincided twice and NDVI was earlier once. In districts at z < −1.5, SIF
was earlier in 7 of 37, NDVI in 15, and 15 coincided. H4 stays not supported: neither index is
consistently earlier.
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
**Cross-correlation and TROPOMI.** Cross-correlation over the post-peak decline, which does not depend on
scaling, gives 10, 12, 14, 4, 0, 9, 20, −1 and −3 days, closer to the decline-scaled
estimate. TROPOMI SIF (2018–2020), not built from MODIS reflectance, put SIF first in all
three years under both scalings (decline-scaled 10.4, 10.3 and 27.7 days).
""")

st.warning("""
**Is the remaining lead an NDVI property? For GOSIF, mostly yes.** MODIS NIRv and EVI, from the
same composites, also decline before NDVI: NIRv in 9 of 9 years (+22.8 days season-scaled, +9.9
decline-scaled), EVI in 9 and 8 (+17.1 and +7.7), as much as GOSIF (+20.9 and +4.3). Compared
directly, GOSIF is not ahead of NIRv: first in 4 of 9 years season-scaled and in none
decline-scaled. But GOSIF is predicted from MODIS reflectance, so that is partly built in.
TROPOMI, which is not, declined before NIRv in all three of its years (by 1–13 days): too few
years to call it a fluorescence lead, but enough to keep the question open.

**The same in 2001–2014:** season-scaled, SIF led NDVI in all 14 years (+27.4 days) and NIRv by
almost as much (+26.6); decline-scaled, NIRv declined before SIF in 11 of 14 years.
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
With two drought years neither difference means much. In 2001–2014, with five drought years,
the lead was again not larger in drought (+28.3 against +26.9 days season-scaled).
""")

section_divider()

st.header("RQ3: Rainfall Trigger and Declarations")

st.image("outputs/figures/rq3_declaration_timeline.png", use_container_width=True)
styled_caption("2015 and 2018: satellite drought alarms (z < −3), the rainfall trigger and the declaration dates.")

st.info("""
**Rainfall Trigger-1 (the Manual's rule, reconstructed on CHIRPS).** A dry spell of four consecutive standard weeks after
the normal onset, each below 50% of normal weekly rain, or scanty rainfall, or SPI below −1.5.
For the region it fired on 22 July 2015 and in no other year of 2015–2023, including 2018. At district level it
flagged 7 of 15 drought district-years (six districts in 2015, Aurangabad in 2018) and one normal
one (Aurangabad 2023). Wherever a satellite alarm also fired, the trigger came first: SIF by a
median of 25.5 days, NDVI by 33.5. NDVI flagged seven of the eight drought district-years it missed.

**What it missed.** Seven of those eight had June–September rainfall within IMD's normal band, but every
one with yield data had a poor harvest. Against crop loss it flagged 7 of 18 poor-harvest district-years
with no false alarm, NDVI 13, the two together 14. The state's 31 October 2018 declaration listed severe
drought in talukas of Bid, Jalna, Osmanabad and Parbhani, districts the reconstruction missed, and 2015
was declared under the older paisewari system.

**Per pixel and settings.** Met over at least a quarter of the district, it flagged 10 drought
district-years and the same one normal one. With three dry weeks instead of four it flags 14 but
also 26 normal district-years; my earlier, stricter approximation flagged 2. In 2001–2014 it
flagged 11 of 40 drought district-years (18 per pixel), against 6 for NDVI at z < −3.
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
meaningful benchmark is the rainfall trigger, and it came first: in 2015 it fired 33.5 days before
both satellite alarms and 86 days before the declaration.
""")

section_divider()

st.header("Study at a Glance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("H4 SIF earlier drought alarm", "Not supported", "alarms within one composite", delta_color="off")
with c2:
    st.metric("SIF first, decline-scaled", "6 / 9 years")
with c3:
    st.metric("SIF first, season-scaled", "9 / 9 years")
with c4:
    st.metric("Drought years (2015–23 / 2001–14)", "2 / 5")

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("H2 district differences", "Not supported")
with c6:
    st.metric("H3 drought widens lag", "Not supported")
with c7:
    st.metric("Rainfall Trigger-1 flagged", "7 / 15", "10 per pixel; 1 false alarm", delta_color="off")
with c8:
    st.metric("Alarms before final declarations", "27–53 days")

section_divider()

st.header("Limitations")

st.markdown("""
- **Few drought years.** Only 2015 and 2018 meet the regional drought criterion in 2015–2023,
  under every baseline tested. The 2001–2014 test adds five, but their
  vegetation anomalies were weaker, so few seasons reach the strict alarm threshold.
- **Normalisation dependence.** The seasonal lead depends on how each curve is scaled; the
  double-logistic fits that could give a third estimate are unstable at 8- and 16-day sampling.
- **Lag size and sampling.** GOSIF is 8-day and MOD13Q1 16-day; decline-scaled leads and the
  SIF–NDVI alarm differences are mostly shorter than the NDVI sampling interval, and the sign of
  an alarm difference depends on whether NDVI is interpolated or taken as observed.
- **NDVI coverage.** Many monsoon NDVI composites rest on few clear pixels; the lag direction
  does not change when composites under 25% coverage are dropped, but 2022 reverses at a 50% cut-off.
- **Post-hoc thresholds.** The decline thresholds, the drought cut-off (z < −0.5) and the
  alarm threshold (z < −3) were chosen during the study. The 2001–2014 test applies them
  unchanged, but the analysis is exploratory.
- **GOSIF–MODIS dependence.** GOSIF uses MODIS reflectance as a predictor. TROPOMI removes
  this only for 2018–2020, with one drought year. For 2001–2014, GOSIF is predicted outside
  the OCO-2 period it was trained on.
- **Spatial scale.** All results are regional or district averages at about 5 km over a mixed
  cropland mask; they do not describe individual crops or fields.
- **District non-independence.** District observations are spatially clustered. With
  district and year fixed effects, SIF does not track rainfall anomaly (p = 0.37).
- **Rainfall trigger reconstruction.** Trigger-1 follows the Manual's rule but is computed from CHIRPS on
  district-averaged rainfall and per pixel, not per taluka with gauge data and field inputs as the state
  does, with one onset date for the region; the 2018 declaration covered districts it missed. Its result
  depends on the dry-spell length and on how the weeks are counted.
- **Drought definition.** The 15 drought district-years come from a lenient rainfall cut-off; 9 had
  June–September rainfall within IMD's normal band, so I also score against crop loss.
- **Small clusters.** With eight or nine clusters and a t-distribution, the district yield–SIF link
  is marginal (p ≈ 0.04–0.08).
- **Declarations.** I found only three declaration dates; the 2015 date is the date it was
  reported. Declarations follow field verification, so they are structurally late.
- **Yield data.** One end-of-season number per district-crop, ending in 2022-23 (drought
  −1.08 vs. normal +0.07, p = 0.15).

This version corrects five data-handling errors in the first preprint and adds the
normalisation check, own-district drought baselines, a monsoon-only dry-spell window for the
trigger, a block bootstrap, the EVI/NIRv comparison, a per-pixel trigger and the 2001–2014
out-of-sample test. A final check corrected an alignment error that dated district NDVI alarms
one composite early, and added the NDVI-dating check and the TROPOMI–NIRv comparison. Version
2.2.0 replaces my strict Trigger-1 approximation with the Manual's own rule and scores it against
crop loss and the 2018 declaration list. The full pipeline
reruns from `run_all.py`.
""")

section_divider()

st.header("Conclusion")

st.markdown("""
Across nine Kharif seasons in Marathwada, GOSIF SIF did not flag agricultural drought
resolvably earlier than NDVI. Compared with their own normal-year behaviour, the two raised the
alarm on the same date in 2015 and NDVI one composite earlier in 2018, and across drought
district-years they were usually within one composite of each other, with the direction depending
on how NDVI is placed in time. Applied unchanged to 2001–2014, the same tests gave the same
district-level picture and the same NIRv-shared seasonal lead; only the regional alarms leaned
slightly towards SIF.

SIF's normal seasonal decline appears to start well before NDVI's when each curve is scaled
over the whole season, but most of that lead comes from NDVI not returning to its pre-season
level after the monsoon. Measured over each curve's own decline, or by cross-correlation, the
lead is small and absent in about a third of the years, and MODIS NIRv and EVI lead NDVI by
as much as GOSIF does, so for GOSIF what remains is a property of NDVI. Direct TROPOMI SIF led
NIRv slightly in its three years, which leaves a small fluorescence-specific lead open.

So my conclusion is negative on the question I started from. In this region and dataset,
GOSIF SIF is not an earlier drought alarm than NDVI at the resolution the data allow. The Manual's
rainfall trigger, reconstructed on CHIRPS, came before both satellite alarms wherever both fired and
never fired without a poor harvest in 2015–2022, but it saw 7 of 18 poor harvests where NDVI saw 13, and the
state's 2018 declaration recognised districts it missed. What a drought rule recognises depends on
its rainfall data, its scale and its settings; a vegetation index is most useful here as a
second route to a drought flag, and I found no evidence that GOSIF SIF would add more than NDVI
already does. Testing that properly would need direct SIF
retrievals over more drought seasons and vegetation data sampled more often than every 16 days.
""")

st.markdown("""
---
*GREEN ALIBI — an independent satellite-verification study, Marathwada, Maharashtra.*
""")

styled_caption("GREEN ALIBI — Findings, Limitations & Conclusion")
