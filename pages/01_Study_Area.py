import os
import streamlit as st
import streamlit.components.v1 as components
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Study Area — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Study Area: Marathwada, Maharashtra")

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
regions with different baseline climates. CHIRPS rainfall (see Rainfall Validation) shows
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
sanity-check the spatial results (see Spatial SIF Analysis).
""")

section_divider()

st.info("""
Every calculation uses the FAO GAUL 2015 level-2 outline of these eight districts, not a
bounding rectangle. GAUL spells Beed as "Bid", so that is the name used in tables and maps.
SIF and NDVI are both restricted to cropland (see **Data & Methodology**).
""")

styled_caption("GREEN ALIBI — Study Area")
