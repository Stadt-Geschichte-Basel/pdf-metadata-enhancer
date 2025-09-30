"""Module for enhancing PDF files with metadata."""

import pikepdf
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def enhance_pdf_metadata(
    input_pdf_path: str,
    output_pdf_path: Path,
    metadata: Dict[str, Any],
    verbose: bool = False
) -> None:
    """
    Enhance a PDF file with metadata from CSL-JSON.
    
    Updates both PDF InfoDict and XMP metadata.
    
    Args:
        input_pdf_path: Path to input PDF file
        output_pdf_path: Path for output PDF file
        metadata: CSL-JSON metadata dictionary
        verbose: Enable verbose output
    """
    if verbose:
        print(f"  → Opening PDF: {input_pdf_path}")
    
    # Open PDF
    with pikepdf.open(input_pdf_path) as pdf:
        
        # Extract relevant metadata fields from CSL-JSON
        title = metadata.get("title", "")
        
        # Handle authors
        authors = []
        if "author" in metadata:
            for author in metadata["author"]:
                if "family" in author:
                    name = f"{author.get('given', '')} {author['family']}".strip()
                    authors.append(name)
                elif "literal" in author:
                    authors.append(author["literal"])
        author_string = "; ".join(authors) if authors else ""
        
        # Handle dates
        issued = metadata.get("issued", {})
        if isinstance(issued, dict) and "date-parts" in issued:
            date_parts = issued["date-parts"][0] if issued["date-parts"] else []
            if date_parts:
                year = date_parts[0] if len(date_parts) > 0 else ""
                creation_date = str(year) if year else ""
        else:
            creation_date = ""
        
        # Subject/keywords
        subject = metadata.get("subject", "")
        if isinstance(subject, list):
            subject = "; ".join(subject)
        
        # Publisher
        publisher = metadata.get("publisher", "")
        
        # DOI
        doi = metadata.get("DOI", "")
        
        # Abstract/description
        abstract = metadata.get("abstract", "")
        
        if verbose:
            print(f"  → Updating PDF metadata")
            print(f"    Title: {title[:50]}..." if len(title) > 50 else f"    Title: {title}")
            print(f"    Authors: {author_string[:50]}..." if len(author_string) > 50 else f"    Authors: {author_string}")
        
        # Update PDF Info dictionary
        with pdf.open_metadata() as meta:
            # Dublin Core metadata
            if title:
                meta["dc:title"] = title
            if authors:
                meta["dc:creator"] = authors  # Should be a list
            if subject:
                meta["dc:subject"] = subject
            if publisher:
                meta["dc:publisher"] = publisher
            if abstract:
                meta["dc:description"] = abstract
            if doi:
                meta["dc:identifier"] = f"doi:{doi}"
            
            # Add PDF metadata
            if title:
                pdf.docinfo["/Title"] = title
            if author_string:
                pdf.docinfo["/Author"] = author_string
            if subject:
                pdf.docinfo["/Subject"] = subject
            if abstract:
                pdf.docinfo["/Keywords"] = abstract[:255]  # PDF has limits on keyword length
            
            # Add producer info
            pdf.docinfo["/Producer"] = "pdf-metadata-enhancer/0.1.0"
            
        # Save enhanced PDF
        if verbose:
            print(f"  → Saving enhanced PDF to: {output_pdf_path}")
        
        pdf.save(output_pdf_path)
