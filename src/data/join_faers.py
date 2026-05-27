import pandas as pd
from src.data.load_faers import load_table


def drug_reaction_pairs(year, quarter):
    """
    Build a table of every drug-reaction pair from one FAERS quarter.

    Returns one row per (primaryid, drug, reaction) combination.
    Warning: a patient on N drugs reporting M reactions produces N*M rows.
    To count unique patients, deduplicate on primaryid before counting.
    """
    drug = load_table(year, quarter, "DRUG")
    reac = load_table(year, quarter, "REAC")

    drug_slim = drug[["primaryid", "drugname", "role_cod"]].copy()
    reac_slim = reac[["primaryid", "pt"]].copy()
    reac_slim = reac_slim.rename(columns={"pt": "reaction"})

    pairs = drug_slim.merge(reac_slim, on="primaryid", how="inner")

    pairs["drugname"] = pairs["drugname"].str.strip().str.upper()
    pairs["reaction"] = pairs["reaction"].str.strip().str.upper()

    return pairs


def add_demographics(df, year, quarter):
    """
    Attach patient demographics (age, sex, country) to a joined dataframe.
    Input dataframe must have a primaryid column.
    """
    demo = load_table(year, quarter, "DEMO")
    demo_slim = demo[["primaryid", "age", "age_cod", "sex", "occr_country"]].copy()
    return df.merge(demo_slim, on="primaryid", how="left")


def add_outcomes(df, year, quarter):
    """
    Attach outcome flags to a joined dataframe.

    FAERS outcome codes:
      DE = Death
      LT = Life-threatening
      HO = Hospitalization
      DS = Disability
      CA = Congenital anomaly
      RI = Required intervention
      OT = Other serious
    """
    outc = load_table(year, quarter, "OUTC")
    outc_slim = outc[["primaryid", "outc_cod"]].copy()

    outcome_pivot = outc_slim.assign(value=1).pivot_table(
        index="primaryid",
        columns="outc_cod",
        values="value",
        aggfunc="max",
        fill_value=0,
    ).reset_index()

    outcome_pivot.columns.name = None
    outcome_pivot = outcome_pivot.rename(
        columns={c: f"outcome_{c}" for c in outcome_pivot.columns if c != "primaryid"}
    )

    return df.merge(outcome_pivot, on="primaryid", how="left")


def build_full_dataset(year, quarter):
    """
    Build the full analytical dataset for one quarter.
    Returns drug-reaction pairs with demographics and outcomes attached.
    """
    print(f"Building full dataset for {year} Q{quarter}...")
    pairs = drug_reaction_pairs(year, quarter)
    print(f"  Drug-reaction pairs: {len(pairs):,} rows")

    pairs = add_demographics(pairs, year, quarter)
    print(f"  After demographics: {len(pairs):,} rows")

    pairs = add_outcomes(pairs, year, quarter)
    print(f"  After outcomes: {len(pairs):,} rows")

    return pairs


if __name__ == "__main__":
    df = build_full_dataset(2024, 1)
    print()
    print(f"Final shape: {df.shape}")
    print(f"Unique patients: {df['primaryid'].nunique():,}")
    print(f"Unique drugs: {df['drugname'].nunique():,}")
    print(f"Unique reactions: {df['reaction'].nunique():,}")
