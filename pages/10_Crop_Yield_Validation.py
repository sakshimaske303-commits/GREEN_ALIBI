import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Crop-Yield Validation — GREEN ALIBI", page_icon="🌾", layout="wide")
apply_custom_style()

st.title("🌾 Ground-Truth Validation Against Official Crop-Yield Statistics")

st.markdown("""
Every check on the previous pages compares one remote-sensing product against another —
SIF against NDVI, rainfall against Moran's I, one lag method against a second — or against
an official policy date. None of them touch actual agricultural outcomes on the ground,
which was one of this study's own reviewers' stated reasons for requesting revision. This
study didn't run its own field survey, but the Ministry of Agriculture & Farmers Welfare
publishes exactly the kind of independent ground-truth proxy a remote-sensing drought study
normally leans on when a farm-level survey isn't available: district-season-crop Area/
Production/Yield (APY) statistics, published annually since 1997-98. This page uses them to
ask the most direct version of the field-validation question this study can answer with
public data: **in years this study's own rainfall-anomaly threshold calls a drought year,
did Marathwada's farmers actually harvest less?**
""")

section_divider()

# Method
st.header("Data & Method")

st.markdown("""
The APY dataset was downloaded via the India Data Portal (`data.desagri.gov.in`) and
restricted to the eight Marathwada districts' Kharif season — the monsoon-season crop cycle
this study's SIF/NDVI trajectories track — covering 1997-98 through 2022-23. For every
district-crop pair with at least 10 of those 26 years present (**127 pairs, 16 crops** —
dominated by cotton, soyabean, jowar, tur, and other crops long documented as Marathwada's
principal Kharif crops), each year's yield was converted to a **z-score against that pair's
own 26-year mean and standard deviation** — the same anomaly logic used elsewhere in this
study for CHIRPS rainfall, just applied here to yield instead. Each district-year's per-crop
z-scores were averaged into a single **Yield Anomaly Index**, and district-years were
averaged into one Marathwada-region-year figure for comparison against this study's own
rainfall anomaly and mean regional SIF.

One limitation carries directly into this comparison: the government dataset's most recent
published season is 2022-23, so **2023 — one of this study's own nine SIF/NDVI years — has
no yield ground-truth counterpart yet**, leaving **n = 8 region-years** for the checks below.
""")

section_divider()

# Figure
st.header("Yield Anomaly by Year")

st.image("outputs/figures/crop_yield_anomaly_by_year.png", use_container_width=True)
styled_caption(
    "Official Kharif crop-yield anomaly (z-score vs. each district-crop pair's own "
    "26-year mean), averaged to a single Marathwada region-year figure, all 8 years with "
    "published yield data (2023 not yet published)."
)

_yy_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
_yy_drought = [True, False, False, True, False, False, False, False]
_yy_val = [-1.44, -0.02, -0.31, -0.71, -0.24, 0.65, -0.13, 0.46]

yy_row1 = st.columns(4)
yy_row2 = st.columns(4)
for i, (yr, dr, val) in enumerate(zip(_yy_years, _yy_drought, _yy_val)):
    col = yy_row1[i] if i < 4 else yy_row2[i - 4]
    label = f"{yr} ({'drought' if dr else 'normal'})"
    col.metric(label, f"{val:+.2f}")

section_divider()

# Results
st.header("Results")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("r vs. rainfall anomaly", "0.928", "p = 0.0009")
with m2:
    st.metric("r vs. mean SIF", "0.667", "p = 0.071")
with m3:
    st.metric("Drought years (n=2)", "−1.08", "mean Yield Anomaly Index")
with m4:
    st.metric("Normal years (n=6)", "+0.07", "mean Yield Anomaly Index")

st.success("""
**As a sanity check on the method itself**, the Yield Anomaly Index correlates strongly with
this study's own independently-derived CHIRPS rainfall anomaly (**r = 0.928, p = 0.0009,
n = 8**) — confirming the yield-anomaly construction is capturing genuine year-to-year
agricultural variation and not just noise. Against mean regional SIF, the correlation is
positive and moderate-to-strong (**r = 0.667, p = 0.071, n = 8**): the direction is exactly
what this study's premise predicts — lower-SIF years tend to be lower-yield years — but with
only eight region-years this falls short of conventional significance and should be read as
suggestive, not confirmatory.
""")

st.info("""
**Most directly on the field-validation question itself:** this study's two rainfall-defined
drought years (2015, 2018) show a mean Yield Anomaly Index of **−1.08**, against **+0.07**
for the six normal years with yield data (2016, 2017, 2019, 2020, 2021, 2022) — actual
harvests were worse in the years this study calls drought years, in the same direction the
satellite record and the rainfall record both already say. **2021 itself sits close to zero
(−0.13)** rather than strongly positive, consistent with a normal but not exceptionally good
year — it doesn't stand out from the other five normal years enough to change this
comparison's conclusion either way. A Welch's t-test on that 2-versus-6 comparison gives
**t = −2.87, p = 0.15**: not significant at conventional thresholds, but with a drought-year
group of n = 2 this is expected, not a sign the effect isn't real — the same n = 2 constraint
that limits H3 elsewhere in this study applies here too. This is reported as a consistent,
meaningfully-sized directional finding, not a confirmatory statistical test.
""")

section_divider()

# What this does/doesn't establish
st.header("What This Does and Doesn't Establish")

st.warning("""
This is **not** the field survey a reviewer's comment might implicitly ask for, and it does
**not** validate SIF's within-season lag-detection claims specifically — yield is a single
end-of-season number, not a timing signal. What it **does** establish is that the years and
the region this study calls agriculturally stressed from satellite and rainfall data alone
were, independently, years when Marathwada's farmers grew measurably less — a genuine,
external, government-sourced check that this study's core drought classification tracks real
agricultural outcomes on the ground, not just an internally consistent set of remote-sensing
indices.
""")

styled_caption("GREEN ALIBI — Crop-Yield Validation")
