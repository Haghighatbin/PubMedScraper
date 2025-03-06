import os
import re
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
from Bio import Entrez, Medline
from rich.console import Console
from rich.panel import Panel
from rich.status import Status

import config

# Ensure the results directory exists.
os.makedirs(config.RES_DIR, exist_ok=True)

# Set the email to use with NCBI requests.
Entrez.email = config.NCBI_EMAIL

console = Console()

class PubMedScraper:
    """
    A class to query PubMed for records using specified RCT and critical care filters,
    process the records, and save the results in an Excel file.
    """

    def __init__(self) -> None:
        """
        Initialise the scraper, setting up a timestamped Excel filename in the results folder.
        """
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.excel_filename: str = os.path.join(config.RES_DIR, f"pubmed_results_{timestamp}.xlsx")
        self.all_data: List[Dict[str, Any]] = []
        console.log(
            f"\n[green]Initialised PubMedScraper.[/green]"
            f"Output file: [bold]{self.excel_filename}[/bold]\n"
        )

    def construct_query(self, journal: str) -> str:
        """
        Construct and return a PubMed query string for a specified journal.

        :param journal: The name of the journal for the [TA] field in PubMed.
        :return: The complete query string to be used in PubMed search.
        """
        journal_query = f'"{journal}"[Journal]'
        # query = (
        #     f'({config.RCT_QUERY} AND {config.CRITICAL_QUERY} 
        #       AND ({journal_query}) AND {config.DATE_QUERY}
        #       AND {config.HUMANS_FILTER}) '
        #     f'NOT {config.EXCLUSION_QUERY})'
        # )
        query = (
            f'({config.RCT_QUERY} AND {config.CRITICAL_QUERY} AND ({journal_query}) AND {config.DATE_QUERY} '
            f'{")" if journal.lower() == "annals of intensive care" else f"AND {config.HUMANS_FILTER})"} '
            f'NOT {config.EXCLUSION_QUERY}'
        )
        return query

    def fetch_records(self, query: str, retmax: int = config.MAX_QUERIES) -> List[Dict[str, Any]]:
        """
        Execute a PubMed search query and retrieve MEDLINE records.

        :param query: The PubMed query string to search.
        :param retmax: Maximum number of records to retrieve.
        :return: A list of MEDLINE records, each represented as a dictionary.
        """
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
            search_results = Entrez.read(handle)
            handle.close()
            pmid_list = search_results.get("IdList", [])

            if not pmid_list:
                # console.log(f"[yellow]No records found for query:[/yellow] {query}")
                return []

            handle = Entrez.efetch(db="pubmed", id=pmid_list, rettype="medline", retmode="text")
            records = list(Medline.parse(handle))
            handle.close()
            console.log(f"[green]Fetched {len(records)} records.[/green]")
            return records

        except Exception as e:
            console.log(f"[red]Error fetching records:[/red] {e}")
            return []

    def process_record(self, rec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant fields from a single MEDLINE record.

        :param rec: A single MEDLINE record as a dictionary.
        :return: A dictionary of the extracted data, or an empty dict if an error occurs.
        """
        try:
            journal_title: str = rec.get("JT", "")
            journal_abstract: str = rec.get("TA", "")
            title: str = rec.get("TI", "")
            dp: str = rec.get("DP", "")
            
            year_match = re.search(r"\d{4}", dp)
            year: str = year_match.group(0) if year_match else ""

            issue: str = rec.get("IP", "")
            volume: str = rec.get("VI", "")
            pages: str = rec.get("PG", "")

            authors: List[str] = rec.get("AU", [])
            first_author: str = authors[0] if authors else ""
            last_author: str = authors[-1] if authors else ""

            affiliations = rec.get("AD", "")
            first_author_affiliation: str = affiliations[0] if affiliations else ""
            last_author_affiliation: str = affiliations[-1] if affiliations else ""

            doi: str = ""
            lid = rec.get("LID", "")
            if lid:
                doi_match = re.search(r"(10\.\S+)", lid)
                if doi_match:
                    doi = doi_match.group(1)

            if not doi and "AID" in rec:
                aids = rec["AID"]
                if isinstance(aids, list):
                    for aid in aids:
                        if "[doi]" in aid:
                            doi = aid.split(" [doi]")[0]
                            break
                else:
                    if "[doi]" in aids:
                        doi = aids.split(" [doi]")[0]

            pmid: str = rec.get("PMID", "")
            link: str = config.LINK_TEMPLATE.format(pmid=pmid) if pmid else ""

            return {
                "Journal_TTL": journal_title,
                "Journal_ABBRV": journal_abstract,
                "Title": title,
                "Year": year,
                "Pages": pages,
                "Issue": issue,
                "Volume": volume,
                "First Author": first_author,
                "First Author Affiliation": first_author_affiliation,
                "Last Author": last_author,
                "Last Author Affiliation": last_author_affiliation,
                "DOI": doi,
                "Link": link,
                "Authors": authors,
            }

        except Exception as e:
            console.log(f"[red]Error processing record:[/red] {e}")
            return {}

    def update_excel(self, data: List[Dict[str, Any]]) -> None:
        """
        Create or append to an Excel file with the provided data.

        :param data: A list of record dictionaries to be saved.
        """
        try:
            if os.path.exists(self.excel_filename):
                existing_df = pd.read_excel(self.excel_filename)
                new_df = pd.DataFrame(data, columns=config.OUTPUT_HEADERS)
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                combined_df = pd.DataFrame(data, columns=config.OUTPUT_HEADERS)

            combined_df.to_excel(self.excel_filename, index=False)
            console.log(f"[green]Excel file updated: {self.excel_filename}[/green]")

        except Exception as e:
            console.log(f"[red]Error updating Excel file:[/red] {e}")

    def run(self) -> None:
        """
        Orchestrate the PubMed scraping process by iterating over the configured journals,
        constructing queries, fetching records, processing them, and finally updating the Excel file.
        """
        try:
            for journal in config.JOURNALS:
                console.log(Panel.fit(f"Processing journal: {journal}", title="Journal", style="blue"))

                query: str = self.construct_query(journal)
                
                with console.status(f"Fetching records for {journal}...", spinner="dots"):
                    records: List[Dict[str, Any]] = self.fetch_records(query)

                if not records:
                    console.log(f"[yellow]No records found for journal: {journal}[/yellow]")
                    continue

                with console.status(f"Processing records for {journal}...", spinner="dots"):
                    for rec in records:
                        processed: Dict[str, Any] = self.process_record(rec)
                        if processed:
                            self.all_data.append(processed)

            self.update_excel(self.all_data)
            console.log(Panel.fit("Processing completed.", style="green"))

        except Exception as e:
            console.log(f"[red]An error occurred during processing:[/red] {e}")
            raise

if __name__ == "__main__":
    scraper = PubMedScraper()
    try:
        scraper.run()
    except Exception as e:
        console.log(f"[red]An error occurred in main execution:[/red] {e}")
