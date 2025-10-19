# Stadt-Geschichte-Basel (SGB) Dataset

This directory contains a curated dataset of Digital Object Identifiers (DOIs) and metadata from the Stadt-Geschichte-Basel project.

## Contents

### `dois.txt`

A plain text file containing 88 unique DOIs from the SGB catalog, one per line.

**Format:**
```
10.21255/sgb-01-406352
10.21255/sgb-01.00-586075
10.21255/sgb-01.01-439115
...
```

**Usage:**
- Reference for testing the PDF metadata enhancer tool
- Input for batch processing operations
- Validation of DOI resolution and metadata fetching

### `metadata.json`

Pre-fetched CSL-JSON metadata for all DOIs in `dois.txt`.

**Format:** JSON array of CSL-JSON objects

**Sample Record:**
```json
{
  "DOI": "10.21255/SGB-01.07-191037",
  "URL": "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band1/chapter/289",
  "author": [
    {
      "family": "Lassau",
      "given": "Guido"
    }
  ],
  "copyright": "Creative Commons Attribution Non Commercial 4.0 International",
  "id": "https://doi.org/10.21255/sgb-01.07-191037",
  "issued": {
    "date-parts": [[2024]]
  },
  "language": "de",
  "publisher": "Christoph Merian Verlag",
  "title": "Anhang",
  "type": "article"
}
```

**Fields:**
- `DOI`: Digital Object Identifier
- `URL`: Canonical URL for the resource
- `author`: Array of author objects with family and given names
- `copyright`: License information
- `id`: Persistent identifier URL
- `issued`: Publication date
- `language`: Content language (ISO 639-1 code)
- `publisher`: Publishing organization
- `title`: Document title
- `type`: CSL item type

## Data Source

The DOIs were extracted from the Stadt-Geschichte-Basel e-monograph catalog:

- Band 1-9: https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band{1-9}

## Metadata Harvesting

The metadata was fetched using the `src/scripts/get_metadata.py` script, which:

1. Extracts DOIs from catalog HTML pages
2. Fetches CSL-JSON metadata via content negotiation
3. Validates and formats the data
4. Handles errors with retry logic

**To update the metadata:**

```bash
# Re-fetch metadata from default SGB catalog URLs
uv run python3 src/scripts/get_metadata.py \
  --out-dois sgb/dois.txt \
  --out-json sgb/metadata.json \
  --out-fail sgb/failed_dois_report.txt
```

## License

This dataset is released under the Creative Commons Attribution 4.0 International (CC BY 4.0) License. The individual articles referenced by these DOIs may have different licenses as specified in their metadata.

## Citation

If you use this dataset in your research, please cite:

```
Stadt-Geschichte-Basel Project
Christoph Merian Verlag, 2024
https://emono.unibas.ch/stadtgeschichtebasel/
```

## Usage Example

Create a mapping file for PDF enhancement:

```bash
# Create mapping from SGB DOIs
echo "pdf,doi" > mapping.csv
while read doi; do
  echo "path/to/document.pdf,$doi" >> mapping.csv
done < sgb/dois.txt

# Process PDFs
uv run pdf-metadata-enhancer ingest --input mapping.csv --out-dir output/
```

## Statistics

- **Total DOIs**: 88
- **Language**: Predominantly German (de)
- **Publisher**: Christoph Merian Verlag
- **License**: Creative Commons Attribution Non Commercial 4.0 International
- **Publication Year**: 2024
- **Item Type**: Article

## Maintenance

This dataset is maintained as part of the pdf-metadata-enhancer project. Updates are performed periodically to reflect changes in the SGB catalog.

**Last Updated**: October 2025
