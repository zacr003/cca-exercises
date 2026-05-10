"""
CCA-F Domain 5, Exercise 1 — Long Context and Attention Management (Subdomain 5.1)
===================================================================================

WHAT THIS EXERCISES:
  The "lost in the middle" effect: models reliably process content at the
  beginning and end of long inputs, but can miss content in the middle.
  The fix: place key findings at the BEGINNING of aggregated inputs.
  Also: trim verbose tool outputs to only relevant fields before they accumulate.

KEY RULES:
  - Key findings go at the BEGINNING of long aggregated inputs (not the middle)
  - Use explicit section headers to help the model navigate long inputs
  - Trim verbose tool outputs to relevant fields BEFORE they accumulate in context
  - When 80% of context is tool results -> you have a trimming problem
  - Do NOT pre-aggregate to 20K tokens via summarization (loses information)
  - Modifying upstream agents to return structured data (not verbose content) is the fix

STRUCTURE:
  Part A -- Lost-in-the-middle demonstration: key finding buried vs. at top
  Part B -- Tool output trimming: verbose vs. trimmed response
  Part C -- Upstream structured data: the architectural fix
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
# HELPER: Ask a question about a document
# =====================================================================

def ask_about_document(document: str, question: str) -> str:
    """Submits a document and a question, returns the model's answer."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"Read the following document carefully:\n\n{document}\n\n---\nQuestion: {question}"
        }]
    )
    return response.content[0].text.strip()


# =====================================================================
# PART A: LOST-IN-THE-MIDDLE DEMONSTRATION
# =====================================================================
# We'll create a long document where a critical finding appears in the
# middle, and then ask a question about it. Then we'll restructure the
# document with the critical finding at the top and test again.

PADDING = "Item {n}: Standard transaction processed normally. Amount: ${amount}. Status: completed.\n"

def build_padded_document(key_finding: str, position: str) -> str:
    """
    Builds a long document with a key finding placed at 'start', 'middle', or 'end'.
    The surrounding content is repetitive filler — realistic for aggregated tool outputs.
    """
    filler_before = "".join(
        PADDING.format(n=i, amount=i*10) for i in range(1, 20)
    )
    filler_after = "".join(
        PADDING.format(n=i, amount=i*10) for i in range(20, 40)
    )

    if position == "start":
        return f"=== KEY FINDING ===\n{key_finding}\n\n=== TRANSACTION LOG ===\n{filler_before}{filler_after}"
    elif position == "end":
        return f"=== TRANSACTION LOG ===\n{filler_before}{filler_after}\n=== KEY FINDING ===\n{key_finding}"
    else:  # middle
        return f"=== TRANSACTION LOG ===\n{filler_before}\n=== KEY FINDING ===\n{key_finding}\n{filler_after}"


KEY_FINDING = "CRITICAL ALERT: Account ACT-7734 shows unauthorized withdrawal of $47,500 on March 15. Immediate review required."
QUESTION = "Is there any critical alert or security concern mentioned in this document? If so, what is it?"


def part_a_lost_in_middle():
    print("\n--- PART A: Lost-in-the-Middle Effect ---")
    print("Placing a critical finding at start, middle, and end of a long document.")
    print("Watch whether the model reliably finds it at each position.\n")

    for position in ["start", "middle", "end"]:
        document = build_padded_document(KEY_FINDING, position)
        answer = ask_about_document(document, QUESTION)
        found = "unauthorized" in answer.lower() or "47,500" in answer or "ACT-7734" in answer
        marker = "FOUND" if found else "MISSED"
        print(f"  [{marker}] Key finding at {position.upper()}:")
        print(f"    Response: {answer[:120]}...")
        print()

    print("""
  EXAM TAKEAWAY:
    Models reliably process the BEGINNING and END of long inputs.
    Content in the MIDDLE may be missed (the "lost in the middle" effect).

    FIX: Place key findings summaries at the BEGINNING of aggregated inputs.
    Use explicit section headers (=== KEY FINDING ===) to signal important content.

  WRONG fixes:
    - Pre-aggregate all inputs to 20K tokens via summarization (loses information)
    - Rotate which subagent's output appears first to "average out" position effects
    - Stream results incrementally (position bias still applies to each chunk)
""")


# =====================================================================
# PART B: TOOL OUTPUT TRIMMING
# =====================================================================
# Tool outputs accumulate in context with every API call. An order lookup
# returning 40 fields when only 5 are needed wastes context AND can cause
# the model to attend to irrelevant data.

VERBOSE_ORDER_RESULT = {
    "order_id": "ORD-10041",
    "customer_id": "CUST-555",
    "customer_name": "Jane Smith",
    "status": "shipped",
    "items": [{"sku": "WIDGET-01", "qty": 2, "price": 44.99}],
    "tracking": "1Z999AA10123456784",
    "shipping_method": "UPS Ground",
    "estimated_delivery": "2026-05-12",
    # --- Everything below is noise for most use cases ---
    "warehouse_id": "WH-EAST-07",
    "pick_list_id": "PL-92847",
    "pack_station": "STATION-14",
    "carrier_account": "UPS-ACCT-001",
    "label_generated_at": "2026-05-09T08:14:22Z",
    "weight_kg": 1.2,
    "dimensions_cm": {"l": 30, "w": 20, "h": 10},
    "shipping_cost_internal": 8.50,
    "insurance_value": 90.00,
    "audit_user": "system",
    "audit_timestamp": "2026-05-09T08:15:00Z",
    "created_at": "2026-05-08T14:22:00Z",
    "updated_at": "2026-05-09T08:15:00Z",
    "internal_notes": "Fragile items flagged for careful handling",
    "priority_flag": False,
    "batch_id": "BATCH-20260509-001",
}

TRIMMED_ORDER_RESULT = {
    "order_id": "ORD-10041",
    "customer_name": "Jane Smith",
    "status": "shipped",
    "tracking": "1Z999AA10123456784",
    "estimated_delivery": "2026-05-12",
}

def part_b_tool_trimming():
    print("\n--- PART B: Tool Output Trimming ---")

    verbose_tokens = len(json.dumps(VERBOSE_ORDER_RESULT))
    trimmed_tokens = len(json.dumps(TRIMMED_ORDER_RESULT))
    reduction = (1 - trimmed_tokens / verbose_tokens) * 100

    print(f"  Verbose result:  {verbose_tokens} characters ({len(VERBOSE_ORDER_RESULT)} fields)")
    print(f"  Trimmed result:  {trimmed_tokens} characters ({len(TRIMMED_ORDER_RESULT)} fields)")
    print(f"  Size reduction:  {reduction:.0f}%\n")

    # Ask both to answer a shipping question
    question = "What is the tracking number and estimated delivery for this order?"

    for label, result in [("VERBOSE", VERBOSE_ORDER_RESULT), ("TRIMMED", TRIMMED_ORDER_RESULT)]:
        response = client.messages.create(
            model=MODEL,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": (
                    f"Order data:\n{json.dumps(result)}\n\n"
                    f"Question: {question}"
                )
            }]
        )
        answer = response.content[0].text.strip()
        print(f"  [{label}] {answer[:100]}")

    print(f"""
  KEY POINT:
    Trimmed result is {reduction:.0f}% smaller and answers the question just as well.
    Verbose results accumulate with EVERY tool call. After 10 calls,
    verbose outputs can consume 80%+ of your context window.

    The FIX is upstream: modify the tool/agent to return ONLY relevant fields.
    A PostToolUse hook can trim outputs after the fact, but fixing at the source is better.

  WRONG: "Rotate outputs to avoid lost-in-middle" -- doesn't help
  WRONG: "Pre-summarize all outputs to 20K tokens" -- loses specific data
  CORRECT: Trim at the source; keep only fields relevant to the task
""")


# =====================================================================
# PART C: ARCHITECTURAL FIX — STRUCTURED UPSTREAM DATA
# =====================================================================

def part_c_upstream_fix():
    print("\n--- PART C: Architectural Fix — Upstream Structured Data ---")
    print("""
The trimming in Part B is a reactive fix (PostToolUse hook).
The architectural fix is proactive: design upstream agents to return
STRUCTURED, TRIMMED data in the first place.

SYMPTOM: 80% of context is tool results (verbose order lookups, full API responses)
ROOT CAUSE: tools return everything; coordinator passes everything to next step
FIX: have upstream agents extract and return only what the next step needs

Example:
  BAD:  search_agent returns full HTML page (120,000 characters)
  GOOD: search_agent returns {"title": "...", "summary": "...", "url": "..."}

  BAD:  inventory_agent returns full product catalog JSON (50 fields per item)
  GOOD: inventory_agent returns {"sku": "...", "available": true, "qty": 142}

The synthesis agent downstream only sees the structured data it actually needs.
Reasoning quality IMPROVES because there's no noise to attend to.

EXAM TRAP: "Add more context to help the model" -- adding more = worse
CORRECT: Less context, higher signal = better reasoning on what matters
""")


def main():
    print("=" * 60)
    print("EXERCISE 1 -- Long Context & Attention Management (5.1)")
    print("=" * 60)

    part_a_lost_in_middle()
    part_b_tool_trimming()
    part_c_upstream_fix()

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 5.1")
    print("=" * 60)
    print("""
Lost-in-the-middle effect:
  Models reliably attend to BEGINNING and END of long inputs
  Middle sections may be ignored or given less attention
  FIX: place key findings summaries at the BEGINNING + use section headers

Wrong mitigations:
  Pre-aggregate inputs to 20K tokens via summarization -> loses specific values
  Rotate which subagent appears first -> doesn't fix position bias
  Stream results incrementally -> position bias applies within each stream chunk

Tool output trimming:
  Verbose tool outputs consume context disproportionately to their value
  BEFORE: 40-field order object, 120K-char HTML page
  AFTER:  5-field trimmed object, title + summary paragraph
  Fix at SOURCE (upstream agent design) > PostToolUse hook (reactive)

When 80% of context = tool results:
  This is a trimming problem, not a context window problem
  Fix: have upstream agents return structured trimmed data
  Wrong fix: increase max_tokens (doesn't address what's filling context)
""")


if __name__ == "__main__":
    main()
