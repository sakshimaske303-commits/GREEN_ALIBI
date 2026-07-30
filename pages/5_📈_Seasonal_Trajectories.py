import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Seasonal Trajectories — GREEN ALIBI", page_icon="📈", layout="wide")
apply_custom_style()

st.title("📈 Seasonal SIF vs. NDVI Trajectories")

st.markdown("""
Before any quantitative lag calculation, the first test of this project's core premise was
simple: plot both indices, normalized to their own seasonal peak, side by side across all
three study years, and see whether SIF actually begins declining before NDVI does.
""")

section_divider()

st.image("outputs/figures/sif_vs_ndvi_seasonal_v2.png", use_container_width=True)
styled_caption(
    "Normalized SIF and NDVI seasonal trajectories, Marathwada, 2015 (drought), "
    "2018 (drought), and 2020 (normal monsoon). SIF's post-peak decline precedes "
    "NDVI's decline in all three years."
)

section_divider()

# ============================================================
# INTERPRETATION
# ============================================================
st.header("What This Shows")

col1, col2 = st.columns(2)

with col1:
    st.subheader("The Consistent Pattern")
    st.markdown("""
    Across all three years — regardless of drought classification — SIF begins its
    post-peak decline visibly before NDVI does. NDVI holds near its peak value for a
    noticeably longer stretch after SIF has already started dropping. This pattern is
    replicated identically in 2015, 2018, and 2020, supporting **H1** and the underlying
    physical mechanism covered on the **Physics** pages: fluorescence tracks real-time
    photosynthetic efficiency, while NDVI requires actual structural degradation before
    it moves.
    """)

with col2:
    st.subheader("A Claim That Was Tested and Withdrawn")
    st.markdown("""
    An initial, purely visual read of these three charts suggested the SIF–NDVI gap
    looked distinctly larger in the two drought years than in the normal year. Checking
    that claim rigorously — by measuring each year's decline as a percentage of its own
    peak at each subsequent date, rather than eyeballing the chart — did **not** support
    it: the apparent lag was of broadly similar magnitude across all three years once
    measured carefully. That initial claim was withdrawn rather than left standing. The
    proper, quantitative version of this test is on the **Lag Analysis** page.
    """)

st.info("""
This page establishes *that* SIF leads NDVI's decline. It does not, on its own, establish
*by how much*, or whether that gap is meaningfully different between drought and normal
years — both of which require the numeric threshold-crossing method on the next page.
""")

styled_caption("GREEN ALIBI — Seasonal SIF vs. NDVI Trajectories")