"""
CCA-F Domain 5, Exercise 4 — Structured Error Propagation (Subdomain 5.3)
==========================================================================

WHAT THIS EXERCISES:
  When a subagent fails, it should return structured error context — not
  silence the failure or terminate the whole workflow.

  NEW CONCEPT FROM HANDBOOK:
  Coverage annotations — synthesis output should flag which topics are well-supported
  vs. which have gaps due to unavailable sources. This lets the coordinator
  make targeted re-delegation decisions.

KEY RULES:
  Return: failure type + what was attempted + partial results + potential alternatives
  Anti-pattern 1: silent suppression (return {} or [] on failure)
  Anti-pattern 2: full workflow termination on single subagent failure
  Access failure:    isError: true, errorCategory: "transient|permission"
  Valid empty:       {results: [], status: "success"} — NOT isError
  Non-retryable:     isRetryable: false (corrupted file, permission denied, policy violation)
  Coverage annotations: synthesis output flags well-covered vs. gap topics

STRUCTURE:
  Part A -- Correct structured error responses vs. anti-patterns
  Part B -- Multi-agent recovery: coordinator receives error, tries alternative
  Part C -- Coverage annotations in synthesis output
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
# PART A: STRUCTURED ERRORS VS. ANTI-PATTERNS
# =====================================================================

def part_a_error_responses():
    print("\n--- PART A: Structured Error Responses vs. Anti-Patterns ---")

    # Scenario: a search subagent tries to fetch data and encounters 3 different situations

    situations = [
        {
            "label": "TIMEOUT (transient failure)",
            "description": "The database timed out after 5 seconds",
            "correct_response": {
                "isError": True,
                "errorCategory": "transient",
                "isRetryable": True,
                "description": "Database timed out after 5 seconds. Retry with same parameters.",
                "partialResults": None,
                "attemptedQuery": "SELECT orders WHERE status=pending",
                "suggestedAction": "retry"
            },
            "antipattern_response": {},  # silent suppression
            "why_antipattern_fails": "Coordinator cannot distinguish timeout from 'no results found'"
        },
        {
            "label": "PERMISSION DENIED (403)",
            "description": "Agent does not have access to the financial records table",
            "correct_response": {
                "isError": True,
                "errorCategory": "permission",
                "isRetryable": False,
                "description": "Access denied to financial_records table. Requires elevated permissions.",
                "partialResults": None,
                "suggestedAction": "escalate"
            },
            "antipattern_response": {"results": [], "count": 0},  # looks like empty result
            "why_antipattern_fails": "Coordinator thinks query succeeded with no results; won't try alternative"
        },
        {
            "label": "VALID EMPTY RESULT",
            "description": "Query succeeded but no records matched the criteria",
            "correct_response": {
                "status": "success",
                "results": [],
                "count": 0,
                "message": "No orders matched the search criteria for date range 2026-01-01 to 2026-01-07"
                # Note: NO isError flag -- this is a SUCCESS
            },
            "antipattern_response": {
                "isError": True,
                "errorCategory": "transient",
                "description": "No data returned"  # WRONG: empty = error
            },
            "why_antipattern_fails": "Coordinator retries a successful query, wasting resources"
        }
    ]

    for s in situations:
        print(f"\n  Situation: {s['label']}")
        print(f"  What happened: {s['description']}")
        print(f"\n  CORRECT response:")
        print(f"    {json.dumps(s['correct_response'], indent=4)[:300]}")
        print(f"\n  ANTI-PATTERN response:")
        print(f"    {json.dumps(s['antipattern_response'])}")
        print(f"  Why anti-pattern fails: {s['why_antipattern_fails']}")

    print("""
  KEY DISTINCTIONS:
    Access failure (timeout, 403) -> isError: true + appropriate category + isRetryable
    Valid empty result             -> status: "success", results: []  (NO isError)
    Non-retryable (permission)    -> isRetryable: false + suggestedAction: "escalate"
    Retryable (transient)         -> isRetryable: true + suggestedAction: "retry"

  NEVER:
    Return {} or [] to represent a failure (silent suppression)
    Terminate the entire workflow because one subagent failed
    Retry with identical parameters when the error is non-transient
""")


# =====================================================================
# PART B: MULTI-AGENT RECOVERY
# =====================================================================
# When a coordinator receives a structured error, it can make an intelligent
# decision: retry, try an alternative source, or proceed with partial results.

COORDINATOR_SYSTEM = """You are a research coordinator. You delegate tasks to subagents.
When a subagent returns an error:
  - transient error (isRetryable: true): try once more or try an alternative
  - permission error (isRetryable: false): note the gap, proceed with available results
  - valid empty result (no isError): record as "no data found", not as a failure

Your goal: produce the best possible research output even when some sources fail.
Always report what coverage you achieved vs. what gaps remain."""

RESEARCH_TOOLS = [
    {
        "name": "search_primary_database",
        "description": "Search the primary research database. May have transient timeouts.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    },
    {
        "name": "search_fallback_source",
        "description": "Search the fallback data source. Slower but more reliable.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    },
    {
        "name": "compile_report",
        "description": "Compile all findings into a structured report with coverage annotations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "findings": {"type": "string", "description": "Research findings accumulated"},
                "coverage_notes": {"type": "string", "description": "What topics are well-covered vs. have gaps"}
            },
            "required": ["findings", "coverage_notes"]
        }
    }
]

# Simulate: primary fails with transient error, fallback succeeds
CALL_COUNT = {"primary": 0, "fallback": 0}

def handle_research_tool(name: str, tool_input: dict) -> dict:
    if name == "search_primary_database":
        CALL_COUNT["primary"] += 1
        # First call: transient timeout
        if CALL_COUNT["primary"] == 1:
            return {
                "isError": True,
                "errorCategory": "transient",
                "isRetryable": True,
                "description": "Primary database timed out. Consider using fallback source.",
                "suggestedAction": "retry_or_fallback"
            }
        # Second call: success (simulating retry worked)
        return {
            "status": "success",
            "results": ["Finding A: Revenue grew 15% in Q1", "Finding B: New market entry in Q3"],
            "source": "primary_database"
        }

    if name == "search_fallback_source":
        CALL_COUNT["fallback"] += 1
        return {
            "status": "success",
            "results": ["Finding C: Competitor launched new product line"],
            "source": "fallback_source",
            "note": "Fallback source has 2-day data lag"
        }

    if name == "compile_report":
        return {
            "report_id": "RPT-001",
            "compiled": True,
            "findings": tool_input.get("findings"),
            "coverage_notes": tool_input.get("coverage_notes")
        }

    return {"error": "unknown tool"}


def part_b_multi_agent_recovery():
    print("\n--- PART B: Multi-Agent Recovery ---")
    print("Primary database will timeout on first attempt.")
    print("Watch: coordinator receives structured error and tries alternative.\n")

    messages = [{
        "role": "user",
        "content": "Research Q1 2026 business performance. Use available data sources."
    }]

    for _ in range(6):  # safety cap
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=COORDINATOR_SYSTEM,
            tools=RESEARCH_TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text = next((b.text for b in response.content if hasattr(b, "text")), "")
            print(f"  Final output: {text.strip()[:300]}")
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = handle_research_tool(block.name, block.input)
                    has_error = result.get("isError", False)
                    status_marker = "ERROR" if has_error else "OK"
                    print(f"  [{status_marker}] {block.name}: {json.dumps(result, ensure_ascii=True)[:100]}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=True)
                    })
            messages.append({"role": "user", "content": tool_results})


# =====================================================================
# PART C: COVERAGE ANNOTATIONS
# =====================================================================
# When synthesis output includes coverage annotations, the coordinator
# can evaluate completeness and re-delegate for specific gaps.
# Without annotations, the coordinator accepts incomplete output as done.

def part_c_coverage_annotations():
    print("\n--- PART C: Coverage Annotations ---")
    print("""
CONCEPT: Synthesis output with coverage annotations

When a synthesis subagent compiles a report, it should indicate:
  - Which topics are well-supported (multiple credible sources)
  - Which topics have limited coverage (1 source, or outdated source)
  - Which topics have no coverage (source unavailable or failed)

WITHOUT coverage annotations:
  Coordinator receives: "Here is the research report on Q1 performance."
  Coordinator thinks: "Great, done."
  Reality: Three subtopics had no data due to subagent timeouts
  The user gets an incomplete report with no indication of what's missing

WITH coverage annotations:
  Coordinator receives:
    findings: "Q1 revenue grew 15%..."
    coverage_notes: "Well-covered: revenue, market share. Gap: supply chain (primary source unavailable). No coverage: international operations (requires restricted access)."
  Coordinator can:
    - Re-delegate supply chain query to fallback source
    - Note international operations gap in final report
    - Only surface the report when coverage is sufficient

EXAM PATTERN:
  The coordinator evaluates synthesis output by checking coverage annotations.
  If gaps exist, it generates targeted follow-up queries and re-delegates.
  This is the iterative refinement loop in multi-agent research systems.

EXAMPLE SYNTHESIS OUTPUT WITH ANNOTATIONS:

{
  "executive_summary": "Q1 revenue grew 15% YoY...",
  "detailed_findings": {
    "revenue": {"data": "...", "sources": 3, "coverage": "well-supported"},
    "market_share": {"data": "...", "sources": 2, "coverage": "well-supported"},
    "supply_chain": {"data": null, "sources": 0, "coverage": "gap",
                     "reason": "primary database timed out; fallback not queried yet"},
    "international": {"data": null, "sources": 0, "coverage": "gap",
                      "reason": "requires restricted database access not available"}
  },
  "coverage_summary": "2 of 4 topics well-covered. 2 gaps: supply_chain (retryable), international (permission required)."
}

COORDINATOR LOGIC:
  supply_chain gap + isRetryable=true -> re-delegate to fallback source
  international gap + permission error -> note in report, possibly escalate
  Only mark report as "complete" when coverage is sufficient for the use case
""")


def main():
    print("=" * 60)
    print("EXERCISE 4 -- Error Propagation (5.3)")
    print("=" * 60)

    part_a_error_responses()
    part_b_multi_agent_recovery()
    part_c_coverage_annotations()

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 5.3")
    print("=" * 60)
    print("""
Structured error fields:
  isError        : true for access/execution failures; absent for success (even empty)
  errorCategory  : "transient" | "validation" | "business" | "permission"
  isRetryable    : true = retry may work; false = same params will fail again
  description    : what went wrong and what was attempted
  partialResults : return any partial data even on failure (don't discard)
  suggestedAction: "retry" | "fix_input" | "escalate" | "alternative_workflow"

Critical distinction:
  isError: true  = access or execution FAILED
  {results: []}  = query SUCCEEDED, nothing matched (NOT an error)
  Conflating these causes the coordinator to retry successful empty queries

Error handling decision tree (exam favorite):
  1. Transient? (timeout) -> retry locally with backoff
  2. Validation? (bad input) -> fix input, retry locally
  3. Permission/business? -> can't retry; propagate structured error to coordinator
  4. Alternative available? -> try it
  5. Partial results only? -> return partial + coverage annotations
  6. Unrecoverable? -> escalate to human with full context

Coverage annotations:
  Synthesis output should indicate which topics are well-covered vs. have gaps
  Enables coordinator to evaluate completeness and make targeted re-delegation decisions
  Without annotations: coordinator accepts incomplete output as done
  With annotations: coordinator can loop back for specific uncovered topics

Anti-patterns (NEVER do these):
  Return {} or [] on failure (silent suppression) -> coordinator can't recover
  Terminate entire workflow on single failure -> disproportionate, loses partial progress
  Retry with identical parameters on non-transient errors -> will fail again
  Discard partial results from timed-out subagents -> return what you have + structured error
""")


if __name__ == "__main__":
    main()
