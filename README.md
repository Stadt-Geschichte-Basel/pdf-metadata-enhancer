# pdf-metadata-enhancer

A CLI tool to embed canonical metadata from DOIs into PDF files for digital preservation and accessibility. This tool fetches bibliographic metadata using DOI content negotiation and embeds it into PDF InfoDict and XMP (Dublin Core) fields.

[![GitHub issues](https://img.shields.io/github/issues/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues)
[![GitHub forks](https://img.shields.io/github/forks/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/network)
[![GitHub stars](https://img.shields.io/github/stars/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/stargazers)
[![Code license](https://img.shields.io/github/license/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/blob/main/LICENSE-AGPL.md)
[![Data license](https://img.shields.io/github/license/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/blob/main/LICENSE-CCBY.md)

<!-- [![DOI](https://zenodo.org/badge/GITHUB_REPO_ID.svg)](https://zenodo.org/badge/latestdoi/ZENODO_RECORD) -->

## Quick Start

```bash
# Install
uv sync

# Run
echo "pdf,doi" > mapping.csv
echo "./document.pdf,10.21255/sgb-01-406352" >> mapping.csv
uv run pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/ --verbose
```

## Features

- **DOI Metadata Fetching**: Automatic metadata retrieval using HTTP content negotiation (CSL-JSON)
- **PDF Enhancement**: Embeds metadata into PDF InfoDict and XMP (Dublin Core)
- **Flexible Input**: Supports CSV, TSV, and JSONL mapping files
- **Provenance Tracking**: Creates JSON sidecar files with SHA256 hashes and complete metadata
- **Batch Processing**: Process multiple PDFs in a single run

## Installation

### Requirements

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv)

### Install from source

```bash
git clone https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer.git
cd pdf-metadata-enhancer
uv sync
```

## Usage

The `pdf-metadata-enhancer` CLI tool allows you to embed canonical metadata from DOIs into PDF files.

### Basic Usage

```bash
uv run pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/
```

### Input Format

The tool accepts CSV, TSV, or JSONL files mapping PDF files to their corresponding DOIs:

**CSV format:**

```csv
pdf,doi
./documents/paper1.pdf,10.21255/sgb-01-406352
./documents/paper2.pdf,10.21255/sgb-01.00-586075
```

**JSONL format:**

```jsonl
{"pdf": "./documents/paper1.pdf", "doi": "10.21255/sgb-01-406352"}
{"pdf": "./documents/paper2.pdf", "doi": "10.21255/sgb-01.00-586075"}
```

### Example

```bash
# Create a sample mapping file
echo "pdf,doi" > mapping.csv
echo "data/raw/document.pdf,10.21255/sgb-01-406352" >> mapping.csv

# Run the enhancement
uv run pdf-metadata-enhancer ingest --input mapping.csv --out-dir data/clean/ --verbose
```

### How It Works

1. **Metadata Fetching**: For each DOI, the tool fetches metadata using HTTP content negotiation:

   ```bash
   curl -LH "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.21255/sgb-01-406352
   ```

2. **PDF Enhancement**: Opens the input PDF and embeds metadata into:
   - PDF InfoDict (native PDF metadata dictionary)
   - XMP packet (extensible metadata platform using Dublin Core schema)

3. **Provenance Tracking**: Creates a sidecar JSON file with:
   - SHA256 hashes of input and output files for integrity verification
   - Complete CSL-JSON metadata for reproducibility
   - ISO 8601 timestamp for processing time

### Output

The tool produces:

1. **Enhanced PDF files** with embedded metadata in both PDF InfoDict and XMP (Dublin Core)
2. **Sidecar JSON files** containing:
   - DOI identifier
   - Complete CSL-JSON metadata
   - SHA256 hashes of input and output files
   - Processing timestamp for provenance tracking

#### Embedded Metadata Fields

The tool embeds the following metadata fields from CSL-JSON into PDFs:

**PDF InfoDict:**

- `/Title`: Document title
- `/Author`: Authors (concatenated with semicolons)
- `/Subject`: Abstract/description
- `/Keywords`: Subject keywords
- `/Producer`: Tool identifier

**XMP Dublin Core:**

- `dc:title`: Document title
- `dc:creator`: Authors (as array)
- `dc:subject`: Subject keywords
- `dc:publisher`: Publisher name
- `dc:description`: Abstract/description
- `dc:identifier`: DOI identifier

#### Sidecar Example

```json
{
	"version": "0.1.0",
	"timestamp": "2023-03-15T10:30:00.000Z",
	"input": {
		"path": "data/raw/document.pdf",
		"sha256": "ca134a6dcb00077e..."
	},
	"output": {
		"path": "data/clean/document.pdf",
		"sha256": "c396864095567edd..."
	},
	"doi": "10.21255/sgb-01-406352",
	"metadata": {
		"DOI": "10.21255/sgb-01-406352",
		"title": "Document Title",
		"author": [{ "family": "Müller", "given": "Hans" }]
	}
}
```

### Command-Line Options

```bash
pdf-metadata-enhancer ingest --help
```

Options:

- `-i, --input PATH`: Input CSV/TSV/JSONL file mapping PDFs to DOIs (required)
- `-o, --out-dir PATH`: Output directory for enhanced PDFs and sidecar files (required)
- `-v, --verbose`: Enable verbose output

## Development

### Code Quality

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting Python code.

```bash
# Install development dependencies (including ruff)
uv sync

# Check code
ruff check src/ test/ run_tests.py

# Format code
ruff format src/ test/ run_tests.py

# Fix auto-fixable issues
ruff check --fix src/ test/ run_tests.py
```

### Running Tests

The project includes a comprehensive test suite:

```bash
# Run all tests
uv run python3 run_tests.py

# Run individual test modules
uv run python3 test/test_input_parser.py
uv run python3 test/test_pdf_enhancer.py
uv run python3 test/test_sidecar.py
```

### Project Structure

```
src/
├── pdf_metadata_enhancer/
│   ├── cli.py              # Command-line interface
│   ├── metadata_fetcher.py # DOI metadata fetching
│   ├── pdf_enhancer.py     # PDF metadata embedding
│   ├── input_parser.py     # Input file parsing
│   └── sidecar.py          # Provenance sidecar generation
└── scripts/
    └── get_metadata.py     # DOI extraction and metadata harvesting

test/
├── test_input_parser.py
├── test_pdf_enhancer.py
└── test_sidecar.py

sgb/
├── dois.txt                # SGB DOI list (88 entries)
└── metadata.json           # Pre-fetched SGB metadata
```

### Helper Scripts

#### DOI Metadata Harvester (`src/scripts/get_metadata.py`)

This script automates the process of extracting DOIs from web pages and fetching their metadata:

**Features:**
- Extracts DOIs from HTML pages using pattern matching
- Fetches CSL-JSON metadata via DOI content negotiation
- Concurrent fetching with configurable concurrency
- Provenance tracking (records origin page and line numbers)
- Retry logic with exponential backoff
- Comprehensive error reporting

**Usage:**

```bash
# Fetch from default SGB catalog URLs
uv run python3 src/scripts/get_metadata.py

# Custom URLs
uv run python3 src/scripts/get_metadata.py --url https://example.com/catalog

# Multiple URLs
uv run python3 src/scripts/get_metadata.py \
  --url https://example.com/page1 \
  --url https://example.com/page2

# URLs from file
echo "https://example.com/page1" > urls.txt
echo "https://example.com/page2" >> urls.txt
uv run python3 src/scripts/get_metadata.py --urls-file urls.txt

# Custom output paths and concurrency
uv run python3 src/scripts/get_metadata.py \
  --out-dois my_dois.txt \
  --out-json my_metadata.json \
  --out-fail failures.txt \
  --concurrency 20
```

**Options:**
- `--url`: Add a URL to scan (can be used multiple times)
- `--urls-file`: Path to a text file with one URL per line
- `--concurrency`: Number of concurrent DOI fetches (default: 10)
- `--out-dois`: Output file for DOI list (default: `dois.txt`)
- `--out-json`: Output file for metadata (default: `metadata.json`)
- `--out-fail`: Output file for failure report (default: `failed_dois_report.txt`)

**Output Files:**
1. **DOI list** (`dois.txt`): One DOI per line, lowercase, sorted
2. **Metadata** (`metadata.json`): Array of CSL-JSON objects
3. **Failure report** (`failed_dois_report.txt`): Errors with provenance information

<!-- ## Citation

These tools are openly available to everyone and can be used for any research or educational purpose. If you use this tool in your research, please cite as specified in `CITATION.cff`. The following citation formats are also available through _Zenodo_:

- [BibTeX](https://zenodo.org/record/ZENODO_RECORD/export/hx)
- [CSL](https://zenodo.org/record/ZENODO_RECORD/export/csl)
- [DataCite](https://zenodo.org/record/ZENODO_RECORD/export/dcite4)
- [Dublin Core](https://zenodo.org/record/ZENODO_RECORD/export/xd)
- [DCAT](https://zenodo.org/record/ZENODO_RECORD/export/dcat)
- [JSON](https://zenodo.org/record/ZENODO_RECORD/export/json)
- [JSON-LD](https://zenodo.org/record/ZENODO_RECORD/export/schemaorg_jsonld)
- [GeoJSON](https://zenodo.org/record/ZENODO_RECORD/export/geojson)
- [MARCXML](https://zenodo.org/record/ZENODO_RECORD/export/xm)

_Zenodo_ provides an [API (REST & OAI-PMH)](https://developers.zenodo.org/) to access the data. For example, the following command will return the metadata for the most recent version of the data

```bash
curl -i https://zenodo.org/api/records/ZENODO_RECORD
``` -->

## Support

This project is maintained by [@Stadt-Geschichte-Basel](https://github.com/Stadt-Geschichte-Basel). Please understand that we can't provide individual support via email. We also believe that help is much more valuable when it's shared publicly, so more people can benefit from it.

| Type                                   | Platforms                                                                                         |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 🚨 **Bug Reports**                     | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues)    |
| 📊 **Report bad data**                 | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues)    |
| 📚 **Docs Issue**                      | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues)    |
| 🎁 **Feature Requests**                | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues)    |
| 🛡 **Report a security vulnerability** | See [SECURITY.md](SECURITY.md)                                                                    |
| 💬 **General Questions**               | [GitHub Discussions](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/discussions) |

## Stadt-Geschichte-Basel (SGB) Dataset

This repository includes a curated dataset of DOIs from the Stadt-Geschichte-Basel project:

- **`sgb/dois.txt`**: A list of 88 DOIs from the SGB catalog
- **`sgb/metadata.json`**: Pre-fetched CSL-JSON metadata for all SGB DOIs

### Using the SGB Dataset

The SGB DOIs can be used as a reference for testing and validation:

```bash
# Create a mapping file using SGB DOIs
echo "pdf,doi" > mapping.csv
echo "document.pdf,10.21255/sgb-01-406352" >> mapping.csv

# Process PDFs with SGB metadata
uv run pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/
```

### Fetching Metadata for Custom DOI Lists

The repository includes a helper script to fetch metadata for custom DOI lists:

```bash
# Fetch metadata from default SGB catalog URLs
uv run python3 src/scripts/get_metadata.py

# Fetch metadata from custom URLs
uv run python3 src/scripts/get_metadata.py --url https://example.com/page1 --url https://example.com/page2

# Customize output files
uv run python3 src/scripts/get_metadata.py \
  --out-dois custom_dois.txt \
  --out-json custom_metadata.json \
  --out-fail failed_report.txt \
  --concurrency 20
```

The script:
1. Extracts DOIs from HTML pages
2. Fetches CSL-JSON metadata using content negotiation
3. Creates a DOI list, metadata file, and failure report
4. Supports concurrent fetching for better performance

## Roadmap

No changes are currently planned.

## Contributing

All contributions to this repository are welcome! If you find errors or problems with the data, or if you want to add new data or features, please open an issue or pull request. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Versioning

We use [SemVer](http://semver.org/) for versioning. The available versions are listed in the [tags on this repository](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/tags).

## Authors and acknowledgment

- **Moritz Mähr** - _Initial work_ - [Stadt-Geschichte-Basel](https://github.com/Stadt-Geschichte-Basel)

See also the list of [contributors](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/graphs/contributors) who contributed to this project.

## License

The data in this repository is released under the Creative Commons Attribution 4.0 International (CC BY 4.0) License - see the [LICENSE-CCBY](LICENSE-CCBY.md) file for details. By using this data, you agree to give appropriate credit to the original author(s) and to indicate if any modifications have been made.

The code in this repository is released under the GNU Affero General Public License v3.0 - see the [LICENSE-AGPL](LICENSE-AGPL.md) file for details. By using this code, you agree to make any modifications available under the same license.
