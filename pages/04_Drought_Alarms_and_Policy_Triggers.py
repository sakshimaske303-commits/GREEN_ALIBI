import os

import pandas as pd
import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Drought Alarms and Policy Triggers — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Drought Alarms and Policy Triggers")

st.markdown("""
The question behind this study is a policy one: **would adding satellite fluorescence (SIF) to
India's drought triggers get relief and crop-insurance payouts to farmers sooner?** On this page I
score each candidate signal the way a trigger is judged in practice. Does it fire in drought years?
Does it stay quiet in normal years? And does it fire early enough to matter? The statistical tests
behind these numbers are on **Findings & Conclusion**; here I read the same numbers as a question
of instrument design.
""")

section_divider()

st.header("The Instrument and the Candidates")

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("The rule in use")
    st.markdown("""
    **Rainfall Trigger-1** of India's Manual for Drought Management (2016), which starts drought
    assessment. My approximation: rainfall since 1 June more than 25% below normal, plus a dry
    spell of at least 21 days between 1 July and 30 September.
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
        "Rainfall Trigger-1 (my approximation of the official rule)",
        "NDVI anomaly (already in the system)",
        "SIF anomaly (the proposed addition)",
    ],
    "Drought district-years flagged (of 15)": ["2", "13", "12"],
    "Missed droughts": ["13", "2", "3"],
    "False alarms in normal district-years (of 57)": ["1", "4", "2"],
    "Timing": [
        "Both hits in 2018 (Aurangabad, Bid)",
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
    st.metric("Droughts missed by the rainfall rule", "13 of 15")
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
    The approximated rainfall trigger fired in only 2 of 15 drought district-years. A trigger
    that misses a drought leaves the loss with the farmer until field verification catches up.
    Both satellite anomalies flagged 12 or 13 of the 15. That is a possible case for vegetation
    anomalies alongside rainfall, and it applies to NDVI as much as to SIF.
    """)
with col2:
    st.subheader("False Alarms Fall on the Public Budget")
    st.markdown("""
    A trigger that fires in a normal year pays out where there was no drought loss. SIF did
    slightly better here (2 against NDVI's 4 of 57), and it again had fewer false alarms in the
    2001–2014 test. It is SIF's one consistent advantage, and it rests on very few events.
    """)

section_divider()

st.header("Why Not Simply Loosen the Rainfall Rule?")

st.markdown("""
If the rainfall trigger misses most droughts, the obvious fix is a looser rule. I ran the variants
below on the same district-years.
""")

_TRIG = "data/processed/rainfall_trigger_dates.csv"
_SIG = "data/processed/drought_signal_district.csv"
_LABELS = {
    "main: deficit>25% & spell>=21d": "Main: deficit > 25% and dry spell ≥ 21 days (1 Jul–30 Sep)",
    "deficit>20% & spell>=21d": "Deficit > 20% and dry spell ≥ 21 days",
    "deficit>30% & spell>=21d": "Deficit > 30% and dry spell ≥ 21 days",
    "dry day <1mm": "Dry day counted below 1 mm instead of 2.5 mm",
    "deficit>25% only": "Deficit > 25% alone",
    "spell>=21d only": "Dry spell ≥ 21 days alone",
    "old: spell counted to Dec": "Dry spell counted to December (earlier version)",
}
if os.path.exists(_TRIG) and os.path.exists(_SIG):
    trig = pd.read_csv(_TRIG)
    sig = pd.read_csv(_SIG)[["district", "year", "is_drought"]]
    dist = trig[trig["unit"] != "Marathwada"].merge(
        sig, left_on=["unit", "year"], right_on=["district", "year"], how="inner"
    )
    rows = []
    for variant, g in dist.groupby("variant", sort=False):
        fired = g["trigger_doy"].notna()
        rows.append({
            "Rainfall rule": _LABELS.get(variant, variant),
            "Drought district-years flagged (of 15)": int((fired & g["is_drought"]).sum()),
            "False alarms in normal district-years (of 57)": int((fired & ~g["is_drought"]).sum()),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    styled_caption("Rainfall Trigger-1 variants on district-average CHIRPS rainfall, 2015–2023.")
else:
    st.info("The variant table appears here once `rainfall_trigger_comparison.py` has been run.")

st.warning("""
No version of the rainfall rule does both jobs. With the dry-spell condition it stays quiet in
normal years but misses most droughts. The deficit alone catches 10 of the 15, but it fires in
18 normal district-years, more often than in drought ones. For the region as a whole it misses
2018 and fires in three normal years (2017, 2019, 2023).
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
    sit beside. Where it fired, in Aurangabad both satellite alarms came 15.5 days before it.
    In Bid they came at about the same time: SIF's half a day after, NDVI's 8.5 days after.
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
In Bid 2017, a normal year, the trigger fired over 72% of the district's area. In 2015, the stronger
drought year, it fired over at most 7% of any district. Only Aurangabad 2018 (40%) and Bid 2018 (35%)
crossed a quarter of their area in a drought year.
""")

section_divider()

st.header("What the Evidence Supports, and What It Does Not")

s1, s2 = st.columns(2)
with s1:
    st.success("""
    **Supported**

    - Vegetation anomalies, NDVI or SIF, alongside the rainfall trigger as a check on missed
      droughts: they flagged 12–13 of 15 drought district-years where the rainfall rule flagged 2.
    - Keeping NDVI, which is already in the system, as that vegetation signal.
    - Scoring any proposed trigger on misses, false alarms and timing together, not on lead time alone.
    """)
with s2:
    st.warning("""
    **Not supported**

    - Adding SIF for earlier drought warning: in 11 of the 12 drought district-years flagged by both,
      the two alarms came within one composite, with no consistent winner, and 2001–2014 gave the
      same district-level picture.
    - Reading the lead over official declarations as satellites beating the system.
    - Paying out at field or village level from these 5 km district averages.
    """)

st.markdown("""
These are exploratory findings for one region: two drought years in 2015–2023 (five more, mostly
mild, in 2001–2014), thresholds chosen during the study, and an approximated trigger. The
**Crop-Yield Validation** page shows lower Kharif yields in the two drought years (Yield Anomaly
Index −1.08 against +0.07, not significant with two years), in the direction that makes a missed
trigger costly for farmers.
""")

styled_caption("GREEN ALIBI — Drought Alarms and Policy Triggers")
