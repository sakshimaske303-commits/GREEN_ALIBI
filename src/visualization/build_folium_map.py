import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

YEARS = [2015, 2018, 2020]
DISTRICTS_PATH = "data/raw/marathwada_districts_separate.geojson"
SIF_CSV = "data/processed/sif_by_district.csv"
OUTPUT_HTML = "outputs/interactive_maps/maps/marathwada_sif_by_district.html"

# --- Load districts + SIF data ---
districts = gpd.read_file(DISTRICTS_PATH)
if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")
elif districts.crs.to_epsg() != 4326:
    districts = districts.to_crs("EPSG:4326")

sif_df = pd.read_csv(SIF_CSV)
sif_wide = sif_df.pivot(index="district", columns="year", values="mean_sif").reset_index()
sif_wide.columns = ["ADM2_NAME"] + [f"sif_{y}" for y in sif_wide.columns[1:]]

for y in YEARS:
    sif_wide[f"sif_{y}"] = sif_wide[f"sif_{y}"].round(3)

merged = districts.merge(sif_wide, on="ADM2_NAME", how="left")

# --- Shared color scale across all years, so the three layers are comparable ---
all_values = pd.concat([merged[f"sif_{y}"] for y in YEARS])
vmin, vmax = all_values.min(), all_values.max()

colormap = cm.LinearColormap(
    colors=["#a50026", "#f46d43", "#fee08b", "#66bd63", "#1a9850"],
    vmin=vmin, vmax=vmax,
    caption="Mean SIF (DOY 273)"
)

# --- Build the map ---
center = [merged.geometry.unary_union.centroid.y, merged.geometry.unary_union.centroid.x]
m = folium.Map(location=center, zoom_start=8, tiles="CartoDB positron")

def make_style_function(col):
    def style_function(feature):
        value = feature["properties"].get(col)
        return {
            "fillColor": colormap(value) if value is not None else "#808080",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.75,
        }
    return style_function

for year in YEARS:
    col = f"sif_{year}"
    layer = folium.GeoJson(
        merged.to_json(),
        name=f"SIF — {year}",
        style_function=make_style_function(col),
        tooltip=folium.GeoJsonTooltip(
            fields=["ADM2_NAME", col],
            aliases=["District:", "Mean SIF:"],
            localize=False
        ),
        popup=folium.GeoJsonPopup(
            fields=["ADM2_NAME", col],
            aliases=["District:", f"Mean SIF ({year}):"],
            localize=False
        ),
        show=(year == YEARS[-1])  # only 2020 visible by default; others toggle-able
    )
    layer.add_to(m)

colormap.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

m.save(OUTPUT_HTML)
print(f"Interactive map saved to {OUTPUT_HTML}")