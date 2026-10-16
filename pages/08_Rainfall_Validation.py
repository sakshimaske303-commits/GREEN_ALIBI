import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Rainfall Validation — GREEN ALIBI", page_icon="🌧️", layout="wide")
apply_custom_style()

st.title("🌧️ Rainfall Validation")

st.markdown("""
I needed a measured definition of a drought year rather than one carried in from general
knowledge about Marathwada. This page builds it from CHIRPS daily rainfall alone,
independently of the SIF and NDVI data. Every rainfall anomaly in this study comes from the
same CHIRPS seasonal-total series (1 June – 26 December), compared against a 2001–2020
baseline.
""")

section_divider()

st.header("Regional Rainfall Anomaly")

st.image("outputs/figures/rainfall_anomaly_2015_2023.png", use_container_width=True)
styled_caption("Regional rainfall anomaly (% departure from 2001–2020 climatological mean), all nine study years.")

_rain_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
_rain_mm = ["649.0 mm", "904.7 mm", "817.4 mm", "674.9 mm", "936.3 mm", "1066.5 mm", "970.0 mm", "1130.3 mm", "795.3 mm"]
_rain_pct = ["-21.5%", "+9.4%", "-1.1%", "-18.4%", "+13.3%", "+29.0%", "+17.3%", "+36.7%", "-3.8%"]
_rain_z = [-1.12, 0.49, -0.06, -0.96, 0.69, 1.51, 0.90, 1.91, -0.20]

rain_row1 = st.columns(5)
rain_row2 = st.columns(4)
for i, (yr, mm, pct, z) in enumerate(zip(_rain_years, _rain_mm, _rain_pct, _rain_z)):
    col = rain_row1[i] if i < 5 else rain_row2[i - 5]
    tag = " (drought)" if z < -0.5 else ""
    col.metric(f"{yr}{tag}", mm, pct)

st.info("""
Against a 2001–2020 mean of **826.8 mm** (σ = 158.9 mm), only **2015** (z = −1.12) and
**2018** (z = −0.96) fall below my drought cut-off of z < −0.5. The other seven years are
normal; 2017 and 2023 are slightly below the mean, and 2022 is the wettest year in the
record (+36.7%). The same two years come out as drought years under all four baselines I
tested (2001–2020, 2001–2014, 1981–2014, 1991–2020), and with the 2001–2020 baseline for
every cut-off from −0.3 to −0.75 (with 1981–2014, 2018 drops out at −0.7). Under z < −1.0 only 2015 remains. So every drought-versus-normal comparison in this
study rests on two years out of nine.
""")

section_divider()

st.header("District-Level Rainfall Anomaly")

st.image("outputs/figures/rainfall_anomaly_by_district_static.png", use_container_width=True)
styled_caption("Rainfall anomaly by district (% departure from the regional 2001–2020 mean), 2015–2023.")

st.markdown("""
The deficit was **not spatially uniform**. In 2018, Bid (−38.0%), Aurangabad (−37.3%) and
Osmanabad (−33.9%) had the largest deficits, while Hingoli (+10.2%) and Nanded (+14.6%) had
surpluses, even though the region as a whole was 18.4% short. In 2015, Osmanabad (−36.4%)
had the largest deficit and Hingoli (−8.0%) and Nanded (−7.1%) the mildest.

Part of this is a fixed west–east gradient. District baselines range from 704.9 mm
(Osmanabad) to 1,009.0 mm (Nanded), so against the regional mean Osmanabad (−5.6%),
Aurangabad (−5.0%) and Bid (−4.2%) run below average over the nine years, and Nanded
(+29.5%) and Hingoli (+24.1%) well above it. Because of this I also classified district-years
against each district's own baseline: 6 of 72 classifications change (Hingoli and Nanded
2015 become drought district-years; Aurangabad 2017 and Aurangabad, Bid and Osmanabad 2023
become normal), and the two sets of z-scores correlate at r = 0.83. The own-district
classification (15 drought district-years: all eight districts in 2015, six in 2018 and Jalna
in 2023) is the one used for the district drought-alarm tests; the regional one is a check.
""")

section_divider()

st.header("Interactive District Map")

st.markdown("""
Hover or click on any district to see its exact rainfall anomaly. Use the layer control to
switch between all nine study years (2015–2023).
""")

try:
    with open("outputs/interactive_maps/maps/marathwada_rainfall_by_district.html", "r", encoding="utf-8") as f:
        rain_map_html = f.read()
    components.html(rain_map_html, height=650, scrolling=True)
except FileNotFoundError:
    st.error("Interactive map file not found at outputs/interactive_maps/maps/marathwada_rainfall_by_district.html")

styled_caption("GREEN ALIBI — Rainfall Validation")
