import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Seasonal Trajectories — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Seasonal SIF vs. NDVI Trajectories")

st.markdown("""
The first look at the data: both indices, normalised to their own seasonal peak, side by side
for all nine Kharif seasons. SIF is cropland-weighted GOSIF; NDVI is plotted at each composite's
actual observation day.
""")

section_divider()

st.image("outputs/figures/sif_vs_ndvi_seasonal_v2.png", use_container_width=True)
styled_caption(
    "Normalized cropland-weighted SIF and NDVI (at actual observation day) seasonal trajectories, "
    "Marathwada, 2015–2023, labeled by drought classification. Open squares: NDVI composites with "
    "fewer than 25% of cropland pixels passing the quality screen."
)

section_divider()

st.header("What This Shows")

col1, col2 = st.columns(2)

with col1:
    st.subheader("SIF Appears to Start Down First")
    st.markdown("""
    On this season scale (0 = each year's minimum, 1 = its peak), SIF's post-peak decline
    appears to get under way before NDVI's in all nine years. But look at the end of each panel:
    SIF returns close to its June level, while NDVI stays well above it (0.23–0.59 on this
    scale). Because NDVI never gets back down to its floor, it crosses every decline threshold
    later by construction.

    Scaled over each curve's own decline instead, SIF is first in six of nine years and by at
    most about two weeks (see **Lag Analysis**). Part of what remains may come from normal
    senescence: SIF follows absorbed light, which falls as days shorten, while NDVI saturates
    over dense canopy and stays high longer.
    """)

with col2:
    st.subheader("Drought Years Do Not Show a Bigger Gap")
    st.markdown("""
    The two drought years (2015, 2018) do not show a wider gap than the seven normal years. By
    season-scaled threshold-crossing they average **14.8 days** against **22.6 days** for normal
    years, the opposite of H3. And a lead in the *timing of the normal decline* is not the same as an earlier
    *drought* signal: when I compare each index with its own normal-year behaviour, SIF and NDVI
    depart from normal within one composite of each other (see **Findings**).
    """)

st.info("""
How large the lead is, how certain, and how much it depends on the scaling and the method are on
the next page.
""")

styled_caption("GREEN ALIBI — Seasonal SIF vs. NDVI Trajectories")
