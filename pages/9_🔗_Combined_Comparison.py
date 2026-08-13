import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Combined Comparison — GREEN ALIBI", page_icon="🔗", layout="wide")
apply_custom_style()

st.title("🔗 SIF vs. Rainfall: A Combined Spatial View")

st.markdown("""
The previous two pages showed SIF and rainfall anomaly separately. This page puts them
side by side, deliberately, so the spatial correspondence between the two — measured by
two entirely independent satellite instruments — can be read directly rather than held in
memory across pages.
""")

section_divider()

st.image("outputs/figures/combined_sif_rainfall_comparison.png", use_container_width=True)
styled_caption(
    "SIF (top row) and rainfall anomaly (bottom row) by district, all eight study years, "
    "presented jointly for direct spatial comparison."
)

section_divider()

# ============================================================
# INTERPRETATION
# ============================================================
st.header("Reading the Correspondence")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What Lines Up")
    st.markdown("""
    The deep red, low-SIF zone in the southwest in the drought years (2015, 2018) sits
    largely on top of the deep red, rainfall-deficit zone in the same maps, and this holds
    up as an *average* pattern across all eight years, not just the two drought years:
    **Osmanabad, Bid, and Aurangabad** run driest on average across the full eight-year
    record (−6.9%, −5.7%, −5.4% mean rainfall anomaly), and Osmanabad is also the district
    that most consistently records the lowest district-level SIF (7 of 8 years). At the wet
    end, **Nanded and Hingoli** run well above the regional average in rainfall (+28.0%,
    +22.3%) across the full record.

    This is a genuinely reassuring, physically coherent picture: two independently
    measured satellite products — a fluorescence signal and a precipitation product, from
    entirely different sensors and retrieval physics — are pointing at the same places for
    the same physical reason, across a full eight-year record rather than two hand-picked
    years.
    """)

with col2:
    st.subheader("How Strong Is This, Really?")
    st.markdown("""
    This correspondence was tested statistically, not just visually. Across all 64
    district-year observations (8 districts × 8 years), mean SIF and rainfall anomaly
    are **positively and significantly correlated, though more modestly than the original
    three-year sample suggested**:

    - Pearson **r = 0.567** (p < 0.001)
    - Spearman **ρ = 0.551** (p < 0.001)

    The original three-year sample (r = 0.837) turned out to be on the strong end of what
    a larger, more representative sample supports — this is reported directly as a genuine
    weakening at scale, not hidden behind the still-significant p-value. One caveat still
    applies: these 64 observations are not fully independent, since the eight districts are
    geographically adjacent and share regional weather systems — the Moran's I check below
    quantifies exactly how non-independent. The correlation is reported exactly as
    calculated, without adjustment for this, and is treated as real but moderate
    corroborating evidence rather than a fully independent statistical confirmation.
    """)

section_divider()

# ============================================================
# STATISTICAL CONFIRMATION
# ============================================================
st.header("Quantifying the Correspondence")

st.image("outputs/figures/sif_rainfall_correlation_scatter.png", use_container_width=True)
styled_caption(
    "District-level mean SIF plotted against rainfall anomaly (%), all 64 district-year "
    "observations, with a linear fit (Pearson r = 0.567, p < 0.001)."
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Pearson r", "0.567")
with m2:
    st.metric("Spearman ρ", "0.551")
with m3:
    st.metric("p-value", "< 0.001")
with m4:
    st.metric("District-years (n)", "64")

st.warning("""
This spatial correspondence is still backed by a statistically significant correlation at
more than double the original sample size, not just a visual impression — but the
correlation itself is meaningfully weaker than the original three-year figure (r = 0.837).
It should not be over-read as proof of a rainfall→SIF causal mechanism at the district
level, and the effective sample size is smaller than 64 once spatial non-independence
between neighboring districts is accounted for. It is consistent with the physical
mechanism described on the **Physics** pages, and it survives the same boundary-precision
correction applied throughout this project (see **Data & Methodology**).
""")

section_divider()

# ============================================================
# SPATIAL AUTOCORRELATION — QUANTIFYING "NOT FULLY INDEPENDENT"
# ============================================================
st.header("How Non-Independent, Exactly? A Moran's I Check")

st.markdown("""
The caveat above — that the 64 district-year observations aren't fully independent — has
been stated throughout this project, but as an assertion rather than a measurement. **Moran's
I**, a standard spatial-autocorrelation statistic, was computed for both mean SIF and
rainfall anomaly, separately for each study year, using a Queen-contiguity spatial weights
matrix built from the real district polygons (mean 3.25 neighboring districts per district)
and a 9,999-permutation significance test.
""")

st.image("outputs/figures/spatial_autocorrelation_morans_i.png", use_container_width=True)
styled_caption(
    "Moran's I for district-level mean SIF and rainfall anomaly, by year, all eight "
    "study years (* = p < 0.05, 9,999 permutations)."
)

st.info("""
**Rainfall anomaly is significantly spatially clustered in all 8 of 8 years** (Moran's I
0.26–0.55, p < 0.05 every year) — a fully consistent result, unchanged in character from
the original three-year sample. **Mean SIF is a different, more nuanced story at eight
years: only 4 of 8 years are significant** (2015, 2016, 2018, 2020; I = 0.26–0.31), while
2017, 2019, 2022, and 2023 do not reach significance (I = 0.05–0.20) — down from 3 of 3
significant years in the original sample. This is a genuine, honestly-reported weakening,
not an error: SIF's spatial clustering is real in some years and not detectably present in
others, whereas rainfall's spatial clustering is a robust, year-independent feature of the
region's geography. Combined, 12 of 16 year × variable combinations are significant. This
confirms, with a number, that the effective sample size behind the r = 0.567 correlation
above is well below **n = 64** — it does not undo the correlation as evidence, since the
underlying spatial pattern is real for rainfall and real in half the years for SIF, but it
means the correlation's p-value should not be read as if drawn from 64 fully independent
observations.
""")

styled_caption("GREEN ALIBI — Combined SIF and Rainfall Comparison")