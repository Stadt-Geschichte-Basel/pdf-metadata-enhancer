# Implementation Summary: PDF Metadata Enhancer CLI Tool

**Issue**: [#2 - Implement a CLI tool to embed canonical metadata into PDFs using DOIs](https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer/issues/2)

**Status**: ✅ Complete

## What Was Implemented

### 1. Command-Line Interface (CLI)

- **Main command**: `pdf-metadata-enhancer ingest`
- **Options**:
  - `--input` / `-i`: Input file path (CSV/TSV/JSONL)
  - `--out-dir` / `-o`: Output directory
  - `--verbose` / `-v`: Enable detailed output
- **Built with**: Click framework for robust CLI handling

### 2. Metadata Fetching

- **Module**: `src/pdf_metadata_enhancer/metadata_fetcher.py`
- **Method**: HTTP content negotiation
- **Format**: CSL-JSON via DOI resolution
- **Example**:
  ```bash
  curl -LH "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.21255/sgb-01-406352
  ```

### 3. PDF Enhancement

- **Module**: `src/pdf_metadata_enhancer/pdf_enhancer.py`
- **Library**: pikepdf (robust PDF manipulation)
- **Metadata embedded**:
  - **PDF InfoDict**: Title, Author, Subject, Keywords, Producer
  - **XMP Dublin Core**: dc:title, dc:creator, dc:subject, dc:publisher, dc:description, dc:identifier

### 4. Input Parsing

- **Module**: `src/pdf_metadata_enhancer/input_parser.py`
- **Supported formats**:
  - CSV (comma-separated)
  - TSV (tab-separated)
  - JSONL (JSON lines)
- **Required fields**: `pdf` (file path), `doi` (DOI identifier)

### 5. Provenance Tracking

- **Module**: `src/pdf_metadata_enhancer/sidecar.py`
- **Output**: JSON sidecar file per PDF
- **Contains**:
  - Input/output file paths
  - SHA256 hashes for integrity verification
  - Complete CSL-JSON metadata
  - ISO 8601 timestamp
  - Tool version

### 6. Testing

- **Test files**:
  - `test/test_input_parser.py` - Input parsing tests
  - `test/test_pdf_enhancer.py` - PDF enhancement tests
  - `test/test_sidecar.py` - Provenance tests
- **Test runner**: `run_tests.py`
- **Coverage**: 15+ individual test cases
- **Status**: All tests passing ✅

### 7. Documentation

- **README.md**: Complete usage guide with examples
- **Example files**:
  - `data/raw/example.csv`
  - `data/raw/example.tsv`
  - `data/raw/example.jsonl`

## File Structure

```
pdf-metadata-enhancer/
├── pyproject.toml                      # Python package configuration
├── README.md                           # Complete documentation
├── run_tests.py                        # Test runner
├── src/pdf_metadata_enhancer/
│   ├── __init__.py
│   ├── cli.py                          # CLI interface
│   ├── metadata_fetcher.py             # DOI metadata fetching
│   ├── pdf_enhancer.py                 # PDF metadata embedding
│   ├── input_parser.py                 # Input file parsing
│   └── sidecar.py                      # Provenance tracking
├── test/
│   ├── test_input_parser.py
│   ├── test_pdf_enhancer.py
│   └── test_sidecar.py
└── data/
    ├── raw/                            # Input PDFs and mappings
    │   ├── example.csv
    │   ├── example.tsv
    │   └── example.jsonl
    └── clean/                          # Enhanced PDFs (output)
```

## Usage Example

```bash
# Install
pip install -e .

# Create mapping file
echo "pdf,doi" > mapping.csv
echo "./document.pdf,10.21255/sgb-01-406352" >> mapping.csv

# Enhance PDFs
pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/ --verbose

# Output:
# - output/document.pdf (enhanced with metadata)
# - output/document.pdf.json (provenance sidecar)
```

## Key Technical Decisions

1. **pikepdf over PyPDF2**: More robust, actively maintained, better XMP support
2. **Click framework**: Industry-standard CLI framework with excellent UX
3. **Standalone tests**: No pytest dependency for easier setup
4. **Sidecar approach**: Non-invasive provenance tracking alongside PDFs
5. **SHA256 hashing**: Strong cryptographic hashes for integrity

## Requirements Met

✅ CLI tool for batch processing  
✅ DOI metadata fetching via content negotiation  
✅ CSV/TSV/JSONL input support  
✅ PDF InfoDict embedding  
✅ XMP Dublin Core embedding  
✅ Provenance sidecar generation  
✅ Error handling and logging  
✅ Comprehensive test suite  
✅ Complete documentation

## Out of Scope (As Specified)

- OCR and content rewriting
- Reference extraction
- Complex metadata merging
- Advanced fallback strategies
- Performance optimizations (beyond prototype)

## Testing Results

```
Test Summary
============================================================
Total tests: 3 modules
Passed: All tests (15+ individual cases)
Failed: 0

✓ Input parser: CSV, TSV, JSONL, error handling
✓ PDF enhancer: InfoDict, XMP, minimal metadata
✓ Sidecar: Hash computation, JSON structure
```

## Dependencies

- **pikepdf** >=9.0.0: PDF manipulation
- **click** >=8.1.0: CLI framework
- **requests** >=2.31.0: HTTP client for DOI fetching

## Installation

```bash
git clone https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer.git
cd pdf-metadata-enhancer
pip install -e .
```

## Next Steps (Optional Enhancements)

1. Add support for batch error recovery
2. Implement parallel processing for large batches
3. Add metadata validation against schemas
4. Support additional metadata sources beyond DOIs
5. Add progress bars for long-running operations
6. Create GUI wrapper for non-technical users

## Conclusion

The implementation fully meets the requirements specified in issue #2. The tool provides an end-to-end workflow for embedding DOI-based metadata into PDFs with complete provenance tracking, suitable for digital preservation and accessibility use cases.
