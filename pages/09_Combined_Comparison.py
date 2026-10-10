import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Combined Comparison — GREEN ALIBI", page_icon="🔗", layout="wide")
apply_custom_style()

st.title("🔗 SIF vs. Rainfall: A Combined Spatial View")

st.markdown("""
The previous two pages show SIF and rainfall anomaly separately. Here I put them side by
side and test how closely they match across the 72 district-years (8 districts × 9 years).
""")

section_divider()

st.image("outputs/figures/combined_sif_rainfall_comparison.png", use_container_width=True)
styled_caption(
    "SIF (top row) and rainfall anomaly (bottom row) by district, all nine study years, "
    "presented jointly for direct spatial comparison."
)

section_divider()

st.header("Reading the Correspondence")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What Lines Up")
    st.markdown("""
    The low-SIF zone in the southwest in 2015 and 2018 sits largely on the rainfall-deficit
    zone in the same years. Over the full record, Osmanabad, Aurangabad and Bid run drier
    than the regional mean on average (−5.6%, −5.0%, −4.2%), and Osmanabad also has the
    lowest SIF in 8 of 9 years. Nanded and Hingoli run well above the regional mean in
    rainfall (+29.5%, +24.1%).

    Part of this is a fixed geographic gradient (district baselines range from 704.9 mm in
    Osmanabad to 1,009.0 mm in Nanded), so a match in the average pattern does not by itself
    show that SIF tracks a district's rainfall from one year to the next.
    """)

with col2:
    st.subheader("How Strong Is This?")
    st.markdown("""
    Across the 72 district-years, SIF on day-of-year 273 correlates with rainfall anomaly
    at **r = 0.53** (Spearman ρ = 0.51, both p < 0.0001; p = 0.001 with standard errors
    clustered by year). Season-mean SIF (June–December) correlates more strongly,
    **r = 0.74**, including within years (r = 0.66).

    With district and year fixed effects, the relationship is **not significant**
    (p = 0.37 for season-mean SIF). SIF and rainfall move together across years and across
    districts, but a district's departure from its own average in a given year is not
    reliably tracked by SIF.
    """)

section_divider()

st.header("Quantifying the Correspondence")

st.image("outputs/figures/sif_rainfall_correlation_scatter.png", use_container_width=True)
styled_caption(
    "District SIF (day-of-year 273) against rainfall anomaly (%), 72 district-years, "
    "with a linear fit (Pearson r = 0.53, p < 0.0001)."
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Pearson r (DOY 273 SIF)", "0.53")
with m2:
    st.metric("Pearson r (season-mean SIF)", "0.74")
with m3:
    st.metric("Fixed-effects p (season-mean)", "0.37")
with m4:
    st.metric("District-years (n)", "72")

st.warning("""
The correlation is real across districts and years, but it does not survive district and
year fixed effects, and the 72 observations are not independent: neighbouring districts
share weather (see Moran's I below). I read it as consistent with SIF responding to
rainfall at the regional scale, not as evidence that SIF tracks year-to-year rainfall
within a district.
""")

section_divider()

st.header("How Non-Independent? A Moran's I Check")

st.markdown("""
I computed **Moran's I** for district SIF and rainfall anomaly in each year, with
Queen-contiguity weights built from the district polygons (mean 3.25 neighbours per
district) and a 9,999-permutation test.
""")

st.image("outputs/figures/spatial_autocorrelation_morans_i.png", use_container_width=True)
styled_caption(
    "Moran's I for district SIF (day-of-year 273) and rainfall anomaly, by year "
    "(* = p < 0.05, 9,999 permutations)."
)

st.info("""
**Rainfall anomaly is spatially clustered in all 9 years** (Moran's I 0.26–0.56,
p < 0.05). **Day-of-year-273 SIF is clustered in 4 of 9 years** (2015, 2016, 2018, 2020;
I = 0.26–0.31) and not in 2017, 2019, 2021, 2022 or 2023 (I = 0.05–0.22). **Season-mean
SIF is clustered in all 9 years** (I = 0.29–0.54), so the spatial pattern is clearer in the
seasonal average than on a single date. Either way the district observations are not
independent, which is why I rely on the clustered and fixed-effects versions of the
correlation above rather than on the plain p-value.
""")

styled_caption("GREEN ALIBI — Combined SIF and Rainfall Comparison")
