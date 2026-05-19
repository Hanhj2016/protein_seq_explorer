"""Helpers for an optional curated 3D structure viewer."""

from html import escape
from uuid import uuid4

CURATED_STRUCTURES: dict[str, dict[str, str]] = {
    "EGFR kinase domain (PDB: 1M17)": {
        "label": "EGFR kinase domain",
        "source": "Experimental PDB structure",
        "pdb_id": "1M17",
        "notes": "A classic kinase-domain example used in cancer biology and drug-target discussions.",
    },
    "HER2 kinase domain (PDB: 3PP0)": {
        "label": "HER2 kinase domain",
        "source": "Experimental PDB structure",
        "pdb_id": "3PP0",
        "notes": "Useful for discussing receptor tyrosine kinases and targeted therapy context.",
    },
    "ACE2 receptor fragment (PDB: 6M17)": {
        "label": "ACE2 receptor fragment",
        "source": "Experimental PDB structure",
        "pdb_id": "6M17",
        "notes": "A well-known receptor structure with strong biological relevance.",
    },
    "TP53 DNA-binding domain (PDB: 1TUP)": {
        "label": "TP53 DNA-binding domain",
        "source": "Experimental PDB structure",
        "pdb_id": "1TUP",
        "notes": "Helpful for discussing tumor suppressor biology and domain-level structure.",
    },
}

STRUCTURE_STYLE_PRESETS: dict[str, dict[str, object]] = {
    "Cartoon (Rainbow)": {
        "cartoon": {"color": "spectrum"},
        "hetflag_style": {"stick": {"colorscheme": "greenCarbon", "radius": 0.18}},
    },
    "Cartoon (Teal)": {
        "cartoon": {"color": "#2bb3a8"},
        "hetflag_style": {"stick": {"colorscheme": "greenCarbon", "radius": 0.16}},
    },
    "Stick View": {
        "stick": {"colorscheme": "cyanCarbon", "radius": 0.18},
        "hetflag_style": {"stick": {"colorscheme": "greenCarbon", "radius": 0.16}},
    },
    "Surface View": {
        "cartoon": {"color": "#94a3b8", "opacity": 0.55},
        "surface": {"opacity": 0.82, "color": "white"},
        "hetflag_style": {"stick": {"colorscheme": "greenCarbon", "radius": 0.16}},
    },
}


def get_structure_choices() -> list[str]:
    """Return user-facing dropdown labels for the curated 3D examples."""
    return list(CURATED_STRUCTURES.keys())


def get_structure_style_choices() -> list[str]:
    """Return viewer style preset names."""
    return list(STRUCTURE_STYLE_PRESETS.keys())


def build_structure_info_markdown(choice: str) -> str:
    """Return a short provenance and interpretation note for the selected structure."""
    item = CURATED_STRUCTURES[choice]
    return (
        f"### {item['label']}\n\n"
        f"- Source: **{item['source']}**\n"
        f"- Structure ID: **{item['pdb_id']}**\n"
        f"- Notes: {item['notes']}\n\n"
        "This 3D view is a curated external reference structure. It is **not inferred automatically** "
        "from the pasted sequence in ProteinLens."
    )


def build_structure_context_html(choice: str) -> str:
    """Return a short card explaining why the selected structure matters."""
    item = CURATED_STRUCTURES[choice]
    return f"""
    <div style="
        padding:14px 16px;
        border-radius:18px;
        background:linear-gradient(180deg, #f8fffd 0%, #eef8ff 100%);
        border:1px solid #d7ebe7;
        margin:8px 0 12px 0;
    ">
      <div style="font-size:0.82rem; letter-spacing:0.06em; text-transform:uppercase; color:#0f766e; font-weight:700; margin-bottom:6px;">
        Why This Structure Matters
      </div>
      <div style="font-size:1rem; color:#243b53; line-height:1.5;">
        {item['notes']}
      </div>
    </div>
    """

def build_structure_viewer_html(choice: str, style_choice: str = "Cartoon (Rainbow)") -> str:
    """Return an embeddable 3Dmol.js HTML viewer for a curated PDB structure."""
    item = CURATED_STRUCTURES[choice]
    pdb_id = escape(item["pdb_id"])
    title = escape(item["label"])
    viewer_id = f"viewer_{uuid4().hex}"
    preset = STRUCTURE_STYLE_PRESETS[style_choice]
    preset_json = escape(str(preset).replace("'", '"'), quote=True)
    srcdoc = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      html, body {{
        margin: 0;
        padding: 0;
        background: linear-gradient(180deg, #f7fbff 0%, #eef8ff 100%);
        font-family: Arial, sans-serif;
      }}
      .shell {{
        border: 1px solid #d7ebe7;
        border-radius: 20px;
        overflow: hidden;
        background: linear-gradient(180deg, #f7fbff 0%, #eef8ff 100%);
      }}
      .head {{
        padding: 12px 16px;
        border-bottom: 1px solid #d7ebe7;
        display: flex;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
      }}
      .eyebrow {{
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #0f766e;
        font-weight: 700;
      }}
      .title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: #102a43;
      }}
      .meta {{
        font-size: 0.92rem;
        color: #486581;
      }}
      #{viewer_id} {{
        width: 100%;
        height: 460px;
        background: linear-gradient(180deg, #fdfefe 0%, #eef5fb 100%);
      }}
      .foot {{
        padding: 10px 16px;
        color: #486581;
        font-size: 0.9rem;
        border-top: 1px solid #d7ebe7;
      }}
      .fallback {{
        padding: 24px;
        color: #7b8794;
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <div class="head">
        <div>
          <div class="eyebrow">Curated 3D Reference</div>
          <div class="title">{title}</div>
        </div>
        <div class="meta">PDB ID: <strong>{pdb_id}</strong></div>
      </div>
      <div id="{viewer_id}"></div>
      <div class="foot">
        Rotate and zoom the structure directly in the viewer. This is external public structure data used as a teaching aid.
      </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"></script>
    <script>
      (function() {{
        const viewerElement = document.getElementById("{viewer_id}");
        function showFallback(message) {{
          viewerElement.innerHTML = '<div class="fallback">' + message + '</div>';
        }}
        function initViewer() {{
          if (!viewerElement || typeof $3Dmol === "undefined") {{
            showFallback("3Dmol.js failed to load. Check browser connectivity and reload the page.");
            return;
          }}
          const viewer = $3Dmol.createViewer(viewerElement, {{ backgroundColor: "white" }});
          $3Dmol.download("pdb:{pdb_id}", viewer, {{}}, function() {{
            const preset = JSON.parse('{preset_json}');
            const hetflagStyle = preset.hetflag_style || null;
            delete preset.hetflag_style;
            viewer.setStyle({{}}, preset);
            if (hetflagStyle) {{
              viewer.addStyle({{ hetflag: true }}, hetflagStyle);
            }}
            viewer.zoomTo();
            viewer.render();
          }}, function() {{
            showFallback("The structure file could not be downloaded right now. Please try again later.");
          }});
        }}
        if (document.readyState === "loading") {{
          document.addEventListener("DOMContentLoaded", initViewer);
        }} else {{
          initViewer();
        }}
      }})();
    </script>
  </body>
</html>
    """.strip()

    escaped_srcdoc = escape(srcdoc, quote=True)
    return (
        '<iframe '
        'style="width:100%; height:560px; border:0; border-radius:20px; background:transparent;" '
        f'srcdoc="{escaped_srcdoc}"></iframe>'
    )


def suggest_structure_choice(protein_name: str | None) -> str | None:
    """Return a curated structure suggestion based on a protein name hint."""
    if not protein_name:
        return None

    normalized = protein_name.strip().lower()
    if not normalized:
        return None

    aliases = {
        "egfr": "EGFR kinase domain (PDB: 1M17)",
        "her2": "HER2 kinase domain (PDB: 3PP0)",
        "erbb2": "HER2 kinase domain (PDB: 3PP0)",
        "ace2": "ACE2 receptor fragment (PDB: 6M17)",
        "tp53": "TP53 DNA-binding domain (PDB: 1TUP)",
        "p53": "TP53 DNA-binding domain (PDB: 1TUP)",
    }
    return aliases.get(normalized)
