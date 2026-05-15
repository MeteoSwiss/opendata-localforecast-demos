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
![MeteoSwiss Local Forecast Meteogram](images/meteogram.png)
---

## 🚀 Quick Start

1.  **Find your POI:** Open `poi_finder.ipynb` and search for your town (e.g., `"Zermatt"` or `"8001"`). Copy the resulting `POI = "..."` string.
2.  **Generate Plot:** Open `meteogram.ipynb`, paste your POI code into **Cell 2**, and run all cells.
3.  **Customize:** You can toggle panels (e.g., hide Radiation) by modifying the `PANEL_ORDER` list in the Configuration cell.

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
pip install httpx pandas matplotlib ipywidgets
