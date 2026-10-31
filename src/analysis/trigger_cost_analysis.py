# what the errors of each trigger rule cost, in rupees (policy extension)
# a missed drought leaves the crop loss with farmers; a false alarm pays relief where there was no drought

import numpy as np
import pandas as pd

GOV_TO_GA_DISTRICT = {
    "Chhatrapati Sambhajinagar": "Aurangabad", "Dharashiv": "Osmanabad", "Beed": "Bid", "Jalna": "Jalna",
    "Parbhani": "Parbhani", "Hingoli": "Hingoli", "Nanded": "Nanded", "Latur": "Latur",
}
# Minimum Support Prices, Kharif marketing season 2022-23, Rs per quintal (DES MSP statement)
MSP_2022 = {
    "Soyabean": 4300, "Cotton(Lint)": 6080, "Arhar/Tur": 6600, "Jowar": 2970, "Bajra": 2350,
    "Moong(Green Gram)": 7755, "Maize": 1962, "Urad": 6600, "Groundnut": 5850,
}
# cotton is reported in bales of 170 kg lint; at a ginning outturn of about 34%, one bale is about
# 5 quintals of seed cotton (kapas), the form the MSP is set for
COTTON_KAPAS_QTL_PER_BALE = 5.0
# SDRF/NDRF input subsidy, rainfed areas, crop loss of 33% or more (norms for 2022-23 to 2025-26)
SDRF_RS_PER_HA = 8500
IN_SEASON_DOY = 273  # 30 Sep
THRESHOLDS = ["-1.5", "-2.0", "-3.0"]
W_GRID = [0.5, 1, 2, 3, 5]

# ---------------------------------------------------------------- crop loss per drought district-year
apy = pd.read_csv("data/external/extracted/crop-wise-area-production-yield.csv", low_memory=False)
apy = apy[(apy["state_name"] == "Maharashtra") & (apy["district_name"].isin(GOV_TO_GA_DISTRICT))
          & (apy["season"] == "Kharif")].copy()
apy["district"] = apy["district_name"].map(GOV_TO_GA_DISTRICT)
apy["year"] = apy["year"].str[:4].astype(int)
apy = apy[apy["year"].between(2015, 2022)]

sd = pd.read_csv("data/processed/drought_signal_district.csv")
apy = apy.merge(sd[["district", "year", "is_drought"]], on=["district", "year"], how="left")

priced = apy[apy["crop_name"].isin(MSP_2022)].copy()
share = priced["area"].sum() / apy["area"].sum()
# expected yield: the district-crop mean over that district's normal (non-drought) years, 2015-2022
base = priced[~priced["is_drought"]].groupby(["district", "crop_name"])["yield"].mean().rename("yield_normal")
priced = priced.join(base, on=["district", "crop_name"])
qtl_per_unit = np.where(priced["crop_name"] == "Cotton(Lint)", COTTON_KAPAS_QTL_PER_BALE, 10.0)  # tonne = 10 qtl
priced["loss_rs"] = (priced["yield_normal"] - priced["yield"]) * priced["area"] * qtl_per_unit \
    * priced["crop_name"].map(MSP_2022)

loss = priced.groupby(["district", "year"])["loss_rs"].sum().clip(lower=0).rename("crop_loss_rs").reset_index()
area = apy.groupby("district")["area"].sum() / apy["year"].nunique()  # mean Kharif sown area, 2015-2022
area = area.rename("kharif_area_ha").reset_index()

dy = sd[["district", "year", "is_drought"]].merge(loss, on=["district", "year"], how="left").merge(area, on="district")
dy["loss_imputed"] = dy["is_drought"] & dy["crop_loss_rs"].isna()
# 2023 has no published district yields: value a 2023 drought at the mean loss per hectare of 2015-2022 droughts
per_ha = (dy.loc[dy["is_drought"] & ~dy["loss_imputed"], "crop_loss_rs"].sum()
          / dy.loc[dy["is_drought"] & ~dy["loss_imputed"], "kharif_area_ha"].sum())
dy.loc[dy["loss_imputed"], "crop_loss_rs"] = per_ha * dy.loc[dy["loss_imputed"], "kharif_area_ha"]
dy["relief_rs"] = SDRF_RS_PER_HA * dy["kharif_area_ha"]

print(f"Crops priced: {share:.1%} of Kharif sown area, 2015-2022")
print("\nCrop loss in drought district-years (Rs crore, at 2022-23 MSP):")
for r in dy[dy["is_drought"]].itertuples():
    print(f"  {r.district:11s}{r.year}  {r.crop_loss_rs / 1e7:8.0f}{'  (imputed, no 2023 yields)' if r.loss_imputed else ''}")
print(f"Relief per false alarm (Rs {SDRF_RS_PER_HA}/ha on mean Kharif area): "
      f"{dy['relief_rs'].min() / 1e7:.0f}-{dy['relief_rs'].max() / 1e7:.0f} crore by district")

# ---------------------------------------------------------------- the rules (as in trigger_rule_comparison.py)
T = pd.read_csv("data/processed/rainfall_trigger_dates.csv")
T = T[T["unit"] != "Marathwada"].rename(columns={"unit": "district"})
tr = T.pivot_table(index=["district", "year"], columns="variant", values="trigger_doy", aggfunc="first").reset_index()
tr = tr[["district", "year", "main: deficit>25% & spell>=21d", "deficit>25% only"]].rename(
    columns={"main: deficit>25% & spell>=21d": "T1", "deficit>25% only": "D"})
px = pd.read_csv("data/processed/rainfall_trigger_pixel_by_district.csv")[["district", "year", "doy_25pct_triggered"]]
px = px.rename(columns={"doy_25pct_triggered": "T1px"})
cols = {f"{s}_alarm_{t}": f"{s[0]}{t}" for s in ["SIF", "NDVI"] for t in THRESHOLDS}
d = sd[["district", "year"] + list(cols)].rename(columns=cols).merge(tr, on=["district", "year"], how="left") \
    .merge(px, on=["district", "year"], how="left").merge(dy, on=["district", "year"])
assert len(d) == 72 and d["is_drought"].sum() == 15


def all_of(*c):
    return d[list(c)].max(axis=1, skipna=False)


def any_of(*c):
    return d[list(c)].min(axis=1)


def k_of(k, *c):
    return pd.Series(np.sort(d[list(c)].to_numpy(dtype=float), axis=1)[:, k - 1], index=d.index)


rules = {
    "Rainfall Trigger-1 (district average)": ("Rainfall", d["T1"]),
    "Rainfall Trigger-1 (25% of pixels)": ("Rainfall", d["T1px"]),
    "Rainfall deficit > 25% alone": ("Rainfall", d["D"]),
}
for t in THRESHOLDS:
    rules[f"NDVI anomaly (z < {t})"] = ("Single satellite", d[f"N{t}"])
    rules[f"SIF anomaly (z < {t})"] = ("Single satellite", d[f"S{t}"])
    rules[f"NDVI AND SIF (z < {t})"] = ("Combined", all_of(f"N{t}", f"S{t}"))
rules.update({
    "Deficit AND NDVI (z < -3.0)": ("Combined", all_of("D", "N-3.0")),
    "Deficit AND SIF (z < -3.0)": ("Combined", all_of("D", "S-3.0")),
    "Deficit, then NDVI confirms (z < -3.0)": ("Combined", d["N-3.0"].where(d["N-3.0"] >= d["D"]).where(d["D"].notna())),
    "NDVI OR SIF (z < -3.0)": ("Combined", any_of("N-3.0", "S-3.0")),
    "Trigger-1 OR NDVI (z < -3.0)": ("Combined", any_of("T1", "N-3.0")),
    "2 of 3: deficit, NDVI, SIF (z < -3.0)": ("Combined", k_of(2, "D", "N-3.0", "S-3.0")),
})

dr, nm = d["is_drought"].astype(bool), ~d["is_drought"].astype(bool)
total_loss, total_relief = d.loc[dr, "crop_loss_rs"].sum(), d.loc[dr, "relief_rs"].sum()
rows = []
for timing in ["any date", "by 30 September"]:
    for name, (fam, s) in rules.items():
        fired = s.notna() if timing == "any date" else s.notna() & (s <= IN_SEASON_DOY)
        missed, fa = dr & ~fired, nm & s.notna()  # a false alarm pays relief whenever it fires
        rows.append({
            "timing": timing, "rule": name, "family": fam,
            "drought_flagged": int((dr & fired).sum()), "false_alarms": int(fa.sum()),
            "relief_withheld_in_missed_droughts_cr": d.loc[missed, "relief_rs"].sum() / 1e7,
            "relief_paid_in_normal_years_cr": d.loc[fa, "relief_rs"].sum() / 1e7,
            "crop_loss_in_missed_droughts_cr": d.loc[missed, "crop_loss_rs"].sum() / 1e7,
            "share_of_drought_crop_loss_missed": d.loc[missed, "crop_loss_rs"].sum() / total_loss,
        })
R = pd.DataFrame(rows)
for w in W_GRID:
    R[f"weighted_cost_w{w:g}_cr"] = w * R["relief_withheld_in_missed_droughts_cr"] + R["relief_paid_in_normal_years_cr"]

print(f"\nDrought district-years: crop loss Rs {total_loss / 1e7:,.0f} crore; relief at the SDRF rate "
      f"Rs {total_relief / 1e7:,.0f} crore ({total_relief / total_loss:.0%} of the loss)")
for timing, g in R.groupby("timing", sort=False):
    print(f"\nFlagged at {timing} (Rs crore):")
    print(f"{'rule':42s}{'hit':>4s}{'FA':>4s}{'withheld':>10s}{'paid, normal':>14s}{'crop loss missed':>18s}")
    for r in g.itertuples():
        print(f"{r.rule:42s}{r.drought_flagged:>4d}{r.false_alarms:>4d}{r.relief_withheld_in_missed_droughts_cr:>10,.0f}"
              f"{r.relief_paid_in_normal_years_cr:>14,.0f}{r.crop_loss_in_missed_droughts_cr:>18,.0f}")
    for w in W_GRID:
        b = g.loc[g[f"weighted_cost_w{w:g}_cr"].idxmin()]
        print(f"  lowest cost at w = {w:g}: {b['rule']} ({b[f'weighted_cost_w{w:g}_cr']:,.0f} cr)")

# which rule has the lowest weighted cost as w rises: the lower envelope over w
switch = []
for timing, g in R.groupby("timing", sort=False):
    ws = np.round(np.arange(0.05, 10.0001, 0.01), 2)
    cost = np.outer(ws, g["relief_withheld_in_missed_droughts_cr"]) + g["relief_paid_in_normal_years_cr"].to_numpy()
    best = g["rule"].to_numpy()[cost.argmin(axis=1)]
    start = 0
    for i in range(1, len(ws) + 1):
        if i == len(ws) or best[i] != best[start]:
            switch.append({"timing": timing, "rule": best[start], "w_from": ws[start], "w_to": ws[i - 1]})
            start = i
S = pd.DataFrame(switch)
print("\nLowest-cost rule as the weight w rises (w from 0.05 to 10):")
for r in S.itertuples():
    print(f"  {r.timing:17s} w {r.w_from:5.2f}-{r.w_to:5.2f}: {r.rule}")
S.to_csv("data/processed/trigger_cost_switch_points.csv", index=False)

R.to_csv("data/processed/trigger_cost_comparison.csv", index=False)
dy.to_csv("data/processed/trigger_cost_district_years.csv", index=False)
print("\nSaved trigger_cost_comparison.csv, trigger_cost_district_years.csv, trigger_cost_switch_points.csv")
print("w = weight on one rupee of relief withheld from a drought-hit district, relative to one rupee paid in a normal year.")
