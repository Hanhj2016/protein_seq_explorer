# ProteinLens: AI-assisted Protein Sequence Explorer

## Project Summary

**ProteinLens** is a beginner-friendly bioinformatics project that analyzes protein sequences using Python and AI-assisted interpretation.

It is a strong entry point into Bioinformatics because it connects directly to Biochemistry concepts such as proteins, amino acids, enzymes, and drug targets.

## Project Positioning

> A mini protein sequence explorer that helps students analyze FASTA sequences, visualize amino acid composition, and generate a basic biological profile.

---

# Why This Project Matters

Biochemistry students often study protein structure and function, but many do not use computational tools to analyze sequences.

This project introduces bioinformatics through simple but meaningful questions:

- How long is the protein?
- What is the amino acid composition?
- Which amino acids are most common?
- What might the protein do biologically?
- Could this protein be related to drug targeting?

---

# Key Use Cases

## Use Case 1: Analyze a Single Protein Sequence

### Input

A FASTA sequence or plain protein sequence.

### Output

- sequence length
- amino acid count
- amino acid percentage
- amino acid composition chart
- basic biological interpretation template

## Use Case 2: Compare Two Protein Sequences

### Input

Two FASTA sequences.

### Output

- length comparison
- composition comparison
- difference in top amino acids
- short comparison notes

## Use Case 3: AI-assisted Protein Profile

### Input

Protein name and sequence summary.

### Output

- function summary
- possible drug relevance
- key terms to learn
- verification checklist

---

# Test Data Source

## First Version: Synthetic or Example FASTA

Use a short generated or example protein sequence first.

Reason:

- easier to debug
- smaller
- safe
- no dependence on external download
- good for first demo

## Synthetic FASTA Generation Prompt

```text
Generate a short synthetic protein sequence in FASTA format for a beginner bioinformatics project.

The sequence should:
1. be 120 to 180 amino acids long
2. use standard one-letter amino acid codes
3. have a realistic-looking distribution of amino acids
4. include a FASTA header line
5. return only FASTA content
```

## Example FASTA

```text
>Example_Protein
MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAG
QEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHQYREQIKRVKDSDDVPMVLVGNKCDL
AARTVESRQAQDLARSYGIPYIETSAKTRQGVDDAFYTLVREIRQHKLRKLNPPDESGPG
CMSCKCVLS
```

## Later Version: Download Real Data

For a more realistic version, download FASTA sequences from public protein databases such as:

- UniProt
- NCBI Protein
- PDB sequence records

Suggested protein targets:

| Protein | Why It Is Interesting |
|---|---|
| EGFR | cancer drug target |
| HER2 / ERBB2 | breast cancer drug target |
| TP53 | tumor suppressor |
| ACE2 | receptor biology and drug relevance |
| BRCA1 | cancer biology |
| Insulin receptor | metabolism and signaling |
| Beta-lactamase | antibiotic resistance |

Recommended search terms:

```text
UniProt EGFR FASTA
UniProt HER2 FASTA
UniProt TP53 FASTA
```

For the first version, do not automate database downloads. Let the student manually download or paste FASTA to keep the workflow simple.

---

# Required Analysis

The project should:

1. Accept FASTA or plain sequence input.
2. Clean the sequence.
3. Remove FASTA header if present.
4. Validate amino acid characters.
5. Calculate sequence length.
6. Count amino acids.
7. Calculate amino acid percentages.
8. Identify top 5 most frequent amino acids.
9. Create a bar chart.
10. Generate a cautious biological explanation template.

---

# Suggested Python Functions

```python
def parse_fasta(text):
    pass

def clean_protein_sequence(sequence):
    pass

def calculate_amino_acid_composition(sequence):
    pass

def create_composition_chart(composition_df):
    pass

def generate_protein_profile(sequence_summary, protein_name=None):
    pass
```

---

# Gradio Demo Requirements

## App Name

**ProteinLens**

## Subtitle

**Explore protein sequences with Python and AI**

## Interface Layout

Recommended tabs:

1. Paste Sequence
2. Sequence Summary
3. Amino Acid Composition
4. AI Protein Profile
5. Export

## Fancy UI Elements

Include:

- hero title with emoji, such as `🧬 ProteinLens`
- sample FASTA button
- protein profile card
- sequence length card
- top amino acids card
- amino acid composition chart
- AI explanation box
- verification checklist

## Example Result Cards

```text
Sequence length: 167 amino acids
Most common amino acid: L
Unique amino acids detected: 20
Input type: FASTA
```

## Example AI Explanation Template

```text
This sequence can be analyzed by amino acid composition, but sequence composition alone is not enough to determine protein function. A real biological interpretation should verify the protein identity using a database such as UniProt and review known domains, structure, and literature.
```

---

# Quarto Report Requirements

## Report Title

**ProteinLens: Protein Sequence Analysis Report**

## Suggested Sections

1. Overview
2. Why Protein Sequence Analysis Matters
3. Input Sequence
4. Methods
5. Sequence Summary
6. Amino Acid Composition
7. Biological Interpretation
8. Drug Target Relevance
9. Verification Checklist
10. Limitations
11. Future Improvements
12. What I Learned

## Fancy Quarto Features

Use:

- callout boxes
- figure captions
- code folding
- table of contents
- screenshots from Gradio app

Example callout:

```markdown
::: {.callout-note}
## Important Note
Amino acid composition is only a basic sequence-level analysis. It does not prove protein function or drug relevance.
:::
```

---

# Recommended README Content

The README should include:

- what ProteinLens does
- example protein sequence
- screenshot of the app
- screenshot of the report
- how to run locally
- limitations
- future improvements

---

# Student Learning Goals

By completing this project, the student should learn:

- what FASTA format is
- how protein sequences are represented
- how to parse text data in Python
- how to count amino acids
- how to visualize composition
- how to use Biopython or basic Python for sequence analysis
- why biological interpretation requires database verification
- how AI can help explain, but not replace, biological reasoning

---

# Vibe Coding Prompt

```text
I am a third-year Biochemistry student learning bioinformatics with Python and AI assistance.

I want to build a project called ProteinLens. It analyzes protein sequences.

Please create beginner-friendly Python code with these files:
src/protein_analysis.py
src/plots.py
app.py

The Gradio app should:
1. accept pasted FASTA or plain protein sequence
2. clean the sequence
3. calculate sequence length
4. calculate amino acid counts and percentages
5. display a bar chart of amino acid composition
6. show top amino acids
7. generate a cautious biological interpretation template
8. include a sample FASTA example

Please keep the code modular and explain each function in simple language.
```

---

# Success Criteria

Minimum success:

- FASTA input works.
- Sequence length is correct.
- Amino acid counts are shown.
- Chart is generated.

Good success:

- Gradio app looks polished.
- Quarto report is generated.
- README has screenshots.
- Real UniProt FASTA can be analyzed manually.

Excellent success:

- App has a protein comparison feature.
- App is deployed.
- Student can explain why sequence composition alone is limited.

---

# Visual and Interaction Enhancements

## Required Visuals

ProteinLens should include:

- amino acid composition chart
- sequence length card
- top amino acids card
- protein analysis workflow diagram
- optional 3D structure link or viewer

## Recommended Result Cards

```text
Sequence length
Unique amino acids detected
Most frequent amino acid
Input type: FASTA or plain sequence
Invalid characters detected
```

## Optional 3D Protein Structure Enhancement

This should be a later enhancement, not a first-week requirement.

Possible approaches:

```text
Ask user for protein name or PDB ID
Generate RCSB PDB search link
Add Mol* / Molstar viewer link or embedded viewer later
```

Important:

```text
Amino acid composition alone does not prove protein function.
3D structure should be verified using reliable structure databases.
```

## SVG / Mermaid Diagram

Add a simple workflow diagram:

```text
FASTA input → sequence cleaning → amino acid composition → chart → AI protein profile → database verification
```

## Quarto Visual Additions

Include:

- amino acid composition figure
- protein workflow diagram
- optional screenshot or link to external 3D viewer
- callout note about the limits of sequence-only analysis
