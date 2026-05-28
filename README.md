## 🌤️ MeteoSwiss Open Data: Local Forecast Demos

Click here and try it now! [![launch - renku](https://renkulab.io/renku-badge.svg)](https://renkulab.io/p/meteoswiss/opendata-local-weatherforecast-demo/sessions/01KSM0G2KFE1DJWQ35E72EXV4C/start)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository provides Jupyter notebook examples for accessing and visualizing local weather forecasts from MeteoSwiss, released through Switzerland's **Open Government Data (OGD)** initiative.

Access high-resolution forecasts for **~5,600 points** across Switzerland — including weather stations, towns, and postal code areas (PLZ).

---

## 🌤️ The Meteogram Notebook

`meteogram.ipynb` walks you through the full workflow of accessing MeteoSwiss OGD forecast data, from location discovery to visualization. It is structured as a story with one concept per section:

| Section | What you learn |
|---|---|
| 1 · Choose your location | How forecast data is organised by point of interest (POI) |
| 2 · Explore parameters | What MeteoSwiss publishes and how parameters are grouped |
| 3 · Download the data | How to query the STAC API and parse the CSV files |
| 4 · Visualise | How to render a 9-day meteogram |
| 5 · Daily summary | How pictogram codes map to weather descriptions |

**Key features:**
- **Integrated POI search** — find your location by name or ZIP code directly in the notebook
- **9-day forecast horizon** — hourly data combined with daily summaries
- **Metadata-driven** — units, labels, and panel groupings resolved automatically from OGD metadata
- **Accurate day/night shading** — sunrise and sunset computed per location using astronomical calculations

The plotting code lives in `meteogram_plot.py`, alongside the notebook. The notebook itself focuses on the data and the API; open the module only if you want to customise the chart.

![MeteoSwiss Local Forecast Meteogram](images/meteogram.png)

**Daily Weather Summary Table (example output):**

| Date      | Weather                            | T min (°C) | T max (°C) | Precip. (mm) |
|-----------|------------------------------------|------------|------------|--------------|
| Mon 19.05 | partly sunny, thick passing clouds | 12.3       | 22.1       | 0–2          |
| Tue 20.05 | very cloudy, light rain            | 10.8       | 19.5       | 3–15         |
| Wed 21.05 | high clouds                        | 11.1       | 21.3       | 0            |
| Thu 22.05 | mostly sunny, some clouds          | 12.5       | 23.0       | 0            |
| Fri 23.05 | overcast, some rain showers        | 11.0       | 18.7       | 5–20         |
| Sat 24.05 | sunny                              | 10.2       | 24.1       | 0            |
| Sun 25.05 | mostly sunny, some clouds          | 11.8       | 25.3       | 0            |
| Mon 26.05 | partly sunny, thick passing clouds | 12.0       | 22.8       | 0–3          |
| Tue 27.05 | mostly sunny, some clouds          | 13.0       | 24.2       | 0            |

---

## 🚀 Quick Start

1. **Open `meteogram.ipynb`**
2. **Find your location** — use the interactive search table in section 1 to find your town (e.g. `"Zermatt"` or `"8001"`) and copy the `point_id`
3. **Set your POI** — paste the `point_id` into the `POI` variable in the configuration cell
4. **Run all cells**

To customise the output, edit the configuration cell:
- `PANELS = ["Temperature", "Wind"]` — show only selected panels
- `LANG = "de"` — switch labels to German, French, or Italian

---

## 🛠️ Technical Details

### Data source
Forecast data is fetched directly from the [Federal Geodata Infrastructure STAC API](https://data.geo.admin.ch/api/stac/v1).

- **Collection:** `ch.meteoschweiz.ogd-local-forecasting`
- **Update cycle:** Daily batch at ~04:00 UTC, with 6-hourly refreshes
- **Horizon:** 9 days (D+0 to D+8)

### Repository structure

```
meteogram.ipynb       # Main notebook — data access and API walkthrough
meteogram_plot.py     # Plotting module — all matplotlib code lives here
```

### Architecture

The notebook is **metadata-driven**: it reads the [OGD parameter CSV](https://data.geo.admin.ch/ch.meteoschweiz.ogd-local-forecasting/ogd-local-forecasting_meta_parameters.csv) at runtime to resolve parameter units, panel groupings, and hourly vs. daily granularity — no hardcoded labels.

The plotting module (`meteogram_plot.py`) is intentionally separate so the notebook stays focused on explaining the data. It exposes a single entry point:

```python
from meteogram_plot import plot_meteogram
plot_meteogram(df_hourly, df_daily, ...)
```

---

## 💻 Installation

### Option 1: Cloud (recommended)
Click the **"Run in RenkuLab"** badge above to launch a ready-to-use environment in your browser. No local setup needed.

### Option 2: Local

```bash
git clone https://github.com/MeteoSwiss/opendata-localforecast-demos.git
cd opendata-localforecast-demos
pip install httpx pandas matplotlib openpyxl itables astral
```