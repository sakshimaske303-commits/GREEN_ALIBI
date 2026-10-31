# relief withheld in missed droughts vs relief paid in normal years, per trigger rule (policy extension)

import matplotlib.pyplot as plt
import pandas as pd

R = pd.read_csv("data/processed/trigger_cost_comparison.csv")
S = pd.read_csv("data/processed/trigger_cost_switch_points.csv")
OUTPUT_PNG = "outputs/figures/trigger_cost_frontier.png"
colors = {"Rainfall": "#2166ac", "Single satellite": "#2FA88C", "Combined": "#D9822B"}
labels = {"Rainfall": "Rainfall rule", "Single satellite": "Single satellite anomaly", "Combined": "Combined rule"}

OFFSETS = {"SIF anomaly (z < -3.0)": (10, 8), "Deficit AND SIF (z < -3.0)": (8, 10), "NDVI anomaly (z < -1.5)": (10, -18)}
fig, axes = plt.subplots(1, 2, figsize=(14, 6.4), sharey=True)
for ax, timing, title in [(axes[0], "any date", "Drought counted as flagged at any date"),
                          (axes[1], "by 30 September", "Drought counted as flagged only by 30 September")]:
    g = R[R["timing"] == timing].drop_duplicates(["relief_withheld_in_missed_droughts_cr", "relief_paid_in_normal_years_cr", "family"])
    for fam, z in [("Rainfall", 3), ("Combined", 3), ("Single satellite", 4)]:  # single anomalies drawn on top of ties
        h = g[g["family"] == fam]
        ax.scatter(h["relief_withheld_in_missed_droughts_cr"], h["relief_paid_in_normal_years_cr"], s=55, color=colors[fam],
                   edgecolor="black", linewidth=0.6, zorder=z, label=labels[fam])
    env = S[S["timing"] == timing]
    pts = R[(R["timing"] == timing) & R["rule"].isin(env["rule"])].set_index("rule").loc[env["rule"]]
    ax.plot(pts["relief_withheld_in_missed_droughts_cr"], pts["relief_paid_in_normal_years_cr"], color="#555555",
            lw=1, ls="--", zorder=2)
    for r in env.itertuples():
        p = pts.loc[r.rule]
        txt = f"{r.rule}\nlowest cost for w {r.w_from:.1f}–{r.w_to:.1f}" if r.w_to < 10 else f"{r.rule}\nlowest cost for w ≥ {r.w_from:.1f}"
        ax.annotate(txt, (p["relief_withheld_in_missed_droughts_cr"], p["relief_paid_in_normal_years_cr"]),
                    xytext=OFFSETS.get(r.rule, (8, 6)), textcoords="offset points", fontsize=7.5, color="#333333")
    for name in ["Rainfall Trigger-1 (district average)", "Rainfall deficit > 25% alone"]:
        p = g[g["rule"] == name]
        if len(p) and name not in set(env["rule"]):
            ax.annotate(name, (p["relief_withheld_in_missed_droughts_cr"].iloc[0], p["relief_paid_in_normal_years_cr"].iloc[0]),
                        xytext=(6, -12), textcoords="offset points", fontsize=7.5, color="#333333")
    ax.set_title(title, fontsize=11, loc="left")
    ax.set_xlabel("Relief withheld in missed drought district-years (Rs crore)")
    ax.grid(alpha=0.25)
    ax.set_xlim(-300, 8500)
    ax.set_ylim(-500, 13800)
axes[0].set_ylabel("Relief paid in normal district-years (Rs crore)")
axes[0].legend(loc="center right", fontsize=8.5, frameon=False)
fig.suptitle("The cost of each trigger's errors, Marathwada 2015–2023 (relief at the SDRF rainfed rate of Rs 8,500/ha). "
             "Lower left is better;\nthe dashed line joins the rules with the lowest weighted cost w × withheld + paid, "
             "where w is the weight on a rupee withheld from a drought-hit district", fontsize=10.5, y=1.02)
fig.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved to {OUTPUT_PNG}")
plt.close(fig)
