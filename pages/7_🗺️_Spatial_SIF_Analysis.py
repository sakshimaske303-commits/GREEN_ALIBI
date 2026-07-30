import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Spatial SIF Analysis — GREEN ALIBI", page_icon="🗺️", layout="wide")
apply_custom_style()

st.title("🗺️ Spatial SIF Analysis")

st.markdown("""
The temporal analysis (previous pages) treats Marathwada as a single averaged region. This
page asks a different question: **where** within Marathwada did stress actually concentrate,
in both pixel-level and district-level views.
""")

section_divider()

# ============================================================
# PIXEL-LEVEL SPATIAL MAP
# ============================================================
st.header("Pixel-Level SIF, Day-of-Year 273")

st.image("outputs/figures/sif_spatial_comparison_doy273_v2.png", use_container_width=True)
styled_caption(
    "Spatial SIF distribution, day-of-year 273, 2015/2018/2020, masked to the precise "
    "Marathwada boundary. Boundary outline drawn in black."
)

st.markdown("""
A low-SIF (red) zone is consistently concentrated in the western and southwestern districts
— the western edge of Aurangabad running down through Latur and Osmanabad — in both drought
years, while 2020 is overwhelmingly high-SIF (green) across almost the entire region.
""")

section_divider()

# ============================================================
# DISTRICT-LEVEL STATIC MAP
# ============================================================
st.header("District-Level Mean SIF")

st.image("outputs/figures/sif_by_district_static.png", use_container_width=True)
styled_caption("Mean SIF by district, day-of-year 273, 2015/2018/2020.")

st.markdown("""
Osmanabad recorded the lowest district-level mean SIF in all three years studied
(0.135, 0.151, 0.194), while Nanded recorded the highest in all three years
(0.233, 0.237, 0.265) — with the smallest relative decline between drought and normal
years, consistent with the pixel-level pattern above.
""")

section_divider()

# ============================================================
# INTERACTIVE FOLIUM MAP
# ============================================================
st.header("Interactive District Map")

st.markdown("""
Hover or click on any district below to see its exact mean SIF value. Use the layer control
(top-right of the map) to switch between 2015, 2018, and 2020.
""")

try:
    with open("outputs/interactive_maps/maps/marathwada_sif_by_district.html", "r", encoding="utf-8") as f:
        sif_map_html = f.read()
    components.html(sif_map_html, height=650, scrolling=True)
except FileNotFoundError:
    st.error("Interactive map file not found at outputs/interactive_maps/maps/marathwada_sif_by_district.html")

styled_caption("GREEN ALIBI — Spatial SIF Analysis")