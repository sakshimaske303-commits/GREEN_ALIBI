import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="NDVI Physics — GREEN ALIBI", page_icon="🔬", layout="wide")
apply_custom_style()

st.title("🔬 NDVI Physics: Reflectance, Radiative Transfer, and a Direct Comparison to SIF")

st.markdown("""
Part 1 covered SIF's physical basis. This page covers the physics behind NDVI, the index I
test SIF against, and how the two differ in what they are sensitive to and on what timescale.
""")

section_divider()

col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    st.image("outputs/figures/ndvi_physics_diagram.png", use_container_width=True)
    styled_caption(
        "The physical basis of NDVI: red light absorption by chlorophyll in the palisade "
        "mesophyll versus multiple scattering and reflection of near-infrared light in "
        "the spongy mesophyll."
    )
    st.markdown(
        "<p style='text-align:center; font-size:0.85rem; color:#FBBF24; border:1px solid rgba(251,191,36,0.45); "
        "border-radius:8px; padding:6px 12px; margin:4px auto 0 auto; max-width:720px;'>"
        "&#9432; Visual aid only: this illustration was generated with an AI image tool. "
        "It is not data or a result of this study.</p>",
        unsafe_allow_html=True,
    )

section_divider()

st.header("NDVI: A Reflectance-Based Index")

st.latex(r"NDVI = \frac{NIR - RED}{NIR + RED}")

st.markdown("""
NDVI is built from a genuine, well-established piece of leaf optics. Chlorophyll strongly
**absorbs** red light (roughly 620–680 nm) to drive photosynthesis, so healthy, chlorophyll-
rich leaves reflect very little red light. In the near-infrared (roughly 750–1300 nm),
chlorophyll does not absorb at all — instead, incoming light is scattered multiple times
between a leaf's internal mesophyll cell walls and the air spaces between them, a
consequence of the refractive-index mismatch between plant cell material and air. This
multiple scattering causes healthy leaves to reflect a large fraction of NIR light. NDVI's
large positive values for healthy vegetation come directly from this contrast: low red
reflectance (absorption) alongside high NIR reflectance (structural scattering).

Because NDVI is fundamentally about **canopy structure and pigment content**, it only
changes once those physical properties have actually changed — a reduction in leaf area
index, a genuine drop in chlorophyll concentration, or physical degradation of the
mesophyll's internal scattering structure. All of these are consequences of *sustained*
physiological stress, not its earliest onset.
""")

section_divider()

st.header("A Complication: What the Satellite Actually Sees Is Not Always the Ground")

st.markdown("""
Reflectance-based measurements like NDVI are also vulnerable to a purely atmospheric
physical problem: cloud and cloud-shadow contamination. Clouds scatter incoming sunlight
(via Mie scattering from water droplets, orders of magnitude stronger than the Rayleigh
scattering from clear-sky air molecules) before it ever reaches the ground, and a satellite
sensor observing through or near a cloud records a reflectance value dominated by
atmospheric scattering rather than the vegetation surface beneath it. Marathwada's growing
season overlaps with the monsoon, so this matters here. I keep only MOD13Q1 pixels that its
`SummaryQA` band marks as good or marginal quality, and only cropland pixels. Because a 16-day
MOD13Q1 value can come from any day in its window, I date each composite by the mean of its
pixels' actual observation days (`DayOfYear` band), not by the window start.
""")

section_divider()

st.header("SIF vs. NDVI: A Direct Comparison")

comparison_df = pd.DataFrame({
    "Property": [
        "Physical basis",
        "What it responds to",
        "Response timescale",
        "Retrieval principle",
        "Vulnerable to",
        "This study's finding"
    ],
    "SIF": [
        "Re-emitted photon energy from the photosynthetic light reaction",
        "Photochemical efficiency (Φ_P) and quenching (Φ_NPQ) — real-time physiology",
        "Minutes to hours",
        "Fraunhofer line-filling in reflected sunlight",
        "Faint signal, geometric/canopy escape effects",
        "Not an earlier drought alarm. Seasonal decline first in 9/9 years when scaled over the season, but only 6/9 (−5.5 to +13.4 days) when scaled over its own decline."
    ],
    "NDVI": [
        "Differential reflectance from chlorophyll absorption and leaf structural scattering",
        "Canopy structure, leaf area, chlorophyll content — accumulated structural state",
        "Days to weeks",
        "Simple reflectance-band ratio",
        "Cloud/cloud-shadow contamination, saturation at high biomass",
        "Stays well above its pre-season level after the monsoon, which makes its decline look late on a season scale. As a drought anomaly (z < −3) it coincided with SIF in 6 of 12 district-years flagged by both and was earlier in 5 (SIF in 1)"
    ]
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

section_divider()

st.header("Connecting the Physics to This Study's Hypotheses")

st.markdown("""
H1 predicts SIF's seasonal decline starts before NDVI's, because Φ_F responds quickly while
NDVI depends on slower structural change. The **Seasonal Trajectories** and **Lag Analysis**
pages test this; the lead is large when each curve is scaled over the whole season, but
mostly because NDVI does not return to its pre-season level, and small or absent when each
curve is scaled over its own decline. H2 predicts the lag varies between districts; it does
not once the scaling is matched (Friedman p = 0.97). H3 predicts drought widens the lag; it
does not. H4 predicts SIF departs from its normal-year range before NDVI in drought years; it
does not — the two mostly coincided, and NDVI was otherwise usually first. So
the physics explains why SIF might lead, but in this dataset it did not translate into an
earlier drought signal.
""")

styled_caption("GREEN ALIBI — The Physics, Part 2: NDVI's Mechanism and a Direct SIF Comparison")
