"""Shared app paths and configuration values."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXAMPLE_FASTA_PATH = PROJECT_ROOT / "data/example_protein.fasta"
EXAMPLE_FASTA_VARIANT_PATH = PROJECT_ROOT / "data/example_protein_variant.fasta"
EXPORTS_DIR = PROJECT_ROOT / "outputs/exports"
REPORT_QMD_PATH = PROJECT_ROOT / "report.qmd"
REPORT_HTML_PATH = PROJECT_ROOT / "report.html"
