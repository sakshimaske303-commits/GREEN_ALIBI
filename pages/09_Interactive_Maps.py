import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Interactive Maps — GREEN ALIBI", page_icon="🗺️", layout="wide")
apply_custom_style()

st.title("🗺️ Interactive Maps & Plots")

st.markdown("""
Every map and headline chart from this study in one place — hover or click any district
for its exact value, toggle years on or off in the legend, and use each map's layer
control to switch between study years.
""")

section_divider()

MAPS = {
    "SIF by District": "outputs/interactive_maps/maps/marathwada_sif_by_district.html",
    "Rainfall Anomaly by District": "outputs/interactive_maps/maps/marathwada_rainfall_by_district.html",
    "Seasonal SIF vs. NDVI Trajectories": "outputs/interactive_maps/plots/seasonal_trajectories.html",
    "SIF-to-NDVI Lag by Threshold": "outputs/interactive_maps/plots/lag_by_threshold.html",
    "Bootstrap Confidence Intervals on Lag": "outputs/interactive_maps/plots/bootstrap_lag_ci.html",
}

choice = st.selectbox("Pick a map or chart", list(MAPS.keys()))

try:
    with open(MAPS[choice], "r", encoding="utf-8") as f:
        html = f.read()
    components.html(html, height=650, scrolling=True)
except FileNotFoundError:
    st.error(f"File not found at {MAPS[choice]}")

styled_caption(
    "Same underlying data as the static maps and charts elsewhere in this dashboard, just "
    "hoverable, zoomable, and toggleable. Individual maps are also linked on the Spatial SIF "
    "Analysis and Rainfall Validation pages; the charts summarize the Seasonal Trajectories and "
    "Lag Analysis pages."
)

section_divider()
styled_caption("GREEN ALIBI — Interactive Maps & Plots")
