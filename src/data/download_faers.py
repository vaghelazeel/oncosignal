import os
import requests
from pathlib import Path
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
FAERS_BASE_URL = "https://fis.fda.gov/content/Exports"
QUARTERS = [(y, q) for y in range(2020, 2025) for q in range(1, 5)]


def build_faers_url(year, quarter):
    filename = f"faers_ascii_{year}q{quarter}.zip"
    return f"{FAERS_BASE_URL}/{filename}"


def build_output_path(year, quarter):
    filename = f"faers_ascii_{year}q{quarter}.zip"
    return RAW_DATA_DIR / filename


def download_quarter(year, quarter, overwrite=False):
    if year < 2012 or year > 2025:
        raise ValueError(f"Year {year} outside valid FAERS range")
    if quarter not in (1, 2, 3, 4):
        raise ValueError(f"Quarter must be 1 to 4, got {quarter}")
    output_path = build_output_path(year, quarter)
    if output_path.exists() and not overwrite:
        size_mb = output_path.stat().st_size / 1e6
        print(f"{output_path.name} already exists ({size_mb:.1f} MB), skipping")
        return output_path
    url = build_faers_url(year, quarter)
    print(f"Downloading {year} Q{quarter} from {url}")
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    with open(output_path, "wb") as f:
        with tqdm(total=total_size, unit="B", unit_scale=True, desc=output_path.name, ncols=80) as progress:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                progress.update(len(chunk))
    size_mb = output_path.stat().st_size / 1e6
    print(f"Saved {output_path.name} ({size_mb:.1f} MB)")
    return output_path


def download_all(overwrite=False):
    print(f"Downloading {len(QUARTERS)} FAERS quarters to {RAW_DATA_DIR}")
    downloaded = []
    failed = []
    for year, quarter in QUARTERS:
        try:
            path = download_quarter(year, quarter, overwrite=overwrite)
            downloaded.append(path)
        except requests.HTTPError as e:
            print(f"Failed {year} Q{quarter}: HTTP {e.response.status_code}")
            failed.append((year, quarter, str(e)))
        except Exception as e:
            print(f"Failed {year} Q{quarter}: {e}")
            failed.append((year, quarter, str(e)))
    print(f"Complete: {len(downloaded)} of {len(QUARTERS)}")
    if failed:
        print(f"Failed: {len(failed)}")
    return downloaded


if __name__ == "__main__":
    download_all()
