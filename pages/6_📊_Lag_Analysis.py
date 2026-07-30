import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Lag Analysis — GREEN ALIBI", page_icon="📊", layout="wide")
apply_custom_style()

st.title("📊 Quantitative SIF-to-NDVI Lag Analysis")

st.markdown("""
Replacing visual comparison with a numeric method: for each year, the day-of-year at which
SIF and NDVI crossed five decline thresholds (90%, 80%, 70%, 60%, 50% of seasonal peak) was
calculated via linear interpolation, and the lag at each threshold recorded as the
difference between the two crossing dates.
""")

section_divider()

st.image("outputs/figures/sif_ndvi_lag_by_threshold.png", use_container_width=True)
styled_caption("SIF-to-NDVI decline lag (days), by decline threshold and year.")

section_divider()

# ============================================================
# KEY METRICS
# ============================================================
st.header("Mean Lag by Year")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("2015 (drought)", "24.2 days")
with m2:
    st.metric("2018 (drought)", "5.1 days")
with m3:
    st.metric("2020 (normal)", "25.5 days")

st.markdown("**Grouped by drought classification:**")
g1, g2 = st.columns(2)
with g1:
    st.metric("Drought years (mean)", "14.6 days")
with g2:
    st.metric("Normal year", "25.5 days")

section_divider()

# ============================================================
# FULL DATA TABLE
# ============================================================
st.header("Full Threshold-by-Threshold Results")

lag_data = pd.DataFrame({
    "Year": [2015]*5 + [2018]*5 + [2020]*5,
    "Drought Year": [True]*5 + [True]*5 + [False]*5,
    "Threshold": [0.9, 0.8, 0.7, 0.6, 0.5] * 3,
    "SIF Crossing (DOY)": [262.9, 270.2, 276.4, 282.6, 290.8,
                            251.9, 258.2, 264.7, 270.9, 276.4,
                            251.5, 259.5, 264.1, 277.5, 292.2],
    "NDVI Crossing (DOY)": [282.5, 286.4, 298.9, 304.7, 331.1,
                             254.6, 266.6, 269.4, 272.2, 284.7,
                             255.4, 269.1, 298.7, 316.0, 333.0],
    "Lag (days)": [19.7, 16.2, 22.5, 22.1, 40.3,
                   2.7, 8.5, 4.8, 1.4, 8.3,
                   3.9, 9.6, 34.6, 38.6, 40.8]
})

st.dataframe(lag_data, use_container_width=True, hide_index=True)

section_divider()

# ============================================================
# HONEST INTERPRETATION
# ============================================================
st.header("What This Means for H3")

st.warning("""
**H3 (drought amplifies the SIF–NDVI lag) is not supported by this data.**

The two drought years produced a *smaller* average lag (14.6 days) than the normal year
(25.5 days) — the opposite of the predicted direction. The two drought years also differ
substantially from each other (24.2 vs. 5.1 days) — a gap larger than either year's
difference from the normal year. This indicates that "drought year" is too coarse a
category to predict SIF–NDVI lag behavior on its own, at least at this sample size (n = 3).
""")

st.markdown("""
What **does** hold up: SIF's decline precedes NDVI's decline consistently across all three
years, supporting **H1** in its general form (see **Seasonal Trajectories**). What does not
hold up is the more specific claim that drought severity scales the size of that lead —
a genuine, honestly-reported non-result rather than a confirmed contrary finding, given the
small sample.
""")

styled_caption("GREEN ALIBI — Quantitative Lag Analysis")