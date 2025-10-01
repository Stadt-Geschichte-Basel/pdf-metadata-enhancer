"""Main CLI entry point for pdf-metadata-enhancer."""

import sys
from pathlib import Path

import click

from .input_parser import parse_input_file
from .metadata_fetcher import fetch_metadata_from_doi
from .pdf_enhancer import enhance_pdf_metadata
from .sidecar import create_sidecar


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """CLI tool to embed canonical metadata into PDFs using DOIs."""
    pass


@cli.command()
@click.option(
    "--input",
    "-i",
    "input_file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Input CSV/TSV/JSONL file mapping PDFs to DOIs",
)
@click.option(
    "--out-dir",
    "-o",
    "out_dir",
    required=True,
    type=click.Path(path_type=Path),
    help="Output directory for enhanced PDFs and sidecar files",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
def ingest(input_file: Path, out_dir: Path, verbose: bool):
    """
    Ingest PDFs and enhance them with metadata from DOIs.

    Example:
        pdf-metadata-enhancer ingest --input map.csv --out-dir out/
    """
    # Create output directory if it doesn't exist
    out_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        click.echo(f"Reading input from: {input_file}")
        click.echo(f"Output directory: {out_dir}")

    # Parse input file
    try:
        mappings = parse_input_file(input_file)
        if verbose:
            click.echo(f"Found {len(mappings)} PDF-DOI mappings")
    except Exception as e:
        click.echo(f"Error parsing input file: {e}", err=True)
        sys.exit(1)

    # Process each PDF
    success_count = 0
    error_count = 0

    for mapping in mappings:
        pdf_path = mapping["pdf"]
        doi = mapping["doi"]

        try:
            if verbose:
                click.echo(f"\nProcessing: {pdf_path} (DOI: {doi})")

            # Fetch metadata from DOI
            metadata = fetch_metadata_from_doi(doi, verbose=verbose)

            if metadata is None:
                click.echo(f"  ⚠️  Failed to fetch metadata for DOI: {doi}", err=True)
                error_count += 1
                continue

            # Determine output path
            pdf_filename = Path(pdf_path).name
            output_pdf_path = out_dir / pdf_filename
            sidecar_path = out_dir / f"{pdf_filename}.json"

            # Enhance PDF with metadata
            enhance_pdf_metadata(pdf_path, output_pdf_path, metadata, verbose=verbose)

            # Create sidecar file
            create_sidecar(pdf_path, output_pdf_path, doi, metadata, sidecar_path, verbose=verbose)

            click.echo(f"  ✓ Successfully processed: {pdf_filename}")
            success_count += 1

        except Exception as e:
            click.echo(f"  ✗ Error processing {pdf_path}: {e}", err=True)
            error_count += 1
            if verbose:
                import traceback

                traceback.print_exc()

    # Summary
    click.echo(f"\n{'=' * 60}")
    click.echo("Summary:")
    click.echo(f"  Successfully processed: {success_count}")
    click.echo(f"  Errors: {error_count}")
    click.echo(f"{'=' * 60}")

    if error_count > 0:
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
