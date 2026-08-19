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
**1.** SIF's post-peak seasonal decline precedes NDVI's decline in seven of the eight study
years (all but 2018) — supporting SIF's physical basis as a more temporally responsive
stress indicator (**H1**, general form: supported, though not universal). This finding is
corroborated by two independent lag-estimation methods (threshold-crossing and
cross-correlation — see **Lag Analysis**): no year shows SIF trailing NDVI under either
method, though the cross-correlation method registers 2018, 2020, 2022, and 2023 as
essentially zero-lag rather than strictly positive.
""")

st.warning("""
**2.** The hypothesis that drought amplifies the SIF–NDVI lag (**H3**) is **not
supported, replicated at more than double the original sample size**. Mean lag was smaller
in the two drought years (7.6 days average) than in the six normal years (15.0 days
average) — the same direction found in the original three-year study.
""")

st.info("""
**3.** District-level spatial analysis identifies **Osmanabad** as the most consistently
low-SIF district (lowest of all eight districts in 7 of 8 years), with **Bid** taking over
as the single lowest-SIF district specifically in 2018. This corresponds spatially with the
districts recording the largest average rainfall deficits across the full eight-year record
— Osmanabad, Bid, and Aurangabad (**H2**: supported — the effect is not spatially uniform).
This correspondence is confirmed statistically, though more moderately than the original
sample suggested: mean SIF and rainfall anomaly are significantly correlated across all 64
district-year observations (Pearson r = 0.567, Spearman ρ = 0.551, both p < 0.001, down
from r = 0.837 at the original three-year sample size). Unlike the original sample, no
single district is consistently *highest* in SIF — Aurangabad leads most often (4 of 8
years), but the top spot rotates among four different districts across the record.
""")

st.info("""
**4.** Rainfall deficit itself was spatially uneven within Marathwada, particularly in
2018, when eastern districts (Nanded, Hingoli) recorded near-normal or surplus rainfall
despite a region-wide deficit of 18.3% — showing that "drought year" as a single regional
label conceals meaningful sub-regional variation. This west-drier/east-wetter gradient is
not confined to drought years: averaged across all eight years, Osmanabad, Bid, and
Aurangabad run driest on average while Nanded and Hingoli run consistently wettest.
""")

st.info("""
**5.** A bootstrap check confirms Finding 1's *direction* is robust — no year's
bootstrap-estimated lag distribution dips meaningfully below zero — but shows both its
*exact magnitude* and *consistency* are not: the share of bootstrap replicates showing a
strictly positive lag ranges from under 1% (2023) to 96.8% (2017), and all 28 pairwise
between-year comparisons of confidence intervals overlap. Separately, Moran's I confirms —
with a number rather than a caveat — that the district-level rainfall data behind Finding 3
are spatially clustered in all 8 of 8 years, while SIF is spatially clustered in only 4 of 8
years (down from 3 of 3 in the original sample). Neither check overturns a finding; both
state precisely how much confidence each finding can support. See **Lag Analysis** and
**Combined Comparison** for the full detail.
""")

st.warning("""
**6.** Comparing SIF's and NDVI's 2018 stress-onset dates against the one well-documented
official government drought declaration available (Maharashtra, 31 October 2018) shows a
**genuine reversal** from the study's central finding: NDVI actually crossed its 90%-decline
threshold *before* SIF in 2018 (NDVI: 4 Sep, 57.4 days prior; SIF: 8 Sep, 52.6 days prior) —
consistent with 2018's near-zero and slightly negative lag reported throughout this study.
Both satellite indicators still led the official declaration by roughly **seven to eight
weeks**, a far larger gap than the few-day SIF-vs-NDVI difference that is this study's
central finding. The practically larger opportunity may be satellite monitoring of *either*
kind, versus the current declaration timeline, with SIF's physiological edge over NDVI as a
smaller, year-dependent refinement on top of that — not present in 2018 itself. A
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
    st.metric("SIF leads NDVI decline", "7 / 8 years")
with c2:
    st.metric("Drought-lag amplification (H3)", "Not supported")
with c3:
    st.metric("Rainfall-confirmed drought years", "2 / 8")
with c4:
    st.metric("Spatial SIF-rainfall match", "r = 0.567 ✓")

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("Cross-correlation: lag never negative", "8 / 8 years")
with c6:
    st.metric("Moran's I — rainfall significant", "8 / 8 years")
with c7:
    st.metric("Moran's I — SIF significant", "4 / 8 years")
with c8:
    st.metric("Satellite lead vs. official declaration (2018)", "~7–8 weeks")

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
- The sample, now eight years (2015–2023, excluding 2021), is still unbalanced toward
  normal years: only 2 of 8 years (2015, 2018) meet this study's own rainfall-anomaly
  drought threshold (z-score < -0.5), against 6 normal years. This is itself a finding —
  the original three-year sample (2 of 3 drought years) was considerably more drought-heavy
  than Marathwada's actual climate record — but it also means drought-year statistics in
  this study still rest on an n of 2, not a larger balanced sample.
- 2018 is a genuine, unexplained exception to this study's central SIF-leads-NDVI finding:
  its threshold-crossing lag is marginally negative, its cross-correlation lag is exactly
  zero, only 8.1% of its bootstrap replicates show a positive lag, and its RQ3
  official-declaration comparison shows NDVI crossing threshold *before* SIF — the opposite
  ordering from every other year with a positive lag. No crop-type, sowing-date, or other
  covariate data was available to investigate why 2018 specifically differs; it is reported
  as an open question, not resolved.
- The spatial correspondence between rainfall deficit and SIF stress was tested via
  Pearson and Spearman correlation (r = 0.567, ρ = 0.551, both p < 0.001) rather than left
  as a purely visual comparison; however, with only eight independent study years and eight
  geographically adjacent districts, the 64 district-year observations are not fully
  independent, and this correlation should be read as real but moderate corroborating
  evidence rather than a formally independent statistical confirmation. This is now
  quantified, not just asserted: Moran's I is significantly positive (p < 0.05) for
  rainfall anomaly in all 8 years, but for mean SIF in only 4 of 8 years — a genuine,
  year-dependent weakening from the original three-year sample, where all three years were
  significant for both variables (see **Combined Comparison**).
- The low-SIF zones identified have not been validated against ground-level crop-stress
  or drought-impact reporting for the districts concerned.
- District-level rainfall anomaly was computed relative to a single region-wide
  climatological baseline rather than a per-district climatology.
- SIF- and NDVI-based stress timing was compared against the one well-documented official
  drought-declaration date I could find (Maharashtra, 31 October 2018).
  A comparably verifiable single declaration date for 2015 could not be located, so this
  comparison remains partial — one of eight study years — rather than complete, and that
  one year happens to be 2018, the study's own sign-reversal exception.
- The Earth Engine-based acquisition step for the five newly added years was rewritten as
  a standalone Python script (`src/acquisition/gee_data_acquisition.py`) and was actually
  executed for all eight study years during the sample-size expansion — unlike the original
  three-year study, where this step had only been run interactively and never as a checked-in
  script. Running it surfaced three genuine bugs (a missing Earth Engine Cloud project, a
  MODIS sinusoidal-projection clip error, and the "Beed"/"Bid" district-naming mismatch
  recurring independently in the new script, despite already having been fixed once in the
  original interactive workflow) — all caught and fixed before any figure in this dashboard
  was computed, and documented in the **Development Log**. This closes the original
  reproducibility gap rather than only improving it on paper.
- The exact lag values in **Lag Analysis**, and their year-to-year ranking, carry wider
  uncertainty than the point estimates alone suggest — see the bootstrap confidence
  intervals there, where all 28 pairwise between-year comparisons overlap.
""")

section_divider()

# ============================================================
# CONCLUSION
# ============================================================
st.header("Conclusion")

st.markdown("""
This study finds consistent evidence that Solar-Induced Fluorescence registers the onset
of post-peak seasonal vegetation decline earlier than, or no later than, NDVI in seven of
the eight years studied in Marathwada, Maharashtra — supporting SIF's physical basis,
developed on the **Physics** pages, as a more temporally responsive stress indicator in
most, though not all, years. It does not find evidence that this lag is amplified
specifically by drought conditions — the opposite direction replicated at more than double
the original sample size — and identifies substantial inter-annual and intra-regional
variation that a simple drought/normal binary does not capture. Expanding the sample from
three years to eight also surfaced a genuine, unexplained exception: 2018, despite being
one of only two years meeting this study's own drought threshold, shows an essentially
zero or reversed lag across every method used to measure it.

Independent rainfall validation and spatial cross-referencing between SIF and
precipitation data lend physical coherence to the district-level findings — a
correspondence confirmed statistically at eight years, though more moderately than the
original three-year sample suggested (Pearson r = 0.567, Spearman ρ = 0.551, both
p < 0.001, versus the original r = 0.837), and further characterized, via Moran's I, rather
than only caveated. A comparison against the one available official drought-declaration
date (2018) suggests the practical policy case is better framed as "satellite monitoring
generally, refined by SIF specifically, in most years" than as SIF's edge over NDVI being a
uniform, dominant lever on payout timing — precisely because 2018, the one year with a
verifiable declaration date, is also the year where that edge disappears. Several
limitations — an unbalanced 2-versus-6 drought/normal split, the unexplained 2018 exception,
absence of ground validation, and the spatial non-independence underlying the correlation
above — are reported directly rather than resolved beyond what the available data supports.
The Earth Engine acquisition step, unlike in the original study, was actually scripted and
executed for all eight years during this expansion, closing what had been an open
reproducibility gap.
""")

st.markdown("""
---
*GREEN ALIBI — an independent satellite-verification study, Marathwada, Maharashtra.*
""")

styled_caption("GREEN ALIBI — Findings, Limitations & Conclusion")