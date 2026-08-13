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
    "Spatial SIF distribution, day-of-year 273, all eight study years, masked to the "
    "precise Marathwada boundary. Boundary outline drawn in black."
)

st.markdown("""
A low-SIF (red) zone recurs in the southwestern districts — Osmanabad most consistently,
joined by Bid specifically in 2018 — across most years, while the six normal years show
markedly more green (high-SIF) coverage than the two drought years, 2015 and 2018. Unlike
the original three-year sample, the expanded eight-year picture shows this low-SIF zone
shifting slightly year to year rather than sitting in exactly the same districts every time,
which is part of why the district-level ranking below is less stable at the top than it is
at the bottom.
""")

section_divider()

# ============================================================
# DISTRICT-LEVEL STATIC MAP
# ============================================================
st.header("District-Level Mean SIF")

st.image("outputs/figures/sif_by_district_static.png", use_container_width=True)
styled_caption("Mean SIF by district, day-of-year 273, all eight study years.")

st.markdown("""
Osmanabad recorded the lowest district-level mean SIF in seven of the eight years studied
(2015, 2016, 2017, 2019, 2020, 2022, 2023, ranging 0.135–0.240) — the sole exception is
2018, when **Bid** recorded the lowest value of any district in any year (0.143), even
below Osmanabad's own 2018 figure (0.151). At the top of the ranking, the original
three-year sample's finding that Nanded is "consistently highest" does **not** replicate at
eight years: Nanded is highest in only 2 of 8 years (2015, 2018), while **Aurangabad** is
highest most often (4 of 8: 2016, 2017, 2020, 2022), and Jalna (2019) and Parbhani (2023)
each lead once. The bottom of the ranking is far more stable than the top — this is reported
directly rather than smoothed into the original three-year framing.
""")

section_divider()

# ============================================================
# INTERACTIVE FOLIUM MAP
# ============================================================
st.header("Interactive District Map")

st.markdown("""
Hover or click on any district below to see its exact mean SIF value. Use the layer control
(top-right of the map) to switch between all eight study years (2015–2023, excluding 2021).
""")

try:
    with open("outputs/interactive_maps/maps/marathwada_sif_by_district.html", "r", encoding="utf-8") as f:
        sif_map_html = f.read()
    components.html(sif_map_html, height=650, scrolling=True)
except FileNotFoundError:
    st.error("Interactive map file not found at outputs/interactive_maps/maps/marathwada_sif_by_district.html")

styled_caption("GREEN ALIBI — Spatial SIF Analysis")