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
    ("#00D9C0", "✓", "Two Methodologically Distinct Lag-Estimation Methods"),
    ("#00D9C0", "✓", "Bootstrap Confidence Intervals (2,000 replicates/year)"),
    ("#00D9C0", "✓", "Independent Rainfall Validation (CHIRPS)"),
    ("#00D9C0", "✓", "Moran's I Spatial-Autocorrelation Check"),
    ("#00D9C0", "✓", "Cross-Referenced Against Official Drought Declaration"),
    ("#FBBF24", "!", "H3 (Drought Amplifies Lag) — Honestly Not Supported"),
    ("#FBBF24", "!", "Cross-Correlation/Bootstrap Search-Space Bug — Found, Fixed, Disclosed"),
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
              font-weight:700; font-size:0.85rem; margin-bottom:6px;">Robustness At a Glance</p>
    <div style="display:flex; flex-wrap:wrap; margin-bottom: 6px;">{_badges}</div>
    """,
    unsafe_allow_html=True,
)

section_divider()

st.image("outputs/figures/sif_ndvi_lag_by_threshold.png", use_container_width=True)
styled_caption("SIF-to-NDVI decline lag (days), by decline threshold and year, all eight study years.")

section_divider()

# ============================================================
# KEY METRICS
# ============================================================
st.header("Mean Lag by Year")

_years_lag = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]
_drought_flag = [True, False, False, True, False, False, False, False]
_mean_lag = [16.3, 23.8, 21.6, -1.1, 17.2, 20.6, 5.1, 4.2]

row1 = st.columns(4)
row2 = st.columns(4)
for i, (yr, dr, lag) in enumerate(zip(_years_lag, _drought_flag, _mean_lag)):
    col = row1[i] if i < 4 else row2[i - 4]
    label = f"{yr} ({'drought' if dr else 'normal'})"
    col.metric(label, f"{lag} days")

st.markdown("**Grouped by drought classification:**")
g1, g2 = st.columns(2)
with g1:
    st.metric("Drought years (mean, n=2)", "7.6 days")
with g2:
    st.metric("Normal years (mean, n=6)", "15.0 days")

section_divider()

# ============================================================
# FULL DATA TABLE
# ============================================================
st.header("Full Threshold-by-Threshold Results")

lag_data = pd.DataFrame({
    "Year": [2015]*5 + [2016]*5 + [2017]*5 + [2018]*5 + [2019]*5 + [2020]*5 + [2022]*5 + [2023]*5,
    "Drought Year": [True]*5 + [False]*5 + [False]*5 + [True]*5 + [False]*5 + [False]*5 + [False]*5 + [False]*5,
    "Threshold": [0.9, 0.8, 0.7, 0.6, 0.5] * 8,
    "SIF Crossing (DOY)": [263.6, 270.6, 276.3, 281.7, 289.6,
                            259.6, 266.2, 272.6, 283.2, 291.7,
                            253.5, 260.0, 267.7, 283.8, 290.7,
                            251.4, 257.4, 262.6, 268.0, 273.4,
                            268.8, 276.7, 285.2, 304.7, 314.5,
                            249.4, 258.3, 262.2, 269.3, 289.5,
                            260.3, 270.3, 280.6, 287.2, 295.1,
                            264.7, 269.2, 274.2, 282.4, 287.6],
    "NDVI Crossing (DOY)": [274.5, 278.4, 290.9, 296.7, 323.1,
                             273.4, 280.0, 295.4, 328.0, None,
                             258.1, 274.5, 293.8, 309.4, 327.6,
                             246.6, 258.6, 261.4, 264.2, 276.7,
                             258.7, 292.8, 312.1, 340.6, None,
                             247.2, 261.0, 290.5, 308.0, 324.9,
                             260.3, 274.2, 279.0, 295.0, 310.3,
                             261.4, 273.6, 277.3, 280.9, 305.9],
    "Lag (days)": [10.9, 7.8, 14.6, 15.0, 33.4,
                   13.8, 13.8, 22.8, 44.8, None,
                   4.5, 14.6, 26.2, 25.6, 37.0,
                   -4.8, 1.2, -1.2, -3.7, 3.2,
                   -10.1, 16.2, 26.8, 36.0, None,
                   -2.2, 2.7, 28.3, 38.6, 35.4,
                   -0.0, 4.0, -1.6, 7.8, 15.2,
                   -3.4, 4.4, 3.0, -1.5, 18.3]
})

st.dataframe(lag_data, use_container_width=True, hide_index=True)
st.caption("Blank NDVI/lag values (2016 and 2019, 50% threshold) mean that threshold never resolved within that year's observation window.")

section_divider()

# ============================================================
# HONEST INTERPRETATION
# ============================================================
st.header("What This Means for H3")

st.warning("""
**H3 (drought amplifies the SIF–NDVI lag) is not supported by this data — confirmed at
more than double the original sample size.**

The two drought years (2015, 2018) produced a *smaller* average lag (7.6 days) than the six
normal years (15.0 days) — the opposite of the predicted direction, and the same direction
found in the original three-year study. This indicates that "drought year" is too coarse a
category to predict SIF–NDVI lag behavior on its own — a finding that has now replicated
across two independently sized samples (n = 3 and n = 8 years).
""")

st.markdown("""
What **does** hold up: SIF's decline precedes NDVI's decline in seven of the eight years,
supporting **H1** in its general form (see **Seasonal Trajectories**). What does not
hold up is the more specific claim that drought severity scales the size of that lead —
a genuine, honestly-reported non-result rather than a confirmed contrary finding.
**2018 is a real exception, not noise:** its mean lag is marginally negative, meaning at
most thresholds NDVI and SIF crossed within a few days of each other in either order. This
is discussed directly, not averaged away, and shows up again in the cross-correlation and
bootstrap checks below.
""")

section_divider()

# ============================================================
# CROSS-CORRELATION ROBUSTNESS CHECK
# ============================================================
st.header("Robustness Check: A Methodologically Distinct Lag Method")

st.markdown("""
The threshold-crossing method above is sensitive mainly to *when decline starts*,
especially at high thresholds. As a check on whether that specific choice of method is
driving the lag numbers above, a second, methodologically distinct lag estimate was built
using **time-lagged cross-correlation** — finding the single time-shift that best aligns
the overall shape of the SIF and NDVI curves, rather than any particular threshold
crossing. It runs on the same underlying SIF/NDVI series as the threshold-crossing method,
just a different piece of math — not a second independent dataset.
""")

st.error("""
**A real bug was found and fixed here before this page was published.** This script's lag
search originally ran from 0 to +N/4 days only — it could never test a negative lag, so it
was mathematically impossible for it to ever report NDVI leading SIF, regardless of what
the data showed. Fixed to search the full −N/4 to +N/4 range and rerun from scratch; the
numbers below are the corrected ones. Full account in Development Log, Entry 17.
""")

st.image("outputs/figures/cross_correlation_lag.png", use_container_width=True)
styled_caption(
    "Cross-correlation between SIF(t) and NDVI(t + lag), by year, all eight study years, "
    "searched over both directions (−N/4 to +N/4 days) of each year's decline window. "
    "A negative lag means NDVI leads SIF."
)

_cc_years = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]
_cc_drought = [True, False, False, True, False, False, False, False]
_cc_lag = [4, 2, 27, -4, 18, 0, -9, -10]
_cc_r = [0.9933, 0.9961, 0.9878, 0.9942, 0.9696, 0.9879, 0.9928, 0.9400]

cc_row1 = st.columns(4)
cc_row2 = st.columns(4)
for i, (yr, dr, lag, r) in enumerate(zip(_cc_years, _cc_drought, _cc_lag, _cc_r)):
    col = cc_row1[i] if i < 4 else cc_row2[i - 4]
    label = f"{yr} ({'drought' if dr else 'normal'})"
    col.metric(label, f"{lag} days", f"r = {r:.4f}")

st.success("""
**What this confirms, now that the search can actually find both directions:** SIF clearly
leads in 4 of 8 years (2015, 2016, 2017, 2019), 2020 is a genuine tie at exactly zero, and
NDVI clearly leads in 3 years (2018, 2022, 2023) — not a boundary artifact, but a real
correlation-maximizing lag on the negative side. **H1 now rests on two methods, not one**,
and the two methods only partly agree: cross-correlation confirms the threshold-crossing
direction in 5 of 8 years but reverses it in 2022 and 2023, where threshold-crossing found
a small SIF lead.
""")

st.warning("""
**What this does *not* confirm:** a single shared year-to-year ranking, or that the direction
itself is settled for every year. The threshold-crossing method's largest average lags belong
to 2016 and 2017; cross-correlation agrees 2017 is large (27 days) but ranks 2019 (18 days)
above 2016 (2 days) — the two methods answering slightly different questions (onset timing
vs. whole-curve shape alignment). 2018 stays the year both methods agree breaks the pattern,
but cross-correlation now also flags 2022 and 2023 the same way, which threshold-crossing
does not. It means the *exact* day-count lag values, which single year "wins," and — for
2022/2023 — even the direction itself should be read as method-dependent rather than fixed,
universal facts.
""")

section_divider()

# ============================================================
# UNCERTAINTY QUANTIFICATION — BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================
st.header("How Precise Are These Numbers? A Bootstrap Check")

st.markdown("""
Every lag value above is a single point estimate computed from a small number of discrete
satellite observations — only 14-18 post-peak 8-day dates per year, depending on the year. A
point estimate with no uncertainty range invites a fair question: how much would this number
move if the satellite had happened to catch slightly different overpass dates that season? A
case-resampling bootstrap (2,000 replicates per year, resampling which of that year's
observations feed the fit) answers this directly for the cross-correlation lag estimates
above.
""")

st.error("""
**Same bug, same fix, same re-run as the cross-correlation check above.** This bootstrap's
internal lag search had the identical one-sided range (0 to +N/4), so it was mathematically
impossible for any replicate, in any year, to come back negative — a claim like "100% of
replicates non-negative" was guaranteed by the code, not shown by the data. Fixed to search
both directions and rerun from scratch; the numbers below are the corrected ones. Full
account in Development Log, Entry 17.
""")

st.image("outputs/figures/cross_correlation_lag_bootstrap_ci.png", use_container_width=True)
styled_caption(
    "Cross-correlation lag point estimates with 95% bootstrap confidence intervals "
    "(case-resampling bootstrap, N = 2,000 replicates per year), all eight study years."
)

_bc_years = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]
_bc_drought = [True, False, False, True, False, False, False, False]
_bc_lag = [4, 2, 27, -4, 18, 0, -9, -10]
_bc_ci = ["[0, 11]", "[-3, 7]", "[0, 30]", "[-13, 3]", "[-9, 26]", "[-32, 32]", "[-16, -2]", "[-25, -2]"]
_bc_pct_pos = [89.6, 72.9, 96.1, 7.1, 85.7, 41.3, 0.3, 0.1]
_bc_pct_neg = [2.2, 17.3, 2.0, 87.4, 10.0, 14.6, 99.4, 99.1]

bc_row1 = st.columns(4)
bc_row2 = st.columns(4)
for i, (yr, dr, lag, ci) in enumerate(zip(_bc_years, _bc_drought, _bc_lag, _bc_ci)):
    col = bc_row1[i] if i < 4 else bc_row2[i - 4]
    label = f"{yr} ({'drought' if dr else 'normal'})"
    col.metric(label, f"{lag} days", f"95% CI {ci}")

st.success(f"""
**Direction: genuinely mixed, not uniform.** The share of replicates landing at zero-or-above
breaks down as: 97.8% (2015), 82.7% (2016), 98.0% (2017), 12.7% (2018), 90.0% (2019), 85.4%
(2020), 0.6% (2022), and 0.9% (2023). Flip that around: in 2022 and 2023, {_bc_pct_neg[6]}%
and {_bc_pct_neg[7]}% of replicates land *below* zero — a strong, well-resolved signal in the
NDVI-leads direction, not a weak one. 2018 leans the same way ({_bc_pct_neg[3]}% negative) but
its interval still straddles zero, so it's less settled than 2022/2023. That leaves five years
with real evidence in the SIF-leads direction — 2015 and 2017 strongly, 2016 and 2019 more
moderately, and 2020 sitting almost exactly on the fence.
""")

st.warning("""
**Magnitude: mostly indistinguishable, but not entirely.** The confidence intervals above are
wide relative to the point estimates, and of the **28 possible pairwise comparisons, 24 still
overlap** and aren't distinguishable from each other. But **4 pairs now genuinely don't
overlap** — 2015 vs. 2022, 2015 vs. 2023, 2017 vs. 2022, and 2017 vs. 2023 — meaning the two
years with the clearest SIF-leads signal are statistically distinguishable from the two years
with the clearest NDVI-leads signal. The honest summary: SIF's decline comes out ahead in
about half of the eight years with reasonable-to-strong confidence, NDVI comes out ahead in
two of the eight years with strong confidence, and the remaining two years (2018, 2020) don't
clearly resolve either way.
""")

styled_caption("GREEN ALIBI — Quantitative Lag Analysis")