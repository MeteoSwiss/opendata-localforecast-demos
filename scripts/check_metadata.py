import pandas as pd
import requests
import os
import sys

# 1. Define URLs and Paths
METADATA_URL = "https://data.geo.admin.ch/ch.meteoschweiz.ogd-local-forecasting/ogd-local-forecasting_meta_parameters.csv"
REFERENCE_FILE = "metadata_reference.csv"

def check_metadata():
    print(f"Fetching current metadata from {METADATA_URL}...")
    try:
        # Fetch current metadata (using latin-1 as per MeteoSwiss OGD specs)
        current_df = pd.read_csv(METADATA_URL, sep=';', encoding='latin-1')
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        sys.exit(1)

    # 2. Check if reference file exists
    if not os.path.exists(REFERENCE_FILE):
        print(f"Reference file {REFERENCE_FILE} not found. Creating it now...")
        current_df.to_csv(REFERENCE_FILE, index=False)
        print("✅ Reference file created. Please commit this to the repo.")
        # We exit with 1 so the GitHub Action knows it needs to COMMIT this new file
        sys.exit(1)

    # 3. Compare with existing reference
    reference_df = pd.read_csv(REFERENCE_FILE)
    
    # Simple comparison (you can make this more complex if needed)
    if current_df.equals(reference_df):
        print("✅ No changes detected in metadata.")
        sys.exit(0)
    else:
        print("⚠️ Metadata changes detected!")
        current_df.to_csv(REFERENCE_FILE, index=False)
        sys.exit(1)

if __name__ == "__main__":
    check_metadata()
