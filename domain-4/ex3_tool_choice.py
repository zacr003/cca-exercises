"""
CCA-F Domain 4, Exercise 3 — tool_choice Configuration (Subdomain 4.4)
=======================================================================

WHAT THIS EXERCISES:
  tool_choice controls HOW Claude selects tools. Three settings, three behaviors.
  Getting this wrong is a common exam trap.

THE THREE SETTINGS:
  "auto"                          -- model MAY call a tool OR return text (default)
  "any"                           -- model MUST call SOME tool; it picks which one
  {"type": "tool", "name": "X"}  -- model MUST call tool X specifically

STRUCTURE:
  Part A -- "auto": shows that the model sometimes returns text instead of calling a tool
  Part B -- "any":  guarantees a tool call; model chooses which
  Part C -- forced: guarantees the SPECIFIC tool named
  Part D -- the pattern: force first turn, auto for subsequent turns
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
# TOOL DEFINITIONS
# Two tools available: one extracts metadata, one searches inventory
# =====================================================================

TOOLS = [
    {
        "name": "extract_metadata",
        "description": (
            "Extract structured metadata from a document: title, date, author, document type. "
            "Use this when the user provides a document and needs its metadata extracted."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title":   {"type": ["string", "null"]},
                "date":    {"type": ["string", "null"]},
                "author":  {"type": ["string", "null"]},
                "doc_type":{"type": "string", "enum": ["invoice", "report", "letter", "other"]}
            },
            "required": ["doc_type"]
        }
    },
    {
        "name": "search_inventory",
        "description": (
            "Search product inventory by keyword or SKU. "
            "Returns matching products with availability."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term or SKU"}
            },
            "required": ["query"]
        }
    }
]

SAMPLE_DOCUMENT = "INVOICE #2026-001\nFrom: Acme Corp\nDate: March 15, 2026\nTotal: $500"
CONVERSATIONAL_MESSAGE = "What is 2 + 2?"


# =====================================================================
# HELPER: Run a single API call and report what happened
# =====================================================================

def run_and_report(user_message: str, tool_choice, label: str):
    """Makes one API call and reports whether a tool was called or text returned."""
    kwargs = {
        "model": MODEL,
        "max_tokens": 256,
        "tools": TOOLS,
        "messages": [{"role": "user", "content": user_message}]
    }
    if tool_choice is not None:
        kwargs["tool_choice"] = tool_choice

    response = client.messages.create(**kwargs)

    tool_calls = [b for b in response.content if b.type == "tool_use"]
    text_blocks = [b for b in response.content if hasattr(b, "text")]

    print(f"\n  [{label}]")
    print(f"  Message    : {user_message[:60]}...")
    print(f"  tool_choice: {json.dumps(tool_choice)}")
    print(f"  stop_reason: {response.stop_reason}")

    if tool_calls:
        for tc in tool_calls:
            print(f"  Tool called: {tc.name}")
            print(f"  Tool input : {json.dumps(tc.input, ensure_ascii=True)}")
    elif text_blocks:
        print(f"  Text returned (no tool): {text_blocks[0].text[:80]}")
    else:
        print("  (no text or tool in response)")


# =====================================================================
# PART A: "auto" — model MAY call a tool OR return text
# =====================================================================
# "auto" is the default. The model decides based on the message content.
# For conversational questions ("what is 2+2"), it returns text.
# For document extraction tasks, it might call extract_metadata.
# But there's no GUARANTEE — it might return text for either.

def part_a_auto():
    print("\n--- PART A: tool_choice 'auto' ---")
    print("'auto' = model decides; it may call a tool OR return text")
    print("Watch: conversational question usually gets text, not a tool call")

    run_and_report(CONVERSATIONAL_MESSAGE, "auto", "auto + conversational")
    run_and_report(
        f"Please extract the metadata from this document:\n{SAMPLE_DOCUMENT}",
        "auto",
        "auto + extraction request"
    )
    print("""
  KEY POINT:
  'auto' does not guarantee a tool call. Even for extraction tasks, the model
  might return a text description instead of calling extract_metadata.
  If you need guaranteed structured output, use 'any' or forced selection.
""")


# =====================================================================
# PART B: "any" — model MUST call SOME tool; it picks which
# =====================================================================
# "any" guarantees a tool call happens. But the model chooses which tool.
# Use this when you have multiple valid tools and the model should pick.
# Example: you have 3 extraction schemas and don't know document type yet.

def part_b_any():
    print("\n--- PART B: tool_choice 'any' ---")
    print("'any' = MUST call a tool; model chooses which one")
    print("Watch: even conversational question gets forced into a tool call")

    run_and_report(CONVERSATIONAL_MESSAGE, "any", "any + conversational")
    run_and_report(
        f"Please extract the metadata from this document:\n{SAMPLE_DOCUMENT}",
        "any",
        "any + extraction request"
    )
    print("""
  KEY POINT:
  'any' guarantees the model calls ONE of the available tools.
  The model picks which tool based on the message content and tool descriptions.
  Use 'any' when: document type is unknown and you have multiple extraction schemas.

  EXAM TRAP: "tool_choice:'any' forces a specific tool"
  WRONG -- 'any' forces A tool, but the model picks WHICH one.
  For a specific tool, use forced selection (Part C).
""")


# =====================================================================
# PART C: Forced selection — model MUST call tool X specifically
# =====================================================================
# {"type": "tool", "name": "X"} forces the model to call exactly tool X.
# The model cannot return text or call a different tool.
# Use this when you need guaranteed structured output of a specific schema.

def part_c_forced():
    print("\n--- PART C: Forced tool selection ---")
    print("{'type':'tool','name':'extract_metadata'} = MUST call extract_metadata specifically")
    print("Watch: even a non-document message gets forced to call the extraction tool")

    run_and_report(
        CONVERSATIONAL_MESSAGE,
        {"type": "tool", "name": "extract_metadata"},
        "forced + conversational"
    )
    run_and_report(
        f"Extract metadata:\n{SAMPLE_DOCUMENT}",
        {"type": "tool", "name": "extract_metadata"},
        "forced + extraction request"
    )
    print("""
  KEY POINT:
  Forced selection guarantees extract_metadata is called with NO EXCEPTIONS.
  The model cannot return text. It cannot call search_inventory instead.
  Use this for: first turn of a workflow where you always need a specific extraction.

  Then switch to 'auto' for subsequent turns (the pattern in Part D).
""")


# =====================================================================
# PART D: The recommended pattern
# =====================================================================
# Force a specific tool on the first turn → switch to "auto" for subsequent turns.
# Why: forced selection is too rigid for multi-turn workflows (the model can't adapt).
# But for the first turn, you want guaranteed structured output.

def part_d_pattern():
    print("\n--- PART D: The Recommended Pattern ---")
    print("""
PATTERN: Force specific tool on first turn -> 'auto' for subsequent turns

  Turn 1 (forced):
    tool_choice = {"type": "tool", "name": "extract_metadata"}
    -> Guaranteed metadata extraction
    -> Model CANNOT skip or return text

  Turn 2+ (auto):
    tool_choice = "auto"
    -> Model adapts based on what's needed next
    -> Can call any tool or return a final answer
    -> Appropriate for follow-up questions about the extracted data

Why not forced for all turns?
  Forced selection keeps forcing the same tool on every turn.
  After extraction, the model needs flexibility to call search_inventory,
  ask a clarifying question, or return a final text response.
  'auto' gives it that flexibility for subsequent turns.
""")


def main():
    print("=" * 60)
    print("EXERCISE 3 -- tool_choice Configuration (4.4)")
    print("=" * 60)

    part_a_auto()
    part_b_any()
    part_c_forced()
    part_d_pattern()

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 4.4")
    print("=" * 60)
    print("""
tool_choice options:
  "auto"                        Model may call tool OR return text (default)
  "any"                         Model MUST call SOME tool; it picks which
  {"type":"tool","name":"X"}    Model MUST call tool X specifically
  "none"                        Prevents any tool use (text only)

When to use each:
  "auto"   -- General-purpose agents; tool use is optional based on context
  "any"    -- Guaranteed structured output with multiple possible schemas
             (e.g., unknown document type, have 3 extraction tools, pick one)
  forced   -- Guarantee a specific schema on the first turn of a workflow
  pattern  -- Force first turn, then auto for subsequent turns

EXAM TRAPS:
  "tool_choice:'any' forces a specific tool" -- WRONG: it forces SOME tool, model picks
  "tool_choice:'auto' + stronger prompts to force tool" -- WRONG: 'auto' still allows text
  "tool_choice:'any' for all turns" -- works but too rigid for multi-turn workflows
  "forced selection for all turns" -- too rigid; model can't adapt after first turn
""")


if __name__ == "__main__":
    main()
