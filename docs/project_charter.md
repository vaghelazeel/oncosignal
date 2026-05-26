# OncoSignal

**Machine learning for pharmacovigilance signal detection in oncology using FDA FAERS data.**

---

## Project Charter

| | |
|---|---|
| **Author** | Zeel Vaghela |
| **Repository** | github.com/vaghelazeel/oncosignal |
| **Start date** | May 2026 |
| **Target completion** | July 2026 |

---

## 1. Problem statement

Anticancer drugs cause some of the most severe adverse drug reactions in medicine. Pharmacovigilance teams use the FDA Adverse Event Reporting System (FAERS) to detect post-market safety signals. Traditional disproportionality methods (PRR, ROR, IC) are simple, transparent, and regulator-accepted, but suffer from high false positive rates, late detection, and inability to use unstructured narrative text.

This project applies machine learning and natural language processing to FAERS oncology data to:

1. Reproduce traditional disproportionality signal detection
2. Augment it with supervised and unsupervised machine learning
3. Extract additional signal from narrative report text
4. Compare ML-flagged signals against real FDA safety label updates

---

## 2. Research questions

1. For the top 20 anticancer drugs reported in FAERS 2020 to 2024, what are the most disproportionately reported adverse events?
2. Can supervised machine learning classify report seriousness more accurately than rule-based methods?
3. Can unsupervised clustering reveal hidden patterns in oncology ADR profiles?
4. How do ML-detected signals compare to FDA safety label updates in the same period?

---

## 3. Data sources

| Source | Type | Access |
|---|---|---|
| FDA FAERS Quarterly Data | Public ASCII files | fda.gov |
| DrugBank Open Data | Drug metadata, ATC codes | drugbank.com |
| FDA Orange Book | Approved drug list | fda.gov |

**Time window:** 2020 Q1 to 2024 Q4.

---

## 4. Methodology

- **Phase A — Data engineering:** download, parse, clean, deduplicate
- **Phase B — Oncology filtering:** cross-reference with ATC L01 list
- **Phase C — Traditional disproportionality:** PRR, ROR, IC with CIs
- **Phase D — Supervised ML:** classify report seriousness (LR, RF, XGBoost)
- **Phase E — Unsupervised ML:** UMAP + HDBSCAN clustering, BERTopic
- **Phase F — Interpretation:** SHAP, comparison with FDA label updates

---

## 5. Tech stack

Python 3.12 — pandas, numpy, scipy, scikit-learn, xgboost, shap, spacy, bertopic, sentence-transformers, plotly, jupyter.

---

## 6. Deliverables

- Public GitHub repository
- Executive summary README
- 7 reproducible Jupyter notebooks
- Reusable Python modules in `src/`
- Visualisations
- LinkedIn post
- CV bullet point

---

## 7. Success criteria

- Repo is public at github.com/vaghelazeel/oncosignal
- All notebooks run end-to-end on a fresh clone
- At least 3 concrete insights about oncology drug safety
- LinkedIn post published
- CV updated with tailored bullet