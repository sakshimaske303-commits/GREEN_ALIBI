import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Data & Methodology — GREEN ALIBI", page_icon="🛰️", layout="wide")
apply_custom_style()

st.title("🛰️ Data & Methodology")

st.markdown("""
This page documents the datasets used, the processing pipeline applied to each, and a
boundary-precision correction that was applied to the entire study region partway through
the analysis.
""")

section_divider()

# ============================================================
# DATA SOURCES TABLE
# ============================================================
st.header("Data Sources")

data_sources = pd.DataFrame({
    "Variable": ["SIF", "NDVI", "Land Cover", "Precipitation"],
    "Source": [
        "GOSIF v2 (Li & Xiao, 2019), UNH Global Ecology Group",
        "MODIS MOD13Q1, via Google Earth Engine",
        "MODIS MCD12Q1 (IGBP classification)",
        "CHIRPS Daily, UCSB-CHG, via Google Earth Engine"
    ],
    "Resolution": ["0.05°, 8-day", "250 m, 16-day", "500 m, annual", "0.05°, daily"],
    "Role": [
        "Primary outcome — physiological stress proxy",
        "Comparison outcome — structural/reflectance proxy",
        "Cropland mask (classes 12, 14)",
        "Independent drought validation"
    ]
})

st.dataframe(data_sources, use_container_width=True, hide_index=True)

st.markdown("**Study period:** June 1 – December 31, for 2015, 2018, and 2020.")

section_divider()

# ============================================================
# PROCESSING PIPELINE
# ============================================================
st.header("Processing Pipeline")

tab1, tab2, tab3 = st.tabs(["SIF Processing", "NDVI Processing", "Temporal Alignment"])

with tab1:
    st.markdown("""
    - Eighty-one 8-day GOSIF GeoTIFFs acquired (twenty-seven per study year, June–December,
      after the observation window was extended from an initial June–November cut).
    - Raw digital values scaled by GOSIF's factor of **0.0001** to obtain physical SIF units.
    - Fill-value codes masked prior to any averaging: **32766** (water), **32767**
      (non-vegetated / missing).
    - Each file clipped to the study region boundary (see below) using polygon-based
      raster masking.
    - A regional mean SIF value computed per date, alongside a valid-pixel-fraction
      quality metric.
    """)

with tab2:
    st.markdown("""
    - Initial extraction using raw MOD09Q1 reflectance, without cloud-quality filtering,
      produced a physically implausible time series — single-period swings inconsistent
      with any real vegetation phenology.
    - Root cause: Marathwada's growing season overlaps with the monsoon, and MOD09Q1's
      composited reflectance does not reliably exclude cloud-contaminated pixels without
      explicit quality-band filtering.
    - **Fix:** rebuilt extraction around MOD13Q1, using its native `SummaryQA` band
      (retaining only good- and marginal-quality pixels: QA values 0 and 1), combined with
      the cropland mask.
    - This traded temporal resolution (16-day vs. 8-day) for a physically sound signal —
      a necessary trade given the alternative was an unusable series.
    """)

with tab3:
    st.markdown("""
    - SIF (8-day) and NDVI (16-day) were merged per year using **nearest-date matching**,
      since their native cadences do not align to a common date grid.
    - Each year's series was normalized (0–1) within-year before threshold-crossing
      analysis, so that comparisons across years are relative to each year's own seasonal
      peak rather than an absolute scale.
    """)

section_divider()

# ============================================================
# BOUNDARY CORRECTION STORY
# ============================================================
st.header("A Boundary-Precision Correction")

st.markdown("""
The study region was initially defined as a rectangular bounding box
(75.0–78.5°E, 17.5–20.5°N). Visual inspection in Google Earth Engine — after explicitly
drawing the rectangle on the map, rather than trusting its coordinates blindly — showed
that this box extended beyond Marathwada into neighboring Telangana districts (Nizamabad,
Bidar, Adilabad) and into Solapur and Yavatmal, all outside the study region and subject to
different rainfall regimes. Every regional mean computed up to that point had quietly
included pixels from outside Marathwada.

The boundary was corrected to the precise union of the eight Marathwada districts, sourced
from the **FAO GAUL 2015 level-2** administrative dataset. A subsequent naming-convention
gap was caught during this correction: the 2015-vintage dataset stores Beed district under
its earlier spelling, **"Bid,"** causing an initial filter on "Beed" to silently omit the
district entirely, with no error raised. This was caught by visual inspection rather than
by the script itself, and an explicit district-count check was added to the pipeline
afterward to catch similar naming mismatches automatically in the future.

Both the SIF clipping pipeline (rebuilt using `rasterio.mask` against the true polygon
rather than a rectangular window) and the NDVI extraction pipeline were re-run against this
corrected boundary, and the masking behavior was independently verified before proceeding.
""")

col1, col2 = st.columns([2, 1])
with col1:
    st.image("outputs/figures/boundary_overlay_check.png", use_container_width=True)
    styled_caption(
        "Verification: clipped SIF data (color) overlaid with the true Marathwada "
        "boundary (blue outline) — data is confined exactly within the real district shapes."
    )
with col2:
    st.success("""
    **Why this matters:** an external audit of this project later found that the
    region-wide time series had actually kept building itself from the pre-fix rectangular
    clip, due to a filename-matching bug in the aggregation script — not the corrected
    polygon output the log at the time believed it was using (see **Development_Log.md**,
    Entry 11). Once that bug was fixed and the series regenerated from the correct boundary,
    the core lag findings held up: the numbers shifted modestly but the qualitative
    conclusion — SIF leads NDVI in every year, and drought years still show a *smaller*
    lag than the normal year — did not change.
    """)

section_divider()

# ============================================================
# LAG CALCULATION METHOD
# ============================================================
st.header("Quantitative Lag Calculation")

st.markdown("""
For each year, the day-of-year at which SIF and NDVI (each normalized 0–1 within-year)
crossed a set of decline thresholds — **90%, 80%, 70%, 60%, and 50%** of seasonal peak —
was estimated via linear interpolation between observed dates. Lag at each threshold is
defined as the NDVI crossing date minus the SIF crossing date. This replaced an earlier,
purely visual comparison of the two seasonal curves, which had led to an overstated initial
claim about drought years showing a larger lag — a claim withdrawn once tested numerically
(see **Lag Analysis** page).
""")

styled_caption("GREEN ALIBI — Data & Methodology")