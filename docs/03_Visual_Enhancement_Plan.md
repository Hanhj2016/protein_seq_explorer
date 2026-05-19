# Visual Enhancement Plan for ProteinLens

## Purpose

This document proposes a practical visual upgrade path for `ProteinLens`.

The goal is to make the project feel more vivid, interactive, and presentation-ready without losing scientific clarity or overwhelming the learner.

The plan is split into:

1. a safe version using SVG, HTML, and Plotly only
2. an advanced version that adds interactive 3D structure viewing

---

# Design Direction

## Visual Mood

ProteinLens should feel:

- modern
- scientific
- clear
- slightly vivid
- interactive without being distracting

## Recommended Palette

- deep navy for headings and anchors
- teal for primary actions
- mint and sea-green for biological accents
- soft off-white backgrounds
- darker slate for text

This keeps the interface lively while still feeling like a scientific tool.

## General Visual Rule

The visuals should help answer biological questions, not just decorate the page.

Each visual should support one of these:

- what is in the sequence
- what is common or rare
- where patterns occur
- how two sequences differ
- what is known about a real structure

---

# Version 1: Safe Visual Upgrade

## Goal

Add vivid, interactive visuals using the current sequence-only workflow.

This version does not require external structure databases and fits the current project architecture well.

## Recommended Features

### 1. Summary Result Cards

Upgrade the current summary area into more expressive visual cards.

Suggested cards:

- sequence length
- most common amino acid
- unique amino acids detected
- input type

Possible enhancements:

- color-coded badges
- highlighted top residue
- small accent icons
- more intentional spacing and typography

### 2. Amino Acid Fingerprint Strip

Create an SVG strip showing the full protein sequence as colored blocks or letters.

Possible design:

- one colored block per residue
- residues grouped by chemical class
- hover tooltip for residue identity and position

Why it helps:

- makes the sequence feel tangible
- introduces residue position visually
- gives the learner a better mental model than plain text alone

### 3. Residue Class Legend

Group amino acids into broad biochemical categories:

- hydrophobic
- polar
- charged
- aromatic
- special cases

Then color the sequence strip and charts using those categories.

Why it helps:

- connects sequence analysis back to biochemistry
- makes charts more educational

### 4. Improved Composition Chart

Keep Plotly, but make the chart more expressive.

Suggested improvements:

- highlight top 3 residues with a stronger color
- use residue-class-based color groups
- add cleaner hover text
- optionally add a horizontal mode for easier reading

### 5. Composition Donut Chart

Add a second chart option:

- top amino acids as a donut chart
- remaining amino acids grouped as `Other`

Why it helps:

- gives a second visual angle
- looks more portfolio-ready

### 6. Comparison Delta Chart

For two-sequence comparison, add a chart showing percentage differences.

Recommended design:

- diverging bar chart
- positive values for Sequence 1 enrichment
- negative values for Sequence 2 enrichment

Why it helps:

- much more intuitive than a raw table
- clearly communicates what changed

### 7. Sequence Comparison Heatmap

Add a simple residue-by-sequence heatmap for top amino acid classes or composition percentages.

Why it helps:

- useful for fast visual comparison
- looks more advanced while staying understandable

## Recommended Implementation Areas

Files likely involved:

- `app.py`
- `src/plots.py`
- `src/protein_analysis.py`
- optional new file: `src/sequence_visuals.py`

## Suggested New Functions

```python
def build_sequence_fingerprint_svg(sequence: str) -> str:
    pass

def classify_amino_acid(residue: str) -> str:
    pass

def create_composition_donut(composition: list[dict]) -> object:
    pass

def create_comparison_delta_chart(comparison: dict) -> object:
    pass
```

## Benefits

- low risk
- no extra scientific ambiguity
- improves both app and report visuals
- still beginner-friendly

## Risks

- too many visuals could clutter the app if not grouped well
- custom SVG layout needs careful sizing for long sequences

---

# Version 2: Advanced 3D Structure Upgrade

## Goal

Add an optional 3D structure view for proteins with known or predicted structures.

This should be framed as an advanced extension, not part of the core sequence-only logic.

## Important Scientific Rule

The UI must clearly state where the structure came from:

- experimental PDB structure
- AlphaFold prediction
- or curated example structure

The learner must not be misled into thinking the 3D model was inferred from the pasted sequence alone.

## Recommended Use Cases

Best for:

- named proteins such as EGFR, HER2, TP53, ACE2
- demo proteins with known public structures
- later case-study versions of the app

## Recommended Features

### 1. Optional 3D Structure Tab

Add a separate tab such as:

- `3D Structure View`

This tab should appear only when structure data is available or when a known example is selected.

### 2. Browser-based 3D Viewer

Recommended tools:

- `py3Dmol`
- `3Dmol.js`
- Mol* for a more advanced future version

### 3. Basic Visual Controls

Useful controls:

- rotate
- zoom
- change cartoon/surface/stick style
- highlight selected residues

### 4. Annotation Panel

Beside the 3D viewer, show:

- structure source
- protein name
- chain information
- known domain or region notes
- interpretation caution

### 5. Residue Highlight Linking

Longer-term enhancement:

- click a residue in the sequence map
- highlight the corresponding residue in the 3D view

This is a strong educational feature, but it is more advanced and should come later.

## Recommended Implementation Areas

Potential files:

- `app.py`
- optional new file: `src/structure_viewer.py`
- optional new data folder: `data/structures/`

## Example Workflow

1. user enters a known protein name
2. app loads a predefined PDB or structure reference
3. app shows a 3D viewer tab
4. app explains that the structure is external reference data

## Benefits

- much more vivid and impressive
- strong portfolio value
- directly connects sequence to structural biology

## Risks

- can confuse users if structure provenance is not explicit
- needs extra dependencies or browser integration
- external data management is more complex

---

# Recommended Rollout Order

## Phase A: High-Value Safe Visuals

Implement first:

1. summary cards polish
2. amino acid fingerprint SVG
3. improved composition chart
4. comparison delta chart

This gives a major upgrade without changing the scientific scope.

## Phase B: Secondary Safe Visuals

Implement next:

1. donut chart
2. heatmap
3. residue class legend

## Phase C: Advanced 3D Prototype

Implement only after the 2D visuals feel complete:

1. add a separate 3D viewer tab
2. support one or two curated example proteins
3. clearly label structure provenance

---

# Recommendation

For the current project, the best next build step is:

## Recommended Next Move

Implement Version 1 first.

Why:

- it matches the current sequence-only project scope
- it improves clarity and attractiveness immediately
- it avoids scientific overreach
- it keeps the app beginner-friendly

After that, add Version 2 as an optional advanced extension for known proteins only.

---

# Concrete Next Implementation Block

If we start now, the best first visual enhancement block would be:

1. create `src/sequence_visuals.py`
2. add an SVG sequence fingerprint
3. add a comparison delta chart in `src/plots.py`
4. display both in `app.py`
5. update `report.qmd` to include the new visuals

This would create the most visible improvement with the least risk.
