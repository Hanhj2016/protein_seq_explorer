"""Plot helpers for ProteinLens."""

import plotly.express as px
import plotly.graph_objects as go

from src.sequence_visuals import classify_amino_acid


def create_composition_chart(composition: list[dict[str, object]]):
    """Create a bar chart for amino acid composition percentages."""
    if not composition:
        raise ValueError("No amino acid composition data is available to plot.")

    chart_rows = []
    for item in composition:
        residue_class, color = classify_amino_acid(str(item["amino_acid"]))
        chart_rows.append(
            {
                **item,
                "residue_class": residue_class,
                "display_color": color,
            }
        )

    figure = px.bar(
        chart_rows,
        x="amino_acid",
        y="percentage",
        hover_data=["count", "residue_class"],
        labels={
            "amino_acid": "Amino Acid",
            "percentage": "Percentage (%)",
            "count": "Count",
            "residue_class": "Residue Class",
        },
        color="residue_class",
        color_discrete_map={row["residue_class"]: row["display_color"] for row in chart_rows},
    )
    figure.update_layout(
        title="Amino Acid Composition",
        template="plotly_white",
        xaxis_tickangle=0,
        margin=dict(l=40, r=20, t=60, b=40),
        legend_title_text="Residue Class",
    )
    return figure


def create_comparison_delta_chart(comparison: dict[str, object]):
    """Create a diverging bar chart for residue percentage differences."""
    rows = comparison["composition_comparison"]
    if not rows:
        raise ValueError("No comparison data is available to plot.")

    sorted_rows = sorted(rows, key=lambda item: item["difference"])
    colors = ["#ef476f" if item["difference"] < 0 else "#118ab2" for item in sorted_rows]
    hover_text = [
        (
            f"{item['amino_acid']}: {comparison['first_label']} {item['first_percentage']}%<br>"
            f"{comparison['second_label']} {item['second_percentage']}%<br>"
            f"Difference: {item['difference']}%"
        )
        for item in sorted_rows
    ]

    figure = go.Figure(
        go.Bar(
            x=[item["difference"] for item in sorted_rows],
            y=[item["amino_acid"] for item in sorted_rows],
            orientation="h",
            marker_color=colors,
            hovertext=hover_text,
            hoverinfo="text",
        )
    )
    figure.add_vline(x=0, line_width=2, line_dash="dash", line_color="#94a3b8")
    figure.update_layout(
        title="Residue Enrichment Difference",
        template="plotly_white",
        xaxis_title=f"Difference in percentage ({comparison['first_label']} - {comparison['second_label']})",
        yaxis_title="Amino Acid",
        margin=dict(l=60, r=20, t=60, b=50),
    )
    return figure


def create_top_residues_donut(composition: list[dict[str, object]], top_n: int = 5):
    """Create a donut chart for the top residues and group the rest as Other."""
    if not composition:
        raise ValueError("No amino acid composition data is available to plot.")

    sorted_rows = sorted(composition, key=lambda item: item["count"], reverse=True)
    top_rows = sorted_rows[:top_n]
    other_count = sum(int(item["count"]) for item in sorted_rows[top_n:])
    other_percentage = round(sum(float(item["percentage"]) for item in sorted_rows[top_n:]), 2)

    pie_rows = [
        {
            "label": item["amino_acid"],
            "count": item["count"],
            "percentage": item["percentage"],
            "color": classify_amino_acid(str(item["amino_acid"]))[1],
        }
        for item in top_rows
    ]
    if other_count:
        pie_rows.append(
            {
                "label": "Other",
                "count": other_count,
                "percentage": other_percentage,
                "color": "#cbd5e1",
            }
        )

    figure = go.Figure(
        data=[
            go.Pie(
                labels=[item["label"] for item in pie_rows],
                values=[item["count"] for item in pie_rows],
                hole=0.55,
                marker=dict(colors=[item["color"] for item in pie_rows]),
                textinfo="label+percent",
                hovertemplate="%{label}<br>Count=%{value}<br>Percent=%{percent}<extra></extra>",
            )
        ]
    )
    figure.update_layout(
        title="Top Residues Share",
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False,
    )
    return figure


def create_comparison_heatmap(comparison: dict[str, object]):
    """Create a compact heatmap comparing residue percentages across two sequences."""
    rows = comparison["composition_comparison"]
    if not rows:
        raise ValueError("No comparison data is available to plot.")

    sorted_rows = sorted(rows, key=lambda item: abs(item["difference"]), reverse=True)
    labels = [item["amino_acid"] for item in sorted_rows]
    z_values = [
        [item["first_percentage"] for item in sorted_rows],
        [item["second_percentage"] for item in sorted_rows],
    ]

    figure = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=labels,
            y=[comparison["first_label"], comparison["second_label"]],
            colorscale=[
                [0.0, "#f7fbff"],
                [0.2, "#d6f5ef"],
                [0.4, "#9dd9d2"],
                [0.6, "#53b3cb"],
                [0.8, "#2f6690"],
                [1.0, "#16425b"],
            ],
            hovertemplate="Sequence=%{y}<br>Amino Acid=%{x}<br>Percentage=%{z}%<extra></extra>",
            colorbar=dict(title="Percent"),
        )
    )
    figure.update_layout(
        title="Residue Composition Heatmap",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="Amino Acid",
        yaxis_title="Sequence",
    )
    return figure
