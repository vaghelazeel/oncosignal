"""
FAERS Quarterly Data Downloader

Downloads FDA Adverse Event Reporting System ASCII data archives
from the FDA public export server. Each quarter is saved as a
ZIP file in the data/raw directory.
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

FAERS_BASE_URL = "https://fis.fda.gov/content/Exports"

QUARTERS = [
    (year, q)
    for year in range(2020, 2025)
    for q in range(1, 5)
]


def build_faers_url(year, quarter):
    """Return the FDA download URL for a given FAERS quarter."""
    filename = f"faers_ascii_{year}q{quarter}.zip"
    return f"{FAERS_BASE_URL}/{filename}"


def build_output_path(year, quarter):
    """Return the local save path for a given FAERS quarter."""
    filename = f"faers_ascii_{year}q{qua