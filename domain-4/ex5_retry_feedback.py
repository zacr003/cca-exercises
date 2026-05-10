"""
CCA-F Domain 4, Exercise 5 — Retry-with-Error-Feedback (Subdomain 4.3 / 4.6)
==============================================================================

WHAT THIS EXERCISES:
  When schema-valid extraction fails semantic validation, the correct retry
  strategy includes the specific errors IN the retry prompt.

  Also: retry has LIMITS. If the required information is absent from the source
  document, no amount of retrying will produce it. Know when to stop.

KEY RULES:
  - Include: original document + failed extraction + specific errors in retry prompt
  - Do NOT retry the original prompt blindly (model gets no new information)
  - Do NOT loosen the schema to accept nullable for fields with semantic errors
  - Retryable: information EXISTS in source but was extracted WRONG
  - Non-retryable: information does NOT exist in source at all (accept null/unclear)
  - detected_pattern field: tracks which patterns trigger false positives over time

STRUCTURE:
  Part A -- Blind retry (WRONG): same prompt, model has no new information
  Part B -- Retry-with-feedback (CORRECT): include errors in the retry prompt
  Part C -- Retry limits: when the data isn't in the source at all
  Part D -- detected_pattern for false positive tracking
"""

import sys
import json

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5-20251001"


# =====================================================================
# EXTRACTION TOOL
# =====================================================================

EXTRACTION_TOOL = {
    "name": "extract_report_data",
    "description": "Extract key metrics from a business report.",
    "input_schema": {
        "type": "object",
        "properties": {
            "revenue_q1": {"type": "number", "description": "Q1 revenue in USD"},
            "revenue_q2": {"type": "number", "description": "Q2 revenue in USD"},
            "total_h1":   {"type": "number", "description": "H1 total (should equal Q1 + Q2)"},
            "growth_pct": {"type": ["number", "null"], "description": "YoY growth percentage if stated"},
            "currency":   {"type": "string", "enum": ["USD", "EUR", "GBP", "other"]},
            "conflict_detected": {"type": "boolean", "description": "True if numbers appear inconsistent"},
            "detected_pattern": {
                "type": ["string", "null"],
                "description": (
                    "If extraction was difficult, describe what made it hard "
                    "(e.g., 'ambiguous currency', 'totals stated without breakdown'). "
                    "Used for systematic false-positive tracking. Null if extraction was straightforward."
                )
            }
        },
        "required": ["revenue_q1", "revenue_q2", "total_h1", "currency", "conflict_detected"]
    }
}


# =====================================================================
# SAMPLE DOCUMENT — contains a clear total mismatch
# =====================================================================
# Q1 + Q2 = 1,200,000 + 850,000 = 2,050,000
# But the document states H1 total = 2,100,000
# This is a semantic error -- the model should flag conflict_detected = true

SAMPLE_REPORT = """
BUSINESS PERFORMANCE REPORT — H1 2026

Q1 Revenue: $1,200,000
Q2 Revenue: $850,000
H1 Total Revenue: $2,100,000

Year-over-Year Growth: 12.5%
All figures in USD.
"""


# =====================================================================
# SEMANTIC VALIDATOR
# =====================================================================

def validate(data: dict) -> list:
    """Returns a list of specific validation errors."""
    errors = []

    q1 = data.get("revenue_q1", 0)
    q2 = data.get("revenue_q2", 0)
    total = data.get("total_h1", 0)
    expected = q1 + q2

    if abs(total - expected) > 1:  # more than $1 tolerance
        errors.append(
            f"total_h1 mismatch: Q1({q1}) + Q2({q2}) = {expected}, "
            f"but total_h1 is {total} (difference: {abs(total - expected):.0f})"
        )

    if total > 0 and not data.get("conflict_detected"):
        if abs(total - expected) > 1:
            errors.append("conflict_detected should be True (totals don't add up) but is False")

    return errors


# =====================================================================
# EXTRACTION FUNCTION
# =====================================================================

def extract(messages: list) -> dict:
    """Calls the API with tool_use forced and returns the extracted data."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        tools=[EXTRACTION_TOOL],
        tool_choice={"type": "tool", "name": "extract_report_data"},
        messages=messages
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    return {}


# =====================================================================
# PART A: BLIND RETRY (WRONG)
# =====================================================================
# The model sees the same prompt again. It has no new information.
# It will likely make the same mistake or a different random mistake.
# This does not converge on the correct answer.

def part_a_blind_retry():
    print("\n--- PART A: Blind Retry (WRONG approach) ---")
    print("Re-sending the original prompt without any error information.")
    print("The model gets no new signal — same mistake is likely.\n")

    original_messages = [{"role": "user", "content": f"Extract from:\n\n{SAMPLE_REPORT}"}]

    for attempt in range(1, 3):
        data = extract(original_messages)
        errors = validate(data)
        print(f"  Attempt {attempt}:")
        print(f"    Q1={data.get('revenue_q1')} Q2={data.get('revenue_q2')} "
              f"H1={data.get('total_h1')} conflict={data.get('conflict_detected')}")
        if errors:
            print(f"    FAIL: {errors[0]}")
        else:
            print("    PASS: all validations passed")

    print("""
  KEY POINT: Blind retry gives the model no new information.
  The model cannot correct what it doesn't know is wrong.
  This pattern produces inconsistent results across retries.
""")


# =====================================================================
# PART B: RETRY-WITH-ERROR-FEEDBACK (CORRECT)
# =====================================================================
# Include THREE things in the retry prompt:
#   1. The original document (model needs context)
#   2. The failed extraction (model sees what it got wrong)
#   3. The specific validation errors (model knows WHAT is wrong)
#
# This is targeted correction — the model can fix the specific problem.

def part_b_retry_with_feedback():
    print("\n--- PART B: Retry-with-Error-Feedback (CORRECT approach) ---")
    print("Including the original document + failed extraction + specific errors.\n")

    # First attempt
    messages = [{"role": "user", "content": f"Extract from:\n\n{SAMPLE_REPORT}"}]
    data = extract(messages)
    errors = validate(data)

    print(f"  Attempt 1:")
    print(f"    Q1={data.get('revenue_q1')} Q2={data.get('revenue_q2')} "
          f"H1={data.get('total_h1')} conflict={data.get('conflict_detected')}")

    if not errors:
        print("    PASS on first attempt (model got it right)")
        return

    print(f"    FAIL: {errors}")

    # Retry with specific error feedback
    # Key: include original doc + failed extraction + SPECIFIC errors
    retry_content = (
        f"The previous extraction had validation errors. Please re-extract.\n\n"
        f"ORIGINAL DOCUMENT:\n{SAMPLE_REPORT}\n\n"
        f"PREVIOUS (INCORRECT) EXTRACTION:\n{json.dumps(data, indent=2)}\n\n"
        f"VALIDATION ERRORS TO FIX:\n" +
        "\n".join(f"  - {e}" for e in errors) +
        "\n\nPlease provide a corrected extraction that resolves these errors."
    )

    messages_with_feedback = [{"role": "user", "content": retry_content}]
    data2 = extract(messages_with_feedback)
    errors2 = validate(data2)

    print(f"\n  Attempt 2 (with error feedback):")
    print(f"    Q1={data2.get('revenue_q1')} Q2={data2.get('revenue_q2')} "
          f"H1={data2.get('total_h1')} conflict={data2.get('conflict_detected')}")
    if errors2:
        print(f"    FAIL: {errors2}")
    else:
        print("    PASS: error feedback guided the model to the correct answer")

    print("""
  KEY POINT: The retry includes:
    1. Original document (context)
    2. Failed extraction (model sees what it produced)
    3. Specific validation errors (model knows exactly what to fix)

  This is targeted correction. The model converges on the right answer
  because it has the information needed to fix the specific problem.
""")


# =====================================================================
# PART C: RETRY LIMITS
# =====================================================================
# Retries are effective when the information EXISTS in the source but was
# extracted incorrectly. They are NOT effective when the data doesn't exist.
#
# Example: if you ask for a phone number and there's no phone number in the
# document, no amount of retrying will produce a correct phone number.
# The model will either repeat null or start fabricating.

def part_c_retry_limits():
    print("\n--- PART C: Retry Limits ---")

    absent_doc = """
QUARTERLY SUMMARY
Revenue: $500,000
Note: This document does not contain phone number, address, or contact information.
"""

    tool_with_phone = {
        "name": "extract_contact",
        "description": "Extract contact information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "revenue": {"type": "number"},
                "phone":   {"type": ["string", "null"], "description": "Phone number if present"},
                "address": {"type": ["string", "null"], "description": "Address if present"}
            },
            "required": ["revenue"]
        }
    }

    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        tools=[tool_with_phone],
        tool_choice={"type": "tool", "name": "extract_contact"},
        messages=[{"role": "user", "content": f"Extract from:\n{absent_doc}"}]
    )

    for block in response.content:
        if block.type == "tool_use":
            data = block.input
            print(f"  Extraction result:")
            print(f"    revenue : {data.get('revenue')}")
            print(f"    phone   : {data.get('phone')} <- should be null (not in document)")
            print(f"    address : {data.get('address')} <- should be null (not in document)")

    print("""
  KEY POINT:
    Retryable error  = information EXISTS in source, was extracted incorrectly
    Non-retryable    = information does NOT exist in source
    Action for non-retryable: accept null/unclear values, route to human review if critical

  If you retry when data is absent:
    - Model repeats null (correct behavior, but retry was waste)
    - Model fabricates a value to "help" (WORSE — now you have wrong data marked as found)

  Nullable fields in your schema let the model honestly report "not present"
  instead of being forced to fabricate something to satisfy a required field.
""")


# =====================================================================
# PART D: detected_pattern FOR FALSE POSITIVE TRACKING
# =====================================================================
# Adding a detected_pattern field to structured findings enables you to
# analyze which situations repeatedly cause extraction difficulties.
# Over time, you can improve prompts for those specific patterns.

def part_d_detected_pattern():
    print("\n--- PART D: detected_pattern Field ---")
    print("""
The 'detected_pattern' field (shown in EXTRACTION_TOOL above):

  When the model encounters difficulty, it populates detected_pattern with a
  description of what made extraction hard:
    "totals stated without itemized breakdown"
    "ambiguous currency (both USD and EUR mentioned)"
    "Q4 figures missing, only YTD available"

  When developers review and dismiss a finding (or mark it as correct),
  you can analyze the detected_pattern values across all dismissed findings
  to identify systematic prompt weaknesses.

  Example analysis:
    "15 of our 23 false positives had detected_pattern = 'totals without breakdown'"
    Action: add a few-shot example specifically for that pattern

  Without detected_pattern:
    You know you have 23 false positives, but not why
    Prompt improvement is guesswork

  With detected_pattern:
    You know the specific failure modes
    Targeted prompt improvement based on real data

EXAM TIP: The exam tests that you know this field EXISTS and what it enables.
You don't need to implement the analysis pipeline -- just understand the concept.
""")


def main():
    print("=" * 60)
    print("EXERCISE 5 -- Retry-with-Error-Feedback (4.3 / 4.6)")
    print("=" * 60)

    part_a_blind_retry()
    part_b_retry_with_feedback()
    part_c_retry_limits()
    part_d_detected_pattern()

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 4.3 / 4.6")
    print("=" * 60)
    print("""
Retry-with-error-feedback:
  Include: original document + failed extraction + specific validation errors
  Do NOT: retry the original prompt blindly (no new information)
  Do NOT: loosen the schema (semantic errors will propagate silently)
  Do NOT: ask Claude to explain mistakes in natural language and parse the explanation

Retry limits:
  Retryable: information exists in source, was extracted incorrectly
  Non-retryable: information does not exist in source at all
  Action: accept null/unclear, route to human review if the field is critical

detected_pattern field:
  Purpose: tracks what made extraction difficult for systematic improvement
  Use: analyze dismissed/false-positive findings to find common patterns
  Benefit: targeted prompt improvement vs. guesswork

Self-review bias (4.6):
  Same session reviews = model retains generation reasoning = biased toward defending own decisions
  Fix: independent fresh instance (separate invocation, no generation context)
  Extended thinking in same session does NOT overcome this bias
""")


if __name__ == "__main__":
    main()
