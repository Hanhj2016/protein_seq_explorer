# Visual Presentation and Interaction Strategy

## Purpose

This document adds a visual and interactive presentation layer to the Biochemistry + Python + AI learning plan.

The goal is not only to make the projects technically useful, but also to make them feel exciting, modern, and worth showing to others.

For a student who may not be highly motivated by programming itself, visual presentation can be an important source of interest and pride.

---

# Core Idea

The projects should not look like plain scripts or basic notebooks only.

They should feel like small, polished scientific AI tools:

```text
Biochemistry problem
→ Python analysis
→ interactive visualization
→ AI explanation
→ verification checklist
→ polished Quarto report
```

---

# Recommended Visual Layers

## Level 1: Polished 2D Scientific Charts

Required for all projects.

Examples:

- dose-response curve
- amino acid composition bar chart
- fold-change chart
- top gene chart
- summary statistics table

Recommended tools:

```text
plotly
matplotlib
pandas
```

Plotly is strongly recommended for the Gradio app because it gives hover, zoom, and interactive exploration.

## Level 2: Interactive Plots

Recommended for:

- BioDose AI
- ProteinLens
- GeneShift

Examples:

```text
Hover over a data point
Zoom into a chart
Toggle traces on and off
View details in tooltips
```

## Level 3: SVG / Mermaid Diagrams

Recommended for Quarto reports and portfolio pages.

Use cases:

- analysis workflow diagram
- data pipeline diagram
- AI verification workflow
- protein analysis workflow
- literature reading workflow

Recommended tools:

```text
Mermaid in Quarto
diagrams.net exported as SVG
Excalidraw exported as SVG
simple hand-written SVG for small diagrams
```

## Level 4: 3D Molecular View

Optional but highly motivating for ProteinLens.

Recommended as a Phase 2 or Phase 3 enhancement, not a first-week requirement.

Possible approaches:

1. Link to a public 3D structure page such as RCSB PDB.
2. Embed or link a Mol* / Molstar viewer.
3. Use NGL-style molecular visualization later.
4. Avoid building a custom 3D viewer from scratch at the beginning.

Important note:

Gradio `Model3D` is useful for general 3D files such as `.obj`, `.glb`, or `.stl`, but protein structures are commonly stored as PDB or mmCIF files. For real molecular visualization, Mol* or NGL-style viewers are more appropriate.

## Level 5: Storytelling and Portfolio Presentation

Required for final presentation.

Use:

- Quarto report
- screenshots
- project cards
- result cards
- demo links
- README
- reflection section

---

# Visual Feature Priority

## Must-Have Features

Every serious project should include:

```text
Interactive Plotly charts
Gradio tabs
Result cards
Example data buttons
Quarto callout boxes
Screenshots in README
Clear limitation warning
```

## Strongly Recommended Features

```text
SVG or Mermaid workflow diagrams
AI figure caption generator
Verification checklist
Downloadable summaries
Data quality warnings
Synthetic vs real data badge
```

## Nice-to-Have Features

```text
3D protein structure viewer
Beginner / Advanced explanation toggle
Clickable pathway-style diagram
Quarto portfolio website
Chatbot panel for literature Q&A
```

## Later-Only Features

```text
Full molecular docking visualization
Real RNA-seq pipeline visualization
Complex 3D simulation
Custom JavaScript visualization components
```

---

# Project-Specific Visual Suggestions

## BioDose AI

Best visual features:

```text
Interactive dose-response curve
Result cards
Dataset preview
Data quality warnings
AI figure caption generator
Downloadable summary
```

Recommended result cards:

```text
Drugs detected
Concentrations tested
Total samples
Replicates per condition
Strongest observed response
Missing values
```

Recommended chart:

```text
x-axis: concentration_uM
y-axis: mean cell viability percent
error bars: SEM or SD
trace: drug_name
hover: concentration, mean, SD, SEM, n
```

## ProteinLens

Best visual features:

```text
Amino acid composition chart
Top amino acids card
Sequence length card
Protein workflow diagram
Optional 3D structure link or viewer
```

Recommended result cards:

```text
Sequence length
Unique amino acids detected
Most frequent amino acid
Input type: FASTA or plain sequence
Invalid characters detected
```

Optional 3D enhancement:

```text
Protein name / PDB ID input
RCSB PDB link
Mol* viewer link or embed
```

## TargetReader AI

Best visual features:

```text
Paper summary cards
Key term chips
Verification checklist
Chatbot-style follow-up panel
Original vs AI summary tabs
```

Recommended cards:

```text
Research question
Drug target
Biological system
Methods
Key findings
Limitations
Terms to learn
Manual verification
```

## GeneShift

Best visual features:

```text
Fold-change bar chart
Top up-regulated genes card
Top down-regulated genes card
Heatmap-style chart
Normalization warning
```

Recommended result cards:

```text
Number of genes
Top up-regulated gene
Top down-regulated gene
Stable housekeeping genes
Synthetic or real dataset badge
```

## BioBridge AI

Best visual features:

```text
Portfolio landing page
Project cards
Unified Gradio tabs
Screenshots
Demo links
Quarto website or report
```

Recommended project cards:

```text
BioDose AI — Analyze drug response data
ProteinLens — Explore protein sequences
TargetReader AI — Understand drug target papers
GeneShift — Explore gene expression changes
```

---

# Gradio Interaction Design

## Recommended App Structure

Use `gr.Blocks`.

Suggested structure:

```text
Hero section
Project tabs
Input panel
Analyze button
Result cards
Charts
AI explanation panel
Verification checklist
Export/download area
Footer
```

## Interaction Pattern

Each tab should have two main actions:

```text
Analyze with Python
Generate AI Explanation
```

This teaches an important distinction:

- Python performs the actual calculation.
- The LLM helps explain and summarize.
- Scientific claims must still be verified.

## Example Interaction Flow

```text
1. User selects example dataset
2. User clicks Analyze with Python
3. App shows preview, summary cards, and chart
4. User clicks Generate AI Explanation
5. App calls OpenAI API
6. App shows explanation and verification checklist
7. User downloads summary
```

---

# Quarto Presentation Design

## Recommended Features

Use:

```text
HTML theme
table of contents
code folding
callout boxes
figure captions
tabs
screenshots
demo links
workflow diagrams
reflection section
```

## Suggested YAML

```yaml
---
title: "BioBridge AI"
subtitle: "Biochemistry + Python + AI Portfolio"
format:
  html:
    theme: cosmo
    toc: true
    code-fold: true
    code-tools: true
    number-sections: true
---
```

## Recommended Report Sections

```text
Overview
Biological Motivation
Project Demo
Dataset
Methods
Results
Interactive Visualization
AI-assisted Explanation
Verification Checklist
Limitations
What I Learned
Future Work
```

## Recommended Callouts

```markdown
::: {.callout-tip}
## Key Observation
The interactive chart shows a dose-dependent pattern in the synthetic dataset.
:::

::: {.callout-warning}
## Verification Required
This is a learning project. AI-generated explanations must be verified with original data, biological knowledge, and reliable sources.
:::
```

---

# Visual Assets

## Optional Logo / Banner

The project may include:

```text
assets/logo.png
assets/banner.png
assets/screenshots/
```

Logo ideas:

```text
DNA helix
protein ribbon
lab flask
AI circuit + molecule
```

These can be generated with a design tool or image generation tool, but the student should not spend too much time on branding before the core app works.

## Screenshots Required

At minimum:

```text
home screen
one analysis result
one chart
one AI explanation
one Quarto report page
```

---

# Download and Export Features

Recommended export options:

```text
Download summary as Markdown
Download summary table as CSV
Download figure as PNG
Download AI explanation as TXT or MD
```

Full PDF report generation can come later.

---

# Data Quality Visual Warnings

Add visible warnings for:

```text
missing required columns
missing values
non-numeric concentration
only one replicate
no control group
too few genes
invalid amino acid characters
abstract too short
API key missing
```

This makes the app feel more professional and teaches scientific data quality thinking.

---

# Suggested Two-Week Visual Upgrade Plan

## Week 1: Make It Work

- build core analysis
- create basic Gradio app
- generate one chart
- add sample data

## Week 2: Make It Look Good

- add theme
- add tabs
- add result cards
- add Plotly hover chart
- add AI explanation panel
- add Quarto report
- add screenshots to README

This sequence is important:

> First make it work. Then make it beautiful.

---

# Success Criteria

Minimum success:

```text
The app has a clean UI, one interactive chart, and a Quarto report.
```

Good success:

```text
The app has tabs, result cards, example data, AI explanation, and screenshots.
```

Excellent success:

```text
The app is deployed, has a polished Quarto portfolio page, and includes optional 3D protein structure links or viewer.
```
