# TODO

Remaining follow-up items for ProteinLens after the current feature-complete milestone.

## Priority 1

- Add richer export options beyond `.txt` and `.json`.
  This could include chart image export, standalone AI profile export, and Markdown-friendly summary export.

- Add a workflow diagram to the Quarto report.
  A Mermaid or SVG diagram would better match the visual presentation strategy and make the report feel more portfolio-ready.

## Priority 2

- Add the motivation / mission layer from the updated docs.
  Reframe parts of the app as a small drug-target profiling mission under a broader `BioBridge AI Lab` identity without making the UI feel gimmicky.

- Improve showcase presentation in the README and report.
  Capture polished screenshots and embed them once the visuals are considered stable.

## Priority 3

- Further generalize validation and export utilities into dedicated shared modules.
  The codebase is already more modular now, but validation and export logic can still be separated more cleanly for reuse.

- Evaluate whether a light Biopython integration would add learning value.
  This is not required for the current version, but it would align more closely with the shared technical setup docs.

## Notes

- The current app is already aligned on the main workflow:
  deterministic analysis first, optional AI explanation, visual exploration, export support, Quarto reporting, and optional advanced 3D reference.

- These TODO items are revisit points, not blockers for the current version.
