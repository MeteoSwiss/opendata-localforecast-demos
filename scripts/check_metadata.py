import pandas as pd
import requests
import sys
import os

METADATA_URL = "https://data.geo.admin.ch/ch.meteoschweiz.ogd-local-forecasting/ogd-local-forecasting_meta_parameters.csv"
REFERENCE_FILE = "metadata_reference.csv"

def check_metadata():
    # 1. Fetch live metadata
    try:
        live_df = pd.read_csv(METADATA_URL, encoding='latin-1', sep=';')
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        sys.exit(1)

    # 2. Load reference metadata
    if not os.path.exists(REFERENCE_FILE):
        print("Reference file not found. Creating it now.")
        live_df.to_csv(REFERENCE_FILE, index=False)
        return

    ref_df = pd.read_csv(REFERENCE_FILE)

    # 3. Compare structure and critical columns
    # Check for missing/new parameters (shortnames)
    live_params = set(live_df['shortname'].unique())
    ref_params = set(ref_df['shortname'].unique())

    added = live_params - ref_params
    removed = ref_params - live_params

    if added or removed:
        print(f"🚨 METADATA CHANGE DETECTED!")
        if added: print(f"Added parameters: {added}")
        if removed: print(f"Removed parameters: {removed}")
        
        # Update the reference file so the next run is clean
        live_df.to_csv(REFERENCE_FILE, index=False)
        sys.exit(1) # Exit with error to trigger GitHub Action failure
    else:
        print("✅ Metadata is consistent with reference.")

if __name__ == "__main__":
    check_metadata()
