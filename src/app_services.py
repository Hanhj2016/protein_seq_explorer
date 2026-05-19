"""Application service helpers kept separate from the Gradio layout layer."""

import json
import re
import subprocess
from datetime import datetime

from src.app_config import (
    EXAMPLE_FASTA_PATH,
    EXAMPLE_FASTA_VARIANT_PATH,
    EXPORTS_DIR,
    PROJECT_ROOT,
    REPORT_HTML_PATH,
    REPORT_QMD_PATH,
)
from src.llm_helper import (
    SCIENTIFIC_CAUTION_SYSTEM_PROMPT,
    call_llm,
    format_protein_summary_prompt,
)
from src.plots import (
    create_comparison_delta_chart,
    create_comparison_heatmap,
    create_composition_chart,
    create_top_residues_donut,
)
from src.protein_analysis import (
    build_comparison_difference_table,
    build_comparison_export_payload,
    build_comparison_export_text,
    build_comparison_notes,
    build_comparison_table,
    build_summary_cards,
    build_summary_export_payload,
    build_summary_export_text,
    build_summary_highlights_html,
    build_summary_table,
    build_top_amino_acid_table,
    compare_protein_sequences,
    generate_protein_profile,
    summarize_protein_sequence,
)
from src.sequence_visuals import build_residue_class_legend_html, build_sequence_fingerprint_svg
from src.structure_viewer import (
    build_structure_context_html,
    build_structure_info_markdown,
    build_structure_viewer_html,
    get_structure_choices,
    suggest_structure_choice,
)
from src.ui_content import build_report_open_link


def load_example_fasta() -> str:
    """Load the starter FASTA file into the input box."""
    return EXAMPLE_FASTA_PATH.read_text().strip()


def load_comparison_examples() -> tuple[str, str, str, str]:
    """Load two different sample FASTA sequences for comparison."""
    return (
        EXAMPLE_FASTA_PATH.read_text().strip(),
        EXAMPLE_FASTA_VARIANT_PATH.read_text().strip(),
        "Example Protein",
        "Example Protein Variant",
    )


def _safe_slug(value: str, fallback: str) -> str:
    """Create a simple filesystem-friendly slug."""
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")
    return cleaned or fallback


def _write_export_files(base_name: str, text_content: str, json_payload: dict) -> tuple[str, str]:
    """Write paired text and JSON export files and return their paths."""
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_path = EXPORTS_DIR / f"{base_name}_{timestamp}.txt"
    json_path = EXPORTS_DIR / f"{base_name}_{timestamp}.json"
    text_path.write_text(text_content)
    json_path.write_text(json.dumps(json_payload, indent=2))
    return str(text_path), str(json_path)


def analyze_sequence(sequence_text: str, protein_name: str):
    """Run deterministic sequence analysis and return the UI-facing outputs."""
    summary = summarize_protein_sequence(sequence_text)
    residue_legend = build_residue_class_legend_html()
    ai_placeholder = (
        "AI explanation not generated yet.\n\n"
        "Use the **Generate AI Explanation** button after running deterministic analysis."
    )

    return (
        summary,
        build_summary_highlights_html(summary),
        build_summary_cards(summary),
        build_summary_table(summary),
        build_top_amino_acid_table(summary),
        create_composition_chart(summary["amino_acid_composition"]),
        create_top_residues_donut(summary["amino_acid_composition"]),
        residue_legend,
        residue_legend,
        build_sequence_fingerprint_svg(summary["cleaned_sequence"]),
        generate_protein_profile(summary, protein_name=protein_name),
        ai_placeholder,
        summary["wrapped_sequence"],
    )


def generate_ai_explanation(summary: dict | None, sequence_text: str, protein_name: str):
    """Generate an optional AI explanation from the deterministic summary."""
    active_summary = summary if summary else summarize_protein_sequence(sequence_text)
    user_prompt = format_protein_summary_prompt(active_summary, protein_name=protein_name)
    return call_llm(SCIENTIFIC_CAUTION_SYSTEM_PROMPT, user_prompt)


def compare_sequences(
    first_sequence_text: str,
    second_sequence_text: str,
    first_name: str,
    second_name: str,
):
    """Compare two sequences and return the UI-facing outputs."""
    comparison = compare_protein_sequences(
        first_sequence_text,
        second_sequence_text,
        first_name=first_name,
        second_name=second_name,
    )
    delta_chart = create_comparison_delta_chart(comparison)
    return (
        comparison,
        build_comparison_table(comparison),
        delta_chart,
        create_comparison_heatmap(comparison),
        build_comparison_difference_table(comparison),
        build_comparison_notes(comparison),
        delta_chart,
    )


def export_sequence_results(summary: dict | None, protein_name: str):
    """Export single-sequence results as text and JSON files."""
    if not summary:
        raise ValueError("Analyze a sequence before exporting results.")

    protein_label = protein_name.strip() if protein_name and protein_name.strip() else "protein-sequence"
    base_name = _safe_slug(protein_label, "protein-sequence")
    text_content = build_summary_export_text(summary, protein_name=protein_name)
    json_payload = build_summary_export_payload(summary, protein_name=protein_name)
    return _write_export_files(base_name, text_content, json_payload)


def export_comparison_results(comparison: dict | None):
    """Export comparison results as text and JSON files."""
    if not comparison:
        raise ValueError("Compare two sequences before exporting comparison results.")

    label = f"{comparison['first_label']}-vs-{comparison['second_label']}"
    base_name = _safe_slug(label, "protein-comparison")
    text_content = build_comparison_export_text(comparison)
    json_payload = build_comparison_export_payload(comparison)
    return _write_export_files(base_name, text_content, json_payload)


def render_quarto_report() -> tuple[str, str, str]:
    """Render the Quarto report and return status, output file path, and open link."""
    if not REPORT_QMD_PATH.exists():
        raise FileNotFoundError("Could not find report.qmd in the project root.")

    try:
        completed = subprocess.run(
            ["quarto", "render", REPORT_QMD_PATH.name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "Quarto is not installed or is not available in PATH for this app environment."
        ) from error
    except subprocess.CalledProcessError as error:
        stderr = (error.stderr or "").strip()
        stdout = (error.stdout or "").strip()
        detail = stderr or stdout or "Unknown Quarto render error."
        raise RuntimeError(f"Quarto render failed: {detail}") from error

    if not REPORT_HTML_PATH.exists():
        render_log = (completed.stdout or "").strip()
        raise RuntimeError(
            "Quarto finished but report.html was not created. "
            f"Render output: {render_log or 'No output captured.'}"
        )

    status_message = (
        "Report rendered successfully.\n\n"
        f"`{REPORT_HTML_PATH.name}` is ready to download or open from this tab."
    )
    return status_message, str(REPORT_HTML_PATH), build_report_open_link(REPORT_HTML_PATH)


def load_structure_view_with_style(choice: str, style_choice: str):
    """Load a curated 3D structure view with a selected style preset."""
    return (
        build_structure_info_markdown(choice),
        build_structure_context_html(choice),
        build_structure_viewer_html(choice, style_choice=style_choice),
    )


def suggest_structure_for_name(protein_name: str):
    """Suggest a curated structure based on a known protein name."""
    suggestion = suggest_structure_choice(protein_name)
    if suggestion:
        return suggestion, f"Suggested curated structure: **{suggestion}**"

    return (
        get_structure_choices()[0],
        "No direct curated structure suggestion for that name yet. Choose one manually from the dropdown.",
    )
