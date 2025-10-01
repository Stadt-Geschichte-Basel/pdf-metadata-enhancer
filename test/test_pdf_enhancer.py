"""Tests for the PDF enhancer module."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "src")

import pikepdf

from pdf_metadata_enhancer.pdf_enhancer import enhance_pdf_metadata


def test_enhance_pdf_basic():
    """Test basic PDF enhancement with metadata."""
    # Create a test PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        input_pdf = f.name
        pdf = pikepdf.Pdf.new()
        pdf.add_blank_page()
        pdf.save(input_pdf)

    output_pdf = Path(tempfile.mktemp(suffix=".pdf"))

    try:
        # Metadata to embed
        metadata = {
            "DOI": "10.1234/test",
            "title": "Test Document Title",
            "author": [{"family": "Smith", "given": "John"}, {"family": "Doe", "given": "Jane"}],
            "issued": {"date-parts": [[2023, 3, 15]]},
            "publisher": "Test Publisher",
            "subject": ["Testing", "PDF", "Metadata"],
            "abstract": "This is a test abstract for the document.",
        }

        # Enhance the PDF
        enhance_pdf_metadata(input_pdf, output_pdf, metadata, verbose=False)

        # Verify the output
        assert output_pdf.exists(), "Output PDF was not created"

        # Verify metadata was embedded
        with pikepdf.open(output_pdf) as pdf:
            assert "/Title" in pdf.docinfo
            assert str(pdf.docinfo["/Title"]) == "Test Document Title"

            assert "/Author" in pdf.docinfo
            assert "John Smith" in str(pdf.docinfo["/Author"])
            assert "Jane Doe" in str(pdf.docinfo["/Author"])

            # Producer is set by pikepdf during save, but we can verify the PDF was modified
            assert "/Producer" in pdf.docinfo

        print("✓ Basic PDF enhancement test passed")

    finally:
        Path(input_pdf).unlink()
        if output_pdf.exists():
            output_pdf.unlink()


def test_enhance_pdf_minimal_metadata():
    """Test PDF enhancement with minimal metadata."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        input_pdf = f.name
        pdf = pikepdf.Pdf.new()
        pdf.add_blank_page()
        pdf.save(input_pdf)

    output_pdf = Path(tempfile.mktemp(suffix=".pdf"))

    try:
        # Minimal metadata
        metadata = {"DOI": "10.1234/minimal", "title": "Minimal Document"}

        enhance_pdf_metadata(input_pdf, output_pdf, metadata, verbose=False)

        assert output_pdf.exists()

        with pikepdf.open(output_pdf) as pdf:
            assert "/Title" in pdf.docinfo
            assert str(pdf.docinfo["/Title"]) == "Minimal Document"

        print("✓ Minimal metadata enhancement test passed")

    finally:
        Path(input_pdf).unlink()
        if output_pdf.exists():
            output_pdf.unlink()


def test_enhance_pdf_xmp_metadata():
    """Test that XMP metadata is properly embedded."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        input_pdf = f.name
        pdf = pikepdf.Pdf.new()
        pdf.add_blank_page()
        pdf.save(input_pdf)

    output_pdf = Path(tempfile.mktemp(suffix=".pdf"))

    try:
        metadata = {
            "DOI": "10.1234/xmp-test",
            "title": "XMP Test Document",
            "author": [{"family": "Test", "given": "User"}],
            "publisher": "Test Publisher",
        }

        enhance_pdf_metadata(input_pdf, output_pdf, metadata, verbose=False)

        with pikepdf.open(output_pdf) as pdf:
            with pdf.open_metadata() as meta:
                xmp_str = str(meta)
                # Check that Dublin Core namespace is present
                assert "http://purl.org/dc/elements/1.1/" in xmp_str
                # Check that title is in XMP
                assert "XMP Test Document" in xmp_str

        print("✓ XMP metadata test passed")

    finally:
        Path(input_pdf).unlink()
        if output_pdf.exists():
            output_pdf.unlink()


if __name__ == "__main__":
    print("Running PDF enhancer tests...\n")
    test_enhance_pdf_basic()
    test_enhance_pdf_minimal_metadata()
    test_enhance_pdf_xmp_metadata()
    print("\n✓ All PDF enhancer tests passed!")
