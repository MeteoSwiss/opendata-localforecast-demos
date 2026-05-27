## 🌤️ MeteoSwiss Open Data: Local Forecast Demos

Click here and try it now! [![launch - renku](https://renkulab.io/renku-badge.svg)](https://renkulab.io/p/meteoswiss/opendata-local-weatherforecast-demo/sessions/01KSM0G2KFE1DJWQ35E72EXV4C/start)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository provides Jupyter notebook examples for accessing and visualizing local weather forecasts from MeteoSwiss, released through Switzerland's **Open Government Data (OGD)** initiative.

Access high-resolution forecasts for **~5,600 points** across Switzerland—including weather stations, towns, and postal code areas (PLZ).

---

## 🌤️ The Meteogram Notebook
The `meteogram.ipynb` is an all-in-one tool designed for location discovery, automated data retrieval, and professional visualization.
**Key Features:**
*   **Integrated POI Search:** Find your location by name or ZIP code directly inside the notebook using an interactive search table.
*   **9-Day Forecast Horizon:** High-resolution hourly data combined with daily summaries.
*   **Metadata-Driven:** Automatically resolves units, labels, and groupings from official MeteoSwiss OGD metadata.
*   **Daily Summary Table:** Includes weather pictograms and min/max temperature overviews.
## 🚀 Quick Start
1.  **Open `meteogram.ipynb`**.
2.  **Search:** Use the interactive table in the **Configuration** cell to find your location (e.g., "Zermatt" or "8001").
3.  **Set POI:** Copy the `point_id` and paste it into the `POI` variable.
4.  **Run All:** Execute the notebook to generate your custom meteogram.


![MeteoSwiss Local Forecast Meteogram](images/meteogram.png)

**Daily Weather Summary Table (example output):**

| Date      | Weather                                    | T min (°C) | T max (°C) | Precip. (mm) |
|-----------|--------------------------------------------|------------|------------|---------------|
| Mon 19.05 | partly sunny, thick passing clouds         | 12.3       | 22.1       | 0–2           |
| Tue 20.05 | very cloudy, light rain                    | 10.8       | 19.5       | 3–15          |
| Wed 21.05 | high clouds                                | 11.1       | 21.3       | 0             |
| Thu 22.05 | mostly sunny, some clouds                  | 12.5       | 23.0       | 0             |
| Fri 23.05 | overcast, some rain showers                | 11.0       | 18.7       | 5–20          |
| Sat 24.05 | sunny                                      | 10.2       | 24.1       | 0             |
| Sun 25.05 | mostly sunny, some clouds                  | 11.8       | 25.3       | 0             |
| Mon 26.05 | partly sunny, thick passing clouds         | 12.0       | 22.8       | 0–3           |
| Tue 27.05 | mostly sunny, some clouds                  | 13.0       | 24.2       | 0             |

---

## 🚀 Quick Start

1.  **Find your POI:** Open `poi_finder.ipynb` and search for your town (e.g., `"Zermatt"` or `"8001"`). Copy the resulting `POI = "..."` string.
2.  **Generate Plot:** Open `meteogram.ipynb`, paste your POI code into **Cell 2**, and run all cells.
3.  **Customize:** You can toggle panels (e.g., hide Radiation) by modifying the `PANEL_ORDER` list in the Configuration cell. Set `SHOW_SUMMARY_TABLE = False` to hide the daily weather summary table.

---

## 🛠️ Technical Details

### Data Source
The notebooks fetch data directly from the [Federal Geodata Infrastructure (STAC API)](https://data.geo.admin.ch/api/stac/v1).
*   **Collection:** `ch.meteoschweiz.ogd-local-forecasting`
*   **Update Cycle:** Daily batch update at ~04:00 UTC (with 6-hourly refreshes).
*   **Horizon:** 9 days (D+0 to D+8).

### Architecture
The visualization is **metadata-driven**. It reads a [central OGD parameter CSV](https://data.geo.admin.ch/ch.meteoschweiz.ogd-local-forecasting/ogd-local-forecasting_meta_parameters.csv) to automatically resolve:
*   Parameter units (e.g., °C, hPa, W/m²).
*   Grouping of variables into logical plot panels.
*   Data granularity (hourly vs. daily).

---

## 💻 Installation

### Option 1: Cloud (Recommended)
Click the **"Run in RenkuLab"** badge at the top to launch a ready-to-use environment in your browser.

### Option 2: Local
Clone the repository and install the dependencies:
```bash
git clone https://github.com/MeteoSwiss/opendata-localforecast-demos.git
cd opendata-localforecast-demos
pip install httpx pandas matplotlib ipywidgets openpyxl
