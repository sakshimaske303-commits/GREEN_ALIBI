import os

import pandas as pd
import streamlit as st
from utils.style import apply_custom_style, section_divider, styled_caption, MAGENTA, TEAL, TEXT_LIGHT

st.set_page_config(page_title="Policy Design Lab — GREEN ALIBI", layout="wide")
apply_custom_style()

st.title("Policy Design Lab")

st.markdown(
    f"""
    <h3 style="font-weight:600; color:{MAGENTA}; margin-top:-6px;">
    Who should a drought trigger fail? Combining signals, pricing errors and comparing five drought systems
    </h3>
    <div style="display:flex; flex-wrap:wrap; gap:8px; margin:6px 0 16px 0;">
      <span style="border:1px solid {TEAL}; color:{TEAL}; border-radius:999px; padding:4px 12px; font-size:0.85rem;">Comparative environmental policy</span>
      <span style="border:1px solid {TEAL}; color:{TEAL}; border-radius:999px; padding:4px 12px; font-size:0.85rem;">Policy instruments (Hood's NATO)</span>
      <span style="border:1px solid {TEAL}; color:{TEAL}; border-radius:999px; padding:4px 12px; font-size:0.85rem;">Policy design and change (Hall)</span>
      <span style="border:1px solid {TEAL}; color:{TEAL}; border-radius:999px; padding:4px 12px; font-size:0.85rem;">Environmental economics of errors</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
The rest of this dashboard asks whether a satellite signal fires in a drought. This page asks the design
questions that follow. How should the signals be combined? What does each kind of error cost, and who
carries it? How do other countries give satellite indices power over drought decisions? And what kind of
policy change would each proposal be? Everything here reuses the alarm and trigger dates of the main study
(paper, Appendix A); no main result changes.
""")

st.info("""
**Corrected in version 2.2.0.** Earlier versions used my own approximation of Trigger-1, which was much stricter
than the Manual's rule and flagged only 2 of 15 drought district-years. The rules and costs on this page now use
the Manual's Trigger-1 (a dry spell of four standard weeks, each below 50% of normal weekly rainfall, or scanty
rainfall, or SPI below −1.5).
""")

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Most droughts flagged", "14 of 15", "Trigger-1 OR NDVI; 4 false alarms, as many as NDVI alone", delta_color="off")
with k2:
    st.metric("Manual's rainfall trigger", "7 of 15", "10 per pixel; 1 false alarm; first wherever a satellite also fired", delta_color="off")
with k3:
    st.metric("Relief withheld by the rainfall trigger", "₹4,177 cr", "8 of 15 missed; ₹526 cr with NDVI as a second route", delta_color="off")
with k4:
    st.metric("Systems compared", "5", "India, EU, Spain, USA, Kenya", delta_color="off")

section_divider()

t1, t2, t3, t4 = st.tabs(["1 · Combining the signals", "2 · What the errors cost",
                          "3 · Five systems compared", "4 · Three orders of change"])

# ---------------------------------------------------------------- 1. combined rules
with t1:
    st.subheader("Rainfall first, vegetation as confirmation: does the Manual's order work?")
    st.markdown("""
    India's Manual for Drought Management uses the signals in a sequence. Rainfall is a gate: only when
    Trigger-1 is set off do states look at impact indicators, one of which is the vegetation index, and then
    verify crop loss in the field. So the vegetation index can only confirm a drought that rainfall has
    already flagged. I scored combined rules on the same 72 district-years (15 drought, 57 normal). Each
    rule fires on the date its condition is first met.
    """)
    _RULES = "data/processed/trigger_rule_comparison.csv"
    if os.path.exists(_RULES):
        rr = pd.read_csv(_RULES)
        if os.path.exists("outputs/figures/trigger_rule_comparison.png"):
            st.image("outputs/figures/trigger_rule_comparison.png", use_container_width=True)
            styled_caption("Drought district-years flagged (dark: by 30 September) and false alarms, for each rule, 2015–2023.")
        main_r = rr[rr["setting"] == "2015-2023 (main)"]
        st.dataframe(pd.DataFrame({
            "Rule": main_r["rule"],
            "Drought district-years flagged (of 15)": main_r["drought_flagged"],
            "False alarms (of 57)": main_r["false_alarms"],
            "Flagged by 30 September": main_r["flagged_by_30_sep"],
            "Median alarm date": main_r["median_alarm_date"],
        }), use_container_width=True, hide_index=True)
        with st.expander("Do the results hold? NDVI as observed, and 2001–2014"):
            st.dataframe(pd.DataFrame({
                "Setting": rr["setting"], "Rule": rr["rule"],
                "Drought flagged": rr["drought_flagged"].astype(str) + "/" + rr["drought_n"].astype(str),
                "False alarms": rr["false_alarms"].astype(str) + "/" + rr["normal_n"].astype(str),
            }), use_container_width=True, hide_index=True)
            styled_caption("The 25% deficit and the rules built on it are scored only for 2015–2023; Trigger-1, from the CHIRPS pixel stacks, is scored in both periods.")
    else:
        st.info("The rule comparison appears here once `trigger_rule_comparison.py` has been run.")

    c1, c2 = st.columns(2)
    with c1:
        st.warning("""
        **The rainfall trigger is early and precise; NDVI adds coverage.** The Manual's Trigger-1 flagged 7 of 15
        (10 per pixel), all by 30 September and with one false alarm. NDVI flagged seven of the eight it missed, so
        Trigger-1 OR NDVI flagged 14 with no more false alarms than NDVI alone (4). Rules that wait for a 25%
        rainfall deficit flagged only 7 or 8. These droughts are themselves defined by rainfall, so the counts show
        how the indicators agree, not droughts the Manual would miss.
        """)
    with c2:
        st.info("""
        **SIF as a confirmation step does not hold up.** Requiring SIF to confirm NDVI halved the false
        alarms (2 against 4) with the same 9 droughts flagged by 30 September. But with NDVI taken as
        observed it is 2 against 3, and in 2001–2014 it flagged only 2 of 40 drought district-years against
        6 for NDVI alone.
        """)

# ---------------------------------------------------------------- 2. cost of errors
with t2:
    st.subheader("Pricing the two errors: relief withheld against relief misspent")
    st.markdown("""
    Counting errors treats every district alike and leaves open how a missed drought should weigh against a
    false alarm. So I valued both as the relief they move: the SDRF/NDRF input subsidy for rainfed crops,
    **₹8,500 per hectare**, on each district's Kharif sown area. A missed drought **withholds** that relief
    from a drought-hit district; a false alarm **pays** it where there was no drought.
    """)
    st.latex(r"\text{cost(rule)} = w \times \text{relief withheld in missed droughts} + \text{relief paid in normal years}")
    st.markdown("""
    The weight **w** says how much a rupee that fails to reach a drought-hit district counts against a rupee
    paid in a normal year. I do not choose w; I show where the cheapest rule changes as w rises, in the spirit
    of the cost–loss model for weather warnings (Murphy, 1977).
    """)
    _COST = "data/processed/trigger_cost_comparison.csv"
    _SW = "data/processed/trigger_cost_switch_points.csv"
    if os.path.exists(_COST) and os.path.exists(_SW):
        cc = pd.read_csv(_COST)
        sw = pd.read_csv(_SW)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Kharif output lost, 15 drought district-years", "₹25,450 cr", "at 2022–23 MSP", delta_color="off")
        with m2:
            st.metric("Share of that loss SDRF relief would cover", "31%", "₹7,843 crore", delta_color="off")
        with m3:
            st.metric("Rainfall-gated rule cheapest only if", "w < 0.41", "0.30 if counted by 30 September", delta_color="off")
        if os.path.exists("outputs/figures/trigger_cost_frontier.png"):
            st.image("outputs/figures/trigger_cost_frontier.png", use_container_width=True)
            styled_caption("Relief withheld in missed droughts against relief paid in normal years. Lower left is better; "
                           "the dashed line joins the rules that are cheapest for some weight w.")
        st.markdown("**The cheapest rule, by weight**")
        st.dataframe(pd.DataFrame({
            "Drought counted as flagged": sw["timing"],
            "Weight w from": sw["w_from"], "to": sw["w_to"],
            "Cheapest rule": sw["rule"],
        }), use_container_width=True, hide_index=True)
        styled_caption("Weights from 0.05 to 10. SIF at z < −3 ties with NDVI AND SIF at z < −3.")
        with st.expander("Every rule, in ₹ crore"):
            c_any = cc[cc["timing"] == "any date"]
            st.dataframe(pd.DataFrame({
                "Rule": c_any["rule"],
                "Drought flagged (of 15)": c_any["drought_flagged"],
                "False alarms (of 57)": c_any["false_alarms"],
                "Relief withheld": c_any["relief_withheld_in_missed_droughts_cr"].round(0).astype(int),
                "Relief paid in normal years": c_any["relief_paid_in_normal_years_cr"].round(0).astype(int),
                "Crop loss in missed droughts": c_any["crop_loss_in_missed_droughts_cr"].round(0).astype(int),
            }), use_container_width=True, hide_index=True)
            styled_caption("Drought flagged at any date. Crop loss is valued at 2022–23 MSPs; Jalna 2023 is imputed "
                           "because 2023 district yields are not yet published.")
    else:
        st.info("The cost comparison appears here once `trigger_cost_analysis.py` has been run.")

    e1, e2 = st.columns(2)
    with e1:
        st.warning("""
        **Choosing the rule is a value choice.** Trigger-1 OR NDVI is the cheapest rule for w of about 1.2–7.9
        (2.3–7.7 if only flags by 30 September count). Below that, SIF at z < −3 or the per-pixel rainfall trigger
        on its own is cheapest; above it, a looser NDVI threshold. Which is right depends on how much a missed
        drought should weigh, not on the data.
        """)
    with e2:
        st.info("""
        **The threshold matters more than the index.** Moving NDVI from z < −3 to z < −2 cuts relief withheld
        from ₹889 crore to nothing and raises relief paid in normal years from ₹2,336 to ₹6,492 crore.
        Swapping NDVI for SIF at z < −3 moves them by ₹706 and ₹1,268 crore.
        """)
    styled_caption("Relief is an upper bound: it goes only to farmers with a verified loss of 33% or more, up to 2 ha each. "
                   "PMFBY payouts and the cost of field verification are not included.")

# ---------------------------------------------------------------- 3. comparison
with t3:
    st.subheader("Same satellite signal, different powers")
    st.markdown("""
    What a satellite index is allowed to decide sets who carries a missed drought. I compared India's
    design with four systems that use satellite vegetation or drought indices, one of them in an EU member state.

    | | Logic | What the signal decides | Who carries a missed drought |
    |---|---|---|---|
    | **India**: Manual for Drought Management | Rainfall gate → impact indicators (incl. VCI/NDVI) → field verification | State declaration and relief (SDRF/NDRF) | Farmers, until field verification catches up |
    | **EU**: Combined Drought Indicator | Watch (rainfall) → Warning (+ soil moisture) → Alert (+ fAPAR), 5 km grid | Early warning only | No payment at stake |
    | **Spain**: river-basin drought plans | Index thresholds move each unit from normal to pre-alert, alert and emergency | Water measures; less demanding ecological flows in a prolonged drought | Water users in the unit |
    | **Spain**: pasture-loss insurance | NDVI alone, per pasture zone and ten-day period; pays below the mean − 0.7 SD (standard option) | Payouts to livestock farmers (premiums subsidised by ENESA) | Farmers whose pasture loss the zone index does not see |
    | **USA**: Drought Monitor + Livestock Forage Disaster Program | Weekly county ratings; 8 consecutive weeks at D2 = one monthly payment, up to five | Payments to livestock producers | Producers in counties rated below the threshold |
    | **Kenya**: Livestock Insurance Program | NDVI-based forage index alone | Insurance payouts to pastoralists | Herders whose loss the index does not see |
    """)
    styled_caption("Sources: Manual for Drought Management (2016); Sepulcre-Canto et al. (2012) and Copernicus EDO; "
                   "Confederación Hidrográfica del Júcar (2017); MAPA/ENESA (2020); USDA Farm Service Agency; WOCAT. "
                   "Published designs, not measured performance.")
    s1, s2 = st.columns(2)
    with s1:
        st.info("""
        **Spain sets a much looser threshold.** Its pasture insurance starts paying at NDVI below its mean minus
        0.7 standard deviations, against z < −3 here. In Marathwada, NDVI at z < −1.5 flagged all 15 drought
        district-years but also 24 of 57 normal ones: never the cheapest rule when a flag at any date counts,
        and only at w of about 7.7 or more when only flags by 30 September count. (The baselines differ: mine
        uses only normal years and needs two composites in a row.)
        """)
    with s2:
        st.info("""
        **India's satellite data is information, not authority.** In Hood's (1983) tools of government, India's
        drought response uses all four: nodality (satellite and rainfall monitoring), authority (the trigger
        rules and the notification), treasure (SDRF/NDRF relief, PMFBY payouts) and organisation (drought cells,
        field verification). The satellite signals enter only through nodality; in the U.S., Kenyan and Spanish
        insurance schemes the index itself decides who is paid.
        """)

# ---------------------------------------------------------------- 4. Hall
with t4:
    st.subheader("What kind of change would each proposal be?")
    st.markdown("""
    Hall (1993) separates changes to the **settings** of an instrument, to the **instruments** themselves, and
    to the **goals** behind them. The proposals around this study fall into all three, and the evidence speaks
    to each differently.
    """)
    _card = (
        "<div style='height:100%; padding:16px 18px; border:1px solid rgba(0,217,192,0.35); border-top:4px solid {c};"
        " border-radius:10px; background:rgba(255,255,255,0.03);'>"
        "<p style='color:{c}; text-transform:uppercase; letter-spacing:1.2px; font-weight:700; font-size:0.8rem; margin:0 0 6px 0;'>{t}</p>"
        "<p style='color:" + TEXT_LIGHT + "; margin:0 0 10px 0;'>{w}</p>"
        "<p style='color:" + TEXT_LIGHT + "; margin:0;'><b>{e}</b></p></div>"
    )
    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown(_card.format(c=TEAL, t="First order: settings",
                                 w="Alarm threshold (z < −3 or −2), dry-spell length (three or four weeks) and the weeks it is counted from, district average or per pixel.",
                                 e="Settings move the results most: three dry weeks instead of four take the rainfall trigger from 7 to 14 droughts and from 1 to 26 false alarms."),
                    unsafe_allow_html=True)
    with h2:
        st.markdown(_card.format(c=TEAL, t="Second order: instruments",
                                 w="Adding SIF; letting the vegetation index raise a flag on its own (an OR rule) instead of only confirming rainfall.",
                                 e="No case for SIF as an earlier warning. Trigger-1 OR NDVI flagged 14 of 15 with no extra false alarms, the cheapest rule over most weights."),
                    unsafe_allow_html=True)
    with h3:
        st.markdown(_card.format(c=MAGENTA, t="Third order: goals",
                                 w="Letting a satellite index pay out without field verification, as Kenya's and Spain's livestock insurance do: from compensating verified loss to paying fast against an index.",
                                 e="The study can say how often an index would have been right and what its errors cost. The choice of goal is political."),
                    unsafe_allow_html=True)
    styled_caption("In Hall's account a change of goals does not follow from technical evidence alone; it comes out of a contest over the goals themselves.")

section_divider()

st.success("""
**Bottom line for trigger design.** In Marathwada, the Manual's rainfall trigger was early and precise but missed
about half of the rainfall-defined drought district-years, and NDVI caught most of those. Letting the vegetation
index raise a flag on its own, not only confirm rainfall, caught 14 of 15 at no extra false alarms. Beyond that,
the settings, the dry-spell length and the alarm threshold, not the choice between NDVI and SIF, decide who
carries the errors, and setting them is a value choice that belongs in the open.
""")

styled_caption("GREEN ALIBI — Policy Design Lab · Paper, Appendix A · Scripts: trigger_rule_comparison.py, trigger_cost_analysis.py")
