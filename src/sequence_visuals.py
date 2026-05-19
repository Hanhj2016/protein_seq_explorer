"""SVG and residue-class helpers for sequence-level visualizations."""

AMINO_ACID_CLASSES = {
    "A": ("Hydrophobic", "#2bb3a8"),
    "V": ("Hydrophobic", "#2bb3a8"),
    "I": ("Hydrophobic", "#2bb3a8"),
    "L": ("Hydrophobic", "#2bb3a8"),
    "M": ("Hydrophobic", "#2bb3a8"),
    "F": ("Aromatic", "#4c6ef5"),
    "W": ("Aromatic", "#4c6ef5"),
    "Y": ("Aromatic", "#4c6ef5"),
    "S": ("Polar", "#7bd389"),
    "T": ("Polar", "#7bd389"),
    "N": ("Polar", "#7bd389"),
    "Q": ("Polar", "#7bd389"),
    "C": ("Special", "#f6bd60"),
    "G": ("Special", "#f6bd60"),
    "P": ("Special", "#f6bd60"),
    "D": ("Negative", "#ef476f"),
    "E": ("Negative", "#ef476f"),
    "K": ("Positive", "#9b5de5"),
    "R": ("Positive", "#9b5de5"),
    "H": ("Positive", "#9b5de5"),
}


def classify_amino_acid(residue: str) -> tuple[str, str]:
    """Return the residue class label and display color."""
    return AMINO_ACID_CLASSES.get(residue, ("Unknown", "#94a3b8"))


def build_residue_class_legend_html() -> str:
    """Return a compact HTML legend for residue classes."""
    unique_classes: dict[str, str] = {}
    for class_name, color in AMINO_ACID_CLASSES.values():
        unique_classes[class_name] = color

    badges = "".join(
        (
            "<span style=\"display:inline-flex; align-items:center; gap:8px; margin:4px 10px 4px 0; "
            "padding:6px 10px; border-radius:999px; background:#f8fafc; border:1px solid #dbe7f0;\">"
            f"<span style=\"width:12px; height:12px; border-radius:999px; background:{color}; display:inline-block;\"></span>"
            f"<span style=\"font-size:0.9rem; color:#243b53;\">{class_name}</span>"
            "</span>"
        )
        for class_name, color in unique_classes.items()
    )
    return f"<div style=\"margin:8px 0 12px 0;\">{badges}</div>"


def build_sequence_fingerprint_svg(sequence: str, line_width: int = 50) -> str:
    """Render a simple SVG residue fingerprint with hover tooltips."""
    if not sequence:
        raise ValueError("No sequence is available for the fingerprint view.")

    block = 14
    gap = 2
    rows = (len(sequence) + line_width - 1) // line_width
    width = min(line_width, len(sequence)) * (block + gap) + 120
    height = rows * (block + gap + 12) + 40

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Protein sequence fingerprint">'
    ]
    svg_parts.append(
        '<rect x="0" y="0" width="100%" height="100%" rx="18" fill="#f8fffd" stroke="#d7efe8"/>'
    )
    svg_parts.append(
        '<text x="18" y="24" font-size="14" font-weight="700" fill="#12344d">Sequence Fingerprint</text>'
    )

    y_offset = 40
    for index, residue in enumerate(sequence):
        row = index // line_width
        col = index % line_width
        x = 18 + col * (block + gap)
        y = y_offset + row * (block + gap + 12)
        class_name, color = classify_amino_acid(residue)

        svg_parts.append(
            f'<rect x="{x}" y="{y}" width="{block}" height="{block}" rx="3" fill="{color}" opacity="0.9">'
            f'<title>Position {index + 1}: {residue} ({class_name})</title>'
            "</rect>"
        )

        if col == 0:
            svg_parts.append(
                f'<text x="{x + line_width * (block + gap) + 10}" y="{y + 11}" font-size="10" fill="#486581">'
                f"{index + 1}"
                "</text>"
            )

    svg_parts.append("</svg>")
    return "".join(svg_parts)
