# combined drought-trigger rules: droughts flagged vs false alarms (policy extension)

import pandas as pd
import matplotlib.pyplot as plt

INPUT_CSV = "data/processed/trigger_rule_comparison.csv"
OUTPUT_PNG = "outputs/figures/trigger_rule_comparison.png"

df = pd.read_csv(INPUT_CSV)
df = df[df["setting"] == "2015-2023 (main)"].reset_index(drop=True)
n_d, n_n = int(df["drought_n"].iloc[0]), int(df["normal_n"].iloc[0])


def family(rule):
    if rule.startswith("Rainfall"):
        return "Rainfall rule"
    if rule.startswith(("NDVI anomaly", "SIF anomaly")):
        return "Single satellite anomaly"
    return "Combined rule"


colors = {"Rainfall rule": "#2166ac", "Single satellite anomaly": "#2FA88C", "Combined rule": "#D9822B"}
df["family"] = df["rule"].map(family)
y = list(range(len(df)))[::-1]

fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), sharey=True, gridspec_kw={"width_ratios": [1.25, 1]})

ax = axes[0]
ax.barh(y, df["drought_flagged"], color=[colors[f] for f in df["family"]], alpha=0.35, edgecolor="black", zorder=3,
        label="flagged at any date")
ax.barh(y, df["flagged_by_30_sep"], color=[colors[f] for f in df["family"]], edgecolor="black", zorder=4,
        label="flagged by 30 September")
for yy, a, b in zip(y, df["drought_flagged"], df["flagged_by_30_sep"]):
    ax.text(a + 0.2, yy, f"{a}/{n_d}  ({b} by 30 Sep)", va="center", fontsize=8.5)
ax.set_yticks(y)
ax.set_yticklabels(df["rule"], fontsize=9)
ax.set_xlim(0, n_d + 5)
ax.set_xlabel(f"Drought district-years flagged (of {n_d})")
ax.set_title("Droughts caught (misses stay with farmers)", fontsize=11, loc="left")
ax.grid(axis="x", alpha=0.25)
ax.legend([plt.Rectangle((0, 0), 1, 1, fc="#999999", alpha=0.35, ec="black"),
           plt.Rectangle((0, 0), 1, 1, fc="#999999", ec="black")],
          ["flagged at any date", "flagged by 30 September"], loc="upper right", fontsize=8, frameon=False)

ax2 = axes[1]
ax2.barh(y, df["false_alarms"], color=[colors[f] for f in df["family"]], edgecolor="black", zorder=3)
for yy, v in zip(y, df["false_alarms"]):
    ax2.text(v + 0.2, yy, f"{v}/{n_n}", va="center", fontsize=8.5)
ax2.set_xlim(0, max(df["false_alarms"]) + 3)
ax2.set_xlabel(f"False alarms in normal district-years (of {n_n})")
ax2.set_title("False alarms (paid by the public budget)", fontsize=11, loc="left")
ax2.grid(axis="x", alpha=0.25)

handles = [plt.Rectangle((0, 0), 1, 1, color=c, ec="black") for c in colors.values()]
fig.legend(handles, list(colors), loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.02))
fig.suptitle("Drought-trigger rules scored on 72 district-years, Marathwada 2015–2023 "
             "(satellite alarms at z < −3, own-district rainfall baseline)", fontsize=12, y=1.0)
fig.tight_layout(rect=(0, 0.04, 1, 0.97))
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved to {OUTPUT_PNG}")
plt.close(fig)
