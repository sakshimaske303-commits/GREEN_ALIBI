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

st.header("Pixel-Level SIF, Day-of-Year 273")

st.image("outputs/figures/sif_spatial_comparison_doy273_v2.png", use_container_width=True)
styled_caption(
    "Spatial SIF distribution, day-of-year 273, all nine study years, masked to the "
    "precise Marathwada boundary. Boundary outline drawn in black."
)

st.markdown("""
A low-SIF zone recurs in the southwest of the region — Osmanabad in most years, and Bid in
2018. The pattern shifts a little from year to year rather than sitting on exactly the same
districts every time, which is why the district ranking below is more stable at the bottom
than at the top.
""")

section_divider()

st.header("District-Level Mean SIF")

st.image("outputs/figures/sif_by_district_static.png", use_container_width=True)
styled_caption("Mean SIF by district, day-of-year 273, all nine study years.")

st.markdown("""
Osmanabad has the lowest district SIF on day-of-year 273 in eight of the nine years. The
exception is 2018, when **Bid** (0.143) is lower than Osmanabad (0.151). The highest-SIF
district varies: Aurangabad in five years (2016, 2017, 2020, 2021, 2022), Nanded in two
(2015, 2018), and Jalna (2019) and Parbhani (2023) in one each.

A single date is a noisy snapshot. Day-of-year-273 SIF is spatially clustered (Moran's I,
p < 0.05) in only four years (2015, 2016, 2018, 2020), while season-mean SIF (June–December)
is clustered in all nine. I give the full Moran's I results on **Combined Comparison**.
""")

section_divider()

st.header("Interactive District Map")

st.markdown("""
Hover or click on any district below to see its exact mean SIF value. Use the layer control
(top-right of the map) to switch between all nine study years (2015–2023).
""")

try:
    with open("outputs/interactive_maps/maps/marathwada_sif_by_district.html", "r", encoding="utf-8") as f:
        sif_map_html = f.read()
    components.html(sif_map_html, height=650, scrolling=True)
except FileNotFoundError:
    st.error("Interactive map file not found at outputs/interactive_maps/maps/marathwada_sif_by_district.html")

styled_caption("GREEN ALIBI — Spatial SIF Analysis")
