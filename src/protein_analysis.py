"""Core helpers for beginner-friendly protein sequence analysis."""

from collections import Counter
from copy import deepcopy
from textwrap import fill

STANDARD_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def parse_fasta(text: str) -> tuple[str, str]:
    """Return the inferred input type and sequence body from FASTA or plain text."""
    if not text or not text.strip():
        raise ValueError("No sequence was provided.")

    stripped_text = text.strip()
    if stripped_text.startswith(">"):
        lines = [line.strip() for line in stripped_text.splitlines() if line.strip()]
        header = lines[0]
        sequence = "".join(lines[1:])
        if not sequence:
            raise ValueError("The FASTA input includes a header but no sequence.")
        return "FASTA", sequence

    return "Plain sequence", stripped_text


def clean_protein_sequence(sequence: str) -> str:
    """Normalize whitespace and capitalization for a protein sequence."""
    cleaned = "".join(sequence.split()).upper()
    if not cleaned:
        raise ValueError("The sequence is empty after removing whitespace.")
    return cleaned


def validate_protein_sequence(sequence: str) -> None:
    """Raise an error if the sequence contains non-standard amino acid letters."""
    invalid_characters = sorted({character for character in sequence if character not in STANDARD_AMINO_ACIDS})
    if invalid_characters:
        invalid_text = ", ".join(invalid_characters)
        raise ValueError(
            "The sequence contains invalid or unsupported amino acid characters: "
            f"{invalid_text}. Use standard one-letter amino acid codes only."
        )


def calculate_amino_acid_composition(sequence: str) -> list[dict[str, float | int | str]]:
    """Return counts and percentages for each amino acid found in the sequence."""
    total_length = len(sequence)
    counts = Counter(sequence)

    composition = []
    for amino_acid in sorted(counts):
        count = counts[amino_acid]
        percentage = (count / total_length) * 100
        composition.append(
            {
                "amino_acid": amino_acid,
                "count": count,
                "percentage": round(percentage, 2),
            }
        )

    return composition


def summarize_protein_sequence(text: str) -> dict[str, object]:
    """Parse, clean, validate, and summarize a protein sequence."""
    input_type, raw_sequence = parse_fasta(text)
    cleaned_sequence = clean_protein_sequence(raw_sequence)
    validate_protein_sequence(cleaned_sequence)

    composition = calculate_amino_acid_composition(cleaned_sequence)
    top_amino_acids = sorted(composition, key=lambda item: item["count"], reverse=True)[:5]
    most_common = top_amino_acids[0]["amino_acid"] if top_amino_acids else "N/A"

    return {
        "input_type": input_type,
        "cleaned_sequence": cleaned_sequence,
        "wrapped_sequence": fill(cleaned_sequence, width=60),
        "sequence_length": len(cleaned_sequence),
        "unique_amino_acids_detected": len({character for character in cleaned_sequence}),
        "most_common_amino_acid": most_common,
        "amino_acid_composition": composition,
        "top_amino_acids": top_amino_acids,
    }


def build_summary_table(summary: dict[str, object]) -> list[list[object]]:
    """Return a simple table shape that can be displayed in Gradio."""
    return [
        ["Input type", summary["input_type"]],
        ["Sequence length", summary["sequence_length"]],
        ["Unique amino acids detected", summary["unique_amino_acids_detected"]],
        ["Most common amino acid", summary["most_common_amino_acid"]],
    ]


def build_summary_cards(summary: dict[str, object]) -> str:
    """Return a compact Markdown summary for quick scanning in the UI."""
    return (
        "### Quick Summary\n\n"
        f"- Sequence length: **{summary['sequence_length']} amino acids**\n"
        f"- Most common amino acid: **{summary['most_common_amino_acid']}**\n"
        f"- Unique amino acids detected: **{summary['unique_amino_acids_detected']}**\n"
        f"- Input type: **{summary['input_type']}**\n"
    )


def build_summary_highlights_html(summary: dict[str, object]) -> str:
    """Return a small card-style HTML summary for the app."""
    cards = [
        ("Sequence Length", f"{summary['sequence_length']} aa"),
        ("Most Common", str(summary["most_common_amino_acid"])),
        ("Unique Amino Acids", str(summary["unique_amino_acids_detected"])),
        ("Input Type", str(summary["input_type"])),
    ]
    card_html = "".join(
        (
            "<div style=\"flex:1; min-width:160px; padding:14px 16px; border-radius:16px; "
            "background:linear-gradient(180deg, #f4fffd 0%, #ecfbf7 100%); "
            "border:1px solid #cdeee4;\">"
            f"<div style=\"font-size:0.85rem; color:#0f766e; margin-bottom:6px;\">{label}</div>"
            f"<div style=\"font-size:1.25rem; font-weight:700; color:#102a43;\">{value}</div>"
            "</div>"
        )
        for label, value in cards
    )
    return (
        "<div style=\"display:flex; flex-wrap:wrap; gap:12px; margin:8px 0 4px 0;\">"
        f"{card_html}"
        "</div>"
    )


def build_top_amino_acid_table(summary: dict[str, object]) -> list[list[object]]:
    """Return the top amino acids in a compact table format."""
    return [
        [item["amino_acid"], item["count"], item["percentage"]]
        for item in summary["top_amino_acids"]
    ]


def build_summary_export_payload(summary: dict[str, object], protein_name: str | None = None) -> dict[str, object]:
    """Return a JSON-friendly export payload for a single-sequence analysis."""
    protein_label = protein_name.strip() if protein_name and protein_name.strip() else "Unnamed protein"
    payload = deepcopy(summary)
    payload["protein_name"] = protein_label
    return payload


def build_summary_export_text(summary: dict[str, object], protein_name: str | None = None) -> str:
    """Return a plain-text export for a single-sequence analysis."""
    protein_label = protein_name.strip() if protein_name and protein_name.strip() else "Unnamed protein"
    top_rows = "\n".join(
        f"- {item['amino_acid']}: {item['count']} counts ({item['percentage']}%)"
        for item in summary["top_amino_acids"]
    )
    return (
        f"ProteinLens Sequence Export\n"
        f"Protein name: {protein_label}\n"
        f"Input type: {summary['input_type']}\n"
        f"Sequence length: {summary['sequence_length']}\n"
        f"Unique amino acids detected: {summary['unique_amino_acids_detected']}\n"
        f"Most common amino acid: {summary['most_common_amino_acid']}\n\n"
        f"Top amino acids:\n"
        f"{top_rows}\n\n"
        f"Cleaned sequence:\n"
        f"{summary['wrapped_sequence']}\n"
    )


def generate_protein_profile(summary: dict[str, object], protein_name: str | None = None) -> str:
    """Return a cautious interpretation template without using an LLM yet."""
    protein_label = protein_name.strip() if protein_name and protein_name.strip() else "This protein"
    top_residues = ", ".join(
        f"{item['amino_acid']} ({item['percentage']}%)" for item in summary["top_amino_acids"][:3]
    )

    return (
        f"## Plain-English Summary\n\n"
        f"{protein_label} has a sequence length of {summary['sequence_length']} amino acids. "
        f"The most common detected amino acid is {summary['most_common_amino_acid']}, and the sequence contains "
        f"{summary['unique_amino_acids_detected']} unique amino acid types.\n\n"
        f"## Key Observations\n\n"
        f"- Input type: {summary['input_type']}\n"
        f"- Most enriched residues in this simple composition view: {top_residues}\n"
        f"- This summary reflects sequence composition only, not confirmed structure or function\n\n"
        f"## Possible Biological Interpretation\n\n"
        f"Amino acid composition can help describe a protein at a basic level, but composition alone is not enough "
        f"to identify function, enzyme activity, localization, or drug relevance.\n\n"
        f"## Limitations\n\n"
        f"- No database lookup was used\n"
        f"- No domain, motif, or structure analysis was performed\n"
        f"- No experimental evidence is included\n\n"
        f"## What to Verify Manually\n\n"
        f"- Confirm the protein identity with UniProt or a similar database\n"
        f"- Check whether known domains or motifs match the sequence\n"
        f"- Review literature before making biological or drug-target claims\n"
    )


def _composition_lookup(summary: dict[str, object]) -> dict[str, dict[str, float | int | str]]:
    """Return composition rows indexed by amino acid."""
    return {
        item["amino_acid"]: item
        for item in summary["amino_acid_composition"]
    }


def compare_protein_sequences(
    first_text: str,
    second_text: str,
    first_name: str | None = None,
    second_name: str | None = None,
) -> dict[str, object]:
    """Compare two protein sequences using the same deterministic summary pipeline."""
    first_summary = summarize_protein_sequence(first_text)
    second_summary = summarize_protein_sequence(second_text)

    first_label = first_name.strip() if first_name and first_name.strip() else "Sequence 1"
    second_label = second_name.strip() if second_name and second_name.strip() else "Sequence 2"

    first_lookup = _composition_lookup(first_summary)
    second_lookup = _composition_lookup(second_summary)
    amino_acids = sorted(set(first_lookup) | set(second_lookup))

    comparison_rows = []
    for amino_acid in amino_acids:
        first_percentage = float(first_lookup.get(amino_acid, {}).get("percentage", 0.0))
        second_percentage = float(second_lookup.get(amino_acid, {}).get("percentage", 0.0))
        comparison_rows.append(
            {
                "amino_acid": amino_acid,
                "first_percentage": round(first_percentage, 2),
                "second_percentage": round(second_percentage, 2),
                "difference": round(first_percentage - second_percentage, 2),
            }
        )

    largest_differences = sorted(
        comparison_rows,
        key=lambda item: abs(item["difference"]),
        reverse=True,
    )[:5]

    length_difference = first_summary["sequence_length"] - second_summary["sequence_length"]

    notes = [
        f"{first_label} length: {first_summary['sequence_length']} amino acids",
        f"{second_label} length: {second_summary['sequence_length']} amino acids",
        f"Length difference ({first_label} - {second_label}): {length_difference} amino acids",
        (
            f"Most common amino acid in {first_label}: "
            f"{first_summary['most_common_amino_acid']}"
        ),
        (
            f"Most common amino acid in {second_label}: "
            f"{second_summary['most_common_amino_acid']}"
        ),
    ]

    return {
        "first_label": first_label,
        "second_label": second_label,
        "first_summary": first_summary,
        "second_summary": second_summary,
        "length_difference": length_difference,
        "composition_comparison": comparison_rows,
        "largest_differences": largest_differences,
        "notes": notes,
    }


def build_comparison_table(comparison: dict[str, object]) -> list[list[object]]:
    """Return a compact table comparing high-level sequence metrics."""
    first_summary = comparison["first_summary"]
    second_summary = comparison["second_summary"]
    return [
        ["Label", comparison["first_label"], comparison["second_label"]],
        ["Input type", first_summary["input_type"], second_summary["input_type"]],
        ["Sequence length", first_summary["sequence_length"], second_summary["sequence_length"]],
        [
            "Unique amino acids",
            first_summary["unique_amino_acids_detected"],
            second_summary["unique_amino_acids_detected"],
        ],
        [
            "Most common amino acid",
            first_summary["most_common_amino_acid"],
            second_summary["most_common_amino_acid"],
        ],
    ]


def build_comparison_notes(comparison: dict[str, object]) -> str:
    """Return a Markdown comparison summary for the UI."""
    largest_differences = "\n".join(
        (
            f"- {item['amino_acid']}: "
            f"{comparison['first_label']} {item['first_percentage']}% vs "
            f"{comparison['second_label']} {item['second_percentage']}% "
            f"(difference {item['difference']}%)"
        )
        for item in comparison["largest_differences"]
    )

    notes_text = "\n".join(f"- {note}" for note in comparison["notes"])

    return (
        "## Comparison Summary\n\n"
        f"{notes_text}\n\n"
        "## Largest Composition Differences\n\n"
        f"{largest_differences}\n\n"
        "## Interpretation Reminder\n\n"
        "These differences are useful for describing the sequences, but they do not prove functional differences. "
        "A stronger biological conclusion would still need database, domain, structure, or experimental validation.\n"
    )


def build_comparison_difference_table(comparison: dict[str, object]) -> list[list[object]]:
    """Return the largest composition differences in table form."""
    return [
        [
            item["amino_acid"],
            item["first_percentage"],
            item["second_percentage"],
            item["difference"],
        ]
        for item in comparison["largest_differences"]
    ]


def build_comparison_export_payload(comparison: dict[str, object]) -> dict[str, object]:
    """Return a JSON-friendly export payload for sequence comparison."""
    return deepcopy(comparison)


def build_comparison_export_text(comparison: dict[str, object]) -> str:
    """Return a plain-text export for sequence comparison."""
    top_rows = "\n".join(
        (
            f"- {item['amino_acid']}: "
            f"{comparison['first_label']} {item['first_percentage']}% vs "
            f"{comparison['second_label']} {item['second_percentage']}% "
            f"(difference {item['difference']}%)"
        )
        for item in comparison["largest_differences"]
    )
    return (
        f"ProteinLens Comparison Export\n"
        f"Sequence 1: {comparison['first_label']}\n"
        f"Sequence 2: {comparison['second_label']}\n"
        f"Sequence 1 length: {comparison['first_summary']['sequence_length']}\n"
        f"Sequence 2 length: {comparison['second_summary']['sequence_length']}\n"
        f"Length difference: {comparison['length_difference']}\n\n"
        f"Largest composition differences:\n"
        f"{top_rows}\n"
    )
