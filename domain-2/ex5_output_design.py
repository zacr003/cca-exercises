"""
CCA-F Domain 2, Exercise 5 -- Tool Output Design (Subdomain 2.5)

WHAT THIS EXERCISES:
  Tool output shape determines context quality. Verbose, noisy output accumulates
  quickly across tool calls and degrades the agent's reasoning.

KEY CONCEPTS:
  1. Trim verbose tool output to only business-relevant fields
  2. PostToolUse hook trims BEFORE the model processes the result
  3. Edit -> Read + Write fallback when match text is not unique
  4. Pagination for large result sets (100K+ tokens of output)
  5. Rate limiting belongs in the MCP server (token bucket) -- not in prompts

STRUCTURE:
  Part A -- verbose tool output floods context; Claude sees noise
  Part B -- trimmed output; only business fields remain
  Part C -- Edit -> Read + Write fallback demo (no API needed)
  Part D -- pagination concept demo
"""

import sys
import json
import copy
import pathlib
import tempfile

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


# ==============================================================
# VERBOSE vs. TRIMMED TOOL IMPLEMENTATIONS
# ==============================================================

def get_product_details_verbose(product_id):
    """
    ANTI-PATTERN: returns everything from the backend.
    Internal IDs, audit timestamps, query metrics, system fields --
    none of this is useful to Claude, but all of it consumes context tokens.
    """
    return {
        # Fields Claude needs
        "product_id":   product_id,
        "name":         "Blue Widget Pro",
        "price":        89.99,
        "in_stock":     True,
        "category":     "Widgets",
        "description":  "A high-quality blue widget for professional use.",

        # Internal noise -- useless to the agent
        "internal_sku":       "INT-WGT-BLU-PRO-001",
        "warehouse_bin":      "A4-SHELF-22-BIN-7",
        "last_audit_ts":      "2026-04-15T03:22:11.847Z",
        "audit_by":           "svc-warehouse-audit-bot",
        "db_row_version":     7,
        "shard_key":          "us-east-1:products:0x4A2F",
        "etag":               "W/\"7-abc123def456\"",
        "query_plan_hash":    "0xDEADBEEF",
        "query_duration_ms":  43,
        "cache_hit":          False,
        "replica_id":         "replica-03.us-east-1.rds",
        "index_seek_count":   1,
        "raw_sql_params":     ["INT-WGT-BLU-PRO-001"],
        "internal_flags": {
            "is_featured":      True,
            "is_clearance":     False,
            "vendor_managed":   False,
            "hazmat_class":     None,
            "export_controlled": False
        }
    }


def get_product_details_trimmed(product_id):
    """
    CORRECT: return only what Claude needs to answer the customer's question.
    Token-efficient; no noise accumulates across multiple tool calls.
    """
    return {
        "product_id":  product_id,
        "name":        "Blue Widget Pro",
        "price":       89.99,
        "in_stock":    True,
        "category":    "Widgets",
        "description": "A high-quality blue widget for professional use."
    }


TOOL_DEF = {
    "name": "get_product_details",
    "description": "Get product information by product ID.",
    "input_schema": {
        "type": "object",
        "properties": {
            "product_id": {"type": "string"}
        },
        "required": ["product_id"]
    }
}


def run_product_query(implementation, label):
    user_message = "What can you tell me about product WIDGET-001? Is it in stock?"
    print(f"\n  [{label}]")

    messages = [{"role": "user", "content": user_message}]
    for _ in range(3):
        response = client.messages.create(
            model=MODEL,
            max_tokens=256,
            tools=[TOOL_DEF],
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"  Agent: {block.text.strip()}")
            return

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = implementation(block.input["product_id"])
                    token_estimate = len(json.dumps(result)) // 4
                    print(f"  Tool result (~{token_estimate} tokens): {json.dumps(result, ensure_ascii=True)[:200]}")
                    if len(json.dumps(result)) > 200:
                        print("  ... (truncated for display)")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=True)
                    })
            messages.append({"role": "user", "content": tool_results})


# ==============================================================
# PART C -- Edit -> Read + Write fallback
#
# The Edit tool requires a UNIQUE match in the target file.
# If the same string appears multiple times, Edit fails.
# Fallback: Read the full file, modify in Python, Write the whole file back.
#
# This is pure Python -- no API call needed. Demonstrates the pattern.
# ==============================================================

def demo_edit_fallback():
    """
    Simulate the Edit -> Read + Write fallback.
    A file has 'TODO: add source summary' in three places.
    Edit would fail (non-unique match). Read + Write succeeds.
    """
    # Create a temp file with non-unique content
    tmp = pathlib.Path(tempfile.gettempdir()) / "demo_report.md"
    original_content = """# Research Report

## Section 1
TODO: add source summary

## Section 2
TODO: add source summary

## Section 3
TODO: add source summary
"""
    tmp.write_text(original_content, encoding="utf-8")

    print(f"\n  Temp file: {tmp}")
    print(f"  Original content:\n{original_content}")

    # Step 1: Try Edit (would fail -- non-unique match)
    print("  Step 1: Edit tool would FAIL -- 'TODO: add source summary' appears 3 times.")
    print("          Edit requires a unique match. Falling back to Read + Write.\n")

    # Step 2: Read
    content = tmp.read_text(encoding="utf-8")
    print(f"  Step 2: Read -- {len(content)} chars loaded.")

    # Step 3: Modify all occurrences in Python
    updated = content.replace(
        "TODO: add source summary",
        "Summary added by agent."
    )
    print(f"  Step 3: Replace all occurrences.")

    # Step 4: Write back
    tmp.write_text(updated, encoding="utf-8")
    print(f"  Step 4: Write -- full file written back.\n")
    print(f"  Updated content:\n{updated}")

    # Cleanup
    tmp.unlink()


# ==============================================================
# PART D -- Pagination concept
#
# When a tool could return 100K+ tokens of results, paginate.
# Return: first page + total count + next_page token.
# Agent fetches subsequent pages only if needed.
# ==============================================================

def get_audit_log_paginated(page_token=None, page_size=3):
    """
    Mock paginated tool response.
    Real implementation would use page_token for cursor-based pagination.
    """
    all_entries = [
        {"ts": "2026-05-01T10:00:00Z", "action": "login",    "user": "alice"},
        {"ts": "2026-05-01T10:05:00Z", "action": "edit",     "user": "alice"},
        {"ts": "2026-05-01T10:10:00Z", "action": "logout",   "user": "alice"},
        {"ts": "2026-05-01T11:00:00Z", "action": "login",    "user": "bob"},
        {"ts": "2026-05-01T11:15:00Z", "action": "delete",   "user": "bob"},
        {"ts": "2026-05-01T11:20:00Z", "action": "logout",   "user": "bob"},
        {"ts": "2026-05-02T09:00:00Z", "action": "login",    "user": "carol"},
    ]

    start = 0 if page_token is None else int(page_token)
    page  = all_entries[start:start + page_size]
    next_token = str(start + page_size) if (start + page_size) < len(all_entries) else None

    return {
        "entries": page,
        "returned": len(page),
        "total": len(all_entries),
        "next_page_token": next_token   # None means last page
    }


def main():
    print("=" * 60)
    print("EXERCISE 5 -- Tool Output Design (2.5)")
    print("=" * 60)

    # ---- Part A: Verbose ----
    print("\n--- PART A: VERBOSE tool output (floods context) ---")
    run_product_query(get_product_details_verbose, "VERBOSE")

    # ---- Part B: Trimmed ----
    print("\n--- PART B: TRIMMED tool output (only business fields) ---")
    run_product_query(get_product_details_trimmed, "TRIMMED")

    # ---- Part C: Edit fallback ----
    print("\n--- PART C: Edit -> Read + Write fallback (non-unique match) ---")
    demo_edit_fallback()

    # ---- Part D: Pagination ----
    print("\n--- PART D: Paginated tool output ---")
    print("  First page:")
    page1 = get_audit_log_paginated()
    print(f"  {json.dumps(page1, ensure_ascii=True, indent=2)}")

    if page1["next_page_token"]:
        print("\n  Second page:")
        page2 = get_audit_log_paginated(page_token=page1["next_page_token"])
        print(f"  {json.dumps(page2, ensure_ascii=True, indent=2)}")

    # ---- Hook note ----
    print("\n--- HOOK NOTE: PostToolUse for output trimming ---")
    print("""
  See hook_post_output_trim.py for the Claude Code hook implementation.
  The hook intercepts the tool result BEFORE Claude processes it and
  injects trimming context (or strips verbose fields).

  EXAM TRAP: PostToolUse hook that returns BOTH formatted summary AND
  raw output still sends the full raw content to the model.
  The hook should return ONLY the trimmed/formatted version.

  Rate limiting:
    CORRECT  -- Token bucket implemented in the MCP server
    WRONG    -- System prompt: "wait 1 second between calls"
    WRONG    -- PreToolUse hook: time.sleep(1) before each call
    Reason   -- Prompt-based rate limiting is probabilistic and unreliable;
                server-side enforcement is deterministic
""")

    print("=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 2.5")
    print("=" * 60)
    print("""
Output trimming:
  CORRECT  -- Strip internal IDs, audit timestamps, query metrics before returning
  CORRECT  -- PostToolUse hook returns ONLY formatted summary (not summary + raw)
  WRONG    -- Return full backend response and rely on Claude to ignore noise

Edit -> Read + Write fallback:
  When Edit fails due to non-unique match:
    Step 1: Read the full file
    Step 2: Modify all occurrences in application code
    Step 3: Write the full file back

Pagination:
  Return: first page + total count + next_page token
  Agent requests subsequent pages only if task requires them
  Prevents 100K+ token results from flooding context in a single call

Rate limiting:
  CORRECT  -- Token bucket in the MCP server implementation
  WRONG    -- System prompt instructions to pause between calls
  WRONG    -- PreToolUse hook sleep delay
""")


if __name__ == "__main__":
    main()
