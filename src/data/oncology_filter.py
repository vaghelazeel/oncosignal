"""
Oncology drug filter for FAERS analysis.

The ONCOLOGY_DRUGS set contains generic and brand names of major
anti-cancer agents across all main drug classes used in oncology.
Names are stored in uppercase to match FAERS drug name conventions.

Coverage includes:
  - Immune checkpoint inhibitors (PD-1, PD-L1, CTLA-4)
  - Targeted small-molecule kinase inhibitors
  - Monoclonal antibodies
  - Cytotoxic chemotherapy
  - Hormonal agents
  - CAR-T cell therapies
  - Antibody-drug conjugates
  - Selected immunomodulators used in haematological malignancies

This list is not exhaustive. It captures the most clinically important
and most frequently reported oncology drugs in FAERS.
"""

ONCOLOGY_DRUGS = {
    # Immune checkpoint inhibitors
    "PEMBROLIZUMAB", "KEYTRUDA",
    "NIVOLUMAB", "OPDIVO",
    "ATEZOLIZUMAB", "TECENTRIQ",
    "DURVALUMAB", "IMFINZI",
    "AVELUMAB", "BAVENCIO",
    "IPILIMUMAB", "YERVOY",
    "CEMIPLIMAB", "LIBTAYO",
    "DOSTARLIMAB", "JEMPERLI",

    # EGFR inhibitors (lung cancer, etc.)
    "OSIMERTINIB", "TAGRISSO",
    "ERLOTINIB", "TARCEVA",
    "GEFITINIB", "IRESSA",
    "AFATINIB", "GILOTRIF",
    "CETUXIMAB", "ERBITUX",
    "PANITUMUMAB", "VECTIBIX",
    "AMIVANTAMAB", "RYBREVANT",

    # BTK inhibitors
    "IBRUTINIB", "IMBRUVICA",
    "ACALABRUTINIB", "CALQUENCE",
    "ZANUBRUTINIB", "BRUKINSA",

    # BCL-2 inhibitor
    "VENETOCLAX", "VENCLEXTA",

    # CDK4/6 inhibitors (breast cancer)
    "PALBOCICLIB", "IBRANCE",
    "RIBOCICLIB", "KISQALI",
    "ABEMACICLIB", "VERZENIO",

    # HER2 inhibitors
    "TRASTUZUMAB", "HERCEPTIN",
    "PERTUZUMAB", "PERJETA",
    "TRASTUZUMAB EMTANSINE", "KADCYLA",
    "TRASTUZUMAB DERUXTECAN", "ENHERTU",
    "TUCATINIB", "TUKYSA",
    "LAPATINIB", "TYKERB",

    # VEGF / VEGFR inhibitors
    "BEVACIZUMAB", "AVASTIN",
    "SORAFENIB", "NEXAVAR",
    "SUNITINIB", "SUTENT",
    "PAZOPANIB", "VOTRIENT",
    "AXITINIB", "INLYTA",
    "CABOZANTINIB", "CABOMETYX", "COMETRIQ",
    "LENVATINIB", "LENVIMA",
    "REGORAFENIB", "STIVARGA",
    "RAMUCIRUMAB", "CYRAMZA",

    # BRAF / MEK inhibitors (melanoma)
    "VEMURAFENIB", "ZELBORAF",
    "DABRAFENIB", "TAFINLAR",
    "ENCORAFENIB", "BRAFTOVI",
    "TRAMETINIB", "MEKINIST",
    "COBIMETINIB", "COTELLIC",
    "BINIMETINIB", "MEKTOVI",

    # ALK / ROS1 inhibitors
    "CRIZOTINIB", "XALKORI",
    "ALECTINIB", "ALECENSA",
    "BRIGATINIB", "ALUNBRIG",
    "LORLATINIB", "LORBRENA",
    "CERITINIB", "ZYKADIA",

    # JAK inhibitors (myelofibrosis, polycythaemia)
    "RUXOLITINIB", "JAKAFI",
    "FEDRATINIB", "INREBIC",

    # mTOR inhibitors
    "EVEROLIMUS", "AFINITOR",
    "TEMSIROLIMUS", "TORISEL",

    # PARP inhibitors
    "OLAPARIB", "LYNPARZA",
    "RUCAPARIB", "RUBRACA",
    "NIRAPARIB", "ZEJULA",
    "TALAZOPARIB", "TALZENNA",

    # CAR-T therapies
    "AXICABTAGENE CILOLEUCEL", "YESCARTA",
    "TISAGENLECLEUCEL", "KYMRIAH",
    "BREXUCABTAGENE AUTOLEUCEL", "TECARTUS",
    "LISOCABTAGENE MARALEUCEL", "BREYANZI",
    "IDECABTAGENE VICLEUCEL", "ABECMA",
    "CILTACABTAGENE AUTOLEUCEL", "CARVYKTI",

    # Anti-CD20 / anti-CD38 / anti-SLAMF7 antibodies
    "RITUXIMAB", "RITUXAN",
    "OBINUTUZUMAB", "GAZYVA",
    "OFATUMUMAB", "ARZERRA",
    "DARATUMUMAB", "DARZALEX",
    "ISATUXIMAB", "SARCLISA",
    "ELOTUZUMAB", "EMPLICITI",

    # Multiple myeloma (IMiDs and proteasome inhibitors)
    "LENALIDOMIDE", "REVLIMID",
    "POMALIDOMIDE", "POMALYST",
    "THALIDOMIDE", "THALOMID",
    "BORTEZOMIB", "VELCADE",
    "CARFILZOMIB", "KYPROLIS",
    "IXAZOMIB", "NINLARO",

    # Hormonal therapies (breast and prostate cancer)
    "TAMOXIFEN",
    "ANASTROZOLE", "ARIMIDEX",
    "LETROZOLE", "FEMARA",
    "EXEMESTANE", "AROMASIN",
    "FULVESTRANT", "FASLODEX",
    "ABIRATERONE", "ZYTIGA",
    "ENZALUTAMIDE", "XTANDI",
    "APALUTAMIDE", "ERLEADA",
    "DAROLUTAMIDE", "NUBEQA",
    "LEUPROLIDE", "LUPRON", "ELIGARD",
    "GOSERELIN", "ZOLADEX",
    "BICALUTAMIDE", "CASODEX",

    # FLT3 / IDH inhibitors (AML)
    "MIDOSTAURIN", "RYDAPT",
    "GILTERITINIB", "XOSPATA",
    "QUIZARTINIB", "VANFLYTA",
    "IVOSIDENIB", "TIBSOVO",
    "ENASIDENIB", "IDHIFA",

    # Antibody-drug conjugates
    "BRENTUXIMAB VEDOTIN", "ADCETRIS",
    "INOTUZUMAB OZOGAMICIN", "BESPONSA",
    "GEMTUZUMAB OZOGAMICIN", "MYLOTARG",
    "POLATUZUMAB VEDOTIN", "POLIVY",
    "ENFORTUMAB VEDOTIN", "PADCEV",
    "SACITUZUMAB GOVITECAN", "TRODELVY",

    # KRAS G12C inhibitors
    "SOTORASIB", "LUMAKRAS",
    "ADAGRASIB", "KRAZATI",

    # Cytotoxic chemotherapy
    "CISPLATIN",
    "CARBOPLATIN",
    "OXALIPLATIN",
    "DOXORUBICIN", "ADRIAMYCIN",
    "DAUNORUBICIN",
    "EPIRUBICIN",
    "IDARUBICIN",
    "PACLITAXEL", "TAXOL",
    "DOCETAXEL", "TAXOTERE",
    "CABAZITAXEL", "JEVTANA",
    "VINCRISTINE",
    "VINBLASTINE",
    "VINORELBINE",
    "CYCLOPHOSPHAMIDE", "CYTOXAN",
    "IFOSFAMIDE", "IFEX",
    "METHOTREXATE",
    "FLUOROURACIL", "5-FU",
    "CAPECITABINE", "XELODA",
    "GEMCITABINE", "GEMZAR",
    "CYTARABINE",
    "AZACITIDINE", "VIDAZA",
    "DECITABINE", "DACOGEN",
    "FLUDARABINE",
    "TEMOZOLOMIDE", "TEMODAR",
    "BENDAMUSTINE", "TREANDA",
    "BLEOMYCIN",
    "ETOPOSIDE",
    "IRINOTECAN", "CAMPTOSAR",
    "TOPOTECAN", "HYCAMTIN",
    "MELPHALAN", "ALKERAN",
    "CHLORAMBUCIL", "LEUKERAN",
    "BUSULFAN", "MYLERAN",
    "DACARBAZINE", "DTIC",
    "MITOMYCIN", "MUTAMYCIN",

    # Bispecific antibodies and others
    "BLINATUMOMAB", "BLINCYTO",
    "TEPLIZUMAB", "TZIELD",
    "MOSUNETUZUMAB", "LUNSUMIO",
    "EPCORITAMAB", "EPKINLY",
    "GLOFITAMAB", "COLUMVI",
    "TALQUETAMAB", "TALVEY",
    "TECLISTAMAB", "TECVAYLI",
    "ELRANATAMAB", "ELREXFIO",

    # Other notable agents
    "IMATINIB", "GLEEVEC",
    "DASATINIB", "SPRYCEL",
    "NILOTINIB", "TASIGNA",
    "PONATINIB", "ICLUSIG",
    "BOSUTINIB", "BOSULIF",
    "ASCIMINIB", "SCEMBLIX",
    "HYDROXYUREA",
    "ARSENIC TRIOXIDE", "TRISENOX",
    "TRETINOIN",
    "INTERFERON ALFA",
    "ALDESLEUKIN", "PROLEUKIN",
}


def filter_to_oncology(df, drug_column="drugname"):
    """
    Filter a dataframe to rows where the drug name matches a known oncology drug.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain a column with drug names (uppercase strings).
    drug_column : str
        Name of the column holding drug names.

    Returns
    -------
    pandas.DataFrame
        Subset of df containing only oncology drug rows.
    """
    if drug_column not in df.columns:
        raise ValueError(f"Column '{drug_column}' not found in dataframe")
    return df[df[drug_column].isin(ONCOLOGY_DRUGS)].copy()


def list_oncology_matches(df, drug_column="drugname"):
    """
    Return a sorted list of unique oncology drug names found in the dataframe.
    Useful for diagnosing coverage of the curated list.
    """
    if drug_column not in df.columns:
        raise ValueError(f"Column '{drug_column}' not found in dataframe")
    matched = df[df[drug_column].isin(ONCOLOGY_DRUGS)][drug_column].unique()
    return sorted(matched)


if __name__ == "__main__":
    print(f"Oncology drug list contains {len(ONCOLOGY_DRUGS):,} entries")
    print("(includes both generic and brand names)")