import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption, MAGENTA

st.set_page_config(page_title="Data & Methodology — GREEN ALIBI", page_icon="🛰️", layout="wide")
apply_custom_style()

st.title("🛰️ Data & Methodology")

st.markdown("""
This page documents the datasets used, the processing pipeline applied to each, and a
boundary-precision correction that was applied to the entire study region partway through
the analysis.
""")

section_divider()

# ---- Proof popovers: pulsing button reveals a screenshot inline; falls back
# to a quiet "not added yet" note if the PNG isn't in outputs/proof_screenshots/ ----
st.markdown(f"""
<style>
    div[data-testid="stPopover"] button {{
        animation: proof-blink 1.8s ease-in-out infinite;
        border: 3px solid {MAGENTA} !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        min-height: unset !important;
        min-width: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stPopover"] button p {{
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1 !important;
    }}
    @keyframes proof-blink {{
        0%, 100% {{ box-shadow: 0 0 0px rgba(233, 30, 140, 0); }}
        50% {{ box-shadow: 0 0 12px rgba(233, 30, 140, 0.85); }}
    }}
</style>
""", unsafe_allow_html=True)

import os as _os
PROOF_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "outputs", "proof_screenshots")

def proof_popover(filename, caption):
    path = _os.path.join(PROOF_DIR, filename)
    with st.popover("📷"):
        if _os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.caption(f"Screenshot not added yet — save it as `outputs/proof_screenshots/{filename}`.")

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

col_sp1, col_sp2 = st.columns([0.94, 0.06])
with col_sp1:
    st.markdown("""
    **Study period:** June 1 – late December (day-of-year 153–361), for eight years —
    2015, 2016, 2017, 2018, 2019, 2020, 2022, and 2023. The study originally covered three
    years (2015, 2018, 2020); five more were added in a later expansion pass to address
    this study's own recurring small-sample limitation, using the identical acquisition
    and processing pipeline throughout.
    """)
with col_sp2:
    proof_popover("01_sif_ndvi_data_excel.png", "The merged SIF–NDVI dataset (marathwada_sif_ndvi_merged.csv) opened in Excel — the core file behind the lag analysis.")

section_divider()

# ============================================================
# PROCESSING PIPELINE
# ============================================================
st.header("Processing Pipeline")

tab1, tab2, tab3 = st.tabs(["SIF Processing", "NDVI Processing", "Temporal Alignment"])

with tab1:
    st.markdown("""
    - 216 8-day GOSIF GeoTIFFs acquired across all eight study years (twenty-seven per
      year, June–December, after the observation window was extended from an initial
      June–November cut). The original 81 files (three years) were pulled first; a
      further 135 files, for the five newly added years, were downloaded in a later
      expansion pass using the identical seasonal window and file-naming convention.
    - Raw digital values scaled by GOSIF's factor of **0.0001** to obtain physical SIF units.
    - Fill-value codes masked prior to any averaging: **32766** (water), **32767**
      (non-vegetated / missing).
    - Each file clipped to the study region boundary (see below) using polygon-based
      raster masking.
    - A regional mean SIF value computed per date, alongside a valid-pixel-fraction
      quality metric.
    """)
    col_t1a, col_t1b = st.columns([0.94, 0.06])
    with col_t1b:
        proof_popover("02_clip_gosif_vscode.png", "clip_gosif.py open in VS Code — the rasterio.mask script that clips each GOSIF raster to the exact Marathwada boundary polygon.")

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

The exact same naming gap reappeared, independently, when the acquisition step was later
rewritten as a standalone Python script for the eight-year sample-size expansion — the new
script's own district list also used "Beed" rather than "Bid," silently dropping the
district from all eight years' region- and district-level exports on the first run. This
was caught by counting rows in the by-district output rather than trusting a clean run, and
the full extraction was re-run and re-verified before any figure in this dashboard was
computed. It's recorded here rather than smoothed over, since it's a useful reminder that
"we already fixed this once" doesn't mean a rewritten script inherits the fix automatically.

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
    col_b1, col_b2 = st.columns([0.94, 0.06])
    with col_b2:
        proof_popover("04_qgis_boundary_check.png", "QGIS — visual QA of the clipped GOSIF raster against the Marathwada boundary polygon, to independently sanity-check the rasterio.mask clipping (optional — only if you redo this check in QGIS).")
with col2:
    st.success("""
    **Why this matters:** going back through this project later, I found that the
    region-wide time series had actually kept building itself from the pre-fix rectangular
    clip, due to a filename-matching bug in the aggregation script — not the corrected
    polygon output the log at the time believed it was using (see **GA_Development_Log.md**,
    Entry 11). Once that bug was fixed and the series regenerated from the correct boundary,
    the core lag findings held up: the numbers shifted modestly but the qualitative
    conclusion — SIF leads NDVI in most years, and drought years still show a *smaller*
    lag than normal years — did not change. The same held true after the eight-year
    expansion and its own "Bid" district fix: the numbers shifted again, and 2018 emerged
    as a genuine exception rather than a leading example, but the group-level finding
    (drought years smaller lag than normal years) replicated a second time.
    """)

section_divider()

# ============================================================
# LAG CALCULATION METHOD
# ============================================================
col_lag1, col_lag2 = st.columns([0.94, 0.06])
with col_lag1:
    st.header("Quantitative Lag Calculation")
with col_lag2:
    st.markdown("<div style='margin-top: 2.2rem;'></div>", unsafe_allow_html=True)
    proof_popover("03_cross_correlation_vscode.png", "cross_correlation_lag.py open in VS Code — the independent cross-correlation robustness check on the SIF-to-NDVI lag.")

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