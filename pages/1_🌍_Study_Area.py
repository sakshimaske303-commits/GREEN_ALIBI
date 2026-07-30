import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Study Area — GREEN ALIBI", page_icon="🌍", layout="wide")
apply_custom_style()

st.title("🌍 Study Area: Marathwada, Maharashtra")

st.markdown("""
The study region comprises the eight districts constituting **Marathwada**, a division of
Maharashtra state in western India, selected for its recurring, well-documented history of
agricultural drought — including the severe 2015 Latur water crisis and the 2018 drought that
affected much of the region.
""")

section_divider()

# ============================================================
# REFERENCE MAP
# ============================================================

col_a, col_b, col_c = st.columns([1, 3, 1])
with col_b:
    st.image("outputs/figures/fig.jpeg", use_container_width=True)
    styled_caption(
        "Figure 1. Location of the study area — (a) Maharashtra within India, "
        "(b) Marathwada within Maharashtra, (c) the eight constituent districts of Marathwada."
    )

st.subheader("The Eight Districts")
d1, d2, d3, d4 = st.columns(4)
districts = ["Aurangabad", "Jalna", "Parbhani", "Hingoli", "Nanded", "Beed (Bid)", "Latur", "Osmanabad"]
for col, name in zip([d1, d2, d3, d4, d1, d2, d3, d4], districts):
    col.markdown(f"- {name}")

section_divider()

# ============================================================
# WHY MARATHWADA
# ============================================================
st.header("Why This Region")

st.markdown("""
Marathwada sits in Maharashtra's rain-shadow zone, east of the Western Ghats, making it
structurally more drought-prone than the state's coastal and western districts. It has a
recent history of well-documented drought years — including 2015 and 2018, both used as
study years in this project — alongside genuinely normal monsoon years such as 2020, which
provides a natural drought/non-drought comparison within a single, geographically coherent
region rather than across regions with different baseline climates.

Studying one's own home region also carries a practical advantage: local familiarity with
which districts are typically hardest hit made it possible to sanity-check satellite-derived
findings (Section: Spatial SIF Analysis) against independent, real-world expectation, rather
than relying solely on the data in isolation.
""")

section_divider()

# ============================================================
# BOUNDARY PRECISION NOTE
# ============================================================
st.info("""
**A methodological note carried through this entire study:** the exact geographic boundary
used for every calculation here is the precise administrative outline of these eight districts
(FAO GAUL 2015 level-2 dataset) — not an approximate bounding rectangle. This distinction,
and why it mattered, is covered in detail on the **Data & Methodology** page.
""")

styled_caption("GREEN ALIBI — Study Area")