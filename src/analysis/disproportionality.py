import pandas as pd
import numpy as np
from pathlib import Path
from src.data.join_faers import load_full_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"


def calculate_prr_ror(year, quarter, role_filter="PS", min_reports=3):
    """
    Calculate Proportional Reporting Ratio (PRR) and Reporting Odds Ratio (ROR)
    for every drug-reaction pair in one FAERS quarter.

    For each drug-reaction pair, builds a 2x2 contingency table:
                       Reaction = X    Reaction != X
        Drug = D            a               b
        Drug != D           c               d

    PRR = (a / (a + b)) / (c / (c + d))
    ROR = (a / b) / (c / d) = (a * d) / (b * c)

    EMA signal criteria (commonly used):
      PRR >= 2 AND chi-square >= 4 AND a >= 3

    Parameters
    ----------
    year : int
    quarter : int
    role_filter : str or None
        Filter to specific drug role. 'PS' = Primary Suspect.
    min_reports : int
        Minimum a (joint count) to include the pair in output.

    Returns
    -------
    pandas.DataFrame with columns:
        drugname, reaction, a, b, c, d, prr, ror, chi_square, is_signal
    """
    print(f"Loading dataset for {year} Q{quarter}...")
    df = load_full_dataset(year, quarter)
    print(f"Loaded {len(df):,} rows")

    if role_filter is not None:
        before = len(df)
        df = df[df["role_cod"] == role_filter]
        print(f"Filtered to role_cod='{role_filter}': {before:,} -> {len(df):,} rows")

    df = df[["primaryid", "drugname", "reaction"]].dropna()
    df = df.drop_duplicates(subset=["primaryid", "drugname", "reaction"])
    print(f"Unique (patient, drug, reaction) triples: {len(df):,}")

    total_reports = df["primaryid"].nunique()
    print(f"Total unique patients: {total_reports:,}")

    print("Building contingency table counts...")
    pair_counts = df.groupby(["drugname", "reaction"]).size().reset_index(name="a")
    pair_counts = pair_counts[pair_counts["a"] >= min_reports]
    print(f"Drug-reaction pairs with at least {min_reports} reports: {len(pair_counts):,}")

    drug_totals = df.groupby("drugname")["primaryid"].nunique().reset_index(name="drug_total")
    reaction_totals = df.groupby("reaction")["primaryid"].nunique().reset_index(name="reaction_total")

    result = pair_counts.merge(drug_totals, on="drugname")
    result = result.merge(reaction_totals, on="reaction")

    result["b"] = result["drug_total"] - result["a"]
    result["c"] = result["reaction_total"] - result["a"]
    result["d"] = total_reports - result["a"] - result["b"] - result["c"]

    result = result[(result["b"] > 0) & (result["c"] > 0) & (result["d"] > 0)]

    a = result["a"]
    b = result["b"]
    c = result["c"]
    d = result["d"]

    result["prr"] = (a / (a + b)) / (c / (c + d))
    result["ror"] = (a * d) / (b * c)

    n = a + b + c + d
    expected_a = (a + b) * (a + c) / n
    expected_b = (a + b) * (b + d) / n
    expected_c = (c + d) * (a + c) / n
    expected_d = (c + d) * (b + d) / n

    result["chi_square"] = (
        ((a - expected_a) ** 2 / expected_a)
        + ((b - expected_b) ** 2 / expected_b)
        + ((c - expected_c) ** 2 / expected_c)
        + ((d - expected_d) ** 2 / expected_d)
    )

    result["is_signal"] = (
        (result["prr"] >= 2) & (result["chi_square"] >= 4) & (result["a"] >= 3)
    )

    result = result[
        ["drugname", "reaction", "a", "b", "c", "d", "prr", "ror", "chi_square", "is_signal"]
    ]
    result = result.sort_values("prr", ascending=False).reset_index(drop=True)

    return result


def save_signals(df, year, quarter, role_filter="PS"):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    full_path = REPORTS_DIR / f"disproportionality_full_{year}q{quarter}.csv"
    df.to_csv(full_path, index=False)
    print(f"Saved full results: {full_path.name} ({len(df):,} pairs)")

    signals_only = df[df["is_signal"]].copy()
    signals_path = REPORTS_DIR / f"disproportionality_signals_{year}q{quarter}.csv"
    signals_only.to_csv(signals_path, index=False)
    print(f"Saved signals only: {signals_path.name} ({len(signals_only):,} signals)")

    return full_path, signals_path


if __name__ == "__main__":
    print("=" * 70)
    print(f"Disproportionality analysis (PRR, ROR), FAERS 2024 Q1")
    print(f"Primary suspect role only")
    print(f"EMA signal criteria: PRR >= 2, chi-square >= 4, a >= 3")
    print("=" * 70)
    print()

    results = calculate_prr_ror(2024, 1, role_filter="PS", min_reports=3)

    print()
    print(f"Total drug-reaction pairs analysed: {len(results):,}")
    print(f"Pairs meeting EMA signal criteria: {results['is_signal'].sum():,}")
    print()

    print("Top 20 signals by PRR (filtered to a >= 10 to avoid sparse pairs):")
    print()
    top_signals = results[(results["is_signal"]) & (results["a"] >= 10)].head(20)
    print(top_signals[["drugname", "reaction", "a", "prr", "ror", "chi_square"]].to_string(index=False))

    print()
    save_signals(results, 2024, 1)