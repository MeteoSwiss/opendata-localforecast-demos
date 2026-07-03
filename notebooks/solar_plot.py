"""
solar_plot.py
-------------
Plotting helpers for the MeteoSwiss OGD Solar Production demo notebook.

This module handles all matplotlib rendering so the notebook can focus on
explaining the data and the simple PV model. You don't need to read this to
understand how to use the MeteoSwiss OGD API — it's purely visualisation
plumbing.
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

COLORS = {
    "power":  "#FF8C00",
    "energy": "#FFB74D",
}

plt.rcParams.update({
    "figure.dpi":        120,
    "figure.facecolor":  "white",
    "axes.grid":         True,
    "axes.grid.which":   "major",
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "font.size":         9,
    "axes.titlesize":    10,
    "axes.labelsize":    9,
    "legend.framealpha": 0.6,
    "legend.fontsize":   7,
})


def _format_hourly_axis(ax, local_tz):
    ax.xaxis.set_major_locator(mdates.DayLocator(tz=local_tz))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[6, 12, 18], tz=local_tz))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%d %b", tz=local_tz))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H", tz=local_tz))
    ax.tick_params(axis="x", which="minor", labelsize=7)


def plot_solar_production(
    df_hourly,
    df_daily,
    poi_name,
    elev_str,
    runtime_dt,
    local_tz,
    pv_capacity_kwp,
    save_path="solar_production.png",
):
    """
    Render the hourly PV power forecast and the daily PV energy total.

    Parameters
    ----------
    df_hourly       : pd.DataFrame  Hourly forecast data incl. "pv_power_kw" (time-indexed)
    df_daily        : pd.DataFrame  Daily forecast data incl. "pv_energy_kwh" (date-indexed)
    poi_name        : str           Human-readable location name
    elev_str        : str           Elevation string, e.g. ", 519 m a.s.l." (may be empty)
    runtime_dt      : datetime      Model run timestamp (timezone-aware)
    local_tz        : ZoneInfo      Local timezone for axis labels
    pv_capacity_kwp : float         Illustrative PV system capacity, shown as a reference line
    save_path       : str           File path for the saved PNG
    """
    fig, (ax_power, ax_energy) = plt.subplots(
        2, 1, figsize=(14, 6.5), gridspec_kw={"height_ratios": [1.4, 1]}
    )

    ax_power.plot(df_hourly.index, df_hourly["pv_power_kw"],
                  color=COLORS["power"], lw=1.3, label="Estimated PV power")
    ax_power.axhline(pv_capacity_kwp, color="grey", lw=0.8, ls=":",
                      label=f"Installed capacity ({pv_capacity_kwp:.1f} kWp)")
    ax_power.set_ylabel("Power (kW)")
    ax_power.set_ylim(bottom=0)
    ax_power.set_xlim(df_hourly.index[0], df_hourly.index[-1])
    ax_power.set_title("Estimated hourly PV power")
    _format_hourly_axis(ax_power, local_tz)
    ax_power.legend(loc="upper right")

    ax_energy.bar(df_daily.index, df_daily["pv_energy_kwh"], width=0.6,
                  color=COLORS["energy"], alpha=0.85, label="Estimated daily PV energy")
    ax_energy.set_ylabel("Energy (kWh)")
    ax_energy.set_ylim(bottom=0)
    ax_energy.set_title("Estimated daily PV energy")
    ax_energy.xaxis.set_major_locator(mdates.DayLocator(tz=local_tz))
    ax_energy.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%d.%m", tz=local_tz))
    ax_energy.legend(loc="upper right")

    fig.suptitle(
        f"Estimated Solar Production — {poi_name}{elev_str}\n"
        f"Model run: {runtime_dt.strftime('%Y-%m-%d %H:%M %Z')} "
        f"(illustrative {pv_capacity_kwp:.1f} kWp system)",
        fontsize=13, fontweight="bold",
    )
    fig.set_layout_engine("constrained")
    plt.show()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"✓ Solar production chart saved to {save_path}")
