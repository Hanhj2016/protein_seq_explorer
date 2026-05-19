"""Reusable UI HTML fragments for the Gradio application."""

from pathlib import Path


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


def build_report_open_link(report_path: Path) -> str:
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
