"""
pictograms.py
-------------
Weather pictograms for the MeteoSwiss symbol codes (1–42 day, 101–142 night)
used by the OGD local forecast parameters `jp2000d0` and `jww003i0`.

Icons and descriptions are bundled in the `icons/` folder next to this module.
"""

import base64
import json
from functools import lru_cache
from pathlib import Path

import matplotlib.image as mpimg
import pandas as pd

ICON_DIR = Path(__file__).parent / "icons"
ICON_SIZE = 64


@lru_cache(maxsize=1)
def _symbols():
    with open(ICON_DIR / "symbols.json", encoding="utf-8") as f:
        return {int(code): entry for code, entry in json.load(f).items()}


def _icon_path(code):
    """Return the PNG path for a symbol code, or None for NaN / unknown codes."""
    if code is None or pd.isna(code):
        return None
    path = ICON_DIR / "png" / str(ICON_SIZE) / f"{int(code)}.png"
    return path if path.exists() else None


def load_descriptions(lang="en"):
    """Map symbol code → description in `lang` ("de", "fr", "it", "en"; falls back to English)."""
    key = f"description_{lang}"
    return {code: entry.get(key, entry["description_en"]) for code, entry in _symbols().items()}


@lru_cache(maxsize=None)
def load_icon(code):
    """Return the icon for a symbol code as an RGBA array, or None if there is none."""
    path = _icon_path(code)
    return mpimg.imread(path) if path else None


def icon_html(code, size=32):
    """Return a self-contained <img> tag (base64 PNG) for a symbol code, or "" if there is none."""
    path = _icon_path(code)
    if path is None:
        return ""
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<img src="data:image/png;base64,{data}" width="{size}" height="{size}" alt="{int(code)}">'
