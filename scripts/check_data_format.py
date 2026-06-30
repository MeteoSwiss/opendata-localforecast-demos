#!/usr/bin/env python3
"""
check_data_format.py

Fetches the four OGD local-forecasting data sources and verifies their
structure against the column layout the Meteogram notebook depends on.

Exit 0 = all checks pass.
Exit 1 = one or more format changes detected.
"""
import re
import sys
from datetime import datetime, timedelta
from io import StringIO
from zoneinfo import ZoneInfo

import httpx
import pandas as pd

COLLECTION_ID = "ch.meteoschweiz.ogd-local-forecasting"
STAC_BASE_URL = "https://data.geo.admin.ch/api/stac/v1"
METADATA_URL = (
    f"https://data.geo.admin.ch/{COLLECTION_ID}/"
    "ogd-local-forecasting_meta_parameters.csv"
)
POI_LIST_URL = (
    f"https://data.geo.admin.ch/{COLLECTION_ID}/"
    "ogd-local-forecasting_meta_point.csv"
)
LOCAL_TZ = ZoneInfo("Europe/Zurich")

# Columns the notebook reads by name — any removal breaks it
REQUIRED_META_COLS = {
    "parameter_shortname",
    "parameter_unit",
    "parameter_granularity",
    "parameter_group_de", "parameter_group_fr",
    "parameter_group_it", "parameter_group_en",
    "parameter_description_de", "parameter_description_fr",
    "parameter_description_it", "parameter_description_en",
}
REQUIRED_POI_COLS = {
    "point_id", "point_type_id", "point_name",
    "postal_code", "point_type_en", "station_abbr",
}
# point_height_masl is used for elevation but the notebook guards its absence
OPTIONAL_POI_COLS = {"point_height_masl"}

REQUIRED_DATA_COLS = {"point_id", "point_type_id"}
ASSET_KEY_PATTERN = re.compile(r"vnut12\.lssw\.\d{12}\.\w+\.csv")

issues: list[str] = []


def ok(label: str, detail: str = "") -> None:
    print(f"  ✓  {label}")


def fail(label: str, detail: str = "") -> None:
    print(f"  ✗  {label}" + (f": {detail}" if detail else ""))
    issues.append(label)


def check(label: str, passed: bool, detail: str = "") -> None:
    (ok if passed else fail)(label, detail)


# ── 1. Parameter metadata CSV ────────────────────────────────────────────────
print("\n─── Parameter metadata CSV ───────────────────────────────────────────────")
meta_df: pd.DataFrame | None = None
try:
    resp = httpx.get(METADATA_URL, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    meta_df = pd.read_csv(StringIO(resp.content.decode("latin-1")), sep=";")
    actual = set(meta_df.columns)
    missing = REQUIRED_META_COLS - actual
    added = actual - REQUIRED_META_COLS
    ok("HTTP 200 + latin-1/semicolon parseable")
    check("Required columns present", not missing, f"missing: {sorted(missing)}")
    if added:
        print(f"     ℹ  New columns (no action needed): {sorted(added)}")
    print(f"     rows={len(meta_df)}  cols={len(actual)}")
except Exception as exc:
    fail("Fetch/parse", str(exc))

# ── 2. POI list CSV ──────────────────────────────────────────────────────────
print("\n─── POI list CSV ─────────────────────────────────────────────────────────")
poi_df: pd.DataFrame | None = None
try:
    resp = httpx.get(POI_LIST_URL, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    poi_df = pd.read_csv(StringIO(resp.content.decode("latin-1")), sep=";")
    actual = set(poi_df.columns)
    missing = REQUIRED_POI_COLS - actual
    missing_opt = OPTIONAL_POI_COLS - actual
    added = actual - REQUIRED_POI_COLS - OPTIONAL_POI_COLS
    ok("HTTP 200 + latin-1/semicolon parseable")
    check("Required columns present", not missing, f"missing: {sorted(missing)}")
    if missing_opt:
        print(f"     ℹ  Optional column absent (elevation display affected): {sorted(missing_opt)}")
    if added:
        print(f"     ℹ  New columns (no action needed): {sorted(added)}")
    print(f"     rows={len(poi_df)}  cols={len(actual)}")
except Exception as exc:
    fail("Fetch/parse", str(exc))

# ── 3. STAC item ─────────────────────────────────────────────────────────────
print("\n─── STAC item ────────────────────────────────────────────────────────────")
stac_assets: dict = {}
for delta in (0, 1):
    date_str = (datetime.now(LOCAL_TZ) - timedelta(days=delta)).strftime("%Y%m%d")
    item_url = f"{STAC_BASE_URL}/collections/{COLLECTION_ID}/items/{date_str}-ch"
    try:
        resp = httpx.get(item_url, timeout=30)
        if resp.status_code == 200:
            stac_item = resp.json()
            stac_assets = stac_item.get("assets", {})
            print(f"     Using item: {date_str}-ch  ({len(stac_assets)} assets)")
            ok("STAC item reachable")
            check("'assets' key present", bool(stac_assets))
            if stac_assets:
                sample_key = next(iter(stac_assets))
                check(
                    "Asset key pattern vnut12.lssw.YYYYMMDDHHmm.<param>.csv",
                    bool(ASSET_KEY_PATTERN.match(sample_key)),
                    f"sample key: {sample_key!r}",
                )
            break
    except Exception as exc:
        fail(f"STAC fetch ({date_str})", str(exc))
else:
    fail("STAC item reachable (tried today and yesterday)")

# ── 4. Sample data CSV ───────────────────────────────────────────────────────
print("\n─── Sample data CSV (tre200h0) ───────────────────────────────────────────")
SAMPLE_PARAM = "tre200h0"
sample_key = next((k for k in stac_assets if SAMPLE_PARAM in k), None)
if not stac_assets:
    print("  (skipped — STAC item unavailable)")
elif sample_key is None:
    fail(f"'{SAMPLE_PARAM}' asset present in STAC item")
else:
    try:
        url = stac_assets[sample_key]["href"]
        resp = httpx.get(url, timeout=30)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.content.decode("latin-1")), sep=";")
        actual = set(df.columns)
        missing = REQUIRED_DATA_COLS - actual
        has_time_col = any(
            k in c.lower() for c in actual for k in ("date", "time")
        )
        ok("HTTP 200 + latin-1/semicolon parseable")
        check("point_id + point_type_id present", not missing, f"missing: {sorted(missing)}")
        check("Timestamp column present (contains 'date' or 'time')", has_time_col,
              f"columns seen: {sorted(actual)}")
        check(f"Value column '{SAMPLE_PARAM}' present", SAMPLE_PARAM in actual)
        print(f"     rows={len(df)}  cols={sorted(actual)}")
    except Exception as exc:
        fail(f"Fetch/parse {SAMPLE_PARAM}", str(exc))

# ── Summary ──────────────────────────────────────────────────────────────────
print("\n" + "─" * 74)
if issues:
    print(f"  FAIL — {len(issues)} issue(s) detected:")
    for issue in issues:
        print(f"    • {issue}")
    sys.exit(1)
else:
    print("  PASS — all format checks passed")
    sys.exit(0)
