"""Helpers for optional OpenAI-powered explanation generation."""

import os
from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SCIENTIFIC_CAUTION_SYSTEM_PROMPT = dedent(
    """
    You are an AI assistant helping a third-year undergraduate Biochemistry student.
    Explain scientific results clearly and cautiously.
    Do not overstate conclusions.
    If the data is synthetic or limited, say so clearly.
    Separate observations from interpretations.
    Always include a "What to verify manually" section.
    Do not give clinical or medical advice.
    """
).strip()


def get_openai_client() -> OpenAI:
    """Return an OpenAI client using the API key from the local environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to a local .env file before using AI features.")
    return OpenAI(api_key=api_key)


def format_protein_summary_prompt(summary: dict[str, object], protein_name: str | None = None) -> str:
    """Build a compact prompt from deterministic sequence summary data."""
    protein_label = protein_name.strip() if protein_name and protein_name.strip() else "Unknown protein"
    top_amino_acids = ", ".join(
        f"{item['amino_acid']} ({item['count']} counts, {item['percentage']}%)"
        for item in summary["top_amino_acids"]
    )

    return dedent(
        f"""
        Protein name: {protein_label}
        Input type: {summary['input_type']}
        Sequence length: {summary['sequence_length']}
        Unique amino acids detected: {summary['unique_amino_acids_detected']}
        Most common amino acid: {summary['most_common_amino_acid']}
        Top amino acids: {top_amino_acids}

        The sequence data came from a beginner-friendly protein sequence explorer.
        Provide a cautious explanation in Markdown with these headings:
        ## Plain-English Summary
        ## Key Observations
        ## Possible Biological Interpretation
        ## Limitations
        ## What to Verify Manually
        """
    ).strip()


def call_llm(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """Call the OpenAI Responses API and return text output."""
    client = get_openai_client()
    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.responses.create(
        model=selected_model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    output_text = getattr(response, "output_text", "")
    if output_text:
        return output_text

    raise RuntimeError(
        "The AI request completed but returned no text output. "
        "Please try again or check the selected model."
    )
