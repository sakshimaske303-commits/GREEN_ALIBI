# study area map (Fig 3)

import os

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import FuncFormatter


BOUNDARY_PATH = "data/raw/marathwada_districts_separate.geojson"
# India state outlines for the locator inset (FAO GAUL 2015 level 1), exported by
# src/acquisition/gee_india_states_for_locator.py; the inset is skipped if the file is absent
STATES_PATH = "data/external/india_states_gaul_l1.geojson"

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


districts = gpd.read_file(BOUNDARY_PATH)

if districts.empty:
    raise ValueError("Study-area boundary file is empty.")

if "ADM2_NAME" not in districts.columns:
    raise ValueError(
        "Expected district-name column 'ADM2_NAME' was not found."
    )


if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")

map_gdf = districts.to_crs("EPSG:32643")


fig, ax = plt.subplots(
    figsize=(7.2, 7.2),
    dpi=300
)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.set_aspect("equal")


map_gdf.plot(
    ax=ax,
    facecolor="#DDF4F1",
    edgecolor="#1B8F89",
    linewidth=1.4
)


for _, row in map_gdf.iterrows():

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


study_boundary = map_gdf.dissolve()

study_boundary.boundary.plot(
    ax=ax,
    color="#202124",
    linewidth=2.0
)


xmin, ymin, xmax, ymax = map_gdf.total_bounds

x_range = xmax - xmin
y_range = ymax - ymin


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


scale_length = 50_000

bar_x = xmin + 0.08 * x_range
bar_y = ymin + 0.07 * y_range

ax.plot(
    [bar_x, bar_x + scale_length],
    [bar_y, bar_y],
    color="#202124",
    linewidth=4,
    solid_capstyle="butt"
)

ax.plot(
    [bar_x, bar_x],
    [
        bar_y - 0.012 * y_range,
        bar_y + 0.012 * y_range
    ],
    color="#202124",
    linewidth=2
)

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


ax.set_title(
    "Study Area: Marathwada, Maharashtra, India",
    fontsize=16,
    fontweight="bold",
    color="#202124",
    pad=14
)


ax.set_xlabel(
    "Easting (km), UTM zone 43N (EPSG:32643)",
    fontsize=10,
    color="#444444"
)

ax.set_ylabel(
    "Northing (km), UTM zone 43N",
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


for spine in ax.spines.values():
    spine.set_linewidth(0.8)
    spine.set_edgecolor("#BBBBBB")


if os.path.exists(STATES_PATH):
    try:
        states = gpd.read_file(STATES_PATH)
        states = states.set_crs("EPSG:4326") if states.crs is None else states.to_crs("EPSG:4326")
        name_col = "ADM1_NAME" if "ADM1_NAME" in states.columns else states.columns[0]
        inset = ax.inset_axes([0.70, 0.02, 0.28, 0.28])  # empty lower-right corner
        states.plot(ax=inset, facecolor="#F2F2F2", edgecolor="#9E9E9E", linewidth=0.25)
        states[states[name_col].astype(str).str.contains("Maharashtra")].plot(
            ax=inset, facecolor="#BFE6E2", edgecolor="#1B8F89", linewidth=0.5)
        districts.to_crs("EPSG:4326").dissolve().plot(ax=inset, facecolor="#1B8F89", edgecolor="none")
        inset.set_xticks([])
        inset.set_yticks([])
        inset.set_aspect("equal")
        for spine in inset.spines.values():
            spine.set_edgecolor("#888888")
        inset.set_title("India / Maharashtra", fontsize=7, pad=2)
    except Exception as e:  # the locator is decorative: never let it stop the pipeline
        print(f"Locator inset skipped: {e}")
else:
    print(f"Locator inset skipped: {STATES_PATH} not found (run src/acquisition/gee_india_states_for_locator.py)")


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
