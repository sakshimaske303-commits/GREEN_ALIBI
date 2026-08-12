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

_checks = [
    ("#00D9C0", "✓", "Two Independent Lag-Estimation Methods"),
    ("#00D9C0", "✓", "Bootstrap Confidence Intervals (2,000 replicates/year)"),
    ("#00D9C0", "✓", "Independent Rainfall Validation (CHIRPS)"),
    ("#00D9C0", "✓", "Moran's I Spatial-Autocorrelation Check"),
    ("#00D9C0", "✓", "Cross-Referenced Against Official Drought Declaration"),
    ("#FBBF24", "!", "H3 (Drought Amplifies Lag) — Honestly Not Supported"),
    ("#FBBF24", "!", "Exact Year Ranking — Flagged as Method-Sensitive"),
]
_badges = "".join(
    f"""<span style="display:inline-flex; align-items:center; gap:6px; background:rgba(0,217,192,0.08);
        border:1px solid rgba(0,217,192,0.3); border-radius:20px; padding:6px 14px; margin:4px;
        font-size:0.82rem; color:#F2F2F5; font-weight:600;">
        <span style="color:{color}; font-weight:900;">{mark}</span>{label}</span>"""
    for color, mark, label in _checks
)
st.markdown(
    f"""
    <p style="color:#E91E8C; text-transform:uppercase; letter-spacing:1.5px;
              font-weight:700; font-size:0.85rem; margin-bottom:6px;">🔍 Robustness At a Glance</p>
    <div style="display:flex; flex-wrap:wrap; margin-bottom: 6px;">{_badges}</div>
    """,
    unsafe_allow_html=True,
)

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
    st.metric("2015 (drought)", "24.3 days")
with m2:
    st.metric("2018 (drought)", "6.9 days")
with m3:
    st.metric("2020 (normal)", "28.7 days")

st.markdown("**Grouped by drought classification:**")
g1, g2 = st.columns(2)
with g1:
    st.metric("Drought years (mean)", "15.6 days")
with g2:
    st.metric("Normal year", "28.7 days")

section_divider()

# ============================================================
# FULL DATA TABLE
# ============================================================
st.header("Full Threshold-by-Threshold Results")

lag_data = pd.DataFrame({
    "Year": [2015]*5 + [2018]*5 + [2020]*5,
    "Drought Year": [True]*5 + [True]*5 + [False]*5,
    "Threshold": [0.9, 0.8, 0.7, 0.6, 0.5] * 3,
    "SIF Crossing (DOY)": [263.6, 270.6, 276.3, 281.7, 289.6,
                            251.4, 257.4, 262.6, 268.0, 273.4,
                            249.4, 258.3, 262.2, 269.3, 289.5],
    "NDVI Crossing (DOY)": [282.5, 286.4, 298.9, 304.7, 331.1,
                             254.6, 266.6, 269.4, 272.2, 284.7,
                             255.4, 269.1, 298.7, 316.0, 333.0],
    "Lag (days)": [18.9, 15.8, 22.6, 23.0, 41.4,
                   3.2, 9.2, 6.8, 4.3, 11.2,
                   6.0, 10.8, 36.4, 46.7, 43.5]
})

st.dataframe(lag_data, use_container_width=True, hide_index=True)

section_divider()

# ============================================================
# HONEST INTERPRETATION
# ============================================================
st.header("What This Means for H3")

st.warning("""
**H3 (drought amplifies the SIF–NDVI lag) is not supported by this data.**

The two drought years produced a *smaller* average lag (15.6 days) than the normal year
(28.7 days) — the opposite of the predicted direction. The two drought years also differ
substantially from each other (24.3 vs. 6.9 days) — a gap larger than either year's
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

section_divider()

# ============================================================
# CROSS-CORRELATION ROBUSTNESS CHECK
# ============================================================
st.header("Robustness Check: An Independent Lag Method")

st.markdown("""
The threshold-crossing method above is sensitive mainly to *when decline starts*,
especially at high thresholds. As a check on whether that specific choice of method is
driving the lag numbers above, a second, independently computed lag estimate was built
using **time-lagged cross-correlation** — finding the single time-shift that best aligns
the overall shape of the SIF and NDVI curves, rather than any particular threshold
crossing.
""")

st.image("outputs/figures/cross_correlation_lag.png", use_container_width=True)
styled_caption(
    "Cross-correlation between SIF(t) and NDVI(t + lag), by year. Lags tested are capped "
    "at N/4 of the decline window (a standard guideline) to avoid boundary-pinned, unreliable "
    "peak estimates. All three peaks shown are interior maxima, well clear of that boundary."
)

cc1, cc2, cc3 = st.columns(3)
with cc1:
    st.metric("2015 (drought)", "13 days", "r = 0.992")
with cc2:
    st.metric("2018 (drought)", "4 days", "r = 0.995")
with cc3:
    st.metric("2020 (normal)", "7 days", "r = 0.987")

st.success("""
**What this confirms:** every year's correlation-maximizing lag is positive — an entirely
independent method agrees that SIF leads NDVI in all three years. **H1 now rests on two
methods, not one.**
""")

st.warning("""
**What this does *not* confirm:** the same year-to-year *ranking*. The threshold-crossing
method ranked 2020 (normal) highest and 2018 lowest; cross-correlation instead ranks 2015
highest and 2018 lowest — both methods agree 2018 has the smallest lag, but disagree on
whether 2015 or 2020 has the largest. This isn't a contradiction so much as the two methods
answering slightly different questions (onset timing vs. whole-curve shape alignment), but
it means the *exact* day-count lag values, and which single year "wins," should be read as
method-dependent estimates — not precise, method-independent facts. The qualitative
SIF-leads-NDVI finding is the robust result here; the specific ranking is not.
""")

section_divider()

# ============================================================
# UNCERTAINTY QUANTIFICATION — BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================
st.header("How Precise Are These Numbers? A Bootstrap Check")

st.markdown("""
Every lag value above is a single point estimate computed from a small number of discrete
satellite observations — only 17 post-peak 8-day dates per year. A point estimate with no
uncertainty range invites a fair question: how much would this number move if the satellite
had happened to catch slightly different overpass dates that season? A case-resampling
bootstrap (2,000 replicates per year, resampling which of the 17 observations feed the fit)
answers this directly for the cross-correlation lag estimates above.
""")

st.image("outputs/figures/cross_correlation_lag_bootstrap_ci.png", use_container_width=True)
styled_caption(
    "Cross-correlation lag point estimates with 95% bootstrap confidence intervals "
    "(case-resampling bootstrap, N = 2,000 replicates per year)."
)

bc1, bc2, bc3 = st.columns(3)
with bc1:
    st.metric("2015 (drought)", "13 days", "95% CI [5, 20]")
with bc2:
    st.metric("2018 (drought)", "4 days", "95% CI [0, 9]")
with bc3:
    st.metric("2020 (normal)", "7 days", "95% CI [0, 32]")

st.success("""
**Direction: robust.** Across every year, the bootstrap-estimated lag was non-negative in
**100%** of replicates, and strictly positive in 99.9% (2015), 84.5% (2018), and 88.6%
(2020) of replicates. SIF leading NDVI is not a fragile result of one lucky sample.
""")

st.warning("""
**Magnitude: not precise enough to rank years.** The confidence intervals above are wide
relative to the point estimates, and **every pairwise comparison between years' intervals
overlaps**. That means the specific year-to-year ranking discussed above — and the exact
day-count values themselves — are not statistically distinguishable from noise at this
sample size. This is a quantified, stronger version of the caution already given for the
method-sensitivity finding above: treat the *direction* (SIF leads NDVI) as this study's
robust result, and the *exact numbers* as approximate.
""")

styled_caption("GREEN ALIBI — Quantitative Lag Analysis")