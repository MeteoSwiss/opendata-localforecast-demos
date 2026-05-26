"""
meteogram_plot.py
-----------------
Plotting helpers for the MeteoSwiss OGD Local Forecast meteogram notebook.

This module handles all matplotlib rendering so the notebook can focus on
explaining the data and the API. You don't need to read this to understand
how to use the MeteoSwiss OGD API — it's purely visualisation plumbing.
"""

from datetime import timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from astral import LocationInfo
from astral.sun import sun
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

COLORS = {
    # Temperature
    "temp_median":        "#E31A1C",
    "temp_q_fill":        "#FDCDCD",
    "temp_tmin":          "#1F78B4",
    "temp_tmax":          "#E31A1C",
    # Precipitation
    "precip_bar":         "#4292C6",
    "precip_q_fill":      "#9ECAE1",
    "precip_prob":        "#08306B",
    # Wind
    "wind_speed":         "#33A02C",
    "wind_gust":          "#FB9A99",
    "wind_q_fill_speed":  "#D9F0D3",
    "wind_q_fill_gust":   "#FDE0DD",
    # Sunshine / radiation
    "sunshine_bar":       "#FFD700",
    "radiation_global":   "#FF8C00",
    "radiation_diffuse":  "#FFA07A",
    # Clouds
    "cloud_low":          "#636363",
    "cloud_mid":          "#969696",
    "cloud_high":         "#CCCCCC",
    # Zero degree level
    "zero_level":         "#6A3D9A",
    # Background
    "day_bg":             "#FFFDE7",
    "night_bg":           "#E8EAF6",
    "zero_line":          "#999999",
}

# ---------------------------------------------------------------------------
# Matplotlib defaults
# ---------------------------------------------------------------------------

plt.rcParams.update({
    "figure.dpi":       120,
    "figure.facecolor": "white",
    "axes.grid":        True,
    "axes.grid.which":  "major",
    "grid.alpha":       0.3,
    "grid.linestyle":   "--",
    "font.size":        9,
    "axes.titlesize":   10,
    "axes.labelsize":   9,
})

# ---------------------------------------------------------------------------
# Axis helpers
# ---------------------------------------------------------------------------

def _get_sun_times(date, lat: float, lon: float, local_tz):
    """Return (sunrise, sunset) for a given date and location."""
    location = LocationInfo(latitude=lat, longitude=lon, timezone=str(local_tz))
    s = sun(location.observer, date=date, tzinfo=local_tz)
    return s["sunrise"], s["sunset"]


def add_day_night_shading(ax, local_tz, lat: float, lon: float):
    """Shade night periods using astronomical sunrise/sunset for the given coordinates."""
    xlim    = mdates.num2date(ax.get_xlim())
    current = xlim[0].replace(hour=0, minute=0)
    end     = xlim[1]
    while current < end:
        next_day = current + timedelta(days=1)
        try:
            sunrise, sunset = _get_sun_times(current.date(), lat, lon, local_tz)
        except Exception:
            # Fallback to fixed times if astral fails (e.g. polar night/day edge cases)
            sunrise = current.replace(hour=6,  minute=0)
            sunset  = current.replace(hour=21, minute=0)
        ax.axvspan(current,  sunrise,  color=COLORS["night_bg"], alpha=0.3, zorder=0)
        ax.axvspan(sunrise,  sunset,   color=COLORS["day_bg"],   alpha=0.3, zorder=0)
        ax.axvspan(sunset,   next_day, color=COLORS["night_bg"], alpha=0.3, zorder=0)
        current = next_day


def format_time_axis(ax, local_tz, is_bottom=False):
    """Apply date/time tick formatting.  Bottom panel gets labels; others are blank."""
    ax.xaxis.set_major_locator(mdates.DayLocator(tz=local_tz))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[6, 12, 18], tz=local_tz))
    if is_bottom:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%d %b", tz=local_tz))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H", tz=local_tz))
        ax.tick_params(axis="x", which="minor", labelsize=7)
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter(""))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter(""))

# ---------------------------------------------------------------------------
# Individual panel plots
# ---------------------------------------------------------------------------

def plot_temperature(ax, df_hourly, df_daily, param_units, poi_row):
    """Temperature panel: median + Q10/Q90 band + daily Tmin/Tmax + 0°C level."""
    if "tre200h0" in df_hourly:
        ax.plot(df_hourly.index, df_hourly["tre200h0"],
                color=COLORS["temp_median"], lw=1.5, label="T median")
    if "treq10h0" in df_hourly and "treq90h0" in df_hourly:
        ax.fill_between(df_hourly.index,
                        df_hourly["treq10h0"], df_hourly["treq90h0"],
                        color=COLORS["temp_q_fill"], alpha=0.5, label="Q10–Q90")

    dates_noon = df_daily.index + __import__("pandas").Timedelta(hours=12)
    if "tre200pn" in df_daily:
        ax.scatter(dates_noon, df_daily["tre200pn"],
                   color=COLORS["temp_tmin"], marker="v", s=30, zorder=5, label="Tmin")
    if "tre200px" in df_daily:
        ax.scatter(dates_noon, df_daily["tre200px"],
                   color=COLORS["temp_tmax"], marker="^", s=30, zorder=5, label="Tmax")

    ax.axhline(0, color=COLORS["zero_line"], lw=0.5, ls="--")
    ax.set_ylabel(param_units.get("tre200h0", "°C"))

    if "zprfr0hs" in df_hourly:
        ax2 = ax.twinx()
        ax2.plot(df_hourly.index, df_hourly["zprfr0hs"],
                 color=COLORS["zero_level"], lw=1.2, label="0°C level")
        elev_cols = [c for c in poi_row.index
                     if any(k in c.lower() for k in ("elev", "height", "alt"))]
        if elev_cols:
            elev = poi_row[elev_cols[0]]
            ax2.axhline(elev, color=COLORS["zero_line"], lw=0.8, ls=":",
                        label=f"Station ({elev:.0f} m)")
        ax2.set_ylabel(param_units.get("zprfr0hs", "m"))
        lines = ax.get_legend_handles_labels()
        lines2 = ax2.get_legend_handles_labels()
        ax.legend(lines[0] + lines2[0], lines[1] + lines2[1],
                  loc="best", fontsize=7, ncol=5)
    else:
        ax.legend(loc="upper right", fontsize=7, ncol=4)

    ax.set_title("Temperature")


def plot_precipitation(ax, df_hourly, param_units):
    """Precipitation panel: hourly bars + Q10/Q90 band + probability line."""
    ax2 = ax.twinx()
    if "rre150h0" in df_hourly:
        ax.bar(df_hourly.index, df_hourly["rre150h0"], width=1/24,
               color=COLORS["precip_bar"], alpha=0.7, label="Precip median")
    if "rreq10h0" in df_hourly and "rreq90h0" in df_hourly:
        ax.fill_between(df_hourly.index,
                        df_hourly["rreq10h0"], df_hourly["rreq90h0"],
                        color=COLORS["precip_q_fill"], alpha=0.4, label="Q10–Q90")
    if "rp0003i0" in df_hourly:
        ax2.plot(df_hourly.index, df_hourly["rp0003i0"],
                 color=COLORS["precip_prob"], lw=1, ls="--", label="Prob. precip")
        ax2.set_ylabel(param_units.get("rp0003i0", "%"))
        ax2.set_ylim(0, 105)
        ax2.legend(loc="upper left", fontsize=7)
    ax.set_ylabel(param_units.get("rre150h0", "mm"))
    ax.set_title("Precipitation (hourly)")
    ax.legend(loc="upper right", fontsize=7)


def plot_daily_precip(ax, df_daily, df_hourly, param_units, local_tz):
    """Daily precipitation: median bars + Q10/Q90 whiskers."""
    import pandas as pd
    dates_noon = df_daily.index + pd.Timedelta(hours=12)
    positions  = mdates.date2num(dates_noon)

    if "rka150p0" not in df_daily:
        ax.text(0.5, 0.5, "No daily precipitation data",
                transform=ax.transAxes, ha="center")
        return

    median = df_daily["rka150p0"].values
    q10    = df_daily["rreq10p0"].values if "rreq10p0" in df_daily else median
    q90    = df_daily["rreq90p0"].values if "rreq90p0" in df_daily else median

    ax.bar(positions, median, width=0.5,
           color=COLORS["precip_bar"], alpha=0.7, zorder=3)
    for i, pos in enumerate(positions):
        ax.vlines(pos, q10[i], q90[i], color="steelblue", lw=1.5, zorder=4)
        for y in (q10[i], q90[i]):
            ax.hlines(y, pos - 0.15, pos + 0.15, color="steelblue", lw=1.5, zorder=4)

    ax.legend(handles=[
        Patch(facecolor=COLORS["precip_bar"], alpha=0.7, label="Median"),
        Line2D([0], [0], color="steelblue", lw=1.5, label="Q10–Q90"),
    ], loc="upper right", fontsize=7, ncol=2)

    ax.set_ylim(bottom=0)
    ax.set_ylabel(param_units.get("rka150p0", "mm"))
    ax.set_title("Daily Precipitation")
    ax.xaxis.set_major_locator(mdates.DayLocator(tz=local_tz))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%d.%m", tz=local_tz))
    ax.set_xlim(df_hourly.index[0], df_hourly.index[-1])


def plot_wind(ax, df_hourly, param_units):
    """Wind panel: speed + gust lines with Q10/Q90 bands + direction arrows."""
    if "fu3010h0" in df_hourly:
        ax.plot(df_hourly.index, df_hourly["fu3010h0"],
                color=COLORS["wind_speed"], lw=1.2, label="Speed")
    if "fu3q10h0" in df_hourly and "fu3q90h0" in df_hourly:
        ax.fill_between(df_hourly.index,
                        df_hourly["fu3q10h0"], df_hourly["fu3q90h0"],
                        color=COLORS["wind_q_fill_speed"], alpha=0.4, label="Speed Q10–Q90")
    if "fu3010h1" in df_hourly:
        ax.plot(df_hourly.index, df_hourly["fu3010h1"],
                color=COLORS["wind_gust"], lw=1, ls="--", label="Gust")
    if "fu3q10h1" in df_hourly and "fu3q90h1" in df_hourly:
        ax.fill_between(df_hourly.index,
                        df_hourly["fu3q10h1"], df_hourly["fu3q90h1"],
                        color=COLORS["wind_q_fill_gust"], alpha=0.3, label="Gust Q10–Q90")

    if "dkl010h0" in df_hourly and "fu3010h0" in df_hourly:
        step      = 3
        times     = df_hourly.index[::step]
        dirs_rad  = np.deg2rad(df_hourly["dkl010h0"].iloc[::step].values)
        u, v      = -np.sin(dirs_rad), -np.cos(dirs_rad)
        y_level   = ax.get_ylim()[1] * 0.85 if ax.get_ylim()[1] > 0 else 10
        ax.quiver(mdates.date2num(times), np.full(len(times), y_level), u, v,
                  angles="uv", pivot="middle", scale=100, width=0.001,
                  headwidth=3, headlength=4, headaxislength=3.5,
                  color="black", zorder=5)

    ax.set_ylabel(param_units.get("fu3010h0", "km/h"))
    ax.set_title("Wind")
    ax.legend(loc="upper right", fontsize=7, ncol=4)


def plot_sunshine(ax, df_hourly, param_units):
    """Sunshine panel: hourly duration bars."""
    import pandas as pd
    if "sre000h0" in df_hourly:
        ax.bar(df_hourly.index - pd.Timedelta(minutes=30),
               df_hourly["sre000h0"], width=1/24,
               color=COLORS["sunshine_bar"], alpha=0.7, label="Sunshine")
    ax.set_ylim(0, max(ax.get_ylim()[1], 60))
    ax.set_xlim(df_hourly.index[0], df_hourly.index[-1])
    ax.set_ylabel(param_units.get("sre000h0", "min"))
    ax.set_title("Sunshine")
    ax.legend(loc="upper right", fontsize=7)


def plot_radiation(ax, df_hourly, param_units):
    """Radiation panel: global and diffuse lines."""
    if "gre000h0" in df_hourly:
        ax.plot(df_hourly.index, df_hourly["gre000h0"],
                color=COLORS["radiation_global"], lw=1, label="Global")
    if "ods000h0" in df_hourly:
        ax.plot(df_hourly.index, df_hourly["ods000h0"],
                color=COLORS["radiation_diffuse"], lw=1, ls="--", label="Diffuse")
    ax.set_ylim(0, max(ax.get_ylim()[1], 1))
    ax.set_xlim(df_hourly.index[0], df_hourly.index[-1])
    ax.set_ylabel(param_units.get("gre000h0", "W/m²"))
    ax.set_title("Radiation")
    ax.legend(loc="upper right", fontsize=7)


def plot_clouds(ax, df_hourly):
    """Cloud cover panel: stacked area (low / mid / high)."""
    layers = [
        ("nprolohs", "Low",  COLORS["cloud_low"]),
        ("npromths", "Mid",  COLORS["cloud_mid"]),
        ("nprohihs", "High", COLORS["cloud_high"]),
    ]
    available = [(k, label, color) for k, label, color in layers if k in df_hourly]
    if available:
        ax.stackplot(
            df_hourly.index,
            *[df_hourly[k].fillna(0).values * 100 for k, _, _ in available],
            labels=[label for _, label, _ in available],
            colors=[color for _, _, color in available],
            alpha=0.6,
        )
        ax.set_ylim(0, 100)
    ax.set_ylabel("%")
    ax.set_title("Clouds")
    ax.legend(loc="upper right", fontsize=7, ncol=3)

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def plot_meteogram(
    df_hourly,
    df_daily,
    param_units,
    poi_row,
    poi_name,
    elev_str,
    runtime_dt,
    local_tz,
    panels=None,
    save_path="meteogram.png",
):
    """
    Assemble and render the full meteogram figure.

    Parameters
    ----------
    df_hourly   : pd.DataFrame  Hourly forecast data (time-indexed, columns = param shortnames)
    df_daily    : pd.DataFrame  Daily forecast data  (date-indexed, columns = param shortnames)
    param_units : dict          Maps param shortname → unit string
    poi_row     : pd.Series     Metadata row for the selected point of interest
    poi_name    : str           Human-readable location name
    elev_str    : str           Elevation string, e.g. ", 519 m a.s.l." (may be empty)
    runtime_dt  : datetime      Model run timestamp (timezone-aware)
    local_tz    : ZoneInfo      Local timezone for axis labels
    panels      : list[str]     Which panels to show; defaults to all
    save_path   : str           File path for the saved PNG
    """

    PANEL_ORDER = ["Temperature", "Precipitation", "Wind", "Sunshine", "Radiation", "Clouds"]
    selected_panels = panels or PANEL_ORDER

    # Extract POI coordinates for sunrise/sunset calculation
    lat_col = next((c for c in poi_row.index if "lat" in c.lower()), None)
    lon_col = next((c for c in poi_row.index if "lon" in c.lower()), None)
    poi_lat = float(poi_row[lat_col]) if lat_col else 46.8   # fallback: centre of Switzerland
    poi_lon = float(poi_row[lon_col]) if lon_col else  8.2

    # Map panel names to bound plot functions
    panel_functions = {
        "Temperature":   [lambda ax: plot_temperature(ax, df_hourly, df_daily, param_units, poi_row)],
        "Precipitation": [
            lambda ax: plot_precipitation(ax, df_hourly, param_units),
            lambda ax: plot_daily_precip(ax, df_daily, df_hourly, param_units, local_tz),
        ],
        "Wind":          [lambda ax: plot_wind(ax, df_hourly, param_units)],
        "Sunshine":      [lambda ax: plot_sunshine(ax, df_hourly, param_units)],
        "Radiation":     [lambda ax: plot_radiation(ax, df_hourly, param_units)],
        "Clouds":        [lambda ax: plot_clouds(ax, df_hourly)],
    }

    # daily_flags tracks which axes use the independent daily x-axis
    funcs_flat = []
    daily_flags = []
    for panel in selected_panels:
        for i, func in enumerate(panel_functions.get(panel, [])):
            funcs_flat.append(func)
            daily_flags.append(panel == "Precipitation" and i == 1)

    n_axes = len(funcs_flat)
    fig = plt.figure(figsize=(14, 2.8 * n_axes))
    gs  = GridSpec(n_axes, 1, figure=fig)

    ax_first_hourly = None
    axes_all = []

    for i, (func, is_daily) in enumerate(zip(funcs_flat, daily_flags)):
        if is_daily:
            ax = fig.add_subplot(gs[i])
        elif ax_first_hourly is None:
            ax = fig.add_subplot(gs[i])
            ax_first_hourly = ax
        else:
            ax = fig.add_subplot(gs[i], sharex=ax_first_hourly)
        axes_all.append((ax, func, is_daily))

    for idx, (ax, func, is_daily) in enumerate(axes_all):
        func(ax)
        if not is_daily and not df_hourly.empty:
            add_day_night_shading(ax, local_tz, lat=poi_lat, lon=poi_lon)
            is_last_hourly = not any(not d for _, _, d in axes_all[idx + 1:])
            format_time_axis(ax, local_tz, is_bottom=is_last_hourly)
            ax.set_xlim(df_hourly.index[0], df_hourly.index[-1])

    fig.suptitle(
        f"Meteogram — {poi_name}{elev_str}\n"
        f"Model run: {runtime_dt.strftime('%Y-%m-%d %H:%M %Z')}",
        fontsize=13, fontweight="bold",
    )
    fig.set_layout_engine("constrained")
    plt.show()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"✓ Meteogram saved to {save_path}")
