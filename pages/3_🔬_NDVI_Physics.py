import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="NDVI Physics — GREEN ALIBI", page_icon="🔬", layout="wide")
apply_custom_style()

st.title("🔬 NDVI Physics: Reflectance, Radiative Transfer, and a Direct Comparison to SIF")

st.markdown("""
Part 1 covered SIF's physical basis. This page covers the physics behind NDVI — the
indicator SIF is being tested against — and lays out, directly, how the two differ in what
they are physically sensitive to and on what timescale.
""")

section_divider()

# ============================================================
# DIAGRAM — placed prominently near the top, large and centered
# ============================================================
col_a, col_b, col_c = st.columns([1, 4, 1])
with col_b:
    st.image("outputs/figures/ndvi_physics_diagram.png", use_container_width=True)
    styled_caption(
        "The physical basis of NDVI: red light absorption by chlorophyll in the palisade "
        "mesophyll versus multiple scattering and reflection of near-infrared light in "
        "the spongy mesophyll."
    )

section_divider()

# ============================================================
# NDVI'S PHYSICAL BASIS
# ============================================================
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

# ============================================================
# THE ATMOSPHERIC COMPLICATION
# ============================================================
st.header("A Complication: What the Satellite Actually Sees Is Not Always the Ground")

st.markdown("""
Reflectance-based measurements like NDVI are also vulnerable to a purely atmospheric
physical problem: cloud and cloud-shadow contamination. Clouds scatter incoming sunlight
(via Mie scattering from water droplets, orders of magnitude stronger than the Rayleigh
scattering from clear-sky air molecules) before it ever reaches the ground, and a satellite
sensor observing through or near a cloud records a reflectance value dominated by
atmospheric scattering rather than the vegetation surface beneath it. This is a real,
practical issue encountered directly in this project's own data processing (documented in
the **Data & Methodology** page) — Marathwada's growing season overlaps with the monsoon,
and an initial NDVI extraction without explicit cloud-quality filtering produced
physically implausible swings inconsistent with any real vegetation phenology, before being
corrected using MODIS's own cloud-screening quality band.
""")

section_divider()

# ============================================================
# SIDE-BY-SIDE COMPARISON
# ============================================================
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
        "Declines before (or no later than) NDVI in all 8 study years; 2018 is a near-simultaneous exception"
    ],
    "NDVI": [
        "Differential reflectance from chlorophyll absorption and leaf structural scattering",
        "Canopy structure, leaf area, chlorophyll content — accumulated structural state",
        "Days to weeks",
        "Simple reflectance-band ratio",
        "Cloud/cloud-shadow contamination, saturation at high biomass",
        "Declines later, after SIF has already begun dropping"
    ]
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

section_divider()

# ============================================================
# WHY THIS MATTERS FOR THE HYPOTHESES
# ============================================================
st.header("Connecting the Physics to This Study's Hypotheses")

st.markdown("""
H1 predicts SIF should decline before NDVI, directly because Φ_F is coupled to a fast
biochemical process while NDVI depends on slow structural change — this is the physical
mechanism the **Seasonal Trajectories** and **Lag Analysis** pages test quantitatively. H2
predicts this lag need not be spatially uniform, since local canopy structure, crop type,
and soil-moisture buffering can all modulate how quickly photochemical stress translates
into a measurable SIF signal — tested on the **Spatial SIF Analysis** page. H3 predicts
drought severity should scale the size of this lag; whether the physical picture developed
here actually holds up under real, independently-validated rainfall data is addressed
honestly, including where it does not hold up, in the **Lag Analysis** and **Findings**
pages.
""")

styled_caption("GREEN ALIBI — The Physics, Part 2: NDVI's Mechanism and a Direct SIF Comparison")