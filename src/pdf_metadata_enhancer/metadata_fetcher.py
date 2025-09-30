"""Module for fetching metadata from DOIs using content negotiation."""

import requests
from typing import Optional, Dict, Any


def fetch_metadata_from_doi(doi: str, verbose: bool = False) -> Optional[Dict[str, Any]]:
    """
    Fetch metadata from a DOI using HTTP content negotiation.
    
    Args:
        doi: The DOI identifier (e.g., "10.21255/sgb-01-406352")
        verbose: Enable verbose output
        
    Returns:
        Dictionary containing CSL-JSON metadata, or None if fetch fails
    """
    # Construct DOI URL
    if not doi.startswith("http"):
        doi_url = f"https://doi.org/{doi}"
    else:
        doi_url = doi
    
    # Request CSL-JSON format
    headers = {
        "Accept": "application/vnd.citationstyles.csl+json",
        "User-Agent": "pdf-metadata-enhancer/0.1.0 (https://github.com/Stadt-Geschichte-Basel/pdf-metadata-enhancer)"
    }
    
    try:
        if verbose:
            print(f"  → Fetching metadata from: {doi_url}")
        
        response = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        metadata = response.json()
        
        if verbose:
            print(f"  ✓ Successfully fetched metadata")
            print(f"    Title: {metadata.get('title', 'N/A')}")
            if 'author' in metadata:
                authors = metadata['author']
                if isinstance(authors, list) and len(authors) > 0:
                    first_author = authors[0]
                    author_name = f"{first_author.get('family', '')}, {first_author.get('given', '')}"
                    print(f"    First author: {author_name}")
        
        return metadata
        
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"  ✗ Failed to fetch metadata: {e}")
        return None
    except Exception as e:
        if verbose:
            print(f"  ✗ Error processing metadata: {e}")
        return None
