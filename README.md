# pdf-metadata-enhancer

A CLI tool to embed canonical metadata from DOIs into PDF files for digital preservation and accessibility. This tool fetches bibliographic metadata using DOI content negotiation and embeds it into PDF InfoDict and XMP (Dublin Core) fields.

[![GitHub issues](https://img.shields.io/github/issues/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues)
[![GitHub forks](https://img.shields.io/github/forks/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/network)
[![GitHub stars](https://img.shields.io/github/stars/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/stargazers)
[![Code license](https://img.shields.io/github/license/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/blob/main/LICENSE-AGPL.md)
[![Data license](https://img.shields.io/github/license/Stadt-Geschichte-Basel/pdf-metadata-enhancer.svg)](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/blob/main/LICENSE-CCBY.md)
[![DOI](https://zenodo.org/badge/GITHUB_REPO_ID.svg)](https://zenodo.org/badge/latestdoi/ZENODO_RECORD)

## Quick Start

```bash
# Install
pip install -e .

# Run
echo "pdf,doi" > mapping.csv
echo "./document.pdf,10.21255/sgb-01-406352" >> mapping.csv
pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/ --verbose
```

## Features

- **DOI Metadata Fetching**: Automatic metadata retrieval using HTTP content negotiation (CSL-JSON)
- **PDF Enhancement**: Embeds metadata into PDF InfoDict and XMP (Dublin Core)
- **Flexible Input**: Supports CSV, TSV, and JSONL mapping files
- **Provenance Tracking**: Creates JSON sidecar files with SHA256 hashes and complete metadata
- **Batch Processing**: Process multiple PDFs in a single run

## Repository Structure

The structure of this repository follows the [Advanced Structure for Data Analysis](https://the-turing-way.netlify.app/project-design/project-repo/project-repo-advanced.html) of _The Turing Way_ and is organized as follows:

- `analysis/`: scripts and notebooks used to analyze the data
- `assets/`: images, logos, etc. used in the README and other documentation
- `build/`: scripts and notebooks used to build the data
- `data/`: data files
- `documentation/`: documentation for the data and the repository
- `project-management/`: project management documents (e.g., meeting notes, project plans, etc.)
- `src/`: source code for the data (e.g., scripts used to collect or process the data)
- `test/`: tests for the data and source code
- `report.md`: a report describing the analysis of the data

## Data Description

- This repository contains tools and workflows for enhancing PDF metadata to improve digital preservation and accessibility. The tools help extract, validate, and enhance metadata in PDF documents to comply with preservation standards.
- Data models include PDF metadata schemas, controlled vocabularies for document types, subjects, and preservation levels. Field descriptions and validation rules are documented in the source code and configuration files.
- All code is released under the GNU Affero General Public License v3.0, ensuring open access and collaborative development. Data and documentation are released under Creative Commons Attribution 4.0 International (CC BY 4.0) license.

## Installation

### Requirements

- Python 3.10 or higher
- pip package manager (or [uv](https://github.com/astral-sh/uv) for faster installation)

### Install from source

**Using [uv](https://github.com/astral-sh/uv) (recommended for faster installation):**

```bash
git clone https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer.git
cd pdf-metadata-enhancer
uv sync
```

## Usage

The `pdf-metadata-enhancer` CLI tool allows you to embed canonical metadata from DOIs into PDF files.

### Basic Usage

```bash
pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/
```

### Input Format

The tool accepts CSV, TSV, or JSONL files mapping PDF files to their corresponding DOIs:

**CSV format:**

```csv
pdf,doi
./documents/paper1.pdf,10.21255/sgb-01-406352
./documents/paper2.pdf,10.1234/example.doi
```

**JSONL format:**

```jsonl
{"pdf": "./documents/paper1.pdf", "doi": "10.21255/sgb-01-406352"}
{"pdf": "./documents/paper2.pdf", "doi": "10.1234/example.doi"}
```

### Example

```bash
# Create a sample mapping file
echo "pdf,doi" > mapping.csv
echo "data/raw/document.pdf,10.21255/sgb-01-406352" >> mapping.csv

# Run the enhancement
pdf-metadata-enhancer ingest --input mapping.csv --out-dir data/clean/ --verbose
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
pip install -e ".[dev]"
# or with uv:
uv pip install -e ".[dev]"

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
python3 run_tests.py

# Run individual test modules
python3 test/test_input_parser.py
python3 test/test_pdf_enhancer.py
python3 test/test_sidecar.py
```

### Project Structure

```
src/pdf_metadata_enhancer/
├── cli.py              # Command-line interface
├── metadata_fetcher.py # DOI metadata fetching
├── pdf_enhancer.py     # PDF metadata embedding
├── input_parser.py     # Input file parsing
└── sidecar.py          # Provenance sidecar generation

test/
├── test_input_parser.py
├── test_pdf_enhancer.py
└── test_sidecar.py

data/
├── raw/                # Input PDFs and mapping files
└── clean/              # Enhanced PDFs and sidecars
```

## Repository Structure

The structure of this repository follows the [Advanced Structure for Data Analysis](https://the-turing-way.netlify.app/project-design/project-repo/project-repo-advanced.html) of _The Turing Way_ and is organized as follows:

- `analysis/`: scripts and notebooks used to analyze the data
- `build/`: scripts and notebooks used to build the data
- `data/`: data files (raw inputs and clean outputs)
- `documentation/`: documentation for the data and the repository
- `project-management/`: project management documents
- `src/`: source code for the CLI tool and modules
- `test/`: tests for the code
- `report.md`: a report describing the analysis of the data

## Citation

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
```

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
