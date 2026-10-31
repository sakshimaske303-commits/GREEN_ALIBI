import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption, MAGENTA, TEAL

st.set_page_config(page_title="Spatial Patterns — GREEN ALIBI", layout="wide")
apply_custom_style()


def part_heading(kicker, title, anchor):
    st.markdown(
        f"<div id='{anchor}' style='margin:2.6rem 0 0.6rem 0; text-align:center; scroll-margin-top:4rem;'>"
        f"<p style='color:{MAGENTA} !important; text-transform:uppercase; letter-spacing:1.6px; "
        f"font-weight:700; font-size:0.85rem; margin:0 0 4px 0;'>{kicker}</p>"
        f"<p style='color:{TEAL} !important; font-weight:800; font-size:2rem; line-height:1.25; "
        f"margin:0; padding-bottom:0.5rem; border-bottom:2px solid rgba(0,217,192,0.45);'>{title}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )


def page_contents(items):
    links = " ".join(
        f"<a href='#{a}' target='_self' class='ga-toc-btn' style='display:inline-block; margin:4px; padding:6px 14px; "
        f"border:1px solid rgba(0,217,192,0.35); border-radius:20px; background:rgba(0,217,192,0.08); "
        f"color:#F2F2F5; font-size:0.85rem; font-weight:600; text-decoration:none;'>{t}</a>"
        for t, a in items
    )
    st.markdown(
        "<style>"
        "@keyframes ga-toc-blink {"
        "0%, 100% { border-color: rgba(0,217,192,0.35); box-shadow: 0 0 0 rgba(0,217,192,0); background: rgba(0,217,192,0.08); }"
        "50% { border-color: #00D9C0; box-shadow: 0 0 14px rgba(0,217,192,0.65); background: rgba(0,217,192,0.22); }"
        "}"
        ".ga-toc-btn { animation: ga-toc-blink 1.6s ease-in-out infinite; transition: transform 0.15s ease; }"
        ".ga-toc-btn:hover { animation-play-state: paused; border-color: #E91E8C !important; "
        "box-shadow: 0 0 14px rgba(233,30,140,0.6); transform: translateY(-2px); }"
        "@media (prefers-reduced-motion: reduce) { .ga-toc-btn { animation: none; } }"
        "</style>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='text-align:center; margin:0.4rem 0 0.2rem 0;'>"
        f"<span style='color:{MAGENTA}; text-transform:uppercase; letter-spacing:1.5px; font-weight:700; "
        f"font-size:0.8rem; margin-right:6px;'>On this page</span>{links}</div>",
        unsafe_allow_html=True,
    )


st.title("Spatial Patterns: SIF and Rainfall Across the Districts")

page_contents([("Spatial SIF", "spatial-sif"), ("Rainfall validation", "rainfall"),
               ("SIF vs. rainfall", "combined")])

part_heading("Part 1 of 3 · Where stress concentrated", "Spatial SIF Analysis", "spatial-sif")

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
is clustered in all nine. I give the full Moran's I results in Part 3 below.
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

part_heading("Part 2 of 3 · Defining the drought years", "Rainfall Validation", "rainfall")

st.markdown("""
I needed a measured definition of a drought year rather than one carried in from general
knowledge about Marathwada. This part builds it from CHIRPS daily rainfall alone,
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

part_heading("Part 3 of 3 · Putting them together", "SIF vs. Rainfall: A Combined Spatial View", "combined")

st.markdown("""
Parts 1 and 2 show SIF and rainfall anomaly separately. Here I put them side by
side and test how closely they match across the 72 district-years (8 districts × 9 years).
""")

section_divider()

st.image("outputs/figures/combined_sif_rainfall_comparison.png", use_container_width=True)
styled_caption(
    "SIF (top row) and rainfall anomaly (bottom row) by district, all nine study years, "
    "presented jointly for direct spatial comparison."
)

section_divider()

st.header("Reading the Correspondence")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What Lines Up")
    st.markdown("""
    The low-SIF zone in the southwest in 2015 and 2018 sits largely on the rainfall-deficit
    zone in the same years. Over the full record, Osmanabad, Aurangabad and Bid run drier
    than the regional mean on average (−5.6%, −5.0%, −4.2%), and Osmanabad also has the
    lowest SIF in 8 of 9 years. Nanded and Hingoli run well above the regional mean in
    rainfall (+29.5%, +24.1%).

    Part of this is a fixed geographic gradient (district baselines range from 704.9 mm in
    Osmanabad to 1,009.0 mm in Nanded), so a match in the average pattern does not by itself
    show that SIF tracks a district's rainfall from one year to the next.
    """)

with col2:
    st.subheader("How Strong Is This?")
    st.markdown("""
    Across the 72 district-years, SIF on day-of-year 273 correlates with rainfall anomaly
    at **r = 0.53** (Spearman ρ = 0.51, both p < 0.0001; p = 0.001 with standard errors
    clustered by year). Season-mean SIF (June–December) correlates more strongly,
    **r = 0.74**, including within years (r = 0.66).

    With district and year fixed effects, the relationship is **not significant**
    (p = 0.37 for season-mean SIF). SIF and rainfall move together across years and across
    districts, but a district's departure from its own average in a given year is not
    reliably tracked by SIF.
    """)

section_divider()

st.header("Quantifying the Correspondence")

st.image("outputs/figures/sif_rainfall_correlation_scatter.png", use_container_width=True)
styled_caption(
    "District SIF (day-of-year 273) against rainfall anomaly (%), 72 district-years, "
    "with a linear fit (Pearson r = 0.53, p < 0.0001)."
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Pearson r (DOY 273 SIF)", "0.53")
with m2:
    st.metric("Pearson r (season-mean SIF)", "0.74")
with m3:
    st.metric("Fixed-effects p (season-mean)", "0.37")
with m4:
    st.metric("District-years (n)", "72")

st.warning("""
The correlation is real across districts and years, but it does not survive district and
year fixed effects, and the 72 observations are not independent: neighbouring districts
share weather (see Moran's I below). I read it as consistent with SIF responding to
rainfall at the regional scale, not as evidence that SIF tracks year-to-year rainfall
within a district.
""")

section_divider()

st.header("How Non-Independent? A Moran's I Check")

st.markdown("""
I computed **Moran's I** for district SIF and rainfall anomaly in each year, with
Queen-contiguity weights built from the district polygons (mean 3.25 neighbours per
district) and a 9,999-permutation test.
""")

st.image("outputs/figures/spatial_autocorrelation_morans_i.png", use_container_width=True)
styled_caption(
    "Moran's I for district SIF (day-of-year 273) and rainfall anomaly, by year "
    "(* = p < 0.05, 9,999 permutations)."
)

st.info("""
**Rainfall anomaly is spatially clustered in all 9 years** (Moran's I 0.26–0.56,
p < 0.05). **Day-of-year-273 SIF is clustered in 4 of 9 years** (2015, 2016, 2018, 2020;
I = 0.26–0.31) and not in 2017, 2019, 2021, 2022 or 2023 (I = 0.05–0.22). **Season-mean
SIF is clustered in all 9 years** (I = 0.29–0.54), so the spatial pattern is clearer in the
seasonal average than on a single date. Either way the district observations are not
independent, which is why I rely on the clustered and fixed-effects versions of the
correlation above rather than on the plain p-value.
""")

styled_caption("GREEN ALIBI — Spatial Patterns: SIF, Rainfall and Their Correspondence")
