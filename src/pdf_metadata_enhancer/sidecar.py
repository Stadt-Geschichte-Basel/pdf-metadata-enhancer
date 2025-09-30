"""Module for creating provenance sidecar files."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def compute_file_hash(file_path: str) -> str:
    """
    Compute SHA256 hash of a file.

    Args:
        file_path: Path to file

    Returns:
        Hex string of SHA256 hash
    """
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        # Read in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def create_sidecar(
    input_pdf_path: str,
    output_pdf_path: Path,
    doi: str,
    metadata: dict[str, Any],
    sidecar_path: Path,
    verbose: bool = False,
) -> None:
    """
    Create a JSON sidecar file with provenance information.

    Args:
        input_pdf_path: Path to original PDF
        output_pdf_path: Path to enhanced PDF
        doi: DOI identifier
        metadata: CSL-JSON metadata
        sidecar_path: Path for sidecar JSON file
        verbose: Enable verbose output
    """
    if verbose:
        print(f"  → Creating sidecar file: {sidecar_path.name}")

    # Compute hashes
    input_hash = compute_file_hash(input_pdf_path)
    output_hash = compute_file_hash(output_pdf_path)

    # Create provenance record
    sidecar_data = {
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input": {"path": str(input_pdf_path), "sha256": input_hash},
        "output": {"path": str(output_pdf_path), "sha256": output_hash},
        "doi": doi,
        "metadata": metadata,
    }

    # Write sidecar file
    with open(sidecar_path, "w", encoding="utf-8") as f:
        json.dump(sidecar_data, f, indent=2, ensure_ascii=False)

    if verbose:
        print("  ✓ Sidecar file created")
        print(f"    Input hash: {input_hash[:16]}...")
        print(f"    Output hash: {output_hash[:16]}...")
