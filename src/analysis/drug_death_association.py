import pandas as pd
from pathlib import Path
from src.data.join_faers import load_full_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"


def drugs_by_death_count(year, quarter, top_n=20, role_filter=None):
    """
    Rank drugs by the number of unique patients who died after reports
    that listed the drug.

    IMPORTANT: this is a descriptive count, not a causal claim.
    A drug may rank high because:
      - it is genuinely associated with deaths, OR
      - it is very commonly prescribed to seriously ill patients, OR
      - it is reported alongside another suspect drug
    Disproportionality analysis (PRR, ROR) is needed to assess signals.

    Parameters
    ----------
    year : int
    quarter : int
    top_n : int
        Number of top drugs to return.
    role_filter : str or None
        If provided, only count drug entries where role_cod matches.
        Common values:
          'PS' = Primary Suspect drug
          'SS' = Secondary Suspect drug
          'C'  = Concomitant drug
          'I'  = Interacting drug
        Filtering to 'PS' is the most clinically meaningful for safety signals.

    Returns
    -------
    pandas.DataFrame with columns: drugname, death_patient_count, total_patient_count, death_rate_pct
    """
    print(f"Loading dataset for {year} Q{quarter}...")
    df = load_full_dataset(year, quarter)
    print(f"Loaded {len(df):,} rows")

    if role_filter is not None:
        before = len(df)
        df = df[df["role_cod"] == role_filter]
        print(f"Filtered to role_cod='{role_filter}': {before:,} -> {len(df):,} rows")

    if "outcome_DE" not in df.columns:
        raise ValueError("Column outcome_DE not found in dataset")

    df["outcome_DE"] = pd.to_numeric(df["outcome_DE"], errors="coerce").fillna(0)

    deduped = df.drop_duplicates(subset=["primaryid", "drugname"])
    print(f"Deduplicated to unique (patient, drug) combinations: {len(deduped):,}")

    grouped = deduped.groupby("drugname").agg(
        death_patient_count=("outcome_DE", "sum"),
        total_patient_count=("primaryid", "nunique"),
    ).reset_index()

    grouped["death_rate_pct"] = (
        grouped["death_patient_count"] / grouped["total_patient_count"] * 100
    ).round(2)

    grouped = grouped[grouped["total_patient_count"] >= 100]

    ranked = grouped.sort_values("death_patient_count", ascending=False).head(top_n)
    return ranked.reset_index(drop=True)


def save_results(df, year, quarter, label):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / f"drug_death_top_{label}_{year}q{quarter}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {output_path.name}")
    return output_path


if __name__ == "__main__":
    print("=" * 70)
    print("Top 20 drugs by death-associated patient count, 2024 Q1")
    print("Primary suspect role only (role_cod = 'PS')")
    print("Minimum 100 unique patient reports per drug")
    print("=" * 70)
    print()

    results = drugs_by_death_count(2024, 1, top_n=20, role_filter="PS")
    print()
    print(results.to_string(index=False))
    print()
    save_results(results, 2024, 1, "primary_suspect")
