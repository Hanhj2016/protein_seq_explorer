"""Tests for deterministic protein sequence analysis helpers."""

import unittest
from pathlib import Path

from src.app_config import EXAMPLE_FASTA_PATH
from src.app_services import build_analysis_quality_panel, export_sequence_results
from src.llm_helper import format_protein_summary_prompt
from src.protein_analysis import (
    build_comparison_export_text,
    build_summary_export_text,
    build_summary_cards,
    clean_protein_sequence,
    compare_protein_sequences,
    parse_fasta,
    summarize_protein_sequence,
    validate_protein_sequence,
)
from src.sequence_visuals import build_sequence_fingerprint_svg, classify_amino_acid
from src.structure_viewer import (
    build_structure_info_markdown,
    get_structure_choices,
    get_structure_style_choices,
    suggest_structure_choice,
)
from src.ui_content import build_report_open_link


class ProteinAnalysisTests(unittest.TestCase):
    def test_parse_fasta_detects_header_and_sequence(self):
        input_text = ">Example\nACDEFG\nHIK"
        input_type, sequence = parse_fasta(input_text)
        self.assertEqual(input_type, "FASTA")
        self.assertEqual(sequence, "ACDEFGHIK")

    def test_clean_protein_sequence_normalizes_whitespace_and_case(self):
        self.assertEqual(clean_protein_sequence(" acd eF \n g "), "ACDEFG")

    def test_validate_protein_sequence_rejects_invalid_characters(self):
        with self.assertRaises(ValueError) as context:
            validate_protein_sequence("ACDZ")
        self.assertIn("Z", str(context.exception))

    def test_summarize_protein_sequence_returns_expected_metrics(self):
        summary = summarize_protein_sequence(">Example\nAACC")
        self.assertEqual(summary["input_type"], "FASTA")
        self.assertEqual(summary["sequence_length"], 4)
        self.assertEqual(summary["most_common_amino_acid"], "A")
        self.assertEqual(summary["unique_amino_acids_detected"], 2)

    def test_build_summary_cards_contains_core_values(self):
        summary = summarize_protein_sequence("AACC")
        cards = build_summary_cards(summary)
        self.assertIn("Sequence length", cards)
        self.assertIn("Most common amino acid", cards)

    def test_compare_protein_sequences_returns_length_difference(self):
        comparison = compare_protein_sequences("AAAA", "AA")
        self.assertEqual(comparison["length_difference"], 2)
        self.assertEqual(comparison["first_summary"]["sequence_length"], 4)
        self.assertEqual(comparison["second_summary"]["sequence_length"], 2)

    def test_compare_protein_sequences_tracks_composition_differences(self):
        comparison = compare_protein_sequences("AAAA", "CCCC", "Alpha", "Beta")
        self.assertEqual(comparison["first_label"], "Alpha")
        self.assertEqual(comparison["second_label"], "Beta")
        largest = comparison["largest_differences"][0]
        self.assertIn(largest["amino_acid"], {"A", "C"})
        self.assertTrue(abs(largest["difference"]) > 0)

    def test_build_summary_export_text_includes_core_fields(self):
        summary = summarize_protein_sequence("AACC")
        export_text = build_summary_export_text(summary, "Example Protein")
        self.assertIn("ProteinLens Sequence Export", export_text)
        self.assertIn("Example Protein", export_text)
        self.assertIn("Sequence length: 4", export_text)

    def test_build_comparison_export_text_includes_labels(self):
        comparison = compare_protein_sequences("AAAA", "CCCC", "Alpha", "Beta")
        export_text = build_comparison_export_text(comparison)
        self.assertIn("ProteinLens Comparison Export", export_text)
        self.assertIn("Sequence 1: Alpha", export_text)
        self.assertIn("Sequence 2: Beta", export_text)

    def test_classify_amino_acid_returns_expected_group(self):
        residue_class, color = classify_amino_acid("D")
        self.assertEqual(residue_class, "Negative")
        self.assertTrue(color.startswith("#"))

    def test_build_sequence_fingerprint_svg_contains_svg_markup(self):
        svg = build_sequence_fingerprint_svg("ACDE")
        self.assertIn("<svg", svg)
        self.assertIn("Position 1: A", svg)

    def test_create_comparison_delta_chart_returns_figure(self):
        try:
            from src.plots import create_comparison_delta_chart
        except ModuleNotFoundError:
            self.skipTest("plotly is not available in the current test environment")

        comparison = compare_protein_sequences("AAAA", "CCCC", "Alpha", "Beta")
        figure = create_comparison_delta_chart(comparison)
        self.assertEqual(figure.__class__.__name__, "Figure")

    def test_structure_choices_are_available(self):
        choices = get_structure_choices()
        self.assertTrue(len(choices) >= 1)

    def test_structure_info_mentions_external_reference(self):
        info = build_structure_info_markdown(get_structure_choices()[0])
        self.assertIn("external reference structure", info)

    def test_structure_style_choices_are_available(self):
        styles = get_structure_style_choices()
        self.assertTrue(len(styles) >= 1)

    def test_structure_suggestion_finds_known_alias(self):
        self.assertEqual(
            suggest_structure_choice("EGFR"),
            "EGFR kinase domain (PDB: 1M17)",
        )

    def test_export_sequence_results_rejects_missing_summary(self):
        with self.assertRaises(ValueError):
            export_sequence_results(None, "Example")

    def test_build_report_open_link_targets_report_name(self):
        html = build_report_open_link(Path("report.html"))
        self.assertIn("/gradio_api/file=report.html", html)
        self.assertIn("Open Rendered Report", html)

    def test_format_protein_summary_prompt_uses_new_profile_sections(self):
        summary = summarize_protein_sequence("AACC")
        prompt = format_protein_summary_prompt(summary, "Example Protein")
        self.assertIn("## Function Summary", prompt)
        self.assertIn("## Possible Drug Relevance", prompt)
        self.assertIn("## Key Terms To Learn", prompt)
        self.assertIn("## Verification Checklist", prompt)

    def test_build_analysis_quality_panel_marks_example_data(self):
        summary = summarize_protein_sequence(EXAMPLE_FASTA_PATH.read_text())
        panel_html = build_analysis_quality_panel(summary)
        self.assertIn("Example data", panel_html)
        self.assertIn("Validation passed", panel_html)


if __name__ == "__main__":
    unittest.main()
