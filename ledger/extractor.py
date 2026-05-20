"""
Uses Claude to extract structured outcome data from indexed research chunks.
For each program, retrieves relevant research and asks Claude to:
1. Find evidence of actual outcomes/results
2. Identify what worked and what didn't
3. Surface any data not already in the ledger
"""
import os
import json
import anthropic
from config import CLAUDE_MODEL
from ledger.db import get_program, save_extracted_outcomes, save_evidence_links

_client = None


def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


EXTRACTION_PROMPT = """You are analysing Australian housing policy research to extract structured outcome data.

Program: {program_name} ({short_name})
Announced: {announced_year} | Funding: ${funding_committed_bn}B | Type: {program_type}
Description: {description}

Known targets:
{targets_text}

Known outcomes already in our database:
{outcomes_text}

Research evidence retrieved ({n_chunks} sources):
{context}

Your task:
1. Extract any ADDITIONAL outcome data not already captured above (metrics, values, years)
2. Identify key findings about what worked, what failed, and why
3. Note any unintended consequences
4. Assess the evidence quality (High/Medium/Low confidence)

Respond in this exact JSON format:
{{
  "new_outcomes": [
    {{
      "metric": "metric name",
      "actual_value": 1234,
      "actual_unit": "dwellings/$/% etc",
      "measurement_year": 2015,
      "confidence": "High/Medium/Low",
      "source_report": "report name and year",
      "notes": "context"
    }}
  ],
  "key_findings": "2-3 paragraph synthesis of what the research says about this program's effectiveness",
  "what_worked": ["bullet point 1", "bullet point 2"],
  "what_failed": ["bullet point 1", "bullet point 2"],
  "unintended_consequences": ["bullet point 1"],
  "evidence_gaps": "What research is missing that would help assess this program better"
}}"""


def extract_outcomes_for_program(program_id, search_fn):
    """
    Main extraction function. Retrieves research and uses Claude to extract outcomes.
    search_fn: the search.retriever.search function
    """
    data = get_program(program_id)
    program = data["program"]
    if not program:
        return None

    # Build search queries for this program
    queries = [
        f"{program['name']} outcomes results impact",
        f"{program['short_name']} housing policy evaluation",
        f"{program['name']} dwellings delivered completed",
    ]

    # Retrieve relevant chunks
    all_chunks = []
    seen_ids = set()
    for query in queries:
        chunks = search_fn(query, n_results=8)
        for c in chunks:
            cid = c.get("source_url", "") + c.get("text", "")[:50]
            if cid not in seen_ids:
                seen_ids.add(cid)
                all_chunks.append(c)

    all_chunks = all_chunks[:20]

    # Save evidence links
    save_evidence_links(program_id, all_chunks)

    if not all_chunks:
        return {"error": "No research found for this program"}

    # Format context
    context_parts = []
    for i, c in enumerate(all_chunks, 1):
        context_parts.append(
            f"[{i}] {c['title']} ({c['year']}) — {c['source_agency']}\n{c['text']}"
        )
    context = "\n---\n".join(context_parts)

    # Format known data
    targets_text = "\n".join([
        f"  - {t['metric']}: {t['target_value']} {t['target_unit']} by {t['target_year']}"
        for t in data["targets"]
    ]) or "  None recorded"

    outcomes_text = "\n".join([
        f"  - {o['metric']}: {o['actual_value']} {o['actual_unit']} ({o['measurement_year']}) [{o['confidence']} confidence]"
        for o in data["outcomes"]
    ]) or "  None recorded yet"

    prompt = EXTRACTION_PROMPT.format(
        program_name=program["name"],
        short_name=program["short_name"] or "",
        announced_year=program["announced_year"],
        funding_committed_bn=program["funding_committed_bn"],
        program_type=program["program_type"],
        description=program["description"] or "",
        targets_text=targets_text,
        outcomes_text=outcomes_text,
        n_chunks=len(all_chunks),
        context=context[:12000],
    )

    client = get_client()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()

    # Parse JSON response
    try:
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw)
    except Exception:
        result = {"key_findings": raw, "new_outcomes": []}

    # Save to database
    new_outcomes = result.get("new_outcomes", [])
    findings_text = f"""## Key Findings
{result.get('key_findings', '')}

## What Worked
{chr(10).join('- ' + w for w in result.get('what_worked', []))}

## What Failed
{chr(10).join('- ' + f for f in result.get('what_failed', []))}

## Unintended Consequences
{chr(10).join('- ' + c for c in result.get('unintended_consequences', []))}

## Evidence Gaps
{result.get('evidence_gaps', '')}"""

    save_extracted_outcomes(program_id, new_outcomes, findings_text)
    return result
