import os

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import FuncFormatter


# ============================================================
# GREEN ALIBI — FIGURE 3: STUDY AREA MAP
# ============================================================

BOUNDARY_PATH = "data/raw/marathwada_districts_separate.geojson"

OUTPUT_DIR = "outputs/figures"

OUTPUT_PNG = os.path.join(
    OUTPUT_DIR,
    "figure3_study_area_map.png"
)

OUTPUT_PDF = os.path.join(
    OUTPUT_DIR,
    "figure3_study_area_map.pdf"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD ACTUAL STUDY-AREA BOUNDARIES
# ============================================================

districts = gpd.read_file(BOUNDARY_PATH)

if districts.empty:
    raise ValueError("Study-area boundary file is empty.")

if "ADM2_NAME" not in districts.columns:
    raise ValueError(
        "Expected district-name column 'ADM2_NAME' was not found."
    )


# ============================================================
# CRS
# ============================================================

if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")

# Convert to UTM Zone 43N.
# Marathwada lies within UTM Zone 43N.
# This projected CRS uses metres, which allows an accurate
# 50-km scale bar.
map_gdf = districts.to_crs("EPSG:32643")


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(7.2, 7.2),
    dpi=300
)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.set_aspect("equal")


# ============================================================
# STUDY-AREA POLYGONS
# ============================================================

map_gdf.plot(
    ax=ax,
    facecolor="#DDF4F1",
    edgecolor="#1B8F89",
    linewidth=1.4
)


# ============================================================
# DISTRICT LABELS
# ============================================================

for _, row in map_gdf.iterrows():

    # representative_point() guarantees the label point
    # remains inside the district polygon.
    point = row.geometry.representative_point()

    ax.text(
        point.x,
        point.y,
        str(row["ADM2_NAME"]),
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#202124"
    )


# ============================================================
# STUDY-AREA OUTER BOUNDARY
# ============================================================

study_boundary = map_gdf.dissolve()

study_boundary.boundary.plot(
    ax=ax,
    color="#202124",
    linewidth=2.0
)


# ============================================================
# MAP EXTENT
# ============================================================

xmin, ymin, xmax, ymax = map_gdf.total_bounds

x_range = xmax - xmin
y_range = ymax - ymin


# ============================================================
# NORTH ARROW
# ============================================================

arrow_x = xmax - 0.10 * x_range
arrow_y = ymax - 0.13 * y_range

arrow_length = 0.10 * y_range

arrow = FancyArrowPatch(
    (arrow_x, arrow_y),
    (arrow_x, arrow_y + arrow_length),
    arrowstyle="-|>",
    mutation_scale=20,
    linewidth=1.8,
    color="#202124"
)

ax.add_patch(arrow)

ax.text(
    arrow_x,
    arrow_y + arrow_length + 0.02 * y_range,
    "N",
    ha="center",
    va="bottom",
    fontsize=12,
    fontweight="bold",
    color="#202124"
)


# ============================================================
# SCALE BAR — 50 KM
# ============================================================

scale_length = 50_000  # 50 km in metres

bar_x = xmin + 0.08 * x_range
bar_y = ymin + 0.07 * y_range

# Main scale-bar line
ax.plot(
    [bar_x, bar_x + scale_length],
    [bar_y, bar_y],
    color="#202124",
    linewidth=4,
    solid_capstyle="butt"
)

# Left marker
ax.plot(
    [bar_x, bar_x],
    [
        bar_y - 0.012 * y_range,
        bar_y + 0.012 * y_range
    ],
    color="#202124",
    linewidth=2
)

# Right marker
ax.plot(
    [bar_x + scale_length, bar_x + scale_length],
    [
        bar_y - 0.012 * y_range,
        bar_y + 0.012 * y_range
    ],
    color="#202124",
    linewidth=2
)

ax.text(
    bar_x + scale_length / 2,
    bar_y + 0.025 * y_range,
    "50 km",
    ha="center",
    va="bottom",
    fontsize=9,
    fontweight="bold",
    color="#202124"
)


# ============================================================
# TITLE
# ============================================================

ax.set_title(
    "Study Area: Marathwada, Maharashtra, India",
    fontsize=16,
    fontweight="bold",
    color="#202124",
    pad=14
)


# ============================================================
# AXES
# ============================================================

# Because the map is plotted in EPSG:32643, the raw coordinates
# are metres. Display them as kilometres for readability.

ax.set_xlabel(
    "Easting (km)",
    fontsize=10,
    color="#444444"
)

ax.set_ylabel(
    "Northing (km)",
    fontsize=10,
    color="#444444"
)


def metres_to_km(value, position):
    return f"{value / 1000:.0f}"


ax.xaxis.set_major_formatter(
    FuncFormatter(metres_to_km)
)

ax.yaxis.set_major_formatter(
    FuncFormatter(metres_to_km)
)

ax.tick_params(
    labelsize=9,
    colors="#555555"
)


# ============================================================
# CLEAN FRAME
# ============================================================

for spine in ax.spines.values():
    spine.set_linewidth(0.8)
    spine.set_edgecolor("#BBBBBB")


# ============================================================
# EXPORT
# ============================================================

plt.savefig(
    OUTPUT_PNG,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.savefig(
    OUTPUT_PDF,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()