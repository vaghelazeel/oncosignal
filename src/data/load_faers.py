import zipfile
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

TABLE_NAMES = ["DEMO", "DRUG", "REAC", "OUTC", "INDI", "THER", "RPSR"]


def get_zip_path(year, quarter):
    filename = f"faers_ascii_{year}q{quarter}.zip"
    return RAW_DATA_DIR / filename


def load_table(year, quarter, table_name):
    if table_name not in TABLE_NAMES:
        raise ValueError(f"Unknown table {table_name}")

    zip_path = get_zip_path(year, quarter)
    if not zip_path.exists():
        raise FileNotFoundError(f"Archive not found: {zip_path}")

    year_short = str(year)[-2:]
    inner_filename = f"ASCII/{table_name}{year_short}Q{quarter}.txt"

    with zipfile.ZipFile(zip_path) as z:
        with z.open(inner_filename) as f:
            df = pd.read_csv(
                f,
                sep="$",
                dtype=str,
                encoding="latin-1",
                on_bad_lines="skip",
                low_memory=False,
            )

    df.columns = [c.strip().lower() for c in df.columns]
    return df


def load_quarter(year, quarter):
    tables = {}
    for name in TABLE_NAMES:
        try:
            tables[name] = load_table(year, quarter, name)
            print(f"Loaded {name}: {len(tables[name])} rows, {len(tables[name].columns)} columns")
        except Exception as e:
            print(f"Error loading {name}: {e}")
    return tables


if __name__ == "__main__":
    tables = load_quarter(2024, 1)
