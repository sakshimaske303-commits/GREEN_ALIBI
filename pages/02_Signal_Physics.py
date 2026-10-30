import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption, MAGENTA, TEAL

st.set_page_config(page_title="Signal Physics — GREEN ALIBI", layout="wide")
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


st.title("Signal Physics: Fluorescence and Reflectance")

page_contents([("SIF: where absorbed sunlight goes", "fluorescence"),
               ("NDVI: reflectance and a direct comparison", "reflectance")])

part_heading("Part 1 of 2 · Solar-Induced Fluorescence",
             "Fluorescence Physics: Where Does Absorbed Sunlight Actually Go?", "fluorescence")

st.markdown("""
The expectation I tested rests on a piece of plant biophysics: when a leaf absorbs sunlight,
that energy has more than one possible fate. This part covers what SIF physically measures
and why it is expected to respond to stress sooner than NDVI. Whether that shows up in the
satellite data is a separate question, answered on the **Seasonal Lead**, **Drought Alarms and
Policy Triggers** and **Findings** pages.
""")

section_divider()

col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    st.image("outputs/figures/fluorescence_physics_diagram.png", use_container_width=True)
    styled_caption(
        "Energy partitioning of absorbed sunlight in photosynthesis, and its shift under "
        "drought stress — the physical basis of Solar-Induced Fluorescence."
    )
    st.markdown(
        "<p style='text-align:center; font-size:0.85rem; color:#FBBF24; border:1px solid rgba(251,191,36,0.45); "
        "border-radius:8px; padding:6px 12px; margin:4px auto 0 auto; max-width:720px;'>"
        "&#9432; Visual aid only: this illustration was generated with an AI image tool. "
        "It is not data or a result of this study.</p>",
        unsafe_allow_html=True,
    )

section_divider()

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

st.header("Why Fluorescence Reacts Faster Than Reflectance")

st.markdown("""
Under drought stress, a plant's stomata close to conserve water. This restricts the CO₂
supply to the photosynthetic machinery, which throttles the photochemical pathway (**Φ_P**
drops) almost immediately — within minutes to hours, not days. Because the three yields
must still sum to one, that drop in Φ_P has to be absorbed elsewhere: primarily into
increased non-photochemical quenching, with a resulting shift in the fluorescence yield,
**Φ_F**, as well.

This is the physical basis for SIF's expected early-detection potential: **Φ_F is linked to
the state of the photosynthetic machinery**, which changes quickly. NDVI depends on structural
and pigment properties of the canopy — leaf area, chlorophyll content, cell structure — which
change only once stress has lasted long enough to cause visible damage, over days to weeks.

That is the prediction. In my data it does not show: SIF's drought alarms came within one
composite of NDVI's, with no consistent winner. SIF's normal seasonal decline appears to start first,
but mostly because NDVI does not return to its pre-season level after the monsoon; measured over
each curve's own decline, the lead is small and absent in three of nine years. One reason may be
that canopy SIF largely follows absorbed light (APAR, below) and canopy structure rather than
the fluorescence yield, and GOSIF is itself predicted partly from MODIS reflectance. I can't
separate these mechanisms with this dataset.
""")

section_divider()

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

GOSIF, my main SIF product, is not a direct retrieval. It is a statistically modeled,
gridded reconstruction trained on OCO-2's sparse SIF soundings, with MODIS reflectance and
MERRA-2 reanalysis as predictors. That is what gives a gap-free 0.05°, 8-day series over
Marathwada, but it also means GOSIF and MODIS NDVI are not fully independent. To check this
I repeated the lag analysis with TROPOMI SIF (TROPOSIF v2.1), a direct retrieval available
for 2018–2020. TROPOMI agreed on the direction of the lead in all three years.
""")

part_heading("Part 2 of 2 · NDVI",
             "NDVI Physics: Reflectance, Radiative Transfer, and a Direct Comparison to SIF", "reflectance")

st.markdown("""
Part 1 covered SIF's physical basis. This part covers the physics behind NDVI, the index I
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
        "Stays well above its pre-season level after the monsoon, which makes its decline look late on a season scale. As a drought anomaly (z < −3) it was within one composite of SIF in 11 of 12 district-years flagged by both (SIF earlier in 7, same date in 2, NDVI earlier in 3)"
    ]
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

section_divider()

st.header("Connecting the Physics to This Study's Hypotheses")

st.markdown("""
H1 predicts SIF's seasonal decline starts before NDVI's, because Φ_F responds quickly while
NDVI depends on slower structural change. The **Seasonal Lead**
page tests this; the lead is large when each curve is scaled over the whole season, but
mostly because NDVI does not return to its pre-season level, and small or absent when each
curve is scaled over its own decline. H2 predicts the lag varies between districts; it does
not once the scaling is matched (Friedman p = 0.97). H3 predicts drought widens the lag; it
does not. H4 predicts SIF departs from its normal-year range before NDVI in drought years; it
does not — the two alarms came within one composite of each other, with no consistent winner. So
the physics explains why SIF might lead, but in this dataset it did not translate into an
earlier drought signal.
""")

styled_caption("GREEN ALIBI — Signal Physics: Fluorescence and Reflectance")
