import os
import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption, MAGENTA, TEAL

st.set_page_config(page_title="Study Area and Interactive Maps — GREEN ALIBI", layout="wide")
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


st.title("Study Area: Marathwada, Maharashtra")

page_contents([("The study area", "study-area"), ("Interactive maps and plots", "interactive-maps")])

part_heading("Part 1 of 2", "The Study Area", "study-area")

st.markdown("""
The study region comprises the eight districts constituting **Marathwada**, a division of
Maharashtra state in western India, selected for its recurring, well-documented history of
agricultural drought — including the 2015 drought, the Latur water crisis that followed in 2016, and the 2018 drought
that affected much of the region.
""")

section_divider()


col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    interactive_map_path = "outputs/interactive_maps/maps/marathwada_study_area.html"
    if os.path.exists(interactive_map_path):
        with open(interactive_map_path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=480)
        styled_caption(
            "Figure 1. The eight constituent districts of Marathwada — the exact FAO GAUL "
            "2015 level-2 boundary used for every calculation in this study. Hover a district for its name."
        )
    else:
        st.image("outputs/figures/figure3_study_area_map.png", use_container_width=True)
        styled_caption(
            "Figure 1. Study area: the eight districts of Marathwada, Maharashtra, with district "
            "boundaries and names labeled."
        )

st.subheader("The Eight Districts")
d1, d2, d3, d4 = st.columns(4)
districts = ["Aurangabad", "Jalna", "Parbhani", "Hingoli", "Nanded", "Bid", "Latur", "Osmanabad"]
for col, name in zip([d1, d2, d3, d4, d1, d2, d3, d4], districts):
    col.markdown(f"- {name}")

section_divider()

st.header("Why This Region")

st.markdown("""
Marathwada sits in Maharashtra's rain-shadow zone, east of the Western Ghats, making it
structurally more drought-prone than the state's coastal and western districts. It has a
recent history of drought years, including 2015 and 2018, alongside normal and wet monsoon
years, which gives me nine Kharif seasons (2015–2023) within one region instead of across
regions with different baseline climates. CHIRPS rainfall (see Spatial Patterns) shows
that only 2015 (−21.5%, z = −1.12) and 2018 (−18.4%, z = −0.96) meet my drought criterion
(z < −0.5 against the 2001–2020 mean). That holds under four baselines, and with the 2001–2020
baseline for every cut-off from −0.3 to −0.75. The other seven years range from slightly dry (2023, z = −0.20) to clearly
wet (2022, z = +1.91). Two drought years is the main constraint on everything that compares
drought with normal years, so I also ran the main tests, unchanged, on 2001–2014, where 2001,
2002, 2003, 2004 and 2014 meet the same criterion (see Findings & Conclusion).

The deficit was not even across districts. In 2018, Bid (−38.0%), Aurangabad (−37.3%) and
Osmanabad (−33.9%) had the largest deficits while Hingoli and Nanded had surpluses. Across
the 72 district-years, 15 count as drought district-years against each district's own rainfall
record (17 against the regional mean). I'm from Vidarbha, next door, so
I had a rough local sense of which districts are usually hit hardest, which helped me
sanity-check the spatial results (see Spatial Patterns).
""")

section_divider()

st.info("""
Every calculation uses the FAO GAUL 2015 level-2 outline of these eight districts, not a
bounding rectangle. GAUL spells Beed as "Bid", so that is the name used in tables and maps.
SIF and NDVI are both restricted to cropland (see **Data & Methodology**).
""")

part_heading("Part 2 of 2", "Interactive Maps & Plots", "interactive-maps")

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
    "Bootstrap Confidence Intervals on Cross-Correlation Lag": "outputs/interactive_maps/plots/bootstrap_lag_ci.html",
}

choice = st.selectbox("Pick a map or chart", list(MAPS.keys()))

try:
    with open(MAPS[choice], "r", encoding="utf-8") as f:
        html = f.read()
    components.html(html, height=650, scrolling=True)
except FileNotFoundError:
    st.error(f"File not found at {MAPS[choice]}")

styled_caption(
    "Same data as the static maps and charts elsewhere in this dashboard, in hoverable form. "
    "The SIF map shows day-of-year 273; the lag chart shows threshold-crossing lags, and the "
    "bootstrap chart shows cross-correlation lags, which find no SIF lead in 2019, 2022 and 2023. "
    "The two district maps also appear on the Spatial Patterns page; the charts summarize the "
    "Seasonal Lead page."
)

section_divider()
styled_caption("GREEN ALIBI — Study Area and Interactive Maps")
