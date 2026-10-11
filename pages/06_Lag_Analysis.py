import os
import streamlit as st
import pandas as pd
from utils.style import apply_custom_style, section_divider, styled_caption

st.set_page_config(page_title="Lag Analysis — GREEN ALIBI", page_icon="📊", layout="wide")
apply_custom_style()

st.title("📊 Quantitative SIF-to-NDVI Lag Analysis")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")


@st.cache_data
def load_csv(name):
    return pd.read_csv(os.path.join(DATA_DIR, name))


def year_label(yr, dr):
    return f"{yr} ({'drought' if dr else 'normal'})"


st.markdown("""
For each year I find the day SIF and NDVI (each normalised 0–1 within the year) first fall below
five decline thresholds (0.9, 0.8, 0.7, 0.6, 0.5) after their peak, by linear interpolation. The
lag at each threshold is the NDVI crossing date minus the SIF crossing date, so a positive lag
means SIF came first. A year's lag is the mean over the thresholds it reaches. SIF is
cropland-weighted GOSIF; NDVI is dated by actual observation day.

The 0–1 scaling matters. The main figures scale each series from its **seasonal minimum** to its
peak ("season-scaled"). Because NDVI stays well above its pre-season level after the monsoon, this
delays NDVI's crossings by construction. The section *Does the Scaling Matter?* below repeats the
lag with each series scaled from its peak to its own **post-peak minimum** ("decline-scaled").
""")

section_divider()

_checks = [
    ("#00D9C0", "✓", "Two Scalings, Double-Logistic Fit and Cross-Correlation Compared"),
    ("#00D9C0", "✓", "TROPOMI SIF (2018–2020): SIF First Under Both Scalings"),
    ("#00D9C0", "✓", "Block-Bootstrap Intervals (2,000 Replicates per Year)"),
    ("#00D9C0", "✓", "40-Variant Method-Dependence Check"),
    ("#FBBF24", "!", "Season-Scaled Lead Mostly a Scaling Effect"),
    ("#FBBF24", "!", "Decline-Scaled: SIF First in 6/9 Years"),
    ("#FBBF24", "!", "H2 and H3 — Not Supported"),
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
styled_caption("SIF-to-NDVI decline lag (days), by decline threshold and year (season-scaled).")

section_divider()

st.header("Mean Lag by Year (Season-Scaled)")

thr = load_csv("sif_ndvi_lag_by_threshold.csv")
unc = load_csv("lag_uncertainty_threshold.csv")
mean_lag = thr.groupby(["year", "is_drought_year"], as_index=False)["lag_days"].mean()

row1 = st.columns(5)
row2 = st.columns(4)
for i, r in enumerate(mean_lag.itertuples(index=False)):
    col = row1[i] if i < 5 else row2[i - 5]
    u = unc[unc["year"] == r.year].iloc[0]
    col.metric(year_label(r.year, r.is_drought_year), f"{r.lag_days:.1f} days",
               f"95% CI [{u.boot_ci_low:.1f}, {u.boot_ci_high:.1f}]", delta_color="off")

g = mean_lag.groupby("is_drought_year")["lag_days"].mean()
st.markdown("**Grouped by drought classification:**")
g1, g2 = st.columns(2)
with g1:
    st.metric("Drought years (mean, n=2)", f"{g[True]:.1f} days")
with g2:
    st.metric("Normal years (mean, n=7)", f"{g[False]:.1f} days")

st.markdown("""
All nine season-scaled means are positive. Of the 43 threshold crossings that resolved, one goes
the other way: at 0.9 in 2019, NDVI crosses 1.3 days before SIF. The lag grows with depth of
decline in most years, as expected if NDVI's raised post-season floor is stretching its crossings.
The 95% intervals come from a 2,000-replicate moving-block residual bootstrap centred on each
year's lag; every year stays above zero, and 8 of the 36 pairs of years have non-overlapping
intervals.
""")

section_divider()

st.header("Full Threshold-by-Threshold Results")

lag_table = thr.rename(columns={
    "year": "Year",
    "is_drought_year": "Drought Year",
    "threshold": "Threshold",
    "sif_crossing_doy": "SIF Crossing (DOY)",
    "ndvi_crossing_doy": "NDVI Crossing (DOY)",
    "lag_days": "Lag (days)",
})
st.dataframe(lag_table, use_container_width=True, hide_index=True)
st.caption("Blank NDVI/lag values (2016 and 2019 at 0.5) mean NDVI never fell that far within the observation window.")

section_divider()

st.header("Does the Scaling Matter?")

st.image("outputs/figures/normalisation_sensitivity.png", use_container_width=True)
styled_caption("Regional SIF–NDVI lag by year: season-scaled, decline-scaled, and the double-logistic end-of-season date.")

ns = load_csv("normalisation_sensitivity_region.csv")
ns_table = pd.DataFrame({
    "Year": ns["year"],
    "Drought": ns["is_drought"],
    "Season-scaled lag (days)": ns["lag_season"].round(1),
    "Decline-scaled lag (days)": ns["lag_decline"].round(1),
    "SIF post-season floor": ns["sif_postpeak_min_season_scaled"].round(2),
    "NDVI post-season floor": ns["ndvi_postpeak_min_season_scaled"].round(2),
})
st.dataframe(ns_table, use_container_width=True, hide_index=True)
st.caption("Post-season floor = the lowest value after the peak, on the season scale (0 = pre-season minimum, 1 = peak).")

st.warning("""
By late December SIF is back near its June level (floor 0.00–0.28), but NDVI is not (0.23–0.59).
Scaled over each series' own decline, the lag shrinks to −5.5 to +13.4 days: SIF is first in six
years and NDVI in 2019, 2021 and 2022. The double-logistic end-of-season dates swing from −30 to
+41 days with no consistent sign, and the fits are unstable at this sampling, so they are only a
sensitivity check. Cross-correlation (below), which does not depend on scaling, agrees more with
the decline-scaled lag.
""")

st.markdown("""
**Districts.** Season-scaled, SIF is first in all 72 district-years (median 17.7 days) and the
lag differs between districts (Friedman p = 0.043). Decline-scaled, SIF is first in 52 of 72
(median 2.3 days, range −8.1 to 19.9), district means run only from 2.9 to 5.6 days, and the
district effect disappears (Friedman p = 0.97). **H2 is not supported.**
""")

st.warning(f"""
**H3 (drought widens the SIF–NDVI lag) is not supported.** Season-scaled, the two drought years
averaged a *smaller* lag ({g[True]:.1f} days) than the seven normal years ({g[False]:.1f} days);
decline-scaled, 6.5 against 3.6 days. At district level (own rainfall baseline) drought
district-years average 14.8 vs 19.5 days season-scaled (p = 0.080) and 5.8 vs 3.4 decline-scaled
(p = 0.13). With two drought years, none of these differences is interpretable. In the
2001–2014 out-of-sample test, with five drought years, the lead was again not larger in drought
(+28.3 against +26.9 days season-scaled; see Findings & Conclusion).
""")

section_divider()

st.header("A Second Method: Cross-Correlation")

st.markdown("""
Threshold-crossing reads when each series reaches points on its decline. Cross-correlation
instead finds the single shift (searched from −N/4 to +N/4 days) that best aligns the whole
post-peak decline of SIF with NDVI. It uses the same series, so it is a different question
asked of the same data, not an independent dataset.
""")

st.image("outputs/figures/cross_correlation_lag.png", use_container_width=True)
styled_caption(
    "Cross-correlation between SIF and NDVI as a function of the lag applied to NDVI, by year "
    "(−N/4 to +N/4 days). Black markers show the correlation-maximizing lag; a negative lag means NDVI leads SIF."
)

xc = load_csv("cross_correlation_lag_by_year.csv")
cc_row1 = st.columns(5)
cc_row2 = st.columns(4)
for i, r in enumerate(xc.itertuples(index=False)):
    col = cc_row1[i] if i < 5 else cc_row2[i - 5]
    col.metric(year_label(r.year, r.is_drought_year), f"{r.cross_corr_lag_days} days",
               f"r = {r.max_correlation:.3f} (r at 0 = {r.corr_at_zero_lag:.3f})", delta_color="off")

st.info("""
Six years show a SIF lead, 2019 is a tie, and 2022 and 2023 show a small NDVI lead (1 and 3 days).
No estimate sits on the edge of its search window. But the correlation curves are flat: the
correlation at zero shift is already 0.975–0.993, so these peaks mostly say the two declines have
similar shapes, not that the shift is sharply pinned down.
""")

section_divider()

st.header("How Precise Is the Cross-Correlation Lag? A Bootstrap Check")

st.markdown("""
Each year has only 13–17 post-peak observations. I resampled them 2,000 times per year
(case resampling), re-ran the same search on each replicate, and took the 2.5th–97.5th
percentiles as a 95% interval.
""")

st.image("outputs/figures/cross_correlation_lag_bootstrap_ci.png", use_container_width=True)
styled_caption(
    "Cross-correlation lag point estimates with 95% bootstrap confidence intervals "
    "(case resampling, 2,000 replicates per year)."
)

bc = load_csv("cross_correlation_lag_bootstrap_ci.csv")
bc_row1 = st.columns(5)
bc_row2 = st.columns(4)
for i, r in enumerate(bc.itertuples(index=False)):
    col = bc_row1[i] if i < 5 else bc_row2[i - 5]
    lo, hi = r[6], r[7]
    col.metric(year_label(r.year, r.is_drought_year), f"{r.point_estimate_lag_days} days",
               f"95% CI [{lo:.0f}, {hi:.0f}]", delta_color="off")

st.warning("""
Only 2015 and 2016 have intervals that exclude zero on the SIF-lead side. 2018 sits on zero
(97.1% of replicates positive), and 2023 leans the other way (95.9% of replicates negative,
upper bound 0). 31 of 36 pairs of years overlap. So cross-correlation supports a SIF lead
clearly in two or three years, finds none in 2019, 2022 and 2023, and cannot resolve the rest.
""")

section_divider()

st.header("How Much Does the Lead Depend on the Method?")

st.markdown("""
I recomputed the regional lag under 40 combinations of analysis choices: SIF cropland-weighted
or not, NDVI timed by observation date or by compositing window, raw or smoothed series, and five
lag metrics (mean-threshold, 0.9, 0.7, 0.5, cross-correlation).
""")

md = load_csv("method_dependence_claims.csv")
md["all_nine"] = md["C1_years_SIF_leads"] == 9
md["drought_smaller"] = md["C2_drought_minus_normal_z<-0.5"] < 0
md["smallest_2018"] = md["C3_2018_rank_smallest"] == 1
md_table = md.groupby("metric", sort=False).agg(
    variants=("variant", "count"),
    sif_leads_all_9=("all_nine", "sum"),
    drought_lag_smaller=("drought_smaller", "sum"),
    smallest_lag_2018=("smallest_2018", "sum"),
).reset_index()
md_table["metric"] = md_table["metric"].replace({"mean": "Mean threshold", "xcorr": "Cross-correlation"})
md_table = md_table.rename(columns={
    "metric": "Lag metric",
    "variants": "Variants",
    "sif_leads_all_9": "SIF leads all 9 years",
    "drought_lag_smaller": "Drought lag < normal lag",
    "smallest_lag_2018": "2018 smallest lag",
})
st.dataframe(md_table, use_container_width=True, hide_index=True)

st.markdown(f"""
"SIF leads in all nine years" holds in all 8 mean-threshold variants and none of the 8
cross-correlation variants. Drought years have the smaller lag in {int(md["drought_smaller"].sum())}
of 40 variants, and 2018 has the smallest lag in {int(md["smallest_2018"].sum())} of 40. The data-handling
choices on their own matter little: switching to unweighted SIF and window-dated NDVI moves
individual years by −2.5 to +2.6 days and changes no direction. So the direction of the lead is
robust to data handling, but not to the lag metric, and the number of days is not a stable quantity.
""")

section_divider()

st.header("Independent Check: TROPOMI SIF")

st.markdown("""
GOSIF uses MODIS reflectance as a predictor, so it is not fully independent of MODIS NDVI.
TROPOMI SIF is a direct retrieval, available for 2018–2020. I ran the same threshold-crossing lag
against NDVI with it.
""")

tr = load_csv("tropomi_vs_gosif.csv")
tr_main = tr[tr["variant"].str.startswith("main")].copy()
tr_table = pd.DataFrame({
    "Year": tr_main["year"],
    "Composites": tr_main["n_composites"],
    "r (TROPOMI vs GOSIF)": tr_main["r_with_gosif"].round(2),
    "Peak DOY TROPOMI": tr_main["peak_doy_tropomi"],
    "Peak DOY GOSIF": tr_main["peak_doy_gosif"],
    "Lag, TROPOMI (days)": tr_main["lag_tropomi_vs_ndvi"].round(1),
    "Lag, GOSIF (days)": tr_main["lag_gosif_vs_ndvi"].round(1),
})
st.dataframe(tr_table, use_container_width=True, hide_index=True)
st.caption("Main variant: cloud fraction < 0.2, cropland soundings, SIF_Corr_743. Lag = NDVI 0.9–0.5 mean crossing minus SIF crossing.")

st.success(f"""
TROPOMI follows GOSIF's seasonal trajectory closely (r = 0.91–0.97), puts SIF's decline before
NDVI's in all three years, and also gives 2018 the smallest lead. All four variants agree
(lags {tr["lag_tropomi_vs_ndvi"].min():.1f}–{tr["lag_tropomi_vs_ndvi"].max():.1f} days, none negative).
""")

st.warning("""
Decline-scaled, TROPOMI still puts SIF first in all three years (10.4, 10.3 and 27.7 days,
against GOSIF's 3.5, −5.5 and 8.8). The size differs between products, and the check covers just
one drought year (2018), since TROPOMI does not reach back to 2015.
""")

section_divider()

st.header("Is the Lead an NDVI Property? EVI and NIRv")

st.markdown("""
GOSIF is partly predicted from MODIS EVI, and NDVI saturates over dense canopy. So I ran the same
threshold-crossing comparison with two other MOD13Q1 indices from the same composites: EVI, and
NIRv (NDVI × near-infrared reflectance), a proxy for canopy structure and absorbed light.
""")

vi = load_csv("vegetation_index_lag.csv")
vi_cols = {"SIF_vs_NDVI": "SIF before NDVI", "NIRv_vs_NDVI": "NIRv before NDVI",
           "EVI_vs_NDVI": "EVI before NDVI", "SIF_vs_NIRv": "SIF before NIRv"}
vi_rows = []
for key, label in vi_cols.items():
    for how, hl in [("season", "season-scaled"), ("decline", "decline-scaled")]:
        col = vi[f"{key}_{how}"]
        vi_rows.append({"Comparison": label, "Scaling": hl, "Years first": f"{(col > 0).sum()}/{col.notna().sum()}",
                        "Mean lag (days)": round(col.mean(), 1)})
st.dataframe(pd.DataFrame(vi_rows), use_container_width=True, hide_index=True)

st.warning("""
NIRv and EVI lead NDVI by as much as SIF does, and SIF does not lead NIRv. The lead SIF shows over
NDVI is a property of NDVI's late decline, not an early fluorescence response.
""")

styled_caption("GREEN ALIBI — Quantitative Lag Analysis")
