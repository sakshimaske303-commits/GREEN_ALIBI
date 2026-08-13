import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Rainfall Validation — GREEN ALIBI", page_icon="🌧️", layout="wide")
apply_custom_style()

st.title("🌧️ Rainfall Validation")

st.markdown("""
Up to this point, "2015 and 2018 were drought years" had been a label carried in from
general knowledge about Marathwada — not something measured within this project. This page
closes that gap using CHIRPS precipitation data, independently of the SIF and NDVI analysis,
across all eight study years.
""")

section_divider()

# ============================================================
# REGIONAL RAINFALL ANOMALY
# ============================================================
st.header("Regional Rainfall Anomaly")

st.image("outputs/figures/rainfall_anomaly_2015_2023_8years.png", use_container_width=True)
styled_caption("Regional rainfall anomaly (% departure from 2001–2020 climatological mean), all eight study years.")

_rain_years = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]
_rain_mm = ["649.0 mm", "904.7 mm", "817.5 mm", "674.9 mm", "936.4 mm", "1066.5 mm", "1130.7 mm", "795.9 mm"]
_rain_pct = ["-21.5%", "+9.5%", "-1.1%", "-18.3%", "+13.3%", "+29.1%", "+36.8%", "-3.7%"]
_rain_z = [-1.12, 0.49, -0.06, -0.95, 0.69, 1.51, 1.92, -0.19]

rain_row1 = st.columns(4)
rain_row2 = st.columns(4)
for i, (yr, mm, pct, z) in enumerate(zip(_rain_years, _rain_mm, _rain_pct, _rain_z)):
    col = rain_row1[i] if i < 4 else rain_row2[i - 4]
    tag = " (drought)" if z < -0.5 else ""
    col.metric(f"{yr}{tag}", mm, pct)

st.info("""
Against a **twenty-year (2001–2020) climatological mean of 826.4 mm** (σ = 158.8 mm) for
the June–December window, only **2015** (z = -1.12) and **2018** (z = -0.95) cross this
study's own drought threshold (anomaly z-score < -0.5). The other six years — including
2017 and 2023, which are both still mildly below the long-run mean — sit within roughly
one standard deviation of normal, and 2022 was the wettest year of the entire eight-year
record (+36.8%). This independently confirms, via measured precipitation deficit rather
than assumption, that only 2/8 (25%) of the study's years are genuine drought years — a
notably smaller share than the 2/3 (67%) implied by the original three-year sample, and a
finding carried through every other page and document in this project.
""")

section_divider()

# ============================================================
# DISTRICT-LEVEL STATIC MAP
# ============================================================
st.header("District-Level Rainfall Anomaly")

st.image("outputs/figures/rainfall_anomaly_by_district_static.png", use_container_width=True)
styled_caption("Rainfall anomaly by district (% departure from regional 20-year normal), all eight study years.")

st.markdown("""
The regional deficit was **not spatially uniform**, and this holds well beyond the drought
years alone. In 2018, Aurangabad (−37.3%) and Bid (−38.0%) recorded the largest deficits,
while Hingoli (+10.2%) and Nanded (+14.7%) actually recorded rainfall **surpluses** in the
same year — despite the region-wide figure showing an 18.3% deficit.

Averaged across all eight study years, this west-drier / east-wetter gradient is a
persistent feature of the region, not a one-year artifact: **Osmanabad (−6.9%), Bid (−5.7%),
and Aurangabad (−5.4%)** run below the long-term regional mean on average across the full
record, while **Nanded (+28.0%) and Hingoli (+22.3%)** run well above it. This lines up
directly with the SIF-based spatial pattern on the previous page, where Osmanabad recorded
the lowest district-level SIF in 7 of 8 years — the same district that is, on average, the
driest. "Drought year" as a single regional label conceals substantial and *consistent*
west-to-east variation within Marathwada, not just variation confined to 2015 and 2018.
""")

section_divider()

# ============================================================
# INTERACTIVE FOLIUM MAP
# ============================================================
st.header("Interactive District Map")

st.markdown("""
Hover or click on any district to see its exact rainfall anomaly. Use the layer control to
switch between all eight study years (2015–2023, excluding 2021).
""")

try:
    with open("outputs/interactive_maps/maps/marathwada_rainfall_by_district.html", "r", encoding="utf-8") as f:
        rain_map_html = f.read()
    components.html(rain_map_html, height=650, scrolling=True)
except FileNotFoundError:
    st.error("Interactive map file not found at outputs/interactive_maps/maps/marathwada_rainfall_by_district.html")

styled_caption("GREEN ALIBI — Rainfall Validation")