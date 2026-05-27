import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"


def plot_top_drugs_by_death(year, quarter, label="primary_suspect"):
    """
    Read the saved drug-death CSV and produce a horizontal bar chart.
    """
    csv_path = REPORTS_DIR / f"drug_death_top_{label}_{year}q{quarter}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    df = df.sort_values("death_patient_count", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(df["drugname"], df["death_patient_count"], color="#8B0000")

    for bar, rate in zip(bars, df["death_rate_pct"]):
        width = bar.get_width()
        ax.text(
            width + 5,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}  ({rate:.1f}%)",
            va="center",
            fontsize=9,
        )

    ax.set_xlabel("Number of unique patients with death outcome", fontsize=11)
    ax.set_ylabel("")
    ax.set_title(
        f"Top 20 drugs by death-associated reports, FAERS {year} Q{quarter}\n"
        f"Primary suspect role, minimum 100 unique patient reports per drug",
        fontsize=12,
        pad=15,
    )
    ax.set_xlim(0, df["death_patient_count"].max() * 1.20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / f"top20_drug_death_{year}q{quarter}.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved {output_path}")
    return output_path


if __name__ == "__main__":
    plot_top_drugs_by_death(2024, 1)