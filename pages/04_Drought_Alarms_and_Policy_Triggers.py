import os

import pandas as pd
import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Drought Alarms and Policy Triggers — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Drought Alarms and Policy Triggers")

st.markdown("""
The question behind this study is a policy one: **would adding satellite fluorescence (SIF) to
India's drought triggers get drought relief to farmers sooner?** On this page I
score each candidate signal the way a trigger is judged in practice. Does it fire in drought years?
Does it stay quiet in normal years? And does it fire early enough to matter? The statistical tests
behind these numbers are on **Findings & Conclusion**; here I read the same numbers as a question
of instrument design.
""")

section_divider()

st.header("The Instrument and the Candidates")

st.info("""
**Corrected in version 2.2.0.** Earlier versions used my own approximation of Trigger-1, which was much
stricter than the Manual's rule and flagged only 2 of 15 drought district-years. Trigger-1 now follows
the Manual, and every number on this page uses it. The SIF–NDVI comparison does not use the trigger.
""")

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("The rule in use")
    st.markdown("""
    **Rainfall Trigger-1** of India's Manual for Drought Management (2016), which starts drought
    assessment. As the Manual defines it: a **dry spell** of four consecutive standard weeks after the
    normal monsoon onset (from the week of 18–24 June here), each with less than 50% of normal weekly
    rain, sets it off; without one, rainfall must be **scanty** (60% or more below normal) or **SPI below −1.5**.
    """)
with c2:
    st.subheader("The candidates")
    st.markdown("""
    **NDVI** (MODIS), already used in drought assessment, and **SIF** (GOSIF, cropland-weighted),
    the proposed addition. Each is measured as its departure from the normal years at the same
    date. The alarm fires when z < −3 for two 8-day composites in a row.
    """)
with c3:
    st.subheader("The test units")
    st.markdown("""
    **72 district-years** (8 districts × 9 Kharif seasons, 2015–2023): 15 drought and 57 normal,
    each district judged against its own rainfall record. 2001–2014 serves as an out-of-sample check.
    """)

section_divider()

st.header("Three Triggers, Scored on Both Kinds of Error")

st.markdown("""
A trigger is a rule that decides who pays. When it misses a drought, the loss stays with the
farmer. When it fires in a normal year, relief and payouts go where there was no drought loss, and
the public budget pays. So I score each trigger on both errors, not on speed alone.
""")

scorecard = pd.DataFrame({
    "Trigger": [
        "Rainfall Trigger-1 (the Manual's rule, district average)",
        "NDVI anomaly (already in the system)",
        "SIF anomaly (the proposed addition)",
    ],
    "Drought district-years flagged (of 15)": ["7", "13", "12"],
    "Missed droughts": ["8", "2", "3"],
    "False alarms in normal district-years (of 57)": ["1", "4", "2"],
    "Timing": [
        "22 July (2015) and 12 August (2018); before SIF and NDVI wherever both fired",
        "Earlier than SIF in 3, same date in 2, later in 7",
        "Earlier than NDVI in 7, same date in 2, later in 3",
    ],
})
st.dataframe(scorecard, use_container_width=True, hide_index=True)
styled_caption(
    "District drought alarms, 2015–2023, own-district rainfall baseline. Against the regional "
    "baseline (17 drought, 55 normal district-years) both satellite anomalies flag 12; false "
    "alarms SIF 1, NDVI 5."
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Droughts missed by the rainfall rule", "8 of 15", "5 when applied per pixel", delta_color="off")
with m2:
    st.metric("Droughts missed, NDVI / SIF", "2 / 3")
with m3:
    st.metric("False alarms, NDVI / SIF", "4 / 2", "of 57 normal district-years", delta_color="off")
with m4:
    st.metric("SIF and NDVI within one composite", "11 of 12", "drought district-years flagged by both", delta_color="off")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Missed Droughts Fall on Farmers")
    st.markdown("""
    The Manual's rainfall trigger missed 8 of the 15 drought district-years: Aurangabad and Jalna in
    2015, five districts in 2018, when the drought built up late in the season, and Jalna in 2023 (per
    pixel it missed 5). A trigger that misses a drought leaves the loss with the farmer until field
    verification catches up. NDVI flagged seven of those eight, so letting NDVI raise a flag on its own,
    and not only confirm the rainfall trigger, would have caught 14 of the 15.
    """)
with col2:
    st.subheader("False Alarms Fall on the Public Budget")
    st.markdown("""
    A trigger that fires in a normal year pays out where there was no drought loss. The rainfall
    trigger fired in only one of 57 normal district-years (Aurangabad 2023). SIF did slightly better
    than NDVI here (2 against 4), and it again had fewer false alarms in the 2001–2014 test. It is
    SIF's one consistent advantage, and it rests on very few events.
    """)

section_divider()

st.header("How Much Do the Rainfall Rule's Settings Matter?")

st.markdown("""
The Manual leaves room in how a dry spell is counted: usually four weeks, up to three on light
soils, after the due date of monsoon onset. I ran these versions, and my earlier approximation, on
the same district-years.
""")

_TRIG = "data/processed/rainfall_trigger_dates.csv"
_SIG = "data/processed/drought_signal_district.csv"
_LABELS = {
    "main: Manual Trigger 1, 4 dry weeks": "Main: the Manual's rule, dry spell of 4 standard weeks from 18 Jun (or scanty rain, or SPI < −1.5)",
    "Manual Trigger 1, 3 dry weeks (light soils)": "Dry spell of 3 weeks (the Manual's light-soil rule)",
    "Manual Trigger 1, 4 dry weeks counted from July": "Dry spell of 4 weeks, counted from July",
    "Manual Trigger 1, 3 dry weeks counted from July": "Dry spell of 3 weeks, counted from July",
    "earlier approximation: deficit>25% & 21 days <2.5 mm": "My earlier approximation: deficit > 25% and 21 days each < 2.5 mm",
    "deficit>25% only": "Deficit > 25% alone (not the Manual's rule)",
}
if os.path.exists(_TRIG) and os.path.exists(_SIG):
    trig = pd.read_csv(_TRIG)
    sig = pd.read_csv(_SIG)[["district", "year", "is_drought"]]
    dist = trig[(trig["unit"] != "Marathwada") & (trig["year"] >= 2015)].merge(
        sig, left_on=["unit", "year"], right_on=["district", "year"], how="inner"
    )
    rows = []
    dist["order"] = dist["variant"].map({v: i for i, v in enumerate(_LABELS)})
    for variant, g in dist.sort_values("order").groupby("variant", sort=False):
        fired = g["trigger_doy"].notna()
        rows.append({
            "Rainfall rule": _LABELS.get(variant, variant),
            "Drought district-years flagged (of 15)": int((fired & g["is_drought"]).sum()),
            "False alarms in normal district-years (of 57)": int((fired & ~g["is_drought"]).sum()),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    styled_caption("Rainfall Trigger-1 versions on district-average CHIRPS rainfall, 2015–2023 (15 drought, 57 normal district-years).")
else:
    st.info("The variant table appears here once `rainfall_trigger_comparison.py` has been run.")

st.warning("""
One setting moves the result more than any choice of satellite index. With a four-week dry spell the
rule flags 7 of the 15 drought district-years and fires in 1 normal one; with three weeks it flags
14 but fires in 26 normal ones. Counting the weeks only from July gives 6 and 1, and seven-day blocks
from 15 June in place of the standard weeks give 10 and 7. My earlier approximation flagged 2. The
deficit alone, which the Manual does not use on its own, flags 10 but fires in 18 normal district-years.
""")

st.info("""
**How should the signals be combined, and what do the errors cost?** The **Policy Design Lab** page scores
combined rules (rainfall first, vegetation as confirmation), prices each rule's errors in rupees of relief,
compares India's design with the EU, Spain, the USA and Kenya, and classifies the proposals by order of
policy change.
""")

section_divider()

st.header("Is a Hit Early Enough to Matter?")

st.image("outputs/figures/rq3_declaration_timeline.png", use_container_width=True)
styled_caption("2015 and 2018: satellite drought alarms (z < −3), the rainfall trigger and the declaration dates.")

t1, t2 = st.columns(2)
with t1:
    st.subheader("Against the Rainfall Trigger")
    st.markdown("""
    The rainfall trigger is the fair benchmark, because it is the rule a satellite signal would
    sit beside. For the region it fired on 22 July 2015, 33.5 days before both satellite alarms.
    In every drought district-year where it and a satellite alarm both fired, the trigger came
    first: SIF by a median of 25.5 days, NDVI by 33.5. The vegetation index does not warn
    earlier; it catches droughts the trigger misses.
    """)
with t2:
    st.subheader("Against the Declarations")
    st.markdown("""
    The alarms came 52.5 days before the 2015 declaration (both indices), and 27.5 (SIF) and
    35.5 (NDVI) days before the final 2018 declaration. A declaration follows field verification
    of crop damage, so a satellite signal precedes it almost by construction. This gap should not
    be read as satellites beating the system.
    """)

st.info("""
**Timing decides whether a hit is useful.** PMFBY allows an on-account payment of up to 25% of
likely claims when a mid-season adversity is expected to cut yield below half of normal. An alarm
helps here only if it comes while the crop is still in the field. One of NDVI's hits shows the
limit: in Nanded 2015 its alarm came only on 6 December, seven weeks after the 2015 drought
declaration was reported (16 October), and SIF never fired.
It counts as a hit in the scorecard above, but it would not have brought relief any sooner.
""")

section_divider()

st.header("Basis Risk: The Scale Problem")

st.markdown("""
These results are district averages at about 5 km. The official drought procedure works at taluka
level, and PMFBY settles widespread losses over a notified insurance unit, for major crops a village
or village panchayat; only localised losses are assessed field by field. So even a well-timed district
index can pay a farmer whose field was not hurt and miss one whose field was. Insurance economics
calls this gap **basis risk**.

The per-pixel version of the rainfall trigger shows how large the gap can be inside one district.
In the 2018 drought it was met over 64% of Aurangabad but 0–16% of Bid, Latur and Osmanabad, all
drought district-years. In 2015 it covered 78–100% of six districts, 43% of Jalna and only 5% of Aurangabad.
""")

section_divider()

st.header("What the Evidence Supports, and What It Does Not")

s1, s2 = st.columns(2)
with s1:
    st.success("""
    **Supported**

    - Letting a vegetation anomaly raise a drought flag on its own, alongside the rainfall trigger:
      NDVI flagged seven of the eight drought district-years the trigger missed, and the two together
      flagged 14 of 15 with no more false alarms than NDVI alone.
    - Treating the dry-spell length as a policy setting to be set openly: three or four weeks moves the
      rainfall trigger from 7 to 14 droughts flagged and from 1 to 26 false alarms.
    - Keeping NDVI, which is already in the system, as that vegetation signal.
    - Scoring any proposed trigger on misses, false alarms and timing together, not on lead time alone.
    - Setting the alarm threshold openly, as a choice about how much a missed drought weighs against a
      false alarm: it moves the cost of errors more than the choice of index.
    """)
with s2:
    st.warning("""
    **Not supported**

    - Adding SIF for earlier drought warning: in 11 of the 12 drought district-years flagged by both,
      the two alarms came within one composite, with no consistent winner, and 2001–2014 gave the
      same district-level picture.
    - Reading the lead over official declarations as satellites beating the system.
    - Paying out at field or village level from these 5 km district averages.
    - Using satellite anomalies to warn earlier than the Manual's rainfall trigger: it came first in
      every drought district-year where both fired.
    - Reading the trigger's misses as droughts the Manual misses: the droughts here are themselves
      defined by rainfall.
    """)

st.markdown("""
These are exploratory findings for one region: two drought years in 2015–2023 (five more, mostly
mild, in 2001–2014), thresholds chosen during the study, and a district- and pixel-level version of a taluka-level trigger. The
**Crop-Yield Validation** page shows lower Kharif yields in the two drought years (Yield Anomaly
Index −1.08 against +0.07, not significant with two years), in the direction that makes a missed
trigger costly for farmers.
""")

styled_caption("GREEN ALIBI — Drought Alarms and Policy Triggers")
