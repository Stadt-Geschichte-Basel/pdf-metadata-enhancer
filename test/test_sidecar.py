"""Tests for the sidecar module."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "src")

import pikepdf

from pdf_metadata_enhancer.sidecar import compute_file_hash, create_sidecar


def test_compute_file_hash():
    """Test computing file hash."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        temp_path = f.name

    try:
        hash_value = compute_file_hash(temp_path)
        # Known SHA256 for "test content"
        expected = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"
        assert hash_value == expected
        print("✓ File hash test passed")
    finally:
        Path(temp_path).unlink()


def test_create_sidecar():
    """Test creating a sidecar file."""
    # Create test PDFs
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        input_pdf = f.name
        pdf = pikepdf.Pdf.new()
        pdf.add_blank_page()
        pdf.save(input_pdf)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        output_pdf = Path(f.name)
        pdf = pikepdf.Pdf.new()
        pdf.add_blank_page()
        pdf.save(output_pdf)

    sidecar_path = Path(tempfile.mktemp(suffix=".json"))

    try:
        metadata = {"DOI": "10.1234/test", "title": "Test Document"}

        create_sidecar(input_pdf, output_pdf, "10.1234/test", metadata, sidecar_path, verbose=False)

        # Verify sidecar was created
        assert sidecar_path.exists()

        # Verify content
        with open(sidecar_path) as f:
            data = json.load(f)

        assert data["version"] == "0.1.0"
        assert "timestamp" in data
        assert data["doi"] == "10.1234/test"
        assert data["metadata"]["title"] == "Test Document"
        assert "sha256" in data["input"]
        assert "sha256" in data["output"]
        assert len(data["input"]["sha256"]) == 64  # SHA256 hex length

        print("✓ Sidecar creation test passed")

    finally:
        Path(input_pdf).unlink()
        output_pdf.unlink()
        if sidecar_path.exists():
            sidecar_path.unlink()


if __name__ == "__main__":
    print("Running sidecar module tests...\n")
    test_compute_file_hash()
    test_create_sidecar()
    print("\n✓ All sidecar tests passed!")
