"""Tests for the input parser module."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "src")

from pdf_metadata_enhancer.input_parser import parse_input_file


def test_parse_csv():
    """Test parsing a CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("pdf,doi\n")
        f.write("./test1.pdf,10.1234/test1\n")
        f.write("./test2.pdf,10.1234/test2\n")
        csv_path = Path(f.name)

    try:
        mappings = parse_input_file(csv_path)
        assert len(mappings) == 2
        assert mappings[0]["pdf"] == "./test1.pdf"
        assert mappings[0]["doi"] == "10.1234/test1"
        assert mappings[1]["pdf"] == "./test2.pdf"
        assert mappings[1]["doi"] == "10.1234/test2"
        print("✓ CSV parsing test passed")
    finally:
        csv_path.unlink()


def test_parse_tsv():
    """Test parsing a TSV file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
        f.write("pdf\tdoi\n")
        f.write("./test1.pdf\t10.1234/test1\n")
        tsv_path = Path(f.name)

    try:
        mappings = parse_input_file(tsv_path)
        assert len(mappings) == 1
        assert mappings[0]["pdf"] == "./test1.pdf"
        assert mappings[0]["doi"] == "10.1234/test1"
        print("✓ TSV parsing test passed")
    finally:
        tsv_path.unlink()


def test_parse_jsonl():
    """Test parsing a JSONL file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write('{"pdf": "./test1.pdf", "doi": "10.1234/test1"}\n')
        f.write('{"pdf": "./test2.pdf", "doi": "10.1234/test2"}\n')
        jsonl_path = Path(f.name)

    try:
        mappings = parse_input_file(jsonl_path)
        assert len(mappings) == 2
        assert mappings[0]["pdf"] == "./test1.pdf"
        assert mappings[0]["doi"] == "10.1234/test1"
        print("✓ JSONL parsing test passed")
    finally:
        jsonl_path.unlink()


def test_invalid_format():
    """Test that invalid file format raises ValueError."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("test")
        txt_path = Path(f.name)

    try:
        try:
            parse_input_file(txt_path)
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Unsupported file format" in str(e)
        print("✓ Invalid format test passed")
    finally:
        txt_path.unlink()


def test_missing_columns():
    """Test that CSV with missing columns raises ValueError."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("pdf,other\n")
        f.write("./test1.pdf,value\n")
        csv_path = Path(f.name)

    try:
        try:
            parse_input_file(csv_path)
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Invalid CSV/TSV format" in str(e)
        print("✓ Missing columns test passed")
    finally:
        csv_path.unlink()


def test_empty_file():
    """Test that empty file raises ValueError."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("pdf,doi\n")
        csv_path = Path(f.name)

    try:
        try:
            parse_input_file(csv_path)
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "No valid PDF-DOI mappings" in str(e)
        print("✓ Empty file test passed")
    finally:
        csv_path.unlink()


if __name__ == "__main__":
    print("Running input parser tests...\n")
    test_parse_csv()
    test_parse_tsv()
    test_parse_jsonl()
    test_invalid_format()
    test_missing_columns()
    test_empty_file()
    print("\n✓ All input parser tests passed!")
