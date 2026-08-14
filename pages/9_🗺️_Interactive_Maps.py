import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Interactive Maps — GREEN ALIBI", page_icon="🗺️", layout="wide")
apply_custom_style()

st.title("🗺️ Interactive Maps")

st.markdown("""
Both district-level maps from this study in one place — hover or click any district for its
exact value, and use each map's layer control to switch between study years.
""")

section_divider()

MAPS = {
    "SIF by District": "outputs/interactive_maps/maps/marathwada_sif_by_district.html",
    "Rainfall Anomaly by District": "outputs/interactive_maps/maps/marathwada_rainfall_by_district.html",
}

choice = st.selectbox("Pick a map", list(MAPS.keys()))

try:
    with open(MAPS[choice], "r", encoding="utf-8") as f:
        html = f.read()
    components.html(html, height=650, scrolling=True)
except FileNotFoundError:
    st.error(f"Interactive map file not found at {MAPS[choice]}")

styled_caption(
    "Same underlying data as the static maps elsewhere in this dashboard, just hoverable and "
    "zoomable. Also linked individually on the Spatial SIF Analysis and Rainfall Validation pages."
)

section_divider()
styled_caption("GREEN ALIBI — Interactive Maps")
