# opendata-localforecast-demos — Agent Guide

## Purpose

Jupyter notebook demos for accessing and visualising **MeteoSwiss Open Government Data (OGD)** local weather forecasts.
9-day hourly forecasts for ~5,600 Swiss POIs (weather stations, towns, postal-code areas).
Target audience: external developers and data scientists who want to use the MeteoSwiss OGD API.

---

## Repository layout

```
notebooks/
  Meteogram.ipynb      # Main notebook — explains data access and API step by step
  meteogram_plot.py    # All matplotlib code; single public entry point: plot_meteogram()
  meteogram.png        # Output written by the notebook (overwritten on each run)
images/
  meteogram.png        # Screenshot for the README
.github/workflows/
  nightly-notebook-run.yml   # Runs notebook via papermill every night, uploads meteogram.png
  metadata_monitor.yml       # Weekly: checks OGD metadata for changes, opens GH issue
pyproject.toml               # Poetry project; Python 3.10–3.14
```

The two-file split is intentional: the notebook explains *what* the data is and *how* to fetch it;
`meteogram_plot.py` handles all rendering so the notebook stays readable.

---

## OGD API — key URLs

```python
STAC_BASE_URL = "https://data.geo.admin.ch/api/stac/v1"
COLLECTION_ID = "ch.meteoschweiz.ogd-local-forecasting"

# Parameter metadata (units, groups, hourly vs daily)
METADATA_URL = f"https://data.geo.admin.ch/{COLLECTION_ID}/ogd-local-forecasting_meta_parameters.csv"

# POI list (~5,600 locations, columns: point_id, point_type_id, point_name, postal_code, …)
POI_LIST_URL = f"https://data.geo.admin.ch/{COLLECTION_ID}/ogd-local-forecasting_meta_point.csv"

# Today's STAC item (contains asset URLs for each parameter CSV)
item_url = f"{STAC_BASE_URL}/collections/{COLLECTION_ID}/items/{YYYYMMDD}-ch"

# Asset key pattern inside the STAC item
# "vnut12.lssw.YYYYMMDDHHmm.<param_shortname>.csv"
# Sort by the timestamp part to find the latest run.
```

Both metadata CSVs use **semicolon delimiter** and **latin-1 encoding**.

### Data CSVs (one per parameter, fetched from asset URLs)

Each CSV contains data for all POIs. Columns: `point_id`, `point_type_id`, a timestamp column
(`date` or `time`, integer format `YYYYMMDDHHmm`), and the value column named after the parameter.
Filter by **both** `point_id` AND `point_type_id` to uniquely identify a POI.

---

## Key data structures after parsing

| Variable | Type | Description |
|---|---|---|
| `df_hourly` | DataFrame | Time-indexed (tz-aware Europe/Zurich), columns = hourly param shortnames |
| `df_daily` | DataFrame | Date-indexed (normalised), columns = daily param shortnames |
| `PARAM_UNITS` | dict | `{shortname: unit_string}` — from metadata CSV |
| `PARAM_GROUP` | dict | `{shortname: panel_name_en}` — maps params to display panels |
| `DAILY_PARAMS` | set | Shortnames where `parameter_granularity == "D"` |
| `poi_row` | Series | Single row from the POI list for the selected location |

---

## Panel ↔ parameter shortname mapping (key params)

| Panel | Key shortnames |
|---|---|
| Temperature | `tre200h0` (median), `treq10h0`/`treq90h0` (Q10/Q90), `tre200pn`/`tre200px` (daily min/max), `zprfr0hs` (0°C level) |
| Precipitation | `rre150h0` (hourly median), `rreq10h0`/`rreq90h0`, `rp0003i0` (probability %), `rka150p0` (daily total), `rreq10p0`/`rreq90p0` |
| Wind | `fu3010h0` (speed), `fu3010h1` (gust), `fu3q10h0`/`fu3q90h0`, `fu3q10h1`/`fu3q90h1`, `dkl010h0` (direction °) |
| Sunshine | `sre000h0` (duration min) |
| Radiation | `gre000h0` (global W/m²), `ods000h0` (diffuse) |
| Clouds | `nprolohs` (low %), `npromths` (mid), `nprohihs` (high) |
| Summary only | `jp2000d0` (pictogram code), `tre200pn`, `tre200px`, `rreq10p0`, `rreq90p0` |

Params `rka150d0`, `tre200dn`, `tre200dx` are station-only — excluded for POI forecasts (`EXCLUDE_PARAMS`).

---

## `plot_meteogram()` signature

```python
plot_meteogram(
    df_hourly,    # pd.DataFrame  — hourly data, time-indexed
    df_daily,     # pd.DataFrame  — daily data, date-indexed
    param_units,  # dict          — shortname → unit string
    poi_row,      # pd.Series     — POI metadata row
    poi_name,     # str           — human-readable name
    elev_str,     # str           — e.g. ", 519 m a.s.l." or ""
    runtime_dt,   # datetime      — timezone-aware model run timestamp
    local_tz,     # ZoneInfo      — Europe/Zurich
    panels=None,  # list[str]|None — subset of PANEL_ORDER, or None for all
    save_path="meteogram.png",
)
```

`PANEL_ORDER = ["Temperature", "Precipitation", "Wind", "Sunshine", "Radiation", "Clouds"]`

Precipitation produces **two** axes (hourly bars + daily totals) — always together.
Axes that share the hourly time axis use `sharex`; the daily precipitation axis is independent.

---

## Running the notebook

```bash
# Install dependencies
poetry install

# Run via papermill (as the CI does)
poetry run papermill notebooks/Meteogram.ipynb executed_notebooks/Meteogram.ipynb --cwd notebooks

# Or open interactively
poetry run jupyter lab
```

The notebook must be executed from `notebooks/` as the working directory (for `from meteogram_plot import …`).

---

## Configuration variables (user-facing, top of notebook)

| Variable | Default | Notes |
|---|---|---|
| `POI_ID` | `"118802"` | `point_id` from the POI search table |
| `POI_TYPE_ID` | `"2"` | `point_type_id` — required together with `POI_ID` for uniqueness |
| `LANG` | `"en"` | `"de"`, `"fr"`, `"it"`, `"en"` — controls labels and pictogram descriptions |
| `PANELS` | `"all"` | `"all"` or a list like `["Temperature", "Wind"]` |

---

## Common failure modes

| Symptom | Likely cause |
|---|---|
| STAC item 404 | Today's item not yet published (runs at ~04:00 UTC); try yesterday's date |
| Empty df after POI filter | Wrong `point_type_id`; both IDs are required for uniqueness |
| Missing param column in df | Parameter not in this STAC item's assets, or param only exists for stations |
| Pictogram Excel download fails | MeteoSwiss URL for the Excel changed — check `PICTO_URL` in the notebook |
| `parameter_group` column mismatch | OGD metadata CSV schema changed — re-check column names in `meta_df` |

---

## Code style

- Line length: 120 (yapf, pep8 base)
- Type hints required (mypy strict); `ignore_missing_imports = true`
- Pylint active; missing docstrings suppressed (C0114/C0115/C0116)
- No comments unless the WHY is non-obvious
- `meteogram_plot.py` has no notebook imports — it is standalone matplotlib

---

## Extending the meteogram

1. **New panel**: add a `plot_<name>(ax, df_hourly, param_units)` function in `meteogram_plot.py`,
   register it in the `panel_functions` dict inside `plot_meteogram()`, add the name to `PANEL_ORDER`.
2. **New parameter in existing panel**: add the shortname to the relevant `plot_*` function;
   the metadata machinery picks it up automatically if it appears in the OGD metadata CSV.
3. **New language**: the metadata CSV already contains `parameter_description_{de,fr,it,en}` columns;
   the pictogram Excel has columns at fixed integer positions (de=2, fr=3, it=4, en=5).

---

## CI / GitHub Actions

- `nightly-notebook-run.yml`: papermill run every day at 00:00 UTC; uploads `notebooks/meteogram.png` as artifact
- `metadata_monitor.yml`: weekly, looks for `check_metadata.py` (currently deleted — workflow will fail the find step but `continue-on-error: true` means it won't block)
