import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Rainfall Validation — GREEN ALIBI", page_icon="🌧️", layout="wide")
apply_custom_style()

st.title("🌧️ Rainfall Validation")

st.markdown("""
Up to this point, "2015 and 2018 were drought years, 2020 was normal" had been a label
carried in from general knowledge about Marathwada — not something measured within this
project. This page closes that gap using CHIRPS precipitation data, independently of the
SIF and NDVI analysis.
""")

section_divider()

# ============================================================
# REGIONAL RAINFALL ANOMALY
# ============================================================
st.header("Regional Rainfall Anomaly")

st.image("outputs/figures/rainfall_anomaly_2015_2018_2020.png", use_container_width=True)
styled_caption("Regional rainfall anomaly (% departure from 2001–2020 climatological mean), by year.")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("2015", "648.9 mm", "-21.5%")
with m2:
    st.metric("2018", "674.8 mm", "-18.3%")
with m3:
    st.metric("2020", "1066.6 mm", "+29.1%")

st.info("""
Against a **twenty-year (2001–2020) climatological mean of 826.4 mm** (σ = 158.8 mm) for
the June–December window, both 2015 and 2018 were genuine, substantial rainfall shortfalls,
and 2020 was a genuinely wet year by comparison — independently confirming the drought/
normal classification used throughout this study via measured precipitation deficit, not
assumption.
""")

section_divider()

# ============================================================
# DISTRICT-LEVEL STATIC MAP
# ============================================================
st.header("District-Level Rainfall Anomaly")

st.image("outputs/figures/rainfall_anomaly_by_district_static.png", use_container_width=True)
styled_caption("Rainfall anomaly by district (% departure from regional 20-year normal), 2015/2018/2020.")

st.markdown("""
The regional deficit was **not spatially uniform**. In 2018, Aurangabad (−37.2%) and Beed
(−38.1%) recorded the largest deficits, while Hingoli (+10.4%) and Nanded (+14.6%) actually
recorded rainfall **surpluses** in the same year — despite the region-wide figure showing an
18.3% deficit. "Drought year" as a single regional label conceals substantial west-to-east
variation within Marathwada.
""")

section_divider()

# ============================================================
# INTERACTIVE FOLIUM MAP
# ============================================================
st.header("Interactive District Map")

st.markdown("""
Hover or click on any district to see its exact rainfall anomaly. Use the layer control to
switch between 2015, 2018, and 2020.
""")

try:
    with open("outputs/interactive_maps/maps/marathwada_rainfall_by_district.html", "r", encoding="utf-8") as f:
        rain_map_html = f.read()
    components.html(rain_map_html, height=650, scrolling=True)
except FileNotFoundError:
    st.error("Interactive map file not found at outputs/interactive_maps/maps/marathwada_rainfall_by_district.html")

styled_caption("GREEN ALIBI — Rainfall Validation")