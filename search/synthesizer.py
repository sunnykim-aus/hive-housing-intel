"""
Uses Claude to synthesize a research-quality answer from retrieved chunks.
The prompt is tuned for Australian housing policy analysis.
"""
import os
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from config import CLAUDE_MODEL

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

_client = None


def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


SYSTEM_PROMPT = """You are a senior Australian housing policy analyst with deep expertise in:
- Community housing, public housing, and affordable housing sectors
- Federal and state government housing programs (2005–present)
- AHURI research methodology and findings
- Housing finance, planning systems, and supply constraints
- Social policy outcomes and evidence-based evaluation

Your role is to synthesise research evidence from AHURI reports and government publications
to answer questions about Australian housing policy, funding impacts, and sector trends.

When answering:
1. Lead with the direct answer or key finding
2. Cite specific reports by title and year (e.g., "AHURI Final Report 2018 found...")
3. Distinguish between what the evidence shows clearly vs. what is uncertain
4. Note time lags — housing policy outcomes often take 3–7 years to appear in research
5. Where relevant, connect funding inputs to measurable outcomes (dwellings, households, costs)
6. Flag if evidence is thin, contradictory, or if important research gaps exist
7. Use precise language: avoid vague terms like "significant" without quantification

Format responses with clear headings. Use markdown. Be analytical, not just descriptive."""


def _format_context(chunks: list[dict]) -> str:
    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(
            f"[SOURCE {i}] {c['title']} ({c['year']}) — {c['source_agency']} {c['report_type']}\n"
            f"URL: {c['source_url']}\n"
            f"{c['text']}\n"
        )
    return "\n---\n".join(lines)


def synthesize(query: str, chunks: list[dict]) -> str:
    """
    Given a user query and retrieved chunks, return a synthesised analysis from Claude.
    """
    if not chunks:
        return "No relevant research found in the indexed reports. Try running the ingestion pipeline first, or broaden your search terms."

    context = _format_context(chunks)
    user_message = f"""Using the research excerpts below, answer this question:

**{query}**

Research excerpts ({len(chunks)} sources):

{context}

Provide a comprehensive, evidence-based analysis. Cite specific reports where you draw evidence from."""

    client = get_client()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def synthesize_policy_impact(policy_name: str, funding_amount: str, year: int, chunks: list[dict]) -> str:
    """
    Specialised prompt for policy impact analysis: investment → outcomes.
    """
    context = _format_context(chunks)
    user_message = f"""Analyse the impact of this Australian housing policy:

**Policy:** {policy_name}
**Investment:** {funding_amount}
**Announced/Implemented:** {year}

Using the research evidence below, provide an impact assessment covering:
1. **What was intended** — stated goals and targets at announcement
2. **What was delivered** — actual dwellings, households assisted, completions
3. **Unintended consequences** — crowding out, displacement, market effects
4. **Evidence quality** — how robust is the research on this program?
5. **Verdict** — did the investment achieve value for money vs. stated goals?

Research excerpts ({len(chunks)} sources):

{context}"""

    client = get_client()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text
