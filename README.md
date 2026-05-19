# ProteinLens

Beginner-friendly protein sequence analysis with Python, Gradio, and optional AI-assisted interpretation.

ProteinLens is designed as a learning-first bioinformatics mini project for a biochemistry student. The app keeps deterministic Python analysis separate from optional AI explanation so the computational logic stays understandable.

## Overview

ProteinLens currently supports:

- single-sequence analysis from FASTA or plain text
- amino acid count and percentage summaries
- amino acid composition visualization
- cautious deterministic interpretation
- optional AI-generated explanation from summary statistics
- two-sequence comparison
- text and JSON exports for both analysis modes

## Why This Project Exists

This project is meant to help a learner connect:

- biochemistry concepts such as amino acids and proteins
- beginner-friendly Python programming
- AI-assisted explanation without hiding the underlying calculations
- lightweight bioinformatics workflows that feel polished and shareable

## Current Status

The core implementation is in place:

- sequence parsing and validation
- Gradio app for analysis, AI explanation, comparison, and export
- notebook scaffold for step-by-step learning
- Quarto report scaffold for showcase use
- exportable outputs in `outputs/exports/`

## Local Setup

Recommended development workflow for Linux Mint + Miniconda:

```bash
conda create -n proteinlens python=3.12
conda activate proteinlens
pip install -r requirements.txt
```

If you want Quarto report rendering on the same machine, also install Quarto in your Conda setup:

```bash
conda install -y -c conda-forge quarto
```

For a more reproducible one-command Conda setup, you can use:

```bash
conda env create -f environment.yml
conda activate proteinlens
```

## Development Environment Setup

From the project root:

### Option A: Conda environment from `environment.yml`

This is the most reproducible setup for this project because it includes both Python and Quarto:

```bash
conda env create -f environment.yml
conda activate proteinlens
```

### Option B: Manual Conda + `requirements.txt`

If you prefer to build the environment step by step:

1. Create the Conda environment:

```bash
conda create -n proteinlens python=3.12
```

2. Activate it:

```bash
conda activate proteinlens
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Optional but recommended for the report:

```bash
conda install -y -c conda-forge quarto
```

5. Optional AI setup:

Create a local `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The `.env` file should stay local and should not be committed.

## Quick Start

If the environment is already set up:

```bash
conda activate proteinlens
python app.py
```

Then open the local Gradio URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

## Advanced Optional Feature

The current app also includes an `Advanced 3D Reference` tab.

This feature:

- is already implemented in the current version
- uses curated public example structures
- is meant as an enrichment layer, not a replacement for the sequence-first workflow

## Daily Development Commands

Run the Gradio app:

```bash
conda activate proteinlens
python app.py
```

Run tests:

```bash
conda activate proteinlens
python -m unittest discover -s tests
```

Open the notebook workflow:

```bash
conda activate proteinlens
jupyter notebook notebooks/02_protein_lens.ipynb
```

Render the Quarto report:

```bash
conda activate proteinlens
quarto render report.qmd
```

Or, if the Gradio app is already running, open the `Export` tab and click `Render Quarto Report`.
This uses the same local `report.qmd` file and still requires Quarto to be installed in the active environment.

Open the rendered report on Linux Mint:

```bash
xdg-open report.html
```

## Example Data

Example FASTA files are available at:

- `data/example_protein.fasta`
- `data/example_protein_variant.fasta`

## Suggested Screenshots

Add polished screenshots under `assets/screenshots/` and use them in the README and Quarto report.

Recommended screenshots:

- single-sequence analysis view
- AI explanation tab
- comparison view
- export tab
- Quarto report overview

Planned file paths:

- `assets/screenshots/single-sequence-analysis.png`
- `assets/screenshots/ai-explanation-tab.png`
- `assets/screenshots/comparison-view.png`
- `assets/screenshots/export-tab.png`
- `assets/screenshots/quarto-report-overview.png`

## Screenshot Placeholders

Once the image files exist, place them into the sections below.

Single-sequence analysis:

`assets/screenshots/single-sequence-analysis.png`

AI explanation:

`assets/screenshots/ai-explanation-tab.png`

Comparison workflow:

`assets/screenshots/comparison-view.png`

Export workflow:

`assets/screenshots/export-tab.png`

In-app Quarto rendering:

- open the `Export` tab
- click `Render Quarto Report`
- download the generated `report.html` file from the app if needed

## Optional AI Setup

To enable the AI explanation button, create a local `.env` file:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The app keeps deterministic sequence analysis separate from optional AI explanation.

## How To Use The App

Single-sequence workflow:

1. Paste a FASTA or plain protein sequence
2. Optionally enter a protein name
3. Click `Analyze Sequence`
4. Review summary, charts, fingerprint, interpretation, and export tabs
5. Optionally click `Generate AI Explanation`

Comparison workflow:

1. Paste two sequences or click `Load Two Sample Sequences`
2. Optionally enter names for both sequences
3. Click `Compare Sequences`
4. Review the comparison tables, delta chart, heatmap, and export tab

Advanced 3D workflow:

1. Open `Advanced 3D Reference`
2. Choose a curated example
3. Optionally choose a viewer style
4. Click `Load 3D Structure`

This 3D view uses curated public reference structures and is not inferred automatically from the pasted sequence.

## Learning And Reporting Files

- Notebook scaffold: `notebooks/02_protein_lens.ipynb`
- Quarto report scaffold: `report.qmd`
- Screenshot guide: `assets/screenshots/README.md`
- Conda environment file: `environment.yml`

## Project Structure

```text
.
├── app.py
├── data/
├── docs/
├── notebooks/
├── outputs/
├── src/
├── tests/
└── report.qmd
```

## Key Files

- `app.py`: Gradio interface
- `environment.yml`: reproducible Conda environment
- `src/protein_analysis.py`: deterministic sequence analysis
- `src/plots.py`: Plotly visualizations
- `src/sequence_visuals.py`: SVG sequence fingerprint helpers
- `src/structure_viewer.py`: curated 3D reference viewer
- `notebooks/02_protein_lens.ipynb`: learning notebook
- `report.qmd`: Quarto report source

## Next Showcase Step

The main remaining work is to capture polished screenshots, embed them into the README, and render the Quarto report as a final presentation artifact.
