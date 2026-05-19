# Phased Development Plan for Linux Mint + Python 3.12 + Miniconda

## Purpose

This document converts the project goals in the existing docs into a practical build plan for a local development setup based on:

- Linux Mint
- Python 3.12
- Miniconda for environment management

The goal is to keep the workflow beginner-friendly while still building a polished `ProteinLens` project with clear phases.

---

# Environment Assumptions

## Local Platform

- Operating system: Linux Mint
- Python version: 3.12
- Environment manager: Miniconda
- Main coding workflow: AI-assisted Python development

## Recommended Approach

Use one dedicated Conda environment for this project.

Example:

```bash
conda create -n proteinlens python=3.12
conda activate proteinlens
pip install pandas numpy matplotlib plotly scipy statsmodels jupyter gradio biopython openai python-dotenv
```

If you prefer, a future version can split dependencies into:

- core analysis dependencies
- app/demo dependencies
- optional AI/reporting dependencies

For the first version, one environment is simpler and better.

---

# Development Philosophy

This project should be built in layers:

1. Make the biology-facing Python logic work first.
2. Then make the outputs clear and trustworthy.
3. Then wrap the analysis in a polished Gradio app.
4. Then add optional AI explanation carefully.
5. Then create a polished report and portfolio materials.

This avoids building UI around unstable analysis code.

---

# Phase 0: Project Setup

## Goal

Create a clean local project structure and confirm the environment works on Linux Mint.

## Tasks

- Create and activate the Conda environment.
- Install the required Python packages.
- Add a `requirements.txt`.
- Add a `.gitignore` that includes:
  - `.env`
  - `__pycache__/`
  - `*.pyc`
  - `.venv/`
  - `outputs/`
  - `*.db`
- Create the starter folders:
  - `data/`
  - `src/`
  - `notebooks/`
  - `assets/`
  - `outputs/`
- Add a starter example FASTA file in `data/`.

## Deliverables

- Reproducible local environment
- Basic project folder structure
- First example input file

## Exit Criteria

- `python --version` shows Python 3.12 inside the active Conda environment
- imports for `pandas`, `gradio`, `Bio`, and `openai` work

---

# Phase 1: Sequence Parsing and Validation

## Goal

Build the deterministic core logic for accepting and cleaning protein input.

## Tasks

- Create `src/protein_analysis.py`
- Implement:
  - `parse_fasta(text)`
  - `clean_protein_sequence(sequence)`
  - sequence validation against standard amino acid letters
- Support both:
  - FASTA input
  - plain protein sequence input
- Return helpful beginner-friendly error messages for invalid input

## Deliverables

- Reusable protein parsing module
- Cleaned sequence output
- Validation logic

## Exit Criteria

- example FASTA parses correctly
- plain sequence input parses correctly
- invalid characters are detected cleanly

---

# Phase 2: Core Protein Analysis

## Goal

Compute the basic sequence metrics required by the project docs.

## Tasks

- Add sequence length calculation
- Count amino acid frequencies
- Calculate amino acid percentages
- Identify top 5 most common amino acids
- Return the results in a simple structure the student can understand

## Recommended Output Structure

- cleaned sequence
- input type
- sequence length
- amino acid counts
- amino acid percentages
- top amino acids
- unique amino acids detected

## Deliverables

- stable analysis functions in `src/protein_analysis.py`

## Exit Criteria

- one example sequence can be fully analyzed end-to-end from raw input to summary values

---

# Phase 3: Visualization Layer

## Goal

Turn the analysis into clear, attractive plots.

## Tasks

- Create `src/plots.py`
- Build an amino acid composition bar chart
- Use readable labels and colors
- Save chart output if needed to `outputs/`
- Keep plotting code separate from sequence logic

## Deliverables

- plotting helper functions
- first composition chart

## Exit Criteria

- a chart can be generated directly from the analysis output without manual editing

---

# Phase 4: Notebook Learning Workflow

## Goal

Create a notebook that explains the logic step by step for learning and debugging.

## Tasks

- Create `notebooks/02_protein_lens.ipynb`
- Include:
  - project question
  - example FASTA input
  - parsing walkthrough
  - composition calculation
  - chart generation
  - interpretation notes
  - limitations

## Why This Phase Matters

The notebook becomes the learning bridge between raw code and the final app.

## Deliverables

- beginner-friendly exploration notebook

## Exit Criteria

- the notebook can reproduce the same outputs as the Python module

---

# Phase 5: First Gradio App

## Goal

Wrap the deterministic analysis in a simple but polished interactive interface.

## Tasks

- Create `app.py`
- Add interface sections or tabs for:
  - Paste Sequence
  - Sequence Summary
  - Amino Acid Composition
  - Export
- Add:
  - project title
  - subtitle
  - sample FASTA button
  - result cards
  - composition chart
  - validation messages

## UI Priority

The first Gradio version should feel clean and understandable, not overloaded.

## Deliverables

- local Gradio app running on Linux Mint

## Exit Criteria

- pasting sample FASTA produces summary metrics and chart in the browser

---

# Phase 6: Optional AI Explanation Layer

## Goal

Add cautious LLM-assisted explanation without mixing it into the raw calculations.

## Tasks

- Create `src/llm_helper.py`
- Load `OPENAI_API_KEY` and optional `OPENAI_MODEL` from `.env`
- Add a Gradio button such as `Generate AI Explanation`
- Send summarized sequence statistics, not raw sensitive data by default
- Use a cautious scientific prompt
- Return Markdown output with:
  - Plain-English Summary
  - Key Observations
  - Possible Biological Interpretation
  - Limitations
  - What to Verify Manually

## Linux Mint / Conda Notes

- Keep `.env` in the project root
- test API access only after deterministic analysis is already working
- avoid automatic API calls on every input change

## Deliverables

- optional AI explanation workflow

## Exit Criteria

- clicking the AI button produces a clearly separated explanation based on computed summary data

---

# Phase 7: Sequence Comparison

## Goal

Implement the second major use case from the project doc: comparing two proteins.

## Tasks

- accept a second sequence input
- compare lengths
- compare amino acid composition
- compare top amino acids
- produce short comparison notes

## Deliverables

- comparison logic
- comparison view in Gradio

## Exit Criteria

- two pasted sequences can be compared in one workflow

---

# Phase 8: Quarto Report

## Goal

Produce a polished scientific-style report that presents the work clearly.

## Tasks

- Create `report.qmd`
- Include:
  - Overview
  - Why Protein Sequence Analysis Matters
  - Input Sequence
  - Methods
  - Sequence Summary
  - Amino Acid Composition
  - Biological Interpretation
  - Drug Target Relevance
  - Verification Checklist
  - Limitations
  - Future Improvements
  - What I Learned
- Add screenshots from the Gradio app
- Use callouts, captions, and a table of contents

## Deliverables

- rendered Quarto report

## Exit Criteria

- report can be generated locally and is presentation-ready

---

# Phase 9: README and Portfolio Polish

## Goal

Make the repository easy to understand, run, and share.

## Tasks

- Create or refine `README.md`
- Include:
  - what ProteinLens does
  - example input
  - screenshots
  - how to run locally on Linux Mint with Conda
  - limitations
  - future improvements
- Add branding elements:
  - project subtitle
  - emoji or simple visual identity

## Deliverables

- portfolio-ready repository landing page

## Exit Criteria

- a new visitor can understand the project and run it locally with minimal confusion

---

# Recommended Build Order

If time is limited, use this order:

1. Phase 0: Project Setup
2. Phase 1: Sequence Parsing and Validation
3. Phase 2: Core Protein Analysis
4. Phase 3: Visualization Layer
5. Phase 5: First Gradio App
6. Phase 6: Optional AI Explanation Layer
7. Phase 8: Quarto Report
8. Phase 9: README and Portfolio Polish

This order gets a usable project working early while still preserving room for polish.

---

# Recommended Milestones

## Milestone A: Local Analysis Prototype

Complete Phases 0 to 3.

Result:

- local environment works
- sequence parsing works
- composition metrics work
- charts work

## Milestone B: Interactive Demo

Complete Phase 5.

Result:

- a user can paste a sequence into Gradio and inspect the results visually

## Milestone C: AI-assisted Version

Complete Phase 6.

Result:

- the app can produce a cautious AI explanation from analysis summaries

## Milestone D: Showcase Version

Complete Phases 8 and 9.

Result:

- polished report
- polished README
- stronger portfolio value

---

# Practical Notes for Your Setup

- Since you are on Linux Mint, the shell commands in the docs are already close to your environment.
- Since you are using Miniconda, prefer `conda activate proteinlens` instead of `python -m venv`.
- Since you already have Python 3.12, keep the code compatible with 3.12 and avoid unnecessary complexity.
- For the first pass, prioritize stability and clarity over advanced architecture.
- Do not start with deployment, Docker, FastAPI, or React.

---

# Suggested Next Implementation Step

The best next move is:

1. create the Conda environment
2. scaffold the project folders and starter files
3. implement `src/protein_analysis.py`
4. test the example FASTA locally before building the UI

That path gives the fastest reliable progress.
