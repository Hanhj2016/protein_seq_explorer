"""Gradio app for beginner-friendly protein sequence exploration."""

import gradio as gr

from src.app_config import PROJECT_ROOT
from src.app_services import (
    analyze_sequence,
    compare_sequences,
    export_comparison_results,
    export_sequence_results,
    generate_ai_explanation,
    load_comparison_examples,
    load_example_fasta,
    load_structure_view_with_style,
    render_quarto_report,
    suggest_structure_for_name,
)
from src.structure_viewer import get_structure_choices, get_structure_style_choices
from src.ui_content import build_comparison_intro_html, build_hero_html, get_structure_placeholder


def _run_gradio_action(callback, *args):
    """Translate regular Python exceptions into Gradio UI errors."""
    try:
        return callback(*args)
    except (ValueError, RuntimeError, FileNotFoundError) as error:
        raise gr.Error(str(error)) from error


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
            cleaned_sequence_output = gr.Textbox(label="Cleaned Sequence", lines=6)

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

    load_sample_button.click(fn=load_example_fasta, outputs=sequence_input)
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
        fn=lambda sequence_text, protein_name: _run_gradio_action(analyze_sequence, sequence_text, protein_name),
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
        fn=lambda summary, sequence_text, protein_name: _run_gradio_action(
            generate_ai_explanation,
            summary,
            sequence_text,
            protein_name,
        ),
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
        fn=lambda first_text, second_text, first_name, second_name: _run_gradio_action(
            compare_sequences,
            first_text,
            second_text,
            first_name,
            second_name,
        ),
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
        fn=lambda summary, protein_name: _run_gradio_action(export_sequence_results, summary, protein_name),
        inputs=[analysis_state, protein_name_input],
        outputs=[sequence_export_text_file, sequence_export_json_file],
    )
    render_report_button.click(
        fn=lambda: _run_gradio_action(render_quarto_report),
        outputs=[report_render_status, report_html_file, report_open_link],
    )
    export_comparison_button.click(
        fn=lambda comparison: _run_gradio_action(export_comparison_results, comparison),
        inputs=[comparison_state],
        outputs=[comparison_export_text_file, comparison_export_json_file],
    )


if __name__ == "__main__":
    demo.launch(allowed_paths=[str(PROJECT_ROOT)])
