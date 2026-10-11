import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Data & Methodology — GREEN ALIBI", page_icon="🛰️", layout="wide")
apply_custom_style()

st.title("🛰️ Data & Methodology")

st.markdown("""
This page describes the datasets I used, how each is processed, and the checks I ran on the
results. The whole pipeline runs end to end from one script, `run_all.py`.
""")

section_divider()

st.header("Data Sources")

data_sources = pd.DataFrame({
    "Variable": ["SIF (main)", "SIF (independent check)", "NDVI", "Land Cover", "Precipitation", "Crop yields", "Declarations"],
    "Source": [
        "GOSIF v2 (Li & Xiao, 2019), UNH Global Ecology Group",
        "TROPOSIF v2.1, Sentinel-5P TROPOMI (Guanter et al., 2021)",
        "MODIS MOD13Q1, via Google Earth Engine",
        "MODIS MCD12Q1 (IGBP classification)",
        "CHIRPS Daily, UCSB-CHG, via Google Earth Engine",
        "District Area/Production/Yield statistics, Ministry of Agriculture & Farmers Welfare",
        "2015 declaration (reported 16 Oct), 2018 first-stage (23 Oct) and final (31 Oct)",
    ],
    "Resolution": ["0.05°, 8-day", "Daily soundings → 8-day composites, 2018–2020", "250 m, 16-day", "500 m, annual", "0.05°, daily", "District, Kharif season", "Dates"],
    "Role": [
        "Main SIF series, cropland-weighted",
        "Check not built from MODIS reflectance",
        "Comparison index, cropland pixels, timed by observation date",
        "Cropland definition (classes 12, 14)",
        "The single rainfall source for every anomaly (seasonal totals 1981–2023)",
        "Check that the drought classification matches harvests",
        "Timing benchmark for RQ3",
    ]
})

st.dataframe(data_sources, use_container_width=True, hide_index=True)

st.markdown("""
**Study period:** 1 June – 27 December (day-of-year 153–361) of nine Kharif seasons,
2015–2023, for all eight Marathwada districts.

Two things limit how the results can be read. GOSIF uses MODIS reflectance as a predictor,
so GOSIF and MOD13Q1 NDVI are not fully independent; that is why I added the TROPOMI check.
And GOSIF's 0.05° grid (about 5 km) is far coarser than NDVI's 250 m, so every comparison
here is a regional or district signal over a mixed cropland landscape, not a field-scale one.
""")

section_divider()

st.header("Processing Pipeline")

tab1, tab2, tab3, tab4 = st.tabs(["SIF Processing", "NDVI Processing", "Rainfall & Drought Years", "TROPOMI Check"])

with tab1:
    st.markdown("""
    - GOSIF 8-day GeoTIFFs (27 per year) clipped to the FAO GAUL 2015 level-2 outline of the
      eight districts with `rasterio.mask`.
    - Values scaled by GOSIF's factor of **0.0001**; fill values **32767** (water) and
      **32766** (snow/ice or barren) masked before any averaging.
    - Each 0.05° cell weighted by its **cropland fraction**: the share of MCD12Q1 pixels in
      classes 12 or 14 inside that cell, computed in Earth Engine on the GOSIF grid. This makes
      the regional and district SIF series describe mainly farmland, as the NDVI series does.
    - Each 8-day composite dated at its centre (start day + 3.5).
    """)

with tab2:
    st.markdown("""
    - MOD13Q1 pixels kept only where `SummaryQA` marks good or marginal quality (0, 1) and
      MCD12Q1 marks cropland (classes 12, 14).
    - A 16-day MOD13Q1 value can come from any day in its window, so I date each composite by
      the **mean of its pixels' `DayOfYear` values** (the day each pixel was actually observed),
      not by the window start.
    - Each year's NDVI series is normalised on its own observations and linearly interpolated
      onto the SIF composite centre dates.
    - During the monsoon many composites rest on few clear pixels (23 of 117 regional composites
      under 25% coverage); dropping them does not change the direction of any year's lag
      (with a stricter 50% cut-off, 2022 reverses).
    """)

with tab3:
    st.markdown("""
    - One rainfall source throughout: **CHIRPS** seasonal totals (1 June – 26 December) for
      1981–2023, at region and district level, plus daily series for the rainfall trigger.
    - A year is a **drought year** when its seasonal total has z < −0.5 against the 2001–2020
      mean (826.8 mm, σ = 158.9 mm). Only **2015** and **2018** qualify.
    - This holds under three other baselines (2001–2014, 1981–2014, 1991–2020) and every cut-off
      from −0.3 to −0.75. District-years are classified against each district's own 2001–2020
      baseline: 15 of 72 are drought district-years (17 against the regional baseline).
    - **Out-of-sample test:** every method applied unchanged to 2001–2014, where 2001, 2002,
      2003, 2004 and 2014 are drought years, with anomalies standardised against the normal
      years of 2001–2014 only.
    """)

with tab4:
    st.markdown("""
    - TROPOSIF soundings over Marathwada, 2018–2020, kept where cloud fraction < 0.2, solar
      zenith angle < 70° and the land-cover flag is cropland; 53% of 630,091 soundings passed.
    - Main variable: `SIF_Corr_743`; averaged into 8-day composites aligned with GOSIF's.
    - The same threshold-crossing lag against NDVI is computed for each year, under both scalings. Three variants
      (cloud fraction < 0.5, all land cover, uncorrected SIF_743) are also run.
    """)

section_divider()

st.header("How I Measure the Lag")

st.markdown("""
**Threshold-crossing.** Each year's SIF and NDVI series is rescaled 0–1 and linear interpolation
gives the day each series first falls below **0.9, 0.8, 0.7, 0.6 and 0.5** after its peak. The lag
at each threshold is the NDVI crossing date minus the SIF crossing date (positive = SIF first); a
year's lag is the mean over the thresholds it reaches. Two scalings are compared:
*season-scaled* (0 at the seasonal minimum, 1 at the peak — the original method) and
*decline-scaled* (0 at the minimum after the peak). They agree only if both series return to their
pre-season level; NDVI does not, so the season scale delays its crossings. An asymmetric
double-logistic end-of-season date is a third, indicative estimate.

**Cross-correlation.** Over the post-peak decline window, both series are put on a daily grid,
de-meaned, and cross-correlated at shifts from −N/4 to +N/4 days. The best-fitting shift is that
year's lag. Correlation does not depend on scale, so this estimate is unaffected by the scaling
choice.

**Uncertainty.** A 2,000-replicate case-resampling bootstrap for cross-correlation, and a
2,000-replicate moving-block residual bootstrap (blocks of three composites, centred on the
reported lag) plus a leave-one-out jackknife for threshold-crossing.

**District level (H2).** The same lags for all 72 district-years, tested with a two-way ANOVA
(district and year) and a Friedman test.
""")

section_divider()

st.header("Drought Anomaly Alarms (H4)")

st.markdown("""
A seasonal lag says when each index starts its *normal* decline, not when it departs from
normal. So for each composite date I standardise each year's SIF and NDVI against the normal
years at that date, leaving the year itself out: z = (x − normal-year mean) / normal-year s.d.

An **alarm** is the first composite from 1 July at which z stays below a threshold (−0.5, −1,
−1.5, −2, −3) for **two consecutive composites**. At regional scale, z < −3 is the only threshold
at which neither index raises an alarm in any normal year, so it is the main alarm threshold.
The same is done for the 72 district-years (15 drought, 57 normal against each district's own
rainfall baseline; 17 and 55 against the regional one), with a date-by-date AUC
summarising how well each index separates drought from normal district-years.
""")

section_divider()

st.header("Rainfall Trigger and Declarations (RQ3)")

st.markdown("""
India's Manual for Drought Management (2016) starts drought assessment with a rainfall-based
**Trigger-1**. I approximate it as the first day after 1 July on which cumulative rainfall since
1 June is more than **25% below** the 2001–2020 normal for that date *and* a **dry spell of at
least 21 days** (days below 2.5 mm, counted from 1 July to 30 September) has occurred. I also
run variants (20% or 30% deficit, 1 mm dry day, deficit alone, dry spell alone, and dry spells
counted to December as in an earlier version). The state applies the trigger at taluka level, so
this region- and district-level version is an approximation. Satellite alarm dates are compared
against this trigger and against the three declaration dates.
""")

section_divider()

st.header("Method-Dependence Check")

st.markdown("""
To see which findings depend on which choices, I recompute the regional lag under **40
combinations**: SIF cropland-weighted or unweighted; NDVI timed by observation date or by
compositing window; raw or Savitzky–Golay-smoothed series; and lag metric (mean-threshold, 0.9,
0.7, 0.5, or cross-correlation). For each, I record whether SIF leads in all nine years, whether
drought years have a smaller lag than normal years, and whether 2018 has the smallest lag.
All 40 use the season scale; the scaling check is reported separately. Results are on the
**Lag Analysis** page.
""")

col1, col2 = st.columns([2, 1])
with col1:
    st.image("outputs/figures/boundary_overlay_check.png", use_container_width=True)
    styled_caption(
        "Verification: clipped SIF data (color) overlaid with the true Marathwada "
        "boundary (blue outline) — data is confined within the district shapes."
    )
with col2:
    st.info("""
    **Corrections.** I fixed five data-handling errors from the first preprint (listed in the
    Development Log), and every number here comes from the corrected pipeline.
    """)

styled_caption("GREEN ALIBI — Data & Methodology")
