import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption, page_footer

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
    st.metric("Study Years", "3", "2015 · 2018 · 2020")
with col3:
    st.metric("Drought Years", "2", "2015, 2018")
with col4:
    st.metric("Datasets Used", "4", "SIF · NDVI · Rainfall · Land Cover")

section_divider()

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

- 🌍 **Study Area** — where and why Marathwada
- 🔬 **Fluorescence Physics** — the science behind SIF
- 🔬 **NDVI Physics** — the science behind NDVI, and a direct comparison
- 🛰️ **Data & Methodology** — sources, processing, and a boundary-precision correction
- 📈 **Seasonal Trajectories** — SIF vs NDVI across the growing season
- 📊 **Lag Analysis** — the quantitative SIF-to-NDVI decline lag
- 🗺️ **Spatial SIF Analysis** — where stress concentrated, static and interactive
- 🌧️ **Rainfall Validation** — independently confirming the drought years
- 🔗 **Combined Comparison** — SIF and rainfall side by side
- 📝 **Findings & Conclusion** — what this project did and did not find
""")

section_divider()

# ============================================================
# FULL PROJECT DOCUMENTATION
# ============================================================
st.header("📄 Full Project Documentation")

st.markdown("""
The dashboard above presents this project's findings interactively. The full written
documents — including everything not shown here — are available below as PDFs.
""")

doc_col1, doc_col2, doc_col3 = st.columns(3)

with doc_col1:
    with open("Research_Paper.pdf", "rb") as f:
        st.download_button(
            label="📗 Research Paper",
            data=f,
            file_name="Research_Paper.pdf",
            mime="application/pdf",
            use_container_width=True
        )

with doc_col2:
    with open("Project_Journal.pdf", "rb") as f:
        st.download_button(
            label="📘 Project Journal",
            data=f,
            file_name="Project_Journal.pdf",
            mime="application/pdf",
            use_container_width=True
        )

with doc_col3:
    with open("Development_Log.pdf", "rb") as f:
        st.download_button(
            label="📙 Development Log",
            data=f,
            file_name="Development_Log.pdf",
            mime="application/pdf",
            use_container_width=True
        )

section_divider()

# ============================================================
# FOOTER
# ============================================================
page_footer()