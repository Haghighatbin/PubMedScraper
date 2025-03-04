# PubMed RCT & Critical Care Scraper

This repository contains a Python-based scraper that queries PubMed for **Randomised Controlled Trials (RCTs)** in **critical care** journals, processes the resulting records, and saves them in an Excel file. The scraper utilises the [NCBI Entrez](https://www.ncbi.nlm.nih.gov/books/NBK25500/) API (via [BioPython](https://biopython.org/)), [pandas](https://pandas.pydata.org/), and [rich](https://github.com/Textualize/rich) libraries.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Running the Scraper](#running-the-scraper)
  - [Output](#output)
- [Customisation](#customisation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

1. **PubMed Query Construction**  
   Combines search terms for RCTs, critical care, date ranges, and human studies, then filters out meta-analyses and reviews.  

2. **Journal-Focused**  
   Searches a predefined list of key journals by applying the `[TA]` field filter.

3. **Result Parsing**  
   Extracts essential publication information such as title, authors, DOI, and publication details.

4. **Excel Export**  
   Consolidates new results into an Excel workbook (with a timestamped filename) or appends to an existing one.

5. **Custom Logging**  
   Uses the `rich` library to provide stylised log messages in the console.

---

## Directory Structure

```
.
├── config.py         # Configuration for queries, journal list, folder paths, etc.
├── main.py           # Main scraper script
├── requirements.txt  # (Optional) Could include necessary Python packages
└── README.md         # Project documentation
```

- **`RES_DIR`**: The results directory is set in `config.py` (default: `/results/`), where Excel files will be saved.
- **`config.py`**: Contains constants and query definitions used by the scraper.

---

## Requirements

- **Python 3.7+** (Recommended 3.9+)
- The following Python libraries:
  - [Biopython](https://biopython.org/)  
  - [pandas](https://pandas.pydata.org/)  
  - [rich](https://github.com/Textualize/rich)

```
biopython
pandas
rich
openpyxl  # Required for Excel reading/writing
```

(You can install these via `pip install -r requirements.txt`.)

---

## Installation

1. **Clone or Download the Repository**  
   ```bash
   git clone https://github.com/yourusername/pubmed-rct-scraper.git
   cd pubmed-rct-scraper
   ```

2. **Set Up a Python Virtual Environment** (recommended)  
   ```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   # or
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
   or manually:
   ```bash
   pip install biopython pandas rich openpyxl
   ```

4. **Create Results Directory (if needed)**  
   By default, the scraper uses `/results/` (defined in `config.py`). On some operating systems, you may need to create this folder manually or adjust permissions.

---

## Usage

### Configuration

Open `config.py` and update the constants as necessary:

- **`RES_DIR`**: Directory where Excel results will be saved.  
- **`NCBI_EMAIL`**: Your valid email address (required by NCBI).  
- **`RCT_QUERY`**, **`CRITICAL_QUERY`**, **`DATE_QUERY`**: Search strings for the PubMed query.  
- **`JOURNALS`**: List of journals to search.  
- **`OUTPUT_HEADERS`**: Columns for the output Excel sheet.

Ensure you have the right date range and any other query constraints you want.

### Running the Scraper

Simply execute `main.py`:

```bash
python main.py
```

This will:

1. Read each journal name from `JOURNALS`.
2. Construct a PubMed query for that journal.
3. Fetch up to 200 results (adjustable in `main.py`).
4. Parse each record, extract relevant info, and append it to a master list.
5. Write (or append) the results to a timestamped Excel file in `RES_DIR`.

### Output

- **Excel File**: A file named `pubmed_results_YYYYMMDD_HHMMSS.xlsx` (e.g., `pubmed_results_20250304_134501.xlsx`) will be created or updated in your specified `RES_DIR`.

---

## Customisation

1. **Journals**  
   Add or remove journal titles in `config.JOURNALS`.
2. **Search Terms**  
   Modify `config.RCT_QUERY`, `config.CRITICAL_QUERY`, or `config.EXCLUSION_QUERY` to fit your needs.
3. **Maximum Records**  
   Increase or decrease the `retmax` value in `fetch_records()` (within `main.py`).

---

## Troubleshooting

- **Permission Errors**:  
  Make sure your Python script has permission to create or write to the `RES_DIR`.
  
- **Network Issues**:  
  The script relies on the NCBI Entrez API, so it requires internet access. If you have a firewall or proxy, ensure it's correctly configured.

- **No Records Found**:  
  If you see a lot of `[yellow]No records found[/yellow]` messages, check your query parameters. Ensure that your date ranges, journal names, or search terms are correct.

- **Biopython or Other Dependencies Missing**:  
  Double-check that you have installed all dependencies via `pip` or another package manager.

---

## Contributing

Contributions are welcome! If you want to add features, fix bugs, or improve documentation:
1. Fork this repository.
2. Create a new branch for your changes.
3. Submit a pull request.

For any major changes, please open an issue first to discuss what you would like to change.

---

## License

MIT

---

**Author**: Dr Leila Janani (%99) Dr Amin Haghighatbin (%1) <br>
**Contact**: aminhb@tutanota.com

