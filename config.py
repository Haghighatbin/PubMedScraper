"""
Configuration file for the PubMed scraper script.
Defines constants, queries, and paths used in the main script.
"""

import os
from typing import List

#: Folder to save the results. Leila: Ensure this directory exists before writing.
RES_DIR: str = "results"

#: Email associated with the NCBI queries (NCBI requires this!).
NCBI_EMAIL: str = "aminhb@tutanota.com"

#: Query to identify Randomised Controlled Trials (RCTs) in PubMed.
RCT_QUERY: str = (
    '("Randomized Controlled Trial"[Publication Type] OR '
    '"Randomized Controlled Trials as Topic"[MeSH Terms] OR '
    '"Random Allocation"[MeSH Terms] OR '

    '"randomized"[Title/Abstract] OR '
    '"randomised"[Title/Abstract] OR '
    '"randomly"[Title/Abstract])'
)

#: Query to identify Critical Care–relevant articles in PubMed.
CRITICAL_QUERY: str = (
    '('
    '"critical care"[MeSH Terms] OR '
    '"intensive care units"[MeSH Terms] OR '
    '"critical illness"[MeSH Terms] OR '
    '"ICU"[Title/Abstract] OR '
    '"high dependency unit*"[Title/Abstract] OR '
    '"respiration, artificial"[MeSH Terms] OR '
    '"intensive care"[Title/Abstract] OR '
    '"intensive care unit"[Title/Abstract] OR '
    '"critical illness"[Title/Abstract] OR '
    '"Critical Care"[Title/Abstract] OR '
    '"critical ill*"[Title/Abstract] OR '
    '"Intensive therapy"[Title/Abstract] OR '
    '"mechanical ventilation"[Title/Abstract] OR '
    '"mechanical ventilat*"[Title/Abstract]) OR '
    '("mechanical"[Title/Abstract] AND "ventilation"[Title/Abstract])'
    ')'
)

#: Filter to include only human studies in PubMed.
HUMANS_FILTER: str = '"humans"[MeSH Terms]'

#: Exclusion query to filter out reviews and meta-analyses.
EXCLUSION_QUERY: str = (
    'NOT ("systematic review"[Publication Type] OR '
    '"Meta-Analysis"[Publication Type] OR '
    '"Review"[Publication Type])'
)

#: List of target journals (using PubMed’s [TA] field format).
JOURNALS: List[str] = [
    "The New England Journal of Medicine",
    "Lancet",
    "JAMA",
    "American Journal of Respiratory and Critical Care Medicine",
    "Intensive Care Medicine",
    "Critical Care Medicine",
    "Critical care",
    "Chest",
    "BMJ",
    "Annals of Intensive care",
    "JAMA Internal Medicine",
    "JAMA Network Open",
    "Annals of the American Thoracic Society"
]

#: Date range query (January 2020 to January 2025).
DATE_QUERY: str = '("2020/01/01"[PDAT]:"2025/01/01"[PDAT])'

#: Template for PubMed links, formatted with the PMID.
LINK_TEMPLATE: str = "https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

#: Excel output column headers for final results.
OUTPUT_HEADERS: List[str] = [
    "Journal_TTL",
    "Journal_ABBRV",
    "Title",
    "Year",
    "Pages",
    "Issue",
    "Volume",
    "First Author",
    "First Author Affiliation",
    "Last Author",
    "Last Author Affiliation",
    "DOI",
    "Link",
    "Authors"
]
