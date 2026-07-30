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
    st.subheader("What This Is Not")
    st.markdown("""
    Visual correspondence between two maps, however striking, is **not a statistical
    test**. No formal correlation or regression has been run between district-level
    rainfall anomaly and district-level SIF across the three years — with only three
    years and eight districts, such an analysis would additionally be weakened by spatial
    non-independence between neighboring districts (an effective sample much smaller than
    the raw 24 district-year pairs).

    What this page presents is a **visual, physically-motivated consistency check**, and
    it is described as exactly that — nothing stronger.
    """)

st.warning("""
This spatial correspondence should not be over-read as proof of a rainfall→SIF causal
mechanism at the district level. It is consistent with the physical mechanism described
on the **Physics** pages, and it survives the same boundary-precision correction applied
throughout this project (see **Data & Methodology**) — but it remains a qualitative,
not quantitative, cross-validation.
""")

styled_caption("GREEN ALIBI — Combined SIF and Rainfall Comparison")