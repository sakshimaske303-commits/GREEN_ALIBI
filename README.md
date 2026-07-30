# 🌿 GREEN ALIBI — Testing the Fluorescence Advantage

**Testing whether Solar-Induced Fluorescence catches agricultural drought stress in Marathwada, Maharashtra before NDVI can — and whether drought severity actually makes that head-start bigger.**

## 🔗 Live Dashboard

**[View the interactive dashboard →](PASTE_YOUR_STREAMLIT_LINK_HERE)**

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| 📘 [`Project_Journal.md`](./Project_Journal.md) | Polished project summary — methodology, findings, conclusions (start here) |
| 📗 [`Research_Paper.md`](./Research_Paper.md) | Formal academic paper — physical basis, methodology, results, discussion, limitations |
| 📙 [`Development_Log.md`](./Development_Log.md) | Full technical development log — every bug, boundary correction, and methodology iteration |

GREEN ALIBI is a geospatial framework testing whether Solar-Induced Fluorescence (SIF) — a satellite-derived proxy for photosynthetic activity — registers vegetation stress measurably earlier than the Normalized Difference Vegetation Index (NDVI), the reflectance-based indicator that currently underpins India's drought declaration and PMFBY crop-insurance payout process. Where NDVI only changes once a plant's internal structure has already begun to visibly degrade, SIF is grounded in the plant's photosynthetic energy-partitioning process itself, making it a physically earlier signal in principle. This project tests that premise directly, using GOSIF v2 fluorescence data and cloud-screened MODIS NDVI over Marathwada's eight districts across two drought years (2015, 2018) and one normal monsoon year (2020), cross-validated independently against CHIRPS rainfall data.

Built on a **"no compromises"** standard — every result is reported exactly as it came out, including a hypothesis (H3: drought severity amplifies the SIF–NDVI lag) that this study's own data does not support.

---

## 📊 What This Project Does

- Defines the Marathwada study region using precise FAO GAUL 2015 district-level boundaries (not a rectangular bounding box), independently verified via a boundary-overlay diagnostic
- Clips GOSIF v2 SIF rasters to the exact district polygon using `rasterio.mask`, and extracts cloud-screened, cropland-masked MODIS NDVI over the same boundary via Google Earth Engine
- Calculates a quantitative SIF-to-NDVI decline lag (days) at five seasonal decline thresholds, per year, using linear-interpolation crossing-date estimation
- Independently validates the drought/normal year classification using CHIRPS rainfall data against a 20-year (2001–2020) climatological baseline, region-wide and by district
- Cross-references spatial SIF stress patterns against spatial rainfall deficit patterns at the district level, as a physically-motivated (not statistical) consistency check
- Presents all findings through a 10-page Streamlit dashboard, including two dedicated pages explaining the underlying photosynthesis and reflectance physics

## 🔬 Key Findings

**SIF consistently declines before NDVI, in all three years studied.** Across 2015, 2018, and 2020 alike, SIF's post-peak seasonal decline preceded NDVI's, supporting SIF's physical basis as a more temporally responsive stress indicator.

**Drought severity does not amplify the lag — the opposite pattern showed up.** Mean lag was smaller in the two drought years (14.6 days) than in the normal year (25.5 days), and the two drought years differed substantially from each other (24.2 vs 5.1 days). H3 is explicitly reported as not supported by this data.

**Rainfall independently confirms the drought years, and the deficit isn't spatially uniform.** Regional rainfall departed −21.5% (2015), −18.3% (2018), and +29.1% (2020) from a 20-year normal. At the district level, 2018's deficit was concentrated in the west (Aurangabad −37.2%, Bid −38.1%) while eastern districts recorded surpluses (Nanded +14.6%) — a west-to-east gradient reproduced independently in the SIF signal itself.

Full methodology, physical basis, and limitations are documented in `Research_Paper.md`.

## 🗂️ Repository Structure

```text
GREEN_ALIBI/
├── app.py                              # Streamlit dashboard home page
├── pages/                              # 10-page dashboard (chronological order)
│   ├── 1_🌍_Study_Area.py
│   ├── 2_🔬_Fluorescence_Physics.py
│   ├── 3_🔬_NDVI_Physics.py
│   ├── 4_🛰️_Data_and_Methodology.py
│   ├── 5_📈_Seasonal_Trajectories.py
│   ├── 6_📊_Lag_Analysis.py
│   ├── 7_🗺️_Spatial_SIF_Analysis.py
│   ├── 8_🌧️_Rainfall_Validation.py
│   ├── 9_🔗_Combined_Comparison.py
│   └── 10_📝_Findings_and_Conclusion.py
├── utils/
│   └── style.py                        # Shared dashboard theme (navy/magenta/pink/teal)
├── src/
│   ├── analysis/                       # Clipping, zonal stats, lag calc, rainfall analysis
│   └── visualization/                  # Static maps + Folium interactive maps
├── data/
│   ├── raw/                             # GOSIF, NDVI, rainfall, boundary data (gitignored)
│   └── processed/                       # District-level SIF, rainfall, and lag summary CSVs
├── outputs/
│   ├── figures/                          # All static figures (spatial maps, charts, physics diagrams)
│   └── interactive_maps/maps/            # Folium HTML maps (SIF + rainfall by district)
├── Research_Paper.md                    # Formal academic research paper
├── Development_Log.md                   # Full technical development log
└── requirements.txt
```

## 🛠️ Tech Stack

Python · Rasterio · GeoPandas · NumPy / Pandas · Matplotlib · Folium · Branca · Streamlit · Google Earth Engine

## 📚 Data Sources

| Dataset | Provider |
|---|---|
| Solar-Induced Fluorescence | GOSIF v2 (Global Ecology Group, University of New Hampshire) |
| NDVI | MODIS MOD13Q1 (via Google Earth Engine) |
| Land Cover / Cropland Mask | MODIS MCD12Q1, IGBP classification (via Google Earth Engine) |
| Precipitation | CHIRPS Daily (UCSB-CHG, via Google Earth Engine) |
| Administrative Boundaries | FAO GAUL 2015, Level 2 (via Google Earth Engine) |

## ▶️ Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/GREEN_ALIBI.git
cd GREEN_ALIBI
pip install -r requirements.txt
streamlit run app.py
```

## 👤 Author

**Sakshi D. Maske**

Independent Geospatial Researcher

---

*This project's full development process — including every boundary correction, debugging session, and methodology iteration — is documented in `Development_Log.md` for full transparency and reproducibility.*