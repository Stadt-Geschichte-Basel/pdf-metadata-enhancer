"""Tests for the input parser module."""

import pytest
import tempfile
from pathlib import Path
from pdf_metadata_enhancer.input_parser import parse_input_file, parse_csv_tsv, parse_jsonl


def test_parse_csv():
    """Test parsing a CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
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
    finally:
        csv_path.unlink()


def test_parse_tsv():
    """Test parsing a TSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
        f.write("pdf\tdoi\n")
        f.write("./test1.pdf\t10.1234/test1\n")
        tsv_path = Path(f.name)
    
    try:
        mappings = parse_input_file(tsv_path)
        assert len(mappings) == 1
        assert mappings[0]["pdf"] == "./test1.pdf"
        assert mappings[0]["doi"] == "10.1234/test1"
    finally:
        tsv_path.unlink()


def test_parse_jsonl():
    """Test parsing a JSONL file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write('{"pdf": "./test1.pdf", "doi": "10.1234/test1"}\n')
        f.write('{"pdf": "./test2.pdf", "doi": "10.1234/test2"}\n')
        jsonl_path = Path(f.name)
    
    try:
        mappings = parse_input_file(jsonl_path)
        assert len(mappings) == 2
        assert mappings[0]["pdf"] == "./test1.pdf"
        assert mappings[0]["doi"] == "10.1234/test1"
    finally:
        jsonl_path.unlink()


def test_invalid_format():
    """Test that invalid file format raises ValueError."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test")
        txt_path = Path(f.name)
    
    try:
        with pytest.raises(ValueError, match="Unsupported file format"):
            parse_input_file(txt_path)
    finally:
        txt_path.unlink()


def test_missing_columns():
    """Test that CSV with missing columns raises ValueError."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("pdf,other\n")
        f.write("./test1.pdf,value\n")
        csv_path = Path(f.name)
    
    try:
        with pytest.raises(ValueError, match="Invalid CSV/TSV format"):
            parse_input_file(csv_path)
    finally:
        csv_path.unlink()


def test_empty_file():
    """Test that empty file raises ValueError."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("pdf,doi\n")
        csv_path = Path(f.name)
    
    try:
        with pytest.raises(ValueError, match="No valid PDF-DOI mappings"):
            parse_input_file(csv_path)
    finally:
        csv_path.unlink()
