"""
OncoSignal Streamlit Dashboard
Interactive view of FAERS 2024 Q1 disproportionality analysis.
"""

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

# Make src importable
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.oncology_filter import ONCOLOGY_DRUGS, filter_to_oncology


# --- Page config ---
st.set_page_config(
    page_title="OncoSignal",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Paths ---
REPORTS_DIR = PROJECT_ROOT / "reports"


# --- Data loading (cached) ---
@st.cache_data
def load_signals():
    path = REPORTS_DIR / "disproportionality_signals_2024q1.csv"
    return pd.read_csv(path)


@st.cache_data
def load_full():
    path = REPORTS_DIR / "disproportionality_full_2024q1.csv"
    return pd.read_csv(path)


@st.cache_data
def load_drug_death():
    path = REPORTS_DIR / "drug_death_top_primary_suspect_2024q1.csv"
    return pd.read_csv(path)


# --- Sidebar ---
st.sidebar.title("OncoSignal")
st.sidebar.markdown("**FAERS 2024 Q1 Signal Detection**")
st.sidebar.markdown("---")

scope = st.sidebar.radio(
    "Drug scope",
    ["Oncology only", "All drugs (full FAERS)"],
    index=0,
    help=(
        "Oncology only filters to a curated list of cancer drugs. "
        "All drugs shows the complete FAERS dataset for comparison."
    ),
)

page = st.sidebar.radio(
    "Page",
    ["Overview", "Signal Table", "Drug Detail", "Drug-Death Analysis"],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data source: FDA Adverse Event Reporting System (FAERS), 2024 Q1. "
    "This dashboard is hypothesis-generating; signals do not imply causation."
)


# --- Load and apply scope filter ---
signals_df_raw = load_signals()
full_df_raw = load_full()
drug_death_df = load_drug_death()

if scope == "Oncology only":
    signals_df = filter_to_oncology(signals_df_raw)
    full_df = filter_to_oncology(full_df_raw)
    scope_label = "oncology drugs"
else:
    signals_df = signals_df_raw
    full_df = full_df_raw
    scope_label = "all drugs"


# ============================================================
# PAGE: Overview
# ============================================================
if page == "Overview":
    st.title("OncoSignal Dashboard")
    st.markdown(
        f"Pharmacovigilance signal detection on FDA FAERS data using "
        f"traditional disproportionality statistics. "
        f"Current view: **{scope_label}**."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Drug-event pairs", f"{len(full_df):,}")
    col2.metric("Candidate signals", f"{len(signals_df):,}")
    col3.metric("Unique drugs", f"{full_df['drugname'].nunique():,}")
    col4.metric("Unique reactions", f"{full_df['reaction'].nunique():,}")

    st.markdown("---")
    st.subheader(f"Top 10 signals by chi-square ({scope_label})")
    st.caption("Minimum 10 cases per drug-event pair to reduce statistical artefacts.")

    top_signals = (
        signals_df[signals_df["a"] >= 10]
        .sort_values("chi_square", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    if len(top_signals) == 0:
        st.info(
            "No signals meet the minimum 10-case threshold in the current scope. "
            "Switch to 'All drugs' or lower the threshold on the Signal Table page."
        )
    else:
        st.dataframe(top_signals, width="stretch")

    st.markdown("---")
    st.subheader("Methodology")
    st.markdown(
        "Each drug-event pair is mapped to a 2x2 contingency table with cells "
        "**a** (reports with drug AND event), **b** (drug, other events), "
        "**c** (other drugs, event), **d** (other drugs, other events). "
        "From this, PRR, ROR and chi-square are computed. A pair is flagged "
        "as a candidate signal when PRR is elevated and chi-square indicates "
        "a significant association."
    )


# ============================================================
# PAGE: Signal Table
# ============================================================
elif page == "Signal Table":
    st.title("Signal Table")
    st.markdown(
        f"All drug-event pairs flagged as candidate signals ({scope_label}). "
        "Filter by drug, reaction, or thresholds."
    )

    col1, col2 = st.columns(2)
    with col1:
        drug_query = st.text_input("Drug name contains (optional)").strip().upper()
    with col2:
        reaction_query = st.text_input("Reaction contains (optional)").strip().upper()

    col3, col4 = st.columns(2)
    with col3:
        min_a = st.number_input("Minimum cases (cell a)", min_value=1, value=3, step=1)
    with col4:
        min_prr = st.number_input("Minimum PRR", min_value=1.0, value=2.0, step=0.5)

    filtered = signals_df.copy()
    if drug_query:
        filtered = filtered[filtered["drugname"].str.contains(drug_query, na=False)]
    if reaction_query:
        filtered = filtered[filtered["reaction"].str.contains(reaction_query, na=False)]
    filtered = filtered[filtered["a"] >= min_a]
    filtered = filtered[filtered["prr"] >= min_prr]
    filtered = filtered.sort_values("chi_square", ascending=False)

    st.markdown(f"**{len(filtered):,} rows match your filters.**")
    st.dataframe(filtered.reset_index(drop=True), width="stretch", height=600)

    csv = filtered.to_csv(index=False)
    st.download_button(
        "Download filtered results as CSV",
        data=csv,
        file_name="filtered_signals.csv",
        mime="text/csv",
    )


# ============================================================
# PAGE: Drug Detail
# ============================================================
elif page == "Drug Detail":
    st.title("Drug Detail")
    st.markdown(
        f"Inspect the full adverse-event profile for a single drug ({scope_label})."
    )

    drug_list = sorted(full_df["drugname"].dropna().unique().tolist())
    if not drug_list:
        st.info("No drugs available in the current scope.")
    else:
        selected_drug = st.selectbox("Select a drug", drug_list)
        if selected_drug:
            drug_data = full_df[full_df["drugname"] == selected_drug].sort_values(
                "chi_square", ascending=False
            )
            signal_count = int(drug_data["is_signal"].sum())

            col1, col2, col3 = st.columns(3)
            col1.metric("Total reactions reported", f"{len(drug_data):,}")
            col2.metric("Flagged as signals", f"{signal_count:,}")
            col3.metric(
                "Max chi-square",
                f"{drug_data['chi_square'].max():,.0f}" if len(drug_data) else "—",
            )

            st.markdown("---")
            st.subheader(f"All reactions reported for {selected_drug}")
            st.dataframe(
                drug_data.reset_index(drop=True),
                width="stretch",
                height=500,
            )


# ============================================================
# PAGE: Drug-Death Analysis
# ============================================================
elif page == "Drug-Death Analysis":
    st.title("Drug-Death Analysis")
    st.markdown(
        "This page is a **separate analysis** from the disproportionality signals. "
        "It shows crude fatal-outcome rates among primary-suspect drugs in FAERS 2024 Q1. "
        "Unlike the other pages, this view always shows the full top-20 from the source "
        "analysis (not filtered by the sidebar scope) and includes non-oncology drugs "
        "that emerged in the top rankings."
    )

    st.markdown(
        "**Death rate %** = patients with fatal outcome ÷ total patients reported "
        "with the drug as primary suspect."
    )

    sorted_dd = drug_death_df.sort_values(
        "death_rate_pct", ascending=False
    ).reset_index(drop=True)
    st.dataframe(sorted_dd, width="stretch")

    st.markdown("---")
    st.subheader("Visualisation")
    figure_path = PROJECT_ROOT / "reports" / "figures" / "top20_drug_death_2024q1.png"
    if figure_path.exists():
        st.image(str(figure_path), caption="Top 20 drugs by death rate (FAERS 2024 Q1)")
    else:
        st.info("Figure file not found.")

    st.markdown(
        "**Caveat:** A high death rate in FAERS does not imply the drug caused the deaths. "
        "Patients receiving these drugs may have advanced disease, multiple comorbidities, "
        "and high baseline mortality risk. The presence of non-oncology drugs (e.g. "
        "acetaminophen overdose, fentanyl) reflects FAERS as a general adverse-event "
        "registry, not an oncology-specific database."
    )