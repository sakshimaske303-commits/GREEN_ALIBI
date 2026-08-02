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
temporally responsive stress indicator (**H1**, general form: supported). This finding is
corroborated by two independent lag-estimation methods (threshold-crossing and
cross-correlation — see **Lag Analysis**), which agree on the direction of the lag in
every year even though they don't fully agree on its exact magnitude.
""")

st.warning("""
**2.** The hypothesis that drought amplifies the SIF–NDVI lag (**H3**) is **not
supported**. Mean lag was smaller in the two drought years (15.6 days) than in the normal
year (28.7 days), and the two drought years differed substantially from each other
(24.3 vs. 6.9 days).
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

st.info("""
**5.** A bootstrap check confirms Finding 1's *direction* is robust (SIF's lag was
non-negative in 100% of resampled replicates, every year) but shows its *exact magnitude*
is not: every pairwise between-year comparison of confidence intervals overlaps. Separately,
Moran's I confirms — with a number rather than a caveat — that the district-level SIF and
rainfall data behind Finding 3 are spatially clustered, not independent (all three years,
both variables, p < 0.05). Neither check overturns a finding; both state precisely how much
confidence each finding can support. See **Lag Analysis** and **Combined Comparison** for
the full detail.
""")

st.warning("""
**6.** Comparing SIF's and NDVI's 2018 stress-onset dates against the one well-documented
official government drought declaration available (Maharashtra, 31 October 2018) shows both
satellite indicators crossed their 90%-decline threshold roughly **seven weeks** earlier
(SIF: 8 Sep, 53 days prior; NDVI: 12 Sep, 49 days prior) — a far larger gap than the 3–4 day
SIF-vs-NDVI difference that is this study's central finding. The practically larger
opportunity may be satellite monitoring of *either* kind, versus the current declaration
timeline, with SIF's physiological edge over NDVI as a smaller refinement on top of that. A
comparably verifiable 2015 declaration date could not be located, so this comparison covers
2018 only.
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

c5, c6, c7 = st.columns(3)
with c5:
    st.metric("Bootstrap: lag ≥ 0 (all years)", "100% of replicates")
with c6:
    st.metric("Spatial autocorrelation (Moran's I)", "6 / 6 significant")
with c7:
    st.metric("Satellite lead vs. official declaration (2018)", "~7 weeks")

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
  rather than a formally independent statistical confirmation. This is now quantified, not
  just asserted: Moran's I is significantly positive (p < 0.05) for both variables in all
  three years (see **Combined Comparison**).
- The low-SIF zones identified have not been validated against ground-level crop-stress
  or drought-impact reporting for the districts concerned.
- District-level rainfall anomaly was computed relative to a single region-wide
  climatological baseline rather than a per-district climatology.
- SIF- and NDVI-based stress timing was compared against the one well-documented official
  drought-declaration date located during external review (Maharashtra, 31 October 2018).
  A comparably verifiable single declaration date for 2015 could not be located, so this
  comparison remains partial — one of three study years — rather than complete.
- The Earth Engine queries used to acquire NDVI, the cropland mask, and rainfall data were
  originally run interactively in Earth Engine's Code Editor rather than as checked-in
  scripts. A Python translation (`src/acquisition/gee_data_acquisition.py`) has since been
  added to the repository, but has not itself been executed or verified against the
  original output — this project's environment lacks an authenticated Earth Engine
  account. It is a reproducibility improvement, not a re-verified replacement. Everything
  from the GOSIF clipping step onward remains fully scripted, executed, and reproducible.
- The exact lag values in **Lag Analysis**, and their year-to-year ranking, carry wider
  uncertainty than the point estimates alone suggest — see the bootstrap confidence
  intervals there, where every pairwise between-year comparison overlaps.
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
p < 0.001) and further characterized, via Moran's I, rather than only caveated. A
comparison against the one available official drought-declaration date (2018) suggests the
practical policy case is better framed as "satellite monitoring generally, refined by SIF
specifically" than as SIF's few-day edge over NDVI being the dominant lever on payout
timing. Several limitations — sample size, absence of ground validation, the spatial
non-independence underlying the correlation above, and an acquisition step that is now
scripted but not yet re-executed — are reported directly rather than resolved beyond what
the available data supports.
""")

st.markdown("""
---
*GREEN ALIBI — an independent satellite-verification study, Marathwada, Maharashtra.*
""")

styled_caption("GREEN ALIBI — Findings, Limitations & Conclusion")