import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Findings & Conclusion — GREEN ALIBI", page_icon="📝", layout="wide")
apply_custom_style()

st.title("📝 Key Findings, Limitations & Conclusion")

section_divider()

# ============================================================
# KEY FINDINGS
# ============================================================
st.header("Key Findings")

st.success("""
**1.** SIF's post-peak seasonal decline consistently precedes NDVI's decline across all
three study years (2015, 2018, 2020) — supporting SIF's physical basis as a more
temporally responsive stress indicator (**H1**, general form: supported).
""")

st.warning("""
**2.** The hypothesis that drought amplifies the SIF–NDVI lag (**H3**) is **not
supported**. Mean lag was smaller in the two drought years (14.6 days) than in the normal
year (25.5 days), and the two drought years differed substantially from each other
(24.2 vs. 5.1 days).
""")

st.info("""
**3.** District-level spatial analysis identifies a consistent low-SIF zone in the western
and southwestern districts (Aurangabad, Beed, Latur, Osmanabad) during both drought years,
corresponding spatially with the districts recording the largest rainfall deficits in the
same years (**H2**: supported — the effect is not spatially uniform). This correspondence
is confirmed statistically: mean SIF and rainfall anomaly are strongly correlated across
all district-year observations (Pearson r = 0.837, Spearman ρ = 0.857, both p < 0.001).
""")

st.info("""
**4.** Rainfall deficit itself was spatially uneven within Marathwada, particularly in
2018, when eastern districts (Nanded, Hingoli) recorded near-normal or surplus rainfall
despite a region-wide deficit of 18.3% — showing that "drought year" as a single regional
label conceals meaningful sub-regional variation.
""")

section_divider()

# ============================================================
# SUMMARY METRICS
# ============================================================
st.header("Study at a Glance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("SIF leads NDVI decline", "3 / 3 years")
with c2:
    st.metric("Drought-lag amplification (H3)", "Not supported")
with c3:
    st.metric("Rainfall-confirmed drought years", "2 / 2")
with c4:
    st.metric("Spatial SIF-rainfall match", "r = 0.837 ✓")

section_divider()

# ============================================================
# LIMITATIONS
# ============================================================
st.header("Limitations")

st.markdown("""
- GOSIF (the SIF product used here) is a statistically modeled reconstruction, not a
  direct satellite retrieval — it combines OCO-2 SIF soundings with MODIS reflectance
  data and meteorological reanalysis. Since MODIS reflectance also underlies the NDVI
  used for comparison, the two variables are not fully independent at the input-data
  level, a property of the dataset choice this study does not attempt to quantify or
  correct for.
- The sample size (three years: two drought, one normal) is small, and the two drought
  years differ substantially from one another, limiting generalizability of any drought/
  normal comparison.
- The spatial correspondence between rainfall deficit and SIF stress was tested via
  Pearson and Spearman correlation (r = 0.837, ρ = 0.857, both p < 0.001) rather than left
  as a purely visual comparison; however, with only three independent study years and
  eight geographically adjacent districts, the 24 district-year observations are not
  fully independent, and this correlation should be read as strong corroborating evidence
  rather than a formally independent statistical confirmation.
- The low-SIF zones identified have not been validated against ground-level crop-stress
  or drought-impact reporting for the districts concerned.
- District-level rainfall anomaly was computed relative to a single region-wide
  climatological baseline rather than a per-district climatology.
- This study does not compare SIF-based stress timing against official drought-
  declaration dates, which was outside the scope of the data acquired.
""")

section_divider()

# ============================================================
# CONCLUSION
# ============================================================
st.header("Conclusion")

st.markdown("""
This study finds consistent evidence that Solar-Induced Fluorescence registers the onset
of post-peak seasonal vegetation decline earlier than NDVI across all years studied in
Marathwada, Maharashtra — supporting SIF's physical basis, developed on the **Physics**
pages, as a more temporally responsive stress indicator. It does not find evidence that
this lag is amplified specifically by drought conditions, and identifies substantial
inter-annual and intra-regional variation that a simple drought/normal binary does not
capture.

Independent rainfall validation and spatial cross-referencing between SIF and
precipitation data lend physical coherence to the district-level findings — a
correspondence now confirmed statistically (Pearson r = 0.837, Spearman ρ = 0.857, both
p < 0.001) rather than resting on visual impression alone — while several limitations —
sample size, absence of ground validation, and the spatial non-independence underlying the
correlation above — are reported directly rather than resolved beyond what the available
data supports.
""")

st.markdown("""
---
*GREEN ALIBI — an independent satellite-verification study, Marathwada, Maharashtra.*
""")

styled_caption("GREEN ALIBI — Findings, Limitations & Conclusion")