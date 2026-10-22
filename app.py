# Streamlit home page

import os
import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption, page_footer, NAVY_DARK, NAVY_MED, MAGENTA, TEAL, TEXT_LIGHT

st.set_page_config(
    page_title="GREEN ALIBI — Marathwada Drought Study",
    layout="wide"
)

apply_custom_style()

st.markdown("""
<h1 style='text-align:center; font-size:3.2rem; font-weight:800;'>GREEN ALIBI</h1>
<h3 style='text-align:center; font-weight:500; color:#FF6EC7;'>
Testing the Fluorescence Advantage: Does SIF Signal Agricultural Drought Earlier than NDVI in Marathwada?
</h3>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(233, 30, 140, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:16px; margin: 10px 0 18px 0;">
        <a href="https://eartharxiv.org/repository/view/14813/" target="_blank" class="doi-badge-link" style="text-decoration:none;">
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
                        <span>PREPRINT ON EARTHARXIV</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{TEXT_LIGHT}; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        Read the preprint
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
<strong>SIF and NDVI flagged drought within one 8-day composite of each other, with no consistent winner,<br>
in 2015–2023 and in the 2001–2014 test. GOSIF's seasonal head start comes mostly from how NDVI's decline is measured.</strong>
</p>
""", unsafe_allow_html=True)

section_divider()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Districts Studied", "8", "Marathwada")
with col2:
    st.metric("Kharif Seasons", "9", "2015–2023")
with col3:
    st.metric("Drought Years", "2", "2015, 2018 (of 9)")
with col4:
    st.metric("SIF Products", "2", "GOSIF + TROPOMI check")

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.metric("SIF Decline First (decline-scaled)", "6 / 9 years", "−5.5 to +13.4 days", delta_color="off")
with col6:
    st.metric("Season-scaled Lead", "9 / 9 years", "8.0–34.2 days, mostly a scaling effect", delta_color="off")
with col7:
    st.metric("TROPOMI SIF First", "3 / 3 years", "2018–2020, both scalings", delta_color="off")
with col8:
    st.metric("Drought Alarm (z < −3), Districts", "SIF 7 · same 2 · NDVI 3", "11 of 12 within one composite", delta_color="off")

section_divider()

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(233, 30, 140, 0.06);
                border: 1px solid rgba(233, 30, 140, 0.3); border-left: 4px solid {MAGENTA};
                border-radius: 10px;">
        <p style="color:{MAGENTA}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:700; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{TEXT_LIGHT}; font-size:1rem; line-height:1.6; margin:0;">
            Drought declarations in India, and the PMFBY crop-insurance payouts tied to them, rest on
            rainfall deficits and on vegetation indices like NDVI, which respond once crop damage is
            visible. SIF is often proposed as an earlier signal because it is tied to photosynthesis.
            If it really warned earlier, relief could arrive sooner. I tested that on nine Kharif seasons
            in Marathwada. What I found is negative: SIF is not a resolvably earlier drought alarm than NDVI (the two
            alarms came within about one 8-day composite of each other), and its apparent head start in the normal
            seasonal decline is mostly a side-effect of how NDVI's decline is measured. Applied unchanged
            to 2001–2014, which adds five drought years, the district-level picture was the same. H2, H3
            and H4 did not hold up.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.header("What This Project Tests")

st.markdown("""
India's official drought-declaration process, and the crop-insurance payout mechanism under the
**Pradhan Mantri Fasal Bima Yojana (PMFBY)** that depends on it, relies substantially on rainfall-deficit
records and the **Normalized Difference Vegetation Index (NDVI)** — a reflectance-based measure that tracks
canopy greenness and structure, which usually change only after stress has lasted for some time.

**Solar-Induced Fluorescence (SIF)** is tied more directly to photosynthesis, so it is expected to respond
before a crop's greenness changes. I keep two questions apart:

- Does SIF flag **drought** (a departure from normal years) before NDVI? This is the main question, and the answer
  is no. At z < −3 both flagged 2015 on the same date and NDVI was 8 days (one composite) earlier in 2018; across
  the drought district-years flagged by both, SIF was first in 7, they coincided in 2 and NDVI was first in 3,
  almost always by one composite, which NDVI's 16-day sampling cannot resolve.
- Does SIF's **seasonal decline** start before NDVI's? Scaled over the whole season, yes in all 9 years. But NDVI
  stays well above its pre-season level after the monsoon, which delays its crossings by construction. Scaled over
  each curve's own decline, SIF is first in 6 of 9 years by at most about two weeks; cross-correlation agrees.
""")

section_divider()

st.header("Research Questions")

st.markdown("""
1. **In drought years, does SIF depart from its normal-year range before NDVI does?** (main question)
   And does SIF's normal post-peak decline begin before NDVI's?
2. **Does the SIF–NDVI lag differ between districts, and does drought widen it?**
3. **How do satellite drought signals time against the rainfall-based Trigger-1** of India's drought-management
   framework and against the official 2015 and 2018 drought declarations?
""")

section_divider()

st.header("Hypotheses")

h1, h2, h3, h4 = st.columns(4)
with h1:
    st.info("**H1 — depends on scaling**\n\nSIF's seasonal decline begins before NDVI's. 9/9 years scaled over the season; 6/9 scaled over each curve's own decline.")
with h2:
    st.warning("**H2 — not supported**\n\nThe lag differs between districts. Friedman p = 0.043 season-scaled, but p = 0.97 decline-scaled.")
with h3:
    st.warning("**H3 — not supported**\n\nDrought widens the lag. Drought years 14.8 vs 22.6 days season-scaled; 6.5 vs 3.6 decline-scaled.")
with h4:
    st.warning("**H4 — not supported**\n\nSIF departs from its normal-year range before NDVI in drought years. The alarms came within one composite, with no consistent winner.")

section_divider()

st.header("How to Explore This Dashboard")

st.markdown("""
Use the sidebar to move through the study in the order it was actually built:

- **Study Area** — where and why Marathwada
- **Fluorescence Physics** — the science behind SIF
- **NDVI Physics** — the science behind NDVI, and a direct comparison
- **Data & Methodology** — sources, processing pipeline, and the checks I ran
- **Seasonal Trajectories** — SIF vs NDVI across the growing season
- **Lag Analysis** — threshold and cross-correlation lags, uncertainty, method dependence, TROPOMI check
- **Spatial SIF Analysis** — where stress concentrated, static and interactive
- **Rainfall Validation** — how the drought years were defined from CHIRPS rainfall
- **Combined Comparison** — SIF and rainfall side by side
- **Interactive Maps & Plots** — both district-level maps and the three headline charts in one place, hoverable, zoomable, and toggleable
- **Crop-Yield Validation** — checking this study's drought classification against official government harvest statistics
- **Findings & Conclusion** — what this project did and did not find
""")

section_divider()

st.header("Full Project Documentation")

st.markdown("""
The dashboard above presents this project's findings interactively. The full written
documents — including everything not shown here — are available to download below.
""")

_all_docs = [
    {"label": "Executive Summary", "filename": "GA_Executive_Summary"},
    {"label": "Research Paper", "filename": "GA_Research_Paper"},
    {"label": "Development Log", "filename": "GA_Development_Log"},
    {"label": "Policy Brief", "filename": "Policy_Brief"},
]


def _doc_path(stem):
    """prefer a PDF in static/, fall back to the Markdown source in the repo root"""
    pdf = os.path.join("static", stem + ".pdf")
    if os.path.exists(pdf):
        return pdf, "application/pdf"
    md = stem + ".md"
    if os.path.exists(md):
        return md, "text/markdown"
    return None, None


_available = [(d, *_doc_path(d["filename"])) for d in _all_docs]
_available = [x for x in _available if x[1]]
if _available:
    _cols = st.columns(len(_available))
    for _col, (_d, _path, _mime) in zip(_cols, _available):
        with _col:
            with open(_path, "rb") as _f:
                st.download_button(
                    label=f"{_d['label']}",
                    data=_f.read(),
                    file_name=os.path.basename(_path),
                    mime=_mime,
                    use_container_width=True,
                )

section_divider()

page_footer()
