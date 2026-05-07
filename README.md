<h1 align="center">OGD Local Forecast Meteogram</h1>
<h3 align="center">Jupyter Notebook Examples Using MeteoSwiss Local Forecast Data</h3>

<p align="center">
  <img src="images/logo_mch.png" alt="MCH Logo" width="130" />
  <img src="images/logo_opendata.jpeg" alt="Open Data Logo" width="130" />
</p>

This repository provides Jupyter notebook examples for accessing and visualising **local weather forecasts** from **MeteoSwiss**, released through Switzerland's **Open Government Data (OGD)** initiative.

Forecasts are available for ~5600 points across Switzerland — weather stations, towns, and postal code areas — and are updated every 6 hours.

---

## 📓 Notebooks

👉 [![launch - renku](https://renkulab.io/renku-badge.svg)](https://renkulab.io/p/meteoswiss/opendata-local-forecast-demos/sessions/start)

* **[poi_finder.ipynb](poi_finder.ipynb)** 🔍 — Search for a forecast location by **name**, **PLZ**, or **station abbreviation**. Use this first to find the `POI` code you need for the meteogram.

* **[meteogram.ipynb](meteogram.ipynb)** 🌤️ — Generate a multi-panel meteogram (temperature, precipitation, wind, sunshine, clouds, zero-degree level) for any location in Switzerland.

## ⚡ Quick Start

1. Open the **[POI Finder](poi_finder.ipynb)** notebook.
2. Enter your town name or PLZ (e.g. `"1188"` or `"Zürich"`).
3. Copy the `POI = "..."` line from the output.
4. Open the **[Meteogram](meteogram.ipynb)** notebook.
5. Paste the POI value into Cell 2.
6. Run all cells — your meteogram appears at the bottom.

## 🚀 Getting Started

### Option 1: Run in [RenkuLab](https://renkulab.io/)

👉 [![launch - renku](https://renkulab.io/renku-badge.svg)](https://renkulab.io/p/meteoswiss/opendata-local-forecast-demos/sessions/start)

1. Navigate to the project folder.
2. Open `poi_finder.ipynb` to find your location, then `meteogram.ipynb` to generate the forecast. No additional installation required.

### Option 2: Run locally

Clone the repository and install the required packages:

```bash
pip install httpx pandas matplotlib
