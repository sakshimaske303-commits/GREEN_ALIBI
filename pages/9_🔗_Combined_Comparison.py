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
    "SIF (top row) and rainfall anomaly (bottom row) by district, 2015/2018/2020, "
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
    The deep red, low-SIF zone in the southwest in 2015 and 2018 sits almost exactly on
    top of the deep red, rainfall-deficit zone in the same two maps. The districts that
    turned green with rainfall surplus in 2020 are the same districts that turned green
    with healthy SIF that year. **Nanded**, which barely dipped in rainfall in either
    drought year, is also the district that stayed comparatively green in SIF in both of
    those years.

    This is a genuinely reassuring, physically coherent picture: two independently
    measured satellite products — a fluorescence signal and a precipitation product, from
    entirely different sensors and retrieval physics — are pointing at the same places for
    the same physical reason.
    """)

with col2:
    st.subheader("How Strong Is This, Really?")
    st.markdown("""
    This correspondence was tested statistically, not just visually. Across all 24
    district-year observations (8 districts × 3 years), mean SIF and rainfall anomaly
    are **strongly and significantly correlated**:

    - Pearson **r = 0.837** (p < 0.001)
    - Spearman **ρ = 0.857** (p < 0.001)

    One caveat still applies: these 24 observations are not fully independent, since the
    eight districts are geographically adjacent and share regional weather systems — the
    effective number of independent samples is closer to three (one per study year) than
    twenty-four. The correlation is reported exactly as calculated, without adjustment for
    this, and is treated as strong corroborating evidence rather than a fully independent
    statistical confirmation.
    """)

section_divider()

# ============================================================
# STATISTICAL CONFIRMATION
# ============================================================
st.header("Quantifying the Correspondence")

st.image("outputs/figures/sif_rainfall_correlation_scatter.png", use_container_width=True)
styled_caption(
    "District-level mean SIF plotted against rainfall anomaly (%), all 24 district-year "
    "observations, with a linear fit (Pearson r = 0.837, p < 0.001)."
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Pearson r", "0.837")
with m2:
    st.metric("Spearman ρ", "0.857")
with m3:
    st.metric("p-value", "< 0.001")
with m4:
    st.metric("District-years (n)", "24")

st.warning("""
This spatial correspondence is now backed by a statistically significant correlation, not
just a visual impression. It should still not be over-read as proof of a rainfall→SIF
causal mechanism at the district level, and the effective sample size is smaller than 24
once spatial non-independence between neighboring districts is accounted for. It is
consistent with the physical mechanism described on the **Physics** pages, and it survives
the same boundary-precision correction applied throughout this project (see
**Data & Methodology**).
""")

styled_caption("GREEN ALIBI — Combined SIF and Rainfall Comparison")