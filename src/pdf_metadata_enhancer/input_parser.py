"""Module for parsing input files (CSV/TSV/JSONL)."""

import csv
import json
from pathlib import Path


def parse_input_file(input_path: Path) -> list[dict[str, str]]:
    """
    Parse input file and return list of PDF-DOI mappings.

    Supports CSV, TSV, and JSONL formats.

    Args:
        input_path: Path to input file

    Returns:
        List of dictionaries with 'pdf' and 'doi' keys

    Raises:
        ValueError: If file format is not supported or invalid
    """
    suffix = input_path.suffix.lower()

    if suffix == ".jsonl":
        return parse_jsonl(input_path)
    elif suffix in [".csv", ".tsv"]:
        delimiter = "\t" if suffix == ".tsv" else ","
        return parse_csv_tsv(input_path, delimiter)
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Supported formats: .csv, .tsv, .jsonl"
        )


def parse_csv_tsv(input_path: Path, delimiter: str) -> list[dict[str, str]]:
    """
    Parse CSV or TSV file.

    Expected format:
        pdf,doi
        ./path/to/file.pdf,10.21255/sgb-01-406352
    """
    mappings = []

    with open(input_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        # Validate headers
        if "pdf" not in reader.fieldnames or "doi" not in reader.fieldnames:
            raise ValueError(
                f"Invalid CSV/TSV format. Expected columns: 'pdf', 'doi'. "
                f"Found: {reader.fieldnames}"
            )

        for row in reader:
            pdf_path = row["pdf"].strip()
            doi = row["doi"].strip()

            if not pdf_path or not doi:
                continue  # Skip empty rows

            mappings.append({"pdf": pdf_path, "doi": doi})

    if not mappings:
        raise ValueError("No valid PDF-DOI mappings found in input file")

    return mappings


def parse_jsonl(input_path: Path) -> list[dict[str, str]]:
    """
    Parse JSONL file.

    Expected format (one JSON object per line):
        {"pdf": "./path/to/file.pdf", "doi": "10.21255/sgb-01-406352"}
    """
    mappings = []

    with open(input_path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)

                if "pdf" not in obj or "doi" not in obj:
                    raise ValueError(f"Line {line_num}: Missing 'pdf' or 'doi' field")

                mappings.append({"pdf": str(obj["pdf"]).strip(), "doi": str(obj["doi"]).strip()})
            except json.JSONDecodeError as e:
                raise ValueError(f"Line {line_num}: Invalid JSON - {e}") from e

    if not mappings:
        raise ValueError("No valid PDF-DOI mappings found in input file")

    return mappings
