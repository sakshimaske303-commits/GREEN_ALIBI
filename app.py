import os
import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption, page_footer, NAVY_DARK, NAVY_MED, MAGENTA, TEAL, TEXT_LIGHT
from utils.doc_viewer import render_doc_viewer

st.set_page_config(
    page_title="GREEN ALIBI — Marathwada Drought Study",
    page_icon="🌿",
    layout="wide"
)

apply_custom_style()

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<h1 style='text-align:center; font-size:3.2rem; font-weight:800;'>🌿 GREEN ALIBI</h1>
<h3 style='text-align:center; font-weight:500; color:#FF6EC7;'>
Testing Whether Fluorescence Catches Drought Stress Before the Eye Can See It
</h3>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(233, 30, 140, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; margin: 10px 0 18px 0;">
        <a href="https://doi.org/10.5281/zenodo.21762501" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {NAVY_MED}, {NAVY_DARK});
                border: 2px solid {MAGENTA};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(233, 30, 140, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:{TEAL}; font-family:'Poppins',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>ARCHIVED &amp; CITABLE ON ZENODO</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{TEXT_LIGHT}; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        DOI: 10.5281/zenodo.21762501
                    </div>
                </div>
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<p style='text-align:center; font-size:1.1rem;'>
<strong>NDVI shows a plant's alibi — it can still look green.<br>
SIF shows what is physically happening inside it.</strong>
</p>
""", unsafe_allow_html=True)

section_divider()

# ============================================================
# KEY METRICS
# ============================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Districts Studied", "8", "Marathwada")
with col2:
    st.metric("Study Years", "8", "2015–2023 (excl. 2021)")
with col3:
    st.metric("Drought Years", "2", "2015, 2018 (of 8)")
with col4:
    st.metric("Datasets Used", "4", "SIF · NDVI · Rainfall · Land Cover")

section_divider()

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(233, 30, 140, 0.06);
                border: 1px solid rgba(233, 30, 140, 0.3); border-left: 4px solid {MAGENTA};
                border-radius: 10px;">
        <p style="color:{MAGENTA}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:700; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{TEXT_LIGHT}; font-size:1rem; line-height:1.6; margin:0;">
            India's official drought-declaration process and the PMFBY crop-insurance payout mechanism
            lean on NDVI — a signal that only moves once a plant's structure has already visibly
            degraded. That means the farmers relying on that signal find out they're in trouble only
            after damage is done. If SIF genuinely provides an earlier warning, that isn't an academic
            curiosity — it's the difference between a relief payout that arrives in time and one that
            arrives after the season is already lost. This project tests that premise directly, on real
            satellite data over a real drought-prone Maharashtra region, and reports exactly what it
            found — including the parts, like H3, that didn't hold up.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# PROJECT OVERVIEW
# ============================================================
st.header("What This Project Tests")

st.markdown("""
India's official drought-declaration process, and the crop-insurance payout mechanism under the
**Pradhan Mantri Fasal Bima Yojana (PMFBY)** that depends on it, relies substantially on rainfall-deficit
records and the **Normalized Difference Vegetation Index (NDVI)** — a reflectance-based measure that only
changes once a plant's internal structure has already begun to visibly degrade.

**Solar-Induced Fluorescence (SIF)** is grounded in a more direct physical process: it captures a drop in
photosynthetic efficiency *before* a plant's outward greenness changes. This project tests, using real
satellite data over Marathwada, Maharashtra, whether that physical head-start actually shows up as a
measurable, usable time lag — and whether drought conditions make that lag bigger.
""")

section_divider()

# ============================================================
# RESEARCH QUESTIONS
# ============================================================
st.header("Research Questions")

st.markdown("""
1. **Does SIF decline measurably earlier than NDVI** during documented drought-onset periods?
2. **Is the SIF–NDVI lag consistent** across the region, or does it vary by geography?
3. **How does SIF-based stress timing relate to independently measured rainfall deficit**,
   across drought and normal years?
""")

section_divider()

# ============================================================
# HYPOTHESES
# ============================================================
st.header("Hypotheses")

h1, h2, h3 = st.columns(3)
with h1:
    st.info("**H1**\n\nSIF declines significantly before NDVI during a drought episode.")
with h2:
    st.info("**H2**\n\nThe SIF–NDVI lag is not spatially uniform across the study region.")
with h3:
    st.info("**H3**\n\nDrought severity (measured via rainfall deficit) amplifies the lag.")

section_divider()

# ============================================================
# NAVIGATION GUIDE
# ============================================================
st.header("How to Explore This Dashboard")

st.markdown("""
Use the sidebar to move through the study in the order it was actually built:

- **Study Area** — where and why Marathwada
- **Fluorescence Physics** — the science behind SIF
- **NDVI Physics** — the science behind NDVI, and a direct comparison
- **Data & Methodology** — sources, processing, and a boundary-precision correction
- **Seasonal Trajectories** — SIF vs NDVI across the growing season
- **Lag Analysis** — the quantitative SIF-to-NDVI decline lag
- **Spatial SIF Analysis** — where stress concentrated, static and interactive
- **Rainfall Validation** — independently confirming the drought years
- **Combined Comparison** — SIF and rainfall side by side
- **Interactive Maps & Plots** — both district-level maps and the three headline charts in one place, hoverable, zoomable, and toggleable
- **Findings & Conclusion** — what this project did and did not find
""")

section_divider()

# ============================================================
# FULL PROJECT DOCUMENTATION
# ============================================================
st.header("Full Project Documentation")

st.markdown("""
The dashboard above presents this project's findings interactively. The full written
documents — including everything not shown here — open directly below, no download needed.
""")

_all_docs = [
    {"label": "Executive Summary", "filename": "GA_Executive_Summary.pdf"},
    {"label": "Project Report", "filename": "GA_Project_Report.pdf"},
    {"label": "Research Paper", "filename": "GA_Research_Paper.pdf"},
    {"label": "Development Log", "filename": "GA_Development_Log.pdf"},
]
_docs = [d for d in _all_docs if os.path.exists(os.path.join("static", d["filename"]))]
_missing = [d for d in _all_docs if d not in _docs]

if _docs:
    render_doc_viewer(
        docs=_docs,
        colors={
            "navy_dark": NAVY_DARK,
            "navy_med": NAVY_MED,
            "magenta": MAGENTA,
            "teal": TEAL,
            "text_light": TEXT_LIGHT,
        },
    )
for d in _missing:
    st.warning(f"{d['filename']} not found.")

section_divider()

# ============================================================
# FOOTER
# ============================================================
page_footer()