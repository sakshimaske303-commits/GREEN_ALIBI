import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Findings & Conclusion — GREEN ALIBI", page_icon="📝", layout="wide")
apply_custom_style()

st.title("📝 Key Findings, Limitations & Conclusion")

section_divider()

# Key findings
st.header("Key Findings")

st.success("""
**1.** SIF's post-peak seasonal decline precedes NDVI's decline in eight of the nine study
years (all but 2018) under the threshold-crossing method — supporting SIF's physical basis
as a more temporally responsive stress indicator (**H1**, general form: supported, though
not universal). A second, methodologically distinct check (cross-correlation — see **Lag
Analysis**) tells a more mixed story, and only does so honestly after a real bug was found
and fixed: the cross-correlation and bootstrap scripts originally searched only
non-negative lags, making it impossible for either to ever find NDVI leading SIF. Corrected
and rerun, cross-correlation shows SIF clearly leading in 5 of 9 years, a tie in 1 (2020),
and NDVI clearly leading in 3 (2018, 2022, 2023) — 2 of those backed by a bootstrap where
99%+ of replicates land below zero.
""")

st.warning("""
**2.** The hypothesis that drought amplifies the SIF–NDVI lag (**H3**) is **not
supported, replicated at three times the original sample size**. Mean lag was smaller
in the two drought years (7.6 days average) than in the seven normal years (15.1 days
average) — the same direction found in the original three-year study.
""")

st.info("""
**3.** District-level spatial analysis identifies **Osmanabad** as the most consistently
low-SIF district (lowest of all eight districts in 8 of 9 years), with **Bid** taking over
as the single lowest-SIF district specifically in 2018. This corresponds spatially with the
districts recording the largest average rainfall deficits across the full nine-year record
— Osmanabad, Bid, and Aurangabad (**H2**: supported — the effect is not spatially uniform).
This correspondence is confirmed statistically, though more moderately than the original
sample suggested: mean SIF and rainfall anomaly are significantly correlated across all 72
district-year observations (Pearson r = 0.531, Spearman ρ = 0.504, both p < 0.0001, down
from r = 0.837 at the original three-year sample size). Unlike the original sample, no
single district is consistently *highest* in SIF — Aurangabad leads most often (5 of 9
years), but the top spot rotates among four different districts across the record.
""")

st.info("""
**4.** Rainfall deficit itself was spatially uneven within Marathwada, particularly in
2018, when eastern districts (Nanded, Hingoli) recorded near-normal or surplus rainfall
despite a region-wide deficit of 18.3% — showing that "drought year" as a single regional
label conceals meaningful sub-regional variation. This west-drier/east-wetter gradient is
not confined to drought years: averaged across all nine years, Osmanabad, Bid, and
Aurangabad run driest on average while Nanded and Hingoli run consistently wettest.
""")

st.info("""
**5.** A bootstrap check, rerun after the same fix applied to Finding 1's cross-correlation
numbers, shows Finding 1's direction is genuinely mixed rather than uniformly robust: 2022
and 2023 have 99%+ of replicates landing below zero (a strong NDVI-leads signal), 2018 leans
the same way at 87.4%, and four years (2015, 2016, 2017, 2019) show reasonable-to-strong
evidence in the SIF-leads direction, while 2020 and 2021 both sit almost exactly on the
fence. Of the 36 possible pairwise between-year
comparisons, 32 still overlap, but 4 — 2015 vs. 2022, 2015 vs. 2023, 2017 vs. 2022, 2017 vs.
2023 — are genuinely distinguishable, separating the strongest SIF-leads years from the
strongest NDVI-leads years. Separately, Moran's I confirms —
with a number rather than a caveat — that the district-level rainfall data behind Finding 3
are spatially clustered in all 9 of 9 years, while SIF is spatially clustered in only 4 of 9
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

st.info("""
**7.** None of Findings 1–6 touch actual agricultural outcomes — they compare one
remote-sensing product against another, or against an official policy date. **Official
government Kharif crop-yield statistics** (Ministry of Agriculture & Farmers Welfare,
1997-98 to 2022-23) provide an independent, external check: this study's two rainfall-
defined drought years (2015, 2018) show a meaningfully lower Yield Anomaly Index than the
six normal years with yield data available (**−1.08 vs. +0.07**), the same direction the
satellite and rainfall record already point — though not statistically significant at
conventional thresholds given the small drought-year group (n = 2, t = −2.87, p = 0.15).
2021 itself sits close to zero (−0.13), a normal but unremarkable year by this measure too.
See **Crop-Yield Validation** for the full detail.
""")

section_divider()

# Summary metrics
st.header("Study at a Glance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("SIF leads NDVI decline", "8 / 9 years")
with c2:
    st.metric("Drought-lag amplification (H3)", "Not supported")
with c3:
    st.metric("Rainfall-confirmed drought years", "2 / 9")
with c4:
    st.metric("Spatial SIF-rainfall match", "r = 0.531 ✓")

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("Cross-correlation: SIF leads / tied / NDVI leads", "5 / 1 / 3 years")
with c6:
    st.metric("Moran's I — rainfall significant", "9 / 9 years")
with c7:
    st.metric("Moran's I — SIF significant", "4 / 9 years")
with c8:
    st.metric("Satellite lead vs. official declaration (2018)", "~7–8 weeks")

c9, c10 = st.columns(2)
with c9:
    st.metric("Crop-yield anomaly: drought vs. normal years", "−1.08 vs. +0.07")
with c10:
    st.metric("Crop-yield vs. rainfall anomaly correlation", "r = 0.928")

section_divider()

# Limitations
st.header("Limitations")

st.markdown("""
- GOSIF (the SIF product used here) is a statistically modeled reconstruction, not a
  direct satellite retrieval — it combines OCO-2 SIF soundings with MODIS reflectance
  data and meteorological reanalysis. Since MODIS reflectance also underlies the NDVI
  used for comparison, the two variables are not fully independent at the input-data
  level, a property of the dataset choice this study does not attempt to quantify or
  correct for.
- The sample, now nine years (2015–2023), is still unbalanced toward
  normal years: only 2 of 9 years (2015, 2018) meet this study's own rainfall-anomaly
  drought threshold (z-score < -0.5), against 7 normal years. This is itself a finding —
  the original three-year sample (2 of 3 drought years) was considerably more drought-heavy
  than Marathwada's actual climate record — but it also means drought-year statistics in
  this study still rest on an n of 2, not a larger balanced sample.
- 2018 is a genuine, unexplained exception to this study's central SIF-leads-NDVI finding:
  its threshold-crossing lag is marginally negative, its cross-correlation lag is clearly
  negative (−4 days), 87.4% of its bootstrap replicates land below zero, and its RQ3
  official-declaration comparison shows NDVI crossing threshold *before* SIF — the opposite
  ordering from every year with a clear SIF lead. 2022 and 2023 show this same negative-lag
  pattern under cross-correlation and bootstrap (99%+ of bootstrap replicates below zero in
  both), though neither meets this study's own drought threshold, so the exception isn't
  confined to 2018 or to drought years specifically. No crop-type, sowing-date, or other
  covariate data was available to investigate why these years specifically differ; it is
  reported as an open question, not resolved.
- A real bug in the cross-correlation and bootstrap scripts, found and fixed before this
  dashboard was published: both scripts originally searched only non-negative lags (0 to
  N/4), making it mathematically impossible for either to ever report NDVI leading SIF,
  regardless of what the data showed. Fixed to search the full −N/4 to +N/4 range and rerun
  from scratch; this changed three years (2018, 2022, 2023) from a zero/positive
  cross-correlation lag to a genuinely negative one. Disclosed in full rather than folded
  quietly into revised numbers — see **Development Log, Entry 17**.
- The spatial correspondence between rainfall deficit and SIF stress was tested via
  Pearson and Spearman correlation (r = 0.531, ρ = 0.504, both p < 0.0001) rather than left
  as a purely visual comparison; however, with only nine independent study years and eight
  geographically adjacent districts, the 72 district-year observations are not fully
  independent, and this correlation should be read as real but moderate corroborating
  evidence rather than a formally independent statistical confirmation. This is now
  quantified, not just asserted: Moran's I is significantly positive (p < 0.05) for
  rainfall anomaly in all 9 years, but for mean SIF in only 4 of 9 years — a genuine,
  year-dependent weakening from the original three-year sample, where all three years were
  significant for both variables (see **Combined Comparison**).
- This study's drought classification is checked against official government Kharif
  crop-yield statistics (**Crop-Yield Validation** page), rather than left entirely
  unvalidated against ground outcomes — but that check is not a field-level crop-stress
  survey, and it doesn't extend to validating SIF's within-season lag-timing claims
  specifically. It also has its own constraints: the government dataset's most recent
  published season is 2022-23, so 2023 has no yield counterpart yet (n = 8 region-years,
  not 9), and the drought-versus-normal yield comparison itself rests on a small n = 2
  drought-year group, the same constraint that limits H3 elsewhere in this study.
- District-level rainfall anomaly was computed relative to a single region-wide
  climatological baseline rather than a per-district climatology.
- SIF- and NDVI-based stress timing was compared against the one well-documented official
  drought-declaration date I could find (Maharashtra, 31 October 2018).
  A comparably verifiable single declaration date for 2015 could not be located, so this
  comparison remains partial — one of nine study years — rather than complete, and that
  one year happens to be 2018, the study's own sign-reversal exception.
- The Earth Engine-based acquisition step for the five years added during the original
  sample-size expansion was rewritten as a standalone Python script
  (`src/acquisition/gee_data_acquisition.py`) and was actually executed for all eight of
  those years — unlike the original three-year study, where this step had only been run
  interactively and never as a checked-in script. Running it surfaced three genuine bugs (a
  missing Earth Engine Cloud project, a MODIS sinusoidal-projection clip error, and the
  "Beed"/"Bid" district-naming mismatch recurring independently in the new script, despite
  already having been fixed once in the original interactive workflow) — all caught and
  fixed before any figure in this dashboard was computed, and documented in the
  **Development Log**. 2021, the ninth year, was added separately and later, by hand — its
  raw GOSIF rasters had to be tracked down and processed outside this script (see
  **Development Log, Entry 20**).
- The exact lag values in **Lag Analysis**, and their year-to-year ranking, carry wider
  uncertainty than the point estimates alone suggest — see the bootstrap confidence
  intervals there, where 32 of the 36 pairwise between-year comparisons overlap (the
  remaining 4 separate the strongest SIF-leads years from the strongest NDVI-leads years).
""")

section_divider()

# Conclusion
st.header("Conclusion")

st.markdown("""
This study finds that Solar-Induced Fluorescence registers the onset of post-peak seasonal
vegetation decline earlier than, or no later than, NDVI in eight of the nine years studied
in Marathwada, Maharashtra, under the threshold-crossing method — supporting SIF's physical
basis, developed on the **Physics** pages, as a more temporally responsive stress indicator
in most, though not all, years. A second, methodologically distinct cross-correlation check,
corrected after finding it had originally been unable to search for a negative lag, tells a
more mixed story: SIF clearly ahead in 5 years, a genuine tie in 1, and NDVI clearly ahead
in 3 (2018, 2022, 2023), two of those backed by strong bootstrap support. Finding and fixing
that bug, and reporting what the corrected analysis actually says, is as much a part of this
study's result as the headline lag numbers themselves. It does not find evidence that this
lag is amplified specifically by drought conditions — the opposite direction replicated at
three times the original sample size — and identifies substantial inter-annual and
intra-regional variation that a simple drought/normal binary does not capture. Expanding the
sample from three years to nine also surfaced a genuine exception: 2018 remains the year
every method agrees breaks the SIF-leads-NDVI pattern, while 2022 and 2023 turn out to be a
softer, method-dependent version of the same story.

Independent rainfall validation and spatial cross-referencing between SIF and
precipitation data lend physical coherence to the district-level findings — a
correspondence confirmed statistically at nine years, though more moderately than the
original three-year sample suggested (Pearson r = 0.531, Spearman ρ = 0.504, both
p < 0.0001, versus the original r = 0.837), and further characterized, via Moran's I, rather
than only caveated. A comparison against the one available official drought-declaration
date (2018) suggests the practical policy case is better framed as "satellite monitoring
generally, refined by SIF specifically, in most but not all years" than as SIF's edge over
NDVI being a uniform, dominant lever on payout timing — precisely because 2018, the one
year with a verifiable declaration date, is also the year where that edge disappears.
Several limitations — an unbalanced 2-versus-7 drought/normal split, the 2018/2022/2023
exception that isn't fully explained, absence of ground validation, the spatial
non-independence underlying the correlation above, and a real search-space bug in two of
the four lag-estimation checks that changed a genuine finding once fixed — are reported
directly rather than resolved beyond what the available data supports. The Earth Engine
acquisition step, unlike in the original study, was actually scripted and executed for
eight of the nine years during the original sample expansion, closing what had been an open
reproducibility gap; the ninth year, 2021, was added later by hand (**Development Log,
Entry 20**).
""")

st.markdown("""
---
*GREEN ALIBI — an independent satellite-verification study, Marathwada, Maharashtra.*
""")

styled_caption("GREEN ALIBI — Findings, Limitations & Conclusion")