import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D


# ============================================================
# GREEN ALIBI — GRAPHICAL ABSTRACT
# ============================================================

fig = plt.figure(figsize=(16, 7), dpi=300)

ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 16)
ax.set_ylim(0, 7)
ax.axis("off")


# ============================================================
# COLOURS
# ============================================================

TEAL = "#18BDB3"
PINK = "#D82C91"
DARK = "#202124"
GREY = "#666666"
LIGHT = "#F5FBFA"
BORDER = "#D0D0D0"
WHITE = "#FFFFFF"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def draw_box(x, y, width, height, title, body,
             title_size=14, body_size=10.5):

    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        linewidth=1.7,
        edgecolor=TEAL,
        facecolor=LIGHT
    )

    ax.add_patch(patch)

    ax.text(
        x + width / 2,
        y + height - 0.36,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=DARK
    )

    ax.text(
        x + width / 2,
        y + height / 2 - 0.08,
        body,
        ha="center",
        va="center",
        fontsize=body_size,
        color=DARK,
        linespacing=1.35
    )


def draw_arrow(x1, y1, x2, y2):

    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=2,
        color=GREY
    )

    ax.add_patch(arrow)


# ============================================================
# TITLE
# ============================================================

ax.text(
    8,
    6.55,
    "GREEN ALIBI: Does Fluorescence Catch Drought Stress Before NDVI?",
    ha="center",
    va="center",
    fontsize=22,
    fontweight="bold",
    color=DARK
)

ax.text(
    8,
    6.08,
    "Marathwada, Maharashtra, India  |  8 districts  |  "
    "8 growing seasons (2015–2023, excluding 2021)",
    ha="center",
    va="center",
    fontsize=12.5,
    fontweight="bold",
    color=GREY
)


# ============================================================
# STUDY → DATA → ANALYSIS → SPATIAL → POLICY
# ============================================================

draw_box(
    0.45, 4.15, 2.65, 1.35,
    "STUDY",
    "Agricultural drought stress\nacross 8 districts"
)

draw_box(
    3.55, 4.15, 2.65, 1.35,
    "SATELLITE + RAINFALL",
    "GOSIF SIF  |  MODIS NDVI\nCHIRPS rainfall",
    title_size=13
)

draw_box(
    6.65, 4.15, 2.65, 1.35,
    "ANALYSIS",
    "Threshold crossing\nCross-correlation\nBootstrap uncertainty"
)

draw_box(
    9.75, 4.15, 2.65, 1.35,
    "SPATIAL CHECK",
    "District patterns\nMoran's I\nRainfall correspondence"
)

draw_box(
    12.85, 4.15, 2.70, 1.35,
    "POLICY CHECK",
    "2018 satellite signals\nvs official declaration",
    title_size=13
)


# Arrows
draw_arrow(3.10, 4.82, 3.45, 4.82)
draw_arrow(6.20, 4.82, 6.55, 4.82)
draw_arrow(9.30, 4.82, 9.65, 4.82)
draw_arrow(12.40, 4.82, 12.75, 4.82)


# ============================================================
# KEY RESULTS PANEL
# ============================================================

panel = FancyBboxPatch(
    (0.45, 1.25),
    15.10,
    2.35,
    boxstyle="round,pad=0.04,rounding_size=0.10",
    linewidth=1.4,
    edgecolor=BORDER,
    facecolor=WHITE
)

ax.add_patch(panel)

ax.text(
    8,
    3.30,
    "KEY RESULTS",
    ha="center",
    va="center",
    fontsize=15,
    fontweight="bold",
    color=DARK
)


# ============================================================
# RESULT 1
# ============================================================

draw_box(
    0.75,
    1.50,
    3.25,
    1.40,
    "7 / 8 YEARS",
    "SIF decline led NDVI decline\n"
    "under threshold-crossing",
    title_size=17,
    body_size=10.5
)


# ============================================================
# RESULT 2
# ============================================================

draw_box(
    4.35,
    1.50,
    3.25,
    1.40,
    "METHOD-DEPENDENT",
    "Cross-correlation:\n"
    "4 SIF-leading  |  1 tie  |  3 NDVI-leading",
    title_size=13.5,
    body_size=9.5
)


# ============================================================
# RESULT 3
# ============================================================

draw_box(
    7.95,
    1.50,
    3.25,
    1.40,
    "DROUGHT-SEVERITY HYPOTHESIS",
    "7.6 vs 15.0 days\n"
    "Drought years did not show a larger lag\n"
    "H3 not supported",
    title_size=11.5,
    body_size=9.5
)


# ============================================================
# RESULT 4 — 2018 TIMELINE
# ============================================================

timeline_box = FancyBboxPatch(
    (11.55, 1.50),
    3.55,
    1.40,
    boxstyle="round,pad=0.03,rounding_size=0.08",
    linewidth=1.7,
    edgecolor=TEAL,
    facecolor=LIGHT
)

ax.add_patch(timeline_box)

ax.text(
    13.325,
    2.63,
    "2018 POLICY TIMELINE",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color=DARK
)

# Timeline
ax.add_line(
    Line2D(
        [11.95, 14.72],
        [1.98, 1.98],
        linewidth=2,
        color=GREY
    )
)

# NDVI marker
ax.add_patch(
    Circle(
        (12.25, 1.98),
        0.075,
        facecolor=PINK,
        edgecolor=WHITE,
        linewidth=1
    )
)

# SIF marker
ax.add_patch(
    Circle(
        (12.55, 1.98),
        0.075,
        facecolor=TEAL,
        edgecolor=WHITE,
        linewidth=1
    )
)

# Official declaration marker
ax.add_patch(
    Circle(
        (14.35, 1.98),
        0.075,
        facecolor=PINK,
        edgecolor=WHITE,
        linewidth=1
    )
)

ax.text(
    12.25,
    1.76,
    "NDVI\n4 Sep",
    ha="center",
    va="top",
    fontsize=7.5,
    color=DARK
)

ax.text(
    12.55,
    2.18,
    "SIF\n8 Sep",
    ha="center",
    va="bottom",
    fontsize=7.5,
    color=DARK
)

ax.text(
    14.35,
    1.76,
    "Official\n31 Oct",
    ha="center",
    va="top",
    fontsize=7.5,
    color=DARK
)

ax.text(
    13.45,
    2.42,
    "~7–8 weeks",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color=PINK
)


# ============================================================
# CONCLUSION
# ============================================================

ax.text(
    8,
    0.70,
    "CONCLUSION  •  SIF shows promise for earlier detection of "
    "agricultural stress, but its lead over NDVI is year- and "
    "method-dependent.",
    ha="center",
    va="center",
    fontsize=13.5,
    fontweight="bold",
    color=DARK
)


# ============================================================
# EXPORT
# ============================================================

plt.savefig(
    "GREEN_ALIBI_graphical_abstract.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.savefig(
    "GREEN_ALIBI_graphical_abstract.pdf",
    bbox_inches="tight",
    facecolor="white"
)

plt.savefig(
    "GREEN_ALIBI_graphical_abstract.svg",
    bbox_inches="tight",
    facecolor="white"
)

plt.show()