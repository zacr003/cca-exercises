"""
CCA-F Domain 5, Exercise 3 — Context Degradation and Memory Patterns (Subdomains 5.4, 5.5)
============================================================================================

WHAT THIS EXERCISES:
  In long sessions, models lose track of specific details and fall back to generic
  responses. Two patterns fix this: scratchpad files and persistent case-facts blocks.

CONTEXT DEGRADATION (5.4):
  Symptom: agent says "typical patterns" instead of specific class names it found earlier
  Fix: scratchpad files — agent writes key findings to a file and reads them at phase boundaries
  Wrong fix: adding more instructions to an overloaded context (wrong tool for the problem)
  Wrong fix: setting max_tokens lower (max_tokens = OUTPUT length, not SESSION size)

CONVERSATION MEMORY (5.5):
  The Claude API is STATELESS — no session_id, no automatic history retention
  Every API request must include the FULL messages array (all prior turns)
  Fix for long sessions: hybrid context management (summarize old + keep recent + case-facts block)
  Case-facts block: persistent block OUTSIDE summarized history for transactional data (amounts, dates, IDs)

STRUCTURE:
  Part A -- API statelessness: what happens without history vs. with history
  Part B -- Simulated context degradation: agent "forgets" specific details
  Part C -- Scratchpad file pattern: persist key findings outside context
  Part D -- Case-facts block: keep transactional data across summarization
"""

import sys
import json
import os
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


# =====================================================================
# PART A: API STATELESSNESS
# =====================================================================
# The Claude API has NO session memory. Each request is independent.
# To maintain a conversation, YOU must include the full messages array.

def part_a_statelessness():
    print("\n--- PART A: API Statelessness ---")
    print("Demonstrating that without the messages history, Claude 'forgets' prior turns.\n")

    # Turn 1: tell Claude your name
    turn1 = client.messages.create(
        model=MODEL,
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "My name is Zac. Please remember that for our conversation."
        }]
    )
    reply1 = turn1.content[0].text

    # Turn 2 WITHOUT history: Claude doesn't know the name
    turn2_no_history = client.messages.create(
        model=MODEL,
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "What is my name?"  # No history included
        }]
    )
    reply2_no_history = turn2_no_history.content[0].text

    # Turn 2 WITH history: Claude can reference the name
    turn2_with_history = client.messages.create(
        model=MODEL,
        max_tokens=100,
        messages=[
            {"role": "user", "content": "My name is Zac. Please remember that for our conversation."},
            {"role": "assistant", "content": reply1},
            {"role": "user", "content": "What is my name?"}
        ]
    )
    reply2_with_history = turn2_with_history.content[0].text

    print(f"  Turn 1: 'My name is Zac...'")
    print(f"  Turn 1 response: {reply1.strip()[:80]}")
    print()
    print(f"  Turn 2 WITHOUT history: 'What is my name?'")
    print(f"  Response: {reply2_no_history.strip()[:80]}")
    print()
    print(f"  Turn 2 WITH history: 'What is my name?'")
    print(f"  Response: {reply2_with_history.strip()[:80]}")
    print("""
  KEY POINT:
    The API is STATELESS. There is no session_id parameter.
    Every request must include the full messages array.
    Without history, the model has no memory of prior turns.

  EXAM TRAP: "The Claude API retains state between calls"
  WRONG: It does not. You are responsible for passing full conversation history.
""")


# =====================================================================
# PART B: SIMULATED CONTEXT DEGRADATION
# =====================================================================
# We simulate an extended session by injecting lots of filler turns before
# asking about an early finding. This mimics what happens when a long
# codebase exploration fills the context with verbose output.

def part_b_context_degradation():
    print("\n--- PART B: Context Degradation Simulation ---")
    print("We'll inject a key fact early, then bury it under many turns of filler.")
    print("Watch whether the model recalls the specific detail.\n")

    # The key fact we plant early in the conversation
    early_finding = "The custom class is named LegacyHttpRequestWrapper (not HttpServletRequest)."

    # Build a long conversation history with the early finding buried
    messages = [
        {"role": "user", "content": f"Note this important finding: {early_finding}"},
        {"role": "assistant", "content": "Understood. LegacyHttpRequestWrapper is the custom class to use."},
    ]

    # Add many turns of filler to simulate context filling up
    for i in range(15):
        messages.append({"role": "user", "content": f"Now analyze module {i+1}. What are the typical patterns?"})
        messages.append({"role": "assistant", "content": f"Module {i+1} follows standard Java patterns with typical request handling and common design patterns for enterprise applications."})

    # Now ask about the specific early finding
    messages.append({"role": "user", "content": "When handling HTTP requests in this codebase, which class should I use?"})

    response = client.messages.create(
        model=MODEL,
        max_tokens=150,
        messages=messages
    )
    answer = response.content[0].text.strip()

    found_specific = "legacyhttprequestwrapper" in answer.lower()
    found_generic = "httpservletrequest" in answer.lower() or "typical" in answer.lower() or "standard" in answer.lower()

    print(f"  Early finding: '{early_finding}'")
    print(f"  After 15 filler turns, asked: 'Which class should I use for HTTP requests?'")
    print(f"  Answer: {answer[:200]}")
    print()

    if found_specific and not found_generic:
        print("  [FOUND] Model recalled the specific class name")
    elif found_generic and not found_specific:
        print("  [DEGRADED] Model fell back to generic description -- lost the specific finding")
    else:
        print("  [PARTIAL] Model gave a mixed answer")

    print("""
  THIS IS CONTEXT DEGRADATION:
    Symptom: agent says "typical patterns" / "standard approach" instead of
             the specific class/function it found earlier in the session
    Cause:   specific findings pushed into middle of long context, lost in the middle effect
    Fix:     scratchpad files (Part C)
""")


# =====================================================================
# PART C: SCRATCHPAD FILE PATTERN
# =====================================================================
# The fix for context degradation: write key findings to a file.
# At phase boundaries (or before answering questions), the agent reads
# the scratchpad to get the specific details back into context.

def part_c_scratchpad():
    print("\n--- PART C: Scratchpad File Pattern ---")
    print("Writing key findings to a file, then reading them back before answering.\n")

    # Create a temporary scratchpad file
    scratchpad_path = os.path.join(tempfile.gettempdir(), "cca_exercise_scratchpad.json")

    # Step 1: Agent discovers something and writes it to scratchpad
    discoveries = {
        "http_handler_class": "LegacyHttpRequestWrapper",
        "database_connection": "Use LegacyDbPool.getInstance() not DataSource",
        "auth_module": "AuthFilter in com.example.legacy.security package",
        "config_location": "/etc/app/legacy.properties (not application.yml)",
        "note": "All 'Legacy' prefixed classes are the correct ones for this codebase"
    }

    with open(scratchpad_path, "w") as f:
        json.dump(discoveries, f, indent=2)

    print(f"  Scratchpad written to: {scratchpad_path}")
    print(f"  Contents: {json.dumps(discoveries, indent=4)}\n")

    # Step 2: Later in the session, read scratchpad before answering
    with open(scratchpad_path, "r") as f:
        scratchpad_content = json.load(f)

    # Build a long filler context (simulating a long session)
    messages = []
    for i in range(10):
        messages.append({"role": "user", "content": f"Analyze standard module {i}"})
        messages.append({"role": "assistant", "content": f"Standard analysis for module {i} complete."})

    # Now inject scratchpad at the top of the next question
    messages.append({
        "role": "user",
        "content": (
            f"=== KEY FINDINGS (from scratchpad) ===\n"
            f"{json.dumps(scratchpad_content, indent=2)}\n"
            f"=== END SCRATCHPAD ===\n\n"
            f"Question: Which class should I use for handling HTTP requests in this codebase?"
        )
    })

    response = client.messages.create(
        model=MODEL,
        max_tokens=150,
        messages=messages
    )
    answer = response.content[0].text.strip()

    found_specific = "legacyhttprequestwrapper" in answer.lower()
    print(f"  Response with scratchpad injected: {answer[:200]}")
    print(f"\n  [{'FOUND' if found_specific else 'MISSED'}] Specific class recalled from scratchpad")

    # Clean up
    os.remove(scratchpad_path)

    print("""
  HOW IT WORKS:
    1. During exploration: agent writes discoveries to scratchpad file
    2. At phase boundaries: agent reads scratchpad and injects at top of next question
    3. Specific details are always available regardless of how long the session is

  Note: /compact in Claude Code summarizes the conversation to reclaim token budget.
  After /compact, the project CLAUDE.md is re-read from disk automatically.
  Scratchpad files persist independently of conversation compaction.
""")


# =====================================================================
# PART D: CASE-FACTS BLOCK
# =====================================================================
# For customer support conversations, transactional facts (order numbers,
# amounts, dates) get lost during summarization. The fix is a persistent
# "case facts" block maintained OUTSIDE the summarized conversation history.

def part_d_case_facts():
    print("\n--- PART D: Case-Facts Block ---")
    print("""
PROBLEM: Long customer support conversations use summarization to manage context.
         Summarization loses specific values: "Customer mentioned promotional pricing"
         instead of "Customer referenced promo code SUMMER25 for 20% discount".

FIX: Persistent case-facts block maintained OUTSIDE the summarized conversation.
     Every request includes this block, separate from the (possibly summarized) history.

EXAMPLE STRUCTURE:

  Request to Claude:
  -----------------
  [CASE FACTS - always include these]
  Customer ID: CUST-12345
  Order ID: ORD-7890
  Refund Requested: $127.50
  Promo Code Used: SUMMER25 (20% discount applied on 2026-03-10)
  Issues Identified: Wrong item delivered; replacement shipped but also wrong
  Actions Taken: Replacement #1 shipped 2026-03-12; Replacement #2 shipped 2026-03-19

  [CONVERSATION (may be summarized)]
  Customer initially contacted about wrong item...
  [... summarized earlier conversation ...]
  Customer: "This is my third attempt to get the right item. I want a refund."

WHY THIS WORKS:
  The case-facts block is maintained deterministically by YOUR code, not by
  the model's summarization. Specific values (amounts, IDs, dates) CANNOT
  be condensed or paraphrased — they're verbatim in every request.

WRONG alternatives:
  "Raise the summarization threshold" -> just delays the problem; numbers still get lost eventually
  "Instruct Claude to preserve numbers in summaries" -> probabilistic; still degrades
  "Store in external DB and retrieve semantically" -> miss-detection risk on exact values
""")

    # Demonstrate with a concrete example
    case_facts_block = """=== CASE FACTS (always reference these) ===
Customer ID: CUST-12345
Order ID: ORD-7890
Refund Amount Requested: $127.50
Promo Code: SUMMER25 (20% applied 2026-03-10)
Contact Count: 3 previous contacts
Previous Resolution Attempts: replacement shipped twice, both incorrect
==="""

    summarized_history = "Customer has contacted us three times about an order issue. Prior attempts to resolve with replacements were unsuccessful."

    messages = [{
        "role": "user",
        "content": (
            f"{case_facts_block}\n\n"
            f"=== CONVERSATION HISTORY ===\n{summarized_history}\n\n"
            f"Customer now says: 'I just want my $127.50 back, I don't want another replacement.'"
        )
    }]

    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=messages
    )
    answer = response.content[0].text.strip()

    has_amount = "127.50" in answer or "127" in answer
    print(f"  Agent response: {answer[:200]}")
    print(f"\n  [{'CORRECT' if has_amount else 'LOST'}] Specific refund amount $127.50 referenced in response")


def main():
    print("=" * 60)
    print("EXERCISE 3 -- Context Degradation & Memory Patterns (5.4, 5.5)")
    print("=" * 60)

    part_a_statelessness()
    part_b_context_degradation()
    part_c_scratchpad()
    part_d_case_facts()

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 5.4 / 5.5")
    print("=" * 60)
    print("""
Context degradation (5.4):
  Symptom: agent uses "typical patterns" instead of specific findings from earlier
  Fix: scratchpad files — agent writes discoveries, reads them at phase boundaries
  Also: /compact to reclaim token budget during long sessions
  Wrong: add more instructions to an overloaded context
  Wrong: max_tokens lower — max_tokens controls OUTPUT length, not SESSION size

Conversation memory / API statelessness (5.5):
  Claude API is STATELESS — no session_id, no automatic memory
  Every request must include the FULL messages array
  50+ turn sessions: every request re-sends all history -> linear cost growth

Hybrid context management for long sessions:
  1. Summarize older messages
  2. Keep recent turns verbatim
  3. Persistent case-facts block (OUTSIDE summarized history)

Case-facts block:
  Contains: transactional facts (amounts, dates, order IDs, status)
  Maintained by: YOUR application code (deterministic, not summarization)
  Survives: conversation compaction, summarization, context rollover
  Wrong: "raise summarization threshold" (delays but doesn't prevent loss)
  Wrong: "instruct Claude to preserve numbers" (probabilistic)

Auto memory (Claude Code specific):
  Location: ~/.claude/projects/<project>/memory/MEMORY.md
  NOT at: .claude/memory/ (that would be project-level, version-controlled)
  First 200 lines or 25KB loaded automatically at session start
""")


if __name__ == "__main__":
    main()
