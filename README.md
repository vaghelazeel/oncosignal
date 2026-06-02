# OncoSignal

Pharmacovigilance signal detection on FDA FAERS data using traditional
disproportionality statistics, with a focused oncology drug subset.

**Author:** Zeel Vaghela  
**Repository:** github.com/vaghelazeel/oncosignal

---

## What this project does

OncoSignal ingests the FDA Adverse Event Reporting System (FAERS) quarterly
data, computes traditional disproportionality statistics (PRR, ROR,
chi-square) on all observed drug-event pairs, and surfaces statistically
disproportionate adverse-event signals. The dashboard provides both an
oncology-focused view and a full FAERS comparison view. The current analysis
covers FAERS 2024 Q1.

---

## Live dashboard

**Streamlit Community Cloud:**  
https://oncosignal-siidrexffuouzhakut7vfw.streamlit.app

Local launch:

```bash
streamlit run app.py
```

---

## Current results (FAERS 2024 Q1)

**Full FAERS scope:**
- 87,622 drug-event pairs analysed
- 54,303 flagged as candidate signals
- 2,239 unique drugs, 4,682 unique reactions

**Oncology drug subset:**
- 16,176 drug-event pairs analysed
- 9,400 flagged as candidate signals
- 229 unique oncology drugs, 2,188 unique reactions

Signals recovered include the canonical cytokine release syndrome and immune
effector cell-associated neurotoxicity syndrome for CAR-T therapies
(axicabtagene ciloleucel, tisagenlecleucel), immune-mediated adverse events
for checkpoint inhibitors (pembrolizumab), and the FDA-recognised
neuropsychiatric signal for montelukast — validating that the methodology
recovers known regulatory safety signals.

---

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| A | Data engineering: download, parse, join FAERS quarterly files | Done |
| B | Drug normalisation and oncology filter | Done |
| C | Traditional disproportionality (PRR, ROR, chi-square) | Done |
| D | Streamlit dashboard with oncology and full FAERS scope toggle | Done |
| E | Supervised ML for report seriousness classification | Roadmap |
| F | Unsupervised clustering and BERTopic on narrative text | Roadmap |
| G | SHAP interpretation and FDA safety-label comparison | Roadmap |

---

## Repository structure

oncosignal/
├── app.py                         Streamlit dashboard entry point
├── data/
│   ├── raw/                       FAERS quarterly ZIP files (not tracked in git)
│   ├── interim/                   Parsed intermediate parquet files
│   └── processed/                 Cleaned analysis-ready datasets
├── src/
│   ├── data/
│   │   ├── download_faers.py      FAERS downloader
│   │   ├── load_faers.py          Parser for DEMO, DRUG, REAC, OUTC files
│   │   ├── join_faers.py          Case-level table joins
│   │   └── oncology_filter.py     Oncology drug subset filter
│   └── analysis/
│       ├── disproportionality.py        PRR, ROR, chi-square calculations
│       ├── drug_death_association.py    Fatal-outcome analysis
│       └── plot_drug_death.py           Top-20 visualisation
├── reports/
├── tests/
├── docs/
│   └── project_charter.md
├── requirements.txt
├── requirements-research.txt
└── README.md
## Methodology

**Data source:** FDA FAERS quarterly ASCII files, publicly available at fis.fda.gov.

**Pipeline:**

1. Download a FAERS quarter (currently 2024 Q1) and unzip into `data/raw/`
2. Parse DEMO, DRUG, REAC, OUTC files into pandas DataFrames
3. Join on `primaryid` to produce a case-level table
4. Aggregate to drug-event level using primary-suspect drug logic
5. For each drug-event pair, construct a 2x2 contingency table (cells a, b, c, d)
6. Compute disproportionality statistics: PRR, ROR, chi-square
7. Flag pairs as candidate signals using EMA signal detection criteria:
   PRR ≥ 2, minimum case count (cell a) ≥ 3, and chi-square ≥ 4
8. Export results to `reports/` as CSV for downstream analysis and dashboarding

---

## Reproducing the analysis

```bash
# Clone and set up environment
git clone https://github.com/vaghelazeel/oncosignal.git
cd oncosignal
python -m venv .venv
.venv\Scripts\Activate.ps1

# For the dashboard only (lightweight)
pip install -r requirements.txt

# For the full research pipeline
pip install -r requirements-research.txt

# Download FAERS 2024 Q1 (one-off, around 200 MB)
python src/data/download_faers.py

# Run the analysis pipeline
python src/data/load_faers.py
python src/data/join_faers.py
python src/data/oncology_filter.py
python src/analysis/disproportionality.py
python src/analysis/drug_death_association.py
python src/analysis/plot_drug_death.py

# Launch the dashboard locally
streamlit run app.py
```

Outputs land in `reports/`. The dashboard reads from those CSVs and the
figure in `reports/figures/`.

---

## Important caveats

- **Disproportionality is hypothesis-generating, not causal.** A statistically
  disproportionate signal indicates a drug-event pair reported more often
  together than expected under independence; it does not establish that the
  drug caused the event.
- **FAERS is a spontaneous reporting database.** It contains under-reporting,
  reporting bias, and duplicate cases. Results should be interpreted alongside
  clinical context and regulatory safety communications.
- **Rare events produce extreme statistics.** Pairs with very small
  denominators can show PRR values in the hundreds of thousands; these are
  statistical artefacts and require minimum-case thresholds in any clinical
  interpretation.
- **Drug name normalisation is partial.** Brand names and generic names are
  treated as separate entities in this version. For example, MONTELUKAST and
  SINGULAIR appear as two records rather than one. Mapping to RxNorm is on
  the roadmap.
- **Confounding by indication is unaddressed.** Drugs prescribed for serious
  conditions will show high crude rates of progression and death even if the
  drug has no causal role. This is a well-known limitation of spontaneous
  reporting analysis.
- **Drug-Death Analysis uses the full FAERS dataset, not the oncology subset.**
  This is intentional to provide context, and includes non-oncology drugs that
  emerge in the top rankings (e.g., acetaminophen overdose, fentanyl).

---

## Roadmap

The original project charter (`docs/project_charter.md`) describes a
multi-phase ML and NLP extension covering supervised classification of report
seriousness, unsupervised clustering of adverse-event profiles, narrative text
mining with BERTopic, SHAP interpretation, and comparison against FDA
safety-label updates. Phases E, F, and G are planned but not yet implemented.

---

## Tech stack

**Dashboard:** Python 3.12, Streamlit, pandas, numpy, pyarrow

**Research pipeline:** Python 3.12, pandas, numpy, scipy, pyarrow, tqdm,
requests, matplotlib, seaborn. The roadmap will add scikit-learn, xgboost,
shap, spaCy, BERTopic, sentence-transformers.

---

## License

MIT — see [LICENSE](LICENSE) file.
