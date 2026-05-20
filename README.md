# 🌤️ MeteoSwiss Open Data: Local Forecast Demos

[![Run in RenkuLab](https://renkulab.io/renku-badge.svg)](https://renkulab.io/projects/meteoswiss/opendata-localforecast-demos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository provides Jupyter notebook examples for accessing and visualizing local weather forecasts from MeteoSwiss, released through Switzerland's **Open Government Data (OGD)** initiative.

Access high-resolution forecasts for **~5,600 points** across Switzerland—including weather stations, towns, and postal code areas (PLZ).

---

## 📓 Included Notebooks

1.  **`poi_finder.ipynb`** 🔍  
    Search for a forecast location by name, PLZ, or station abbreviation. Use this to find the unique `POI` code required for the visualization.
2.  **`meteogram.ipynb`** 🌤️  
    Generate a comprehensive meteogram including:
    *   **Temperature:** 2m temperature and dew point.
    *   **Precipitation:** Probability and quantity.
    *   **Wind:** Speed, gusts, and direction.
    *   **Sky Conditions:** Sunshine duration, radiation, and cloud layers (low/medium/high).
    *   **Daily Weather Summary Table:** A compact table with weather description, min/max temperature, and precipitation range for each forecast day. Weather descriptions are resolved from MeteoSwiss pictogram codes (available in DE/FR/IT/EN).

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