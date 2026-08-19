import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Fluorescence Physics — GREEN ALIBI", page_icon="🔬", layout="wide")
apply_custom_style()

st.title("🔬 Fluorescence Physics: Where Does Absorbed Sunlight Actually Go?")

st.markdown("""
This project's central claim rests on a specific piece of plant biophysics: when a leaf
absorbs sunlight, that energy does not have only one possible fate. Understanding what SIF
physically measures — and why it responds to stress on a different timescale than NDVI —
starts here.
""")

section_divider()

# ============================================================
# DIAGRAM — placed prominently near the top, large and centered
# ============================================================
col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    st.image("outputs/figures/fluorescence_physics_diagram.png", use_container_width=True)
    styled_caption(
        "Energy partitioning of absorbed sunlight in photosynthesis, and its shift under "
        "drought stress — the physical basis of Solar-Induced Fluorescence."
    )
    styled_caption(
        "AI was used to help generate this image, but the concept and every detail in it are mine."
    )

section_divider()

# ============================================================
# THE THREE PATHWAYS
# ============================================================
st.header("The Three Fates of Absorbed Light Energy")

st.markdown("""
When a chlorophyll molecule inside a leaf absorbs a photon of sunlight, the resulting
excitation energy can only go one of three places. This is not approximate — it follows
directly from conservation of energy at the level of the photosynthetic reaction center:
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("1. Photochemistry")
    st.markdown("""
    The energy drives the electron transport chain, splitting water and ultimately fixing
    CO₂ into sugars. This is the pathway photosynthesis is "for," and the fraction of
    energy channeled here is denoted **Φ_P**.
    """)
with col2:
    st.subheader("2. Heat (NPQ)")
    st.markdown("""
    Excess energy the plant cannot safely use for photochemistry is dissipated as heat,
    through a regulated protective process called **non-photochemical quenching (NPQ)**.
    Its yield is denoted **Φ_NPQ**.
    """)
with col3:
    st.subheader("3. Fluorescence")
    st.markdown("""
    A small remaining fraction — typically 0.5–2% of absorbed energy — is re-emitted as
    light at a slightly longer wavelength than what was absorbed. This is **chlorophyll
    fluorescence**, with yield **Φ_F**. This is what SIF measures.
    """)

st.markdown("Because these three pathways account for all of the absorbed energy, their yields must sum to one:")

st.latex(r"\Phi_P + \Phi_{NPQ} + \Phi_F = 1")

section_divider()

# ============================================================
# WHY THIS RESPONDS FAST
# ============================================================
st.header("Why Fluorescence Reacts Faster Than Reflectance")

st.markdown("""
Under drought stress, a plant's stomata close to conserve water. This restricts the CO₂
supply to the photosynthetic machinery, which throttles the photochemical pathway (**Φ_P**
drops) almost immediately — within minutes to hours, not days. Because the three yields
must still sum to one, that drop in Φ_P has to be absorbed elsewhere: primarily into
increased non-photochemical quenching, with a resulting shift in the fluorescence yield,
**Φ_F**, as well.

This is the physical basis for SIF's early-detection potential: **Φ_F is coupled directly
to the real-time state of the electron transport chain**, a fast biochemical process. NDVI,
by contrast, depends on structural and pigment properties of the leaf and canopy — leaf
area, chlorophyll concentration, cell structure — which only change once sustained stress
has caused actual physiological damage. That structural degradation is a slow process,
typically unfolding over days to weeks, not hours. The lag this project measures between
SIF and NDVI is, physically, the gap between these two timescales: a fast biochemical
signal versus a slow structural one.
""")

section_divider()

# ============================================================
# THE SIF SIGNAL EQUATION
# ============================================================
st.header("What a Satellite Actually Receives")

st.markdown("""
The SIF radiance an instrument observes is not simply Φ_F — it depends on how much light
the canopy absorbed in the first place, and how much of the emitted fluorescence photons
actually escape the canopy structure without being reabsorbed by neighboring leaves:
""")

st.latex(r"SIF = APAR \times \Phi_F \times f_{esc}")

st.markdown("""
where **APAR** is the absorbed photosynthetically active radiation, **Φ_F** is the
fluorescence quantum yield described above, and **f_esc** is the canopy escape probability.
This is why SIF is described as a joint signal of *how much light a canopy is intercepting*
and *how efficiently it is using that light* — both physiologically meaningful quantities.
""")

section_divider()

# ============================================================
# HOW SATELLITES SEE FLUORESCENCE AT ALL
# ============================================================
st.header("Measuring a Faint Signal Hidden in Sunlight")

st.markdown("""
Chlorophyll fluorescence is faint — roughly 1–2% of reflected sunlight in the same
wavelength range — which makes it very difficult to separate fluorescence from ordinary
reflected light using a standard spectrometer. Satellite SIF retrieval exploits a specific
feature of the solar spectrum to solve this: **Fraunhofer lines**, narrow dark absorption
lines in sunlight caused by atoms in the Sun's own atmosphere absorbing specific
wavelengths before the light ever reaches Earth.

Within a Fraunhofer line, incoming sunlight is naturally very dim. A vegetated surface,
however, still emits fluorescence at that exact wavelength — fluorescence is generated by
the plant, not reflected from the sun, so it is *not* suppressed by the Fraunhofer
absorption. The result is that a vegetated pixel appears anomalously brighter within a
Fraunhofer line than bare ground does, and the size of that "filled-in" brightness is used
to retrieve the fluorescence signal directly. Instruments such as OCO-2, GOME-2, and
TROPOMI all exploit this principle, at different Fraunhofer wavelengths, to retrieve SIF
from space.

The GOSIF product used in this study is not a direct satellite retrieval itself, but a
statistically modeled, gridded reconstruction — trained to match OCO-2's sparse, discrete
SIF retrievals using continuous MODIS reflectance and reanalysis meteorological data as
predictors — which is what makes a complete, gap-free 0.05°, 8-day time series over
Marathwada possible in the first place.
""")

styled_caption("GREEN ALIBI — The Physics, Part 1: Energy Partitioning and Fluorescence Retrieval")