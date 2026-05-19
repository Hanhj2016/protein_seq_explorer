"""Gradio app for beginner-friendly protein sequence exploration."""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import gradio as gr

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
    get_structure_style_choices,
    suggest_structure_choice,
)

EXAMPLE_FASTA_PATH = Path("data/example_protein.fasta")
EXAMPLE_FASTA_VARIANT_PATH = Path("data/example_protein_variant.fasta")
EXPORTS_DIR = Path("outputs/exports")
PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_QMD_PATH = PROJECT_ROOT / "report.qmd"
REPORT_HTML_PATH = PROJECT_ROOT / "report.html"


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


def build_hero_html() -> str:
    """Return a more expressive hero block for the top of the app."""
    return """
    <section style="
        padding: 22px 24px 18px 24px;
        border-radius: 24px;
        background:
            radial-gradient(circle at top left, rgba(43, 179, 168, 0.20), transparent 32%),
            radial-gradient(circle at top right, rgba(76, 110, 245, 0.14), transparent 28%),
            linear-gradient(135deg, #f8fffd 0%, #eef8ff 100%);
        border: 1px solid #d7ebe7;
        box-shadow: 0 14px 40px rgba(21, 41, 53, 0.06);
        margin-bottom: 14px;
    ">
      <div style="display:flex; flex-wrap:wrap; gap:18px; align-items:flex-start; justify-content:space-between;">
        <div style="max-width:760px;">
          <div style="font-size:0.88rem; letter-spacing:0.08em; text-transform:uppercase; color:#0f766e; font-weight:700; margin-bottom:10px;">
            Biochemistry + Python + AI
          </div>
          <h1 style="margin:0 0 10px 0; font-size:2.35rem; line-height:1.05; color:#102a43;">🧬 ProteinLens</h1>
          <p style="margin:0 0 10px 0; font-size:1.15rem; color:#243b53;">
            Explore protein sequences with vivid charts, sequence fingerprints, and cautious AI-assisted interpretation.
          </p>
          <p style="margin:0; font-size:0.98rem; color:#486581;">
            Deterministic analysis runs first. The AI layer is optional, and the comparison workflow helps surface sequence-level differences quickly.
          </p>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:10px; max-width:300px;">
          <div style="padding:12px 14px; border-radius:16px; background:#ffffffcc; border:1px solid #d7ebe7; min-width:130px;">
            <div style="font-size:0.8rem; color:#0f766e; margin-bottom:4px;">Core Modes</div>
            <div style="font-weight:700; color:#102a43;">Analyze + Compare</div>
          </div>
          <div style="padding:12px 14px; border-radius:16px; background:#ffffffcc; border:1px solid #d7ebe7; min-width:130px;">
            <div style="font-size:0.8rem; color:#0f766e; margin-bottom:4px;">Outputs</div>
            <div style="font-weight:700; color:#102a43;">Plots + SVG + Export</div>
          </div>
          <div style="padding:12px 14px; border-radius:16px; background:#ffffffcc; border:1px solid #d7ebe7; min-width:130px;">
            <div style="font-size:0.8rem; color:#0f766e; margin-bottom:4px;">Advanced</div>
            <div style="font-weight:700; color:#102a43;">Optional 3D Reference</div>
          </div>
        </div>
      </div>
    </section>
    """


def build_comparison_intro_html() -> str:
    """Return a styled intro card for the comparison section."""
    return """
    <section style="
        padding: 18px 20px;
        border-radius: 22px;
        background: linear-gradient(135deg, #f7fbff 0%, #f8fffd 100%);
        border: 1px solid #d8e8f5;
        margin: 16px 0 12px 0;
    ">
      <div style="font-size:0.85rem; letter-spacing:0.06em; text-transform:uppercase; color:#0f766e; font-weight:700; margin-bottom:8px;">
        Side-by-Side Workflow
      </div>
      <h2 style="margin:0 0 8px 0; color:#102a43;">Compare Two Sequences</h2>
      <p style="margin:0 0 8px 0; color:#243b53;">
        Use this section to compare sequence length, residue enrichment, and amino acid composition across two proteins.
      </p>
      <p style="margin:0; color:#486581;">
        Tip: the sample button loads two different built-in FASTA examples so the comparison charts and tables are immediately meaningful.
      </p>
    </section>
    """


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
    """Run deterministic sequence analysis and format the outputs for Gradio."""
    try:
        summary = summarize_protein_sequence(sequence_text)
    except ValueError as error:
        raise gr.Error(str(error)) from error

    summary_table = build_summary_table(summary)
    summary_cards = build_summary_cards(summary)
    summary_highlights = build_summary_highlights_html(summary)
    top_table = build_top_amino_acid_table(summary)
    chart = create_composition_chart(summary["amino_acid_composition"])
    donut_chart = create_top_residues_donut(summary["amino_acid_composition"])
    fingerprint_svg = build_sequence_fingerprint_svg(summary["cleaned_sequence"])
    residue_legend = build_residue_class_legend_html()
    profile = generate_protein_profile(summary, protein_name=protein_name)
    ai_placeholder = (
        "AI explanation not generated yet.\n\n"
        "Use the **Generate AI Explanation** button after running deterministic analysis."
    )

    return (
        summary,
        summary_highlights,
        summary_cards,
        summary_table,
        top_table,
        chart,
        donut_chart,
        residue_legend,
        residue_legend,
        fingerprint_svg,
        profile,
        ai_placeholder,
        summary["wrapped_sequence"],
    )


def generate_ai_explanation(summary: dict | None, sequence_text: str, protein_name: str):
    """Generate an optional AI explanation from the deterministic summary."""
    try:
        active_summary = summary if summary else summarize_protein_sequence(sequence_text)
    except ValueError as error:
        raise gr.Error(str(error)) from error

    try:
        user_prompt = format_protein_summary_prompt(active_summary, protein_name=protein_name)
        return call_llm(SCIENTIFIC_CAUTION_SYSTEM_PROMPT, user_prompt)
    except Exception as error:
        raise gr.Error(str(error)) from error


def compare_sequences(
    first_sequence_text: str,
    second_sequence_text: str,
    first_name: str,
    second_name: str,
):
    """Compare two sequences and format the results for Gradio."""
    try:
        comparison = compare_protein_sequences(
            first_sequence_text,
            second_sequence_text,
            first_name=first_name,
            second_name=second_name,
        )
    except ValueError as error:
        raise gr.Error(str(error)) from error

    return (
        comparison,
        build_comparison_table(comparison),
        create_comparison_delta_chart(comparison),
        create_comparison_heatmap(comparison),
        build_comparison_difference_table(comparison),
        build_comparison_notes(comparison),
        create_comparison_delta_chart(comparison),
    )


def export_sequence_results(summary: dict | None, protein_name: str):
    """Export single-sequence results as text and JSON files."""
    if not summary:
        raise gr.Error("Analyze a sequence before exporting results.")

    protein_label = protein_name.strip() if protein_name and protein_name.strip() else "protein-sequence"
    base_name = _safe_slug(protein_label, "protein-sequence")
    text_content = build_summary_export_text(summary, protein_name=protein_name)
    json_payload = build_summary_export_payload(summary, protein_name=protein_name)
    return _write_export_files(base_name, text_content, json_payload)


def export_comparison_results(comparison: dict | None):
    """Export comparison results as text and JSON files."""
    if not comparison:
        raise gr.Error("Compare two sequences before exporting comparison results.")

    label = f"{comparison['first_label']}-vs-{comparison['second_label']}"
    base_name = _safe_slug(label, "protein-comparison")
    text_content = build_comparison_export_text(comparison)
    json_payload = build_comparison_export_payload(comparison)
    return _write_export_files(base_name, text_content, json_payload)


def _build_report_open_link(report_path: Path) -> str:
    """Return a small HTML block that opens the rendered report in a new tab."""
    report_url = f"/gradio_api/file={report_path.name}"
    return f"""
    <div style="padding:10px 0 4px 0;">
      <a
        href="{report_url}"
        target="_blank"
        rel="noopener noreferrer"
        style="
          display:inline-block;
          padding:10px 14px;
          border-radius:12px;
          background:linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
          color:#ffffff;
          font-weight:700;
          text-decoration:none;
          box-shadow:0 10px 24px rgba(20, 184, 166, 0.18);
        "
      >
        Open Rendered Report
      </a>
    </div>
    """


def render_quarto_report() -> tuple[str, str, str]:
    """Render the Quarto report and return status, output file path, and open link."""
    if not REPORT_QMD_PATH.exists():
        raise gr.Error("Could not find report.qmd in the project root.")

    try:
        completed = subprocess.run(
            ["quarto", "render", REPORT_QMD_PATH.name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as error:
        raise gr.Error(
            "Quarto is not installed or is not available in PATH for this app environment."
        ) from error
    except subprocess.CalledProcessError as error:
        stderr = (error.stderr or "").strip()
        stdout = (error.stdout or "").strip()
        detail = stderr or stdout or "Unknown Quarto render error."
        raise gr.Error(f"Quarto render failed: {detail}") from error

    if not REPORT_HTML_PATH.exists():
        render_log = (completed.stdout or "").strip()
        raise gr.Error(
            "Quarto finished but report.html was not created. "
            f"Render output: {render_log or 'No output captured.'}"
        )

    status_message = (
        "Report rendered successfully.\n\n"
        f"`{REPORT_HTML_PATH.name}` is ready to download or open from this tab."
    )
    return status_message, str(REPORT_HTML_PATH), _build_report_open_link(REPORT_HTML_PATH)


def load_structure_view(choice: str):
    """Load a curated 3D structure reference view."""
    return (
        build_structure_info_markdown(choice),
        build_structure_context_html(choice),
        build_structure_viewer_html(choice),
    )


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
        return (
            suggestion,
            f"Suggested curated structure: **{suggestion}**",
        )
    return (
        get_structure_choices()[0],
        "No direct curated structure suggestion for that name yet. Choose one manually from the dropdown.",
    )


def get_structure_placeholder() -> tuple[str, str]:
    """Return a lightweight placeholder before the 3D viewer is loaded."""
    return (
        "### Curated 3D Reference\n\n"
        "Select an example and click **Load 3D Structure** to fetch a public reference model.\n\n"
        "This keeps the main app responsive until you explicitly open the structure workflow.",
        """
        <div style="
            min-height: 280px;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            padding:24px;
            border:1px dashed #b8d8d1;
            border-radius:20px;
            background:linear-gradient(180deg, #f8fffd 0%, #eef8ff 100%);
            color:#486581;
        ">
          3D structure view is not loaded yet.<br/>Choose a curated example and click <strong>Load 3D Structure</strong>.
        </div>
        """,
    )


with gr.Blocks(
    title="ProteinLens",
    theme=gr.themes.Soft(
        primary_hue="teal",
        secondary_hue="emerald",
        neutral_hue="slate",
    ),
) as demo:
    gr.HTML(build_hero_html())
    gr.Markdown(
        """
        Use the top section for one-sequence analysis and interpretation.
        The comparison section lower on the page is for side-by-side sequence exploration.
        """
    )

    analysis_state = gr.State(None)
    comparison_state = gr.State(None)

    with gr.Row():
        sequence_input = gr.Textbox(
            label="Protein Sequence Input",
            lines=12,
            placeholder="Paste FASTA or plain protein sequence here...",
        )
        with gr.Column():
            protein_name_input = gr.Textbox(
                label="Protein Name (Optional)",
                placeholder="Example: EGFR",
            )
            load_sample_button = gr.Button("Load Sample FASTA", variant="secondary")
            analyze_button = gr.Button("Analyze Sequence", variant="primary")

    with gr.Tabs():
        with gr.Tab("Sequence Summary"):
            summary_highlights_output = gr.HTML(label="Summary Highlights")
            summary_cards_output = gr.Markdown(label="Quick Summary")
            summary_output = gr.Dataframe(
                headers=["Metric", "Value"],
                datatype=["str", "str"],
                row_count=(4, "fixed"),
                col_count=(2, "fixed"),
                label="Summary Metrics",
            )
            cleaned_sequence_output = gr.Textbox(
                label="Cleaned Sequence",
                lines=6,
            )

        with gr.Tab("Amino Acid Composition"):
            residue_legend_output = gr.HTML(label="Residue Class Legend")
            with gr.Row():
                chart_output = gr.Plot(label="Composition Chart")
                donut_chart_output = gr.Plot(label="Top Residues Donut")
            top_amino_acids_output = gr.Dataframe(
                headers=["Amino Acid", "Count", "Percentage"],
                datatype=["str", "number", "number"],
                row_count=(5, "fixed"),
                col_count=(3, "fixed"),
                label="Top Amino Acids",
            )

        with gr.Tab("Sequence Fingerprint"):
            gr.Markdown(
                "This fingerprint colors residues by broad biochemical class. Hover over each block to inspect position and residue identity."
            )
            fingerprint_legend_output = gr.HTML(label="Fingerprint Legend")
            fingerprint_output = gr.HTML(label="Sequence Fingerprint")

        with gr.Tab("Protein Profile"):
            profile_output = gr.Markdown(label="Interpretation Template")

        with gr.Tab("AI Explanation"):
            gr.Markdown(
                """
                Optional step: this uses summarized sequence statistics and requires
                `OPENAI_API_KEY` in a local `.env` file.
                """
            )
            generate_ai_button = gr.Button("Generate AI Explanation", variant="primary")
            ai_output = gr.Markdown(label="AI Explanation")

        with gr.Tab("Advanced 3D Reference"):
            gr.Markdown(
                """
                Advanced optional extension:
                this tab shows curated public 3D structures for known proteins.
                It is an external teaching reference and is **not derived automatically** from the pasted sequence.
                The core ProteinLens workflow remains sequence-first analysis, visualization, and cautious interpretation.
                """
            )
            with gr.Row():
                structure_choice = gr.Dropdown(
                    choices=get_structure_choices(),
                    value=get_structure_choices()[0],
                    label="Curated Structure Example",
                )
                structure_style_choice = gr.Dropdown(
                    choices=get_structure_style_choices(),
                    value=get_structure_style_choices()[0],
                    label="Viewer Style",
                )
            suggest_structure_button = gr.Button("Suggest Structure From Protein Name", variant="secondary")
            load_structure_button = gr.Button("Load 3D Structure", variant="secondary")
            placeholder_info, placeholder_html = get_structure_placeholder()
            structure_suggestion_output = gr.Markdown(
                value="Enter a known protein name in the main input section to get a curated 3D suggestion.",
                label="Structure Suggestion",
            )
            structure_info_output = gr.Markdown(value=placeholder_info, label="Structure Provenance")
            structure_context_output = gr.HTML(
                value="<div style='display:none;'></div>",
                label="Why This Structure Matters",
            )
            structure_view_output = gr.HTML(value=placeholder_html, label="3D Viewer")

        with gr.Tab("Export"):
            gr.Markdown("Save the current single-sequence results as text and JSON files.")
            export_sequence_button = gr.Button("Export Sequence Results", variant="secondary")
            sequence_export_text_file = gr.File(label="Text Export")
            sequence_export_json_file = gr.File(label="JSON Export")
            gr.Markdown(
                "You can also render the Quarto report from inside the app. "
                "This requires `quarto` to be installed in the active Conda environment."
            )
            render_report_button = gr.Button("Render Quarto Report", variant="secondary")
            report_render_status = gr.Markdown(
                "Report not rendered in this session yet.",
                label="Report Render Status",
            )
            report_html_file = gr.File(label="Rendered HTML Report")
            report_open_link = gr.HTML(
                value="<div style='color:#486581; padding:6px 0;'>Render the report to open it in a new tab here.</div>",
                label="Open Rendered Report",
            )

    gr.HTML(build_comparison_intro_html())

    with gr.Row():
        comparison_sequence_one = gr.Textbox(
            label="Sequence 1 Input",
            lines=10,
            placeholder="Paste the first FASTA or plain protein sequence here...",
        )
        comparison_sequence_two = gr.Textbox(
            label="Sequence 2 Input",
            lines=10,
            placeholder="Paste the second FASTA or plain protein sequence here...",
        )

    with gr.Row():
        comparison_name_one = gr.Textbox(
            label="Sequence 1 Name (Optional)",
            placeholder="Example: EGFR",
        )
        comparison_name_two = gr.Textbox(
            label="Sequence 2 Name (Optional)",
            placeholder="Example: HER2",
        )

    with gr.Row():
        comparison_sample_button = gr.Button("Load Two Sample Sequences", variant="secondary")
        comparison_button = gr.Button("Compare Sequences", variant="primary")

    with gr.Tabs():
        with gr.Tab("Comparison Summary"):
            comparison_summary_output = gr.Dataframe(
                headers=["Metric", "Sequence 1", "Sequence 2"],
                datatype=["str", "str", "str"],
                row_count=(5, "fixed"),
                col_count=(3, "fixed"),
                label="Comparison Metrics",
            )
            comparison_delta_chart_summary_output = gr.Plot(label="Residue Difference Chart")
            comparison_heatmap_summary_output = gr.Plot(label="Residue Composition Heatmap")
            comparison_notes_output = gr.Markdown(label="Comparison Notes")

        with gr.Tab("Top Differences"):
            comparison_difference_output = gr.Dataframe(
                headers=["Amino Acid", "Sequence 1 %", "Sequence 2 %", "Difference"],
                datatype=["str", "number", "number", "number"],
                row_count=(5, "fixed"),
                col_count=(4, "fixed"),
                label="Largest Composition Differences",
            )
            comparison_delta_chart_output = gr.Plot(label="Residue Difference Chart")

        with gr.Tab("Comparison Export"):
            gr.Markdown("Save the current comparison results as text and JSON files.")
            export_comparison_button = gr.Button("Export Comparison Results", variant="secondary")
            comparison_export_text_file = gr.File(label="Comparison Text Export")
            comparison_export_json_file = gr.File(label="Comparison JSON Export")

    load_sample_button.click(
        fn=load_example_fasta,
        outputs=sequence_input,
    )
    comparison_sample_button.click(
        fn=load_comparison_examples,
        outputs=[
            comparison_sequence_one,
            comparison_sequence_two,
            comparison_name_one,
            comparison_name_two,
        ],
    )
    analyze_button.click(
        fn=analyze_sequence,
        inputs=[sequence_input, protein_name_input],
        outputs=[
            analysis_state,
            summary_highlights_output,
            summary_cards_output,
            summary_output,
            top_amino_acids_output,
            chart_output,
            donut_chart_output,
            residue_legend_output,
            fingerprint_legend_output,
            fingerprint_output,
            profile_output,
            ai_output,
            cleaned_sequence_output,
        ],
    )
    generate_ai_button.click(
        fn=generate_ai_explanation,
        inputs=[analysis_state, sequence_input, protein_name_input],
        outputs=ai_output,
    )
    load_structure_button.click(
        fn=load_structure_view_with_style,
        inputs=[structure_choice, structure_style_choice],
        outputs=[structure_info_output, structure_context_output, structure_view_output],
    )
    suggest_structure_button.click(
        fn=suggest_structure_for_name,
        inputs=protein_name_input,
        outputs=[structure_choice, structure_suggestion_output],
    )
    comparison_button.click(
        fn=compare_sequences,
        inputs=[
            comparison_sequence_one,
            comparison_sequence_two,
            comparison_name_one,
            comparison_name_two,
        ],
        outputs=[
            comparison_state,
            comparison_summary_output,
            comparison_delta_chart_summary_output,
            comparison_heatmap_summary_output,
            comparison_difference_output,
            comparison_notes_output,
            comparison_delta_chart_output,
        ],
    )
    export_sequence_button.click(
        fn=export_sequence_results,
        inputs=[analysis_state, protein_name_input],
        outputs=[sequence_export_text_file, sequence_export_json_file],
    )
    render_report_button.click(
        fn=render_quarto_report,
        outputs=[report_render_status, report_html_file, report_open_link],
    )
    export_comparison_button.click(
        fn=export_comparison_results,
        inputs=[comparison_state],
        outputs=[comparison_export_text_file, comparison_export_json_file],
    )

if __name__ == "__main__":
    demo.launch(allowed_paths=[str(PROJECT_ROOT)])
