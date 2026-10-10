# interactive rainfall map

import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
DISTRICTS_PATH = "data/raw/marathwada_districts_separate.geojson"
RAINFALL_CSV = "data/processed/rainfall_anomaly_by_district.csv"
OUTPUT_HTML = "outputs/interactive_maps/maps/marathwada_rainfall_by_district.html"

districts = gpd.read_file(DISTRICTS_PATH)
if districts.crs is None:
    districts = districts.set_crs("EPSG:4326")
elif districts.crs.to_epsg() != 4326:
    districts = districts.to_crs("EPSG:4326")

rain_df = pd.read_csv(RAINFALL_CSV)
rain_wide = rain_df.pivot(index="district", columns="year", values="anomaly_pct").reset_index()
rain_wide.columns = ["ADM2_NAME"] + [f"anomaly_{y}" for y in rain_wide.columns[1:]]

for y in YEARS:
    rain_wide[f"anomaly_{y}"] = rain_wide[f"anomaly_{y}"].round(1)

merged = districts.merge(rain_wide, on="ADM2_NAME", how="left")

all_values = pd.concat([merged[f"anomaly_{y}"] for y in YEARS])
# symmetric about zero so that 0% is the neutral colour
lim = max(abs(all_values.min()), abs(all_values.max()))
vmin, vmax = -lim, lim

colormap = cm.LinearColormap(
    colors=["#a50026", "#f46d43", "#fee08b", "#66bd63", "#1a9850"],
    vmin=vmin, vmax=vmax,
    caption="Rainfall anomaly (% departure from regional 20-yr normal)"
)

center = [merged.geometry.union_all().centroid.y, merged.geometry.union_all().centroid.x]
# Esri Light Gray basemap (the CARTO basemap started asking for an API key)
m = folium.Map(location=center, zoom_start=8, tiles=None)
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri — Esri, HERE, Garmin, &copy; OpenStreetMap contributors",
    name="Light basemap", max_native_zoom=16,
).add_to(m)

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
    col = f"anomaly_{year}"
    layer = folium.GeoJson(
        merged.to_json(),
        name=f"Rainfall anomaly — {year}",
        style_function=make_style_function(col),
        tooltip=folium.GeoJsonTooltip(
            fields=["ADM2_NAME", col],
            aliases=["District:", "Rainfall anomaly (%):"],
            localize=False
        ),
        popup=folium.GeoJsonPopup(
            fields=["ADM2_NAME", col],
            aliases=["District:", f"Rainfall anomaly ({year}, %):"],
            localize=False
        ),
        show=(year == YEARS[-1])
    )
    layer.add_to(m)

colormap.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

m.save(OUTPUT_HTML)
print(f"Interactive rainfall map saved to {OUTPUT_HTML}")
