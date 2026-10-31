import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Crop-Yield Validation — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Crop-Yield Check Against Official Statistics")

st.markdown("""
Every other check in this study compares one remote-sensing or rainfall product with
another, or with a policy date. None of them touch harvests. I did not run a field survey,
but the Ministry of Agriculture & Farmers Welfare publishes district-season-crop
Area/Production/Yield (APY) statistics every year since 1997-98. I use them to ask one
question: **in the years my rainfall threshold calls drought years, did Marathwada harvest
less?**
""")

section_divider()

st.header("Data & Method")

st.markdown("""
I downloaded the APY data from the India Data Portal and kept the eight Marathwada
districts' Kharif season, 1997-98 to 2022-23. Every district-crop pair with at least 10 of
those 26 seasons (**127 pairs, 16 crops**, mostly cotton, soyabean, jowar and tur) was
converted to yield z-scores against its own mean and standard deviation. I averaged the
z-scores into a **Yield Anomaly Index** per district-year, and the districts into one
region-year value.

The yield series ends in 2022-23, so **2023 has no yield value**, leaving **n = 8
region-years**.
""")

section_divider()

st.header("Yield Anomaly by Year")

st.image("outputs/figures/crop_yield_anomaly_by_year.png", use_container_width=True)
styled_caption(
    "Marathwada Kharif Yield Anomaly Index by year, with rainfall anomaly "
    "(2015–2022; 2023 not yet published)."
)

_yy_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
_yy_drought = [True, False, False, True, False, False, False, False]
_yy_val = [-1.44, -0.02, -0.31, -0.71, -0.24, 0.65, -0.13, 0.46]

yy_row1 = st.columns(4)
yy_row2 = st.columns(4)
for i, (yr, dr, val) in enumerate(zip(_yy_years, _yy_drought, _yy_val)):
    col = yy_row1[i] if i < 4 else yy_row2[i - 4]
    label = f"{yr} ({'drought' if dr else 'normal'})"
    col.metric(label, f"{val:+.2f}")

section_divider()

st.header("Results")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("r vs. rainfall anomaly", "0.93", "p = 0.0009")
with m2:
    st.metric("r vs. season-mean SIF", "0.88", "p = 0.004")
with m3:
    st.metric("Drought years (n=2)", "−1.08", "mean Yield Anomaly Index")
with m4:
    st.metric("Normal years (n=6)", "+0.07", "mean Yield Anomaly Index")

st.success("""
The Yield Anomaly Index tracks CHIRPS rainfall anomaly closely (**r = 0.93, p = 0.0009,
n = 8**), so it picks up real year-to-year variation. Its correlation with season-mean
(June–December) regional SIF is **r = 0.88 (p = 0.004)**; after removing zero yields and extreme
outliers, and in area-weighted, detrended and major-crops-only versions, it is r = 0.80–0.85
(p = 0.007–0.017). Using SIF on day-of-year 273 alone instead gives r = 0.67 (p = 0.071). With eight region-years I treat this as supporting, not confirmatory.
""")

st.info("""
The two drought years (2015, 2018) have a mean index of **−1.08**, against **+0.07** for
the six normal years with yield data. Harvests were lower in the expected direction, but the
difference is not significant (Welch t = −2.87, p = 0.15; p = 0.18–0.23 across the
variants). With only two drought years that is not surprising, and I do not read it as
either confirming or ruling out the effect.
""")

section_divider()

st.header("What This Does and Doesn't Establish")

st.warning("""
Yield is one end-of-season number per district-crop. It says nothing about **within-season
timing**, so it cannot test whether SIF or NDVI responds first. It also includes some crops
grown partly outside the Kharif season. What it does show is that the drought classification
I built from rainfall lines up with real harvest outcomes, in the expected direction.
""")

styled_caption("GREEN ALIBI — Crop-Yield Validation")
