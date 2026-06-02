## Methodology

**Data source:** FDA FAERS quarterly ASCII files, publicly available at fis.fda.gov.

**Pipeline:**
1. Download a FAERS quarter (currently 2024 Q1) and unzip into `data/raw/`.
2. Parse DEMO, DRUG, REAC, OUTC files into pandas DataFrames.
3. Join on `primaryid` to produce a case-level table.
4. Aggregate to drug–event level using primary-suspect drug logic.
5. For each drug–event pair, construct a 2x2 contingency table (cells `a`, `b`, `c`, `d`).
6. Compute disproportionality statistics:
   - **PRR** (Proportional Reporting Ratio)
   - **ROR** (Reporting Odds Ratio)
   - **Chi-square** for association strength
7. Flag pairs as candidate signals where PRR is elevated and chi-square indicates association.
8. Export results to `reports/` as CSV for downstream analysis and dashboarding.

## Tech stack

Python 3.12, pandas, numpy, scipy, pyarrow, tqdm, requests, matplotlib, Streamlit (for dashboard).

## Reproducing the analysis

```powershell
# Clone and set up environment
git clone https://github.com/vaghelazeel/oncosignal.git
cd oncosignal
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Download FAERS 2024 Q1 (one-off)
python src/data/download_faers.py

# Run the analysis pipeline
python src/data/load_faers.py
python src/data/join_faers.py
python src/data/oncology_filter.py
python src/analysis/disproportionality.py
python src/analysis/drug_death_association.py
python src/analysis/plot_drug_death.py
```

Outputs land in `reports/`.

## Important caveats

- **Disproportionality is hypothesis-generating, not causal.** A statistically disproportionate signal indicates a drug–event pair that is reported more often together than expected under independence; it does not establish that the drug caused the event.
- **FAERS is a spontaneous reporting database.** It contains under-reporting, reporting bias, and duplicate cases. Results should be interpreted alongside clinical context and regulatory safety communications.
- **Rare events produce extreme statistics.** Pairs with very small denominators can show PRR values in the hundreds of thousands; these are statistical artefacts and require minimum-case thresholds in any clinical interpretation.

## Roadmap

The original project charter (`docs/project_charter.md`) describes a six-phase ML/NLP extension covering supervised classification of report seriousness, unsupervised clustering of adverse-event profiles, narrative text mining with BERTopic, SHAP interpretation, and comparison against FDA safety-label updates. Phases D, E, and F are planned but not implemented in the current release.

## License

MIT — see LICENSE file.