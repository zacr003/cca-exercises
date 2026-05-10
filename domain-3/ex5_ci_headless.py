"""
CCA-F Domain 3, Exercise 5 — CI/CD and Headless Mode (Subdomain 3.6)
=====================================================================

WHAT THIS EXERCISES:
  - The -p / --print flag: makes Claude Code non-interactive (required for CI/CD)
  - --output-format json: machine-parseable output for automated pipelines
  - Why --bare strips all auto-discovery (hooks, skills, MCP, CLAUDE.md)
  - Independent review instance: why you shouldn't review with the same session that generated
  - Why CI-invoked Claude Code reads the same CLAUDE.md (document test standards there!)

HOW TO RUN:
  python domain-3/ex5_ci_headless.py

  This script calls `claude -p` as a subprocess to demonstrate headless mode.
  It does NOT require the Anthropic Python SDK directly — it shells out to Claude Code.

EXAM PATTERNS:
  CORRECT  -- claude -p "prompt"            (non-interactive, required for CI)
  CORRECT  -- claude -p --output-format json (machine-parseable output)
  CORRECT  -- Use --bare for stripped, reproducible CI execution
  WRONG    -- CLAUDE_HEADLESS=true           (does not exist)
  WRONG    -- --batch flag                   (does not exist)
  WRONG    -- --no-config flag               (does not exist)
  WRONG    -- Docker automatically isolates config (it doesn't — use --bare for that)
"""

import subprocess
import json
import sys

# =====================================================================
# PART A: THE -p FLAG — Non-Interactive Mode
# =====================================================================
# Without -p, Claude Code waits for interactive input. In a CI pipeline,
# there is no human to type. The pipeline hangs indefinitely.
#
# With -p (or --print), Claude Code:
#   - Runs the prompt non-interactively
#   - Prints the result to stdout
#   - Exits when done
#
# This is the ONLY way to use Claude Code in automated pipelines.

def demo_headless_mode():
    """
    Runs a simple Claude Code prompt in headless mode using -p.
    This is what a CI pipeline does to invoke Claude Code.
    """
    print("\n" + "=" * 60)
    print("PART A: Headless Mode (-p flag)")
    print("=" * 60)
    print("Running: claude -p 'What is 2 + 2? Answer in one word.'")
    print("(This is non-interactive — no human input required)\n")

    try:
        result = subprocess.run(
            ["claude", "-p", "What is 2 + 2? Answer in one word."],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"Output: {result.stdout.strip()}")
            print("\n[CORRECT] -p flag enables non-interactive execution for CI pipelines")
        else:
            print(f"Error (exit {result.returncode}): {result.stderr.strip()}")
            print("Note: Make sure claude CLI is installed and authenticated")
    except FileNotFoundError:
        print("NOTE: 'claude' CLI not found in PATH.")
        print("Install Claude Code CLI and re-run this exercise.")
        print("\nThe concept: claude -p 'prompt' runs non-interactively.")
        print("Without -p, Claude Code waits for input and the pipeline hangs.")


# =====================================================================
# PART B: --output-format json — Machine-Parseable Output
# =====================================================================
# For CI pipelines that need to POST results as PR comments or write to
# structured logs, plain text is unreliable (you'd have to parse prose).
#
# --output-format json wraps the response in a structured field:
#   { "result": "...", "is_error": false, ... }
#
# Combined with --json-schema, you can also enforce output schemas.

def demo_json_output():
    """
    Demonstrates --output-format json for machine-parseable CI output.
    """
    print("\n" + "=" * 60)
    print("PART B: JSON Output (--output-format json)")
    print("=" * 60)
    print("Running: claude -p --output-format json 'List 3 Python best practices. JSON array only.'\n")

    try:
        result = subprocess.run(
            [
                "claude", "-p",
                "--output-format", "json",
                "List exactly 3 Python best practices as a JSON array of strings. Return only the JSON array, nothing else."
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"Raw stdout:\n{result.stdout.strip()}\n")
            # The outer envelope from --output-format json
            try:
                envelope = json.loads(result.stdout)
                print(f"Parsed envelope type: {type(envelope)}")
                if isinstance(envelope, dict):
                    print(f"Result field: {envelope.get('result', envelope)}")
            except json.JSONDecodeError:
                print("(Output is plain text — JSON parsing depends on the response format)")
            print("\n[CORRECT] Use --output-format json when a pipeline needs to parse the output")
        else:
            print(f"Error: {result.stderr.strip()}")
    except FileNotFoundError:
        print("NOTE: 'claude' CLI not found. Conceptual demo only.")
        print("\nThe concept:")
        print("  claude -p --output-format json 'prompt'")
        print("  → wraps response in structured JSON envelope")
        print("  → CI pipeline can reliably parse the result field")
        print("  → compare: plain text output requires fragile string parsing")


# =====================================================================
# PART C: --bare Flag — Stripped Execution
# =====================================================================
# By default, Claude Code auto-discovers: CLAUDE.md files, hooks,
# skills, MCP servers, and plugins.
#
# --bare strips ALL of that. Use it when you need:
#   - Truly reproducible CI execution (no local config bleeds in)
#   - Performance (skip discovery overhead)
#   - Isolation (test without any local customization)
#
# EXAM TRAP: "Docker containers automatically isolate Claude Code config"
# → WRONG. Docker still auto-discovers config inside the container.
# → Use --bare for truly stripped execution in Docker.

def explain_bare_flag():
    """
    Explains --bare vs default behavior. Conceptual — no API call needed.
    """
    print("\n" + "=" * 60)
    print("PART C: --bare Flag (Stripped Execution)")
    print("=" * 60)
    print("""
Without --bare (default):
  claude -p "Review this code"
  → Loads CLAUDE.md files
  → Discovers and runs hooks (PreToolUse, PostToolUse)
  → Loads skills from .claude/skills/
  → Connects MCP servers from .mcp.json
  → Applies all local configuration

With --bare:
  claude --bare -p "Review this code"
  → Skips CLAUDE.md files
  → Skips hooks
  → Skips skills and plugins
  → Skips MCP server connections
  → Sets CLAUDE_CODE_SIMPLE environment variable
  → Clean, reproducible execution

When to use --bare:
  - CI pipelines where local developer config should NOT bleed in
  - Performance-sensitive headless runs
  - Testing the model without any configuration layer

EXAM TRAP:
  "Docker containers isolate Claude Code from local config"
  → WRONG. Docker still auto-discovers config inside the container.
  → Use --bare explicitly for stripped execution.
  → --bare is not just "quiet mode" — it actively skips skills, hooks, MCP, CLAUDE.md.
""")


# =====================================================================
# PART D: Independent Review Instance
# =====================================================================
# A CI pipeline that generates code and then reviews it with the SAME
# session is flawed. The model retains its reasoning context from
# generation — it's less likely to question its own decisions.
#
# The fix: use a separate, fresh Claude invocation for review.
#
# This is also why you document testing standards in CLAUDE.md:
# CI-invoked Claude Code reads the SAME project CLAUDE.md, so your
# CI review follows the same standards as interactive development.

def explain_review_instance():
    """
    Explains the independent review instance pattern.
    """
    print("\n" + "=" * 60)
    print("PART D: Independent Review Instance")
    print("=" * 60)
    print("""
WRONG pattern (same session):
  Step 1: claude -p "Generate tests for this function"  → generates tests
  Step 2: (same session, same context) "Now review the tests you just wrote"
  → The model knows WHY it made each decision — it defends its own choices
  → Self-review bias: the reviewer and generator share the same reasoning context

CORRECT pattern (independent instance):
  Step 1: claude -p "Generate tests for this function"  → saves output to file
  Step 2: claude -p "Review these tests for correctness" < tests.py  (fresh invocation)
  → The reviewer has NO context from the generation step
  → An independent instance catches subtle issues the generator rationalized away

This is tested on the exam as "multi-instance review architectures" (Domain 4.6).
The principle applies equally in CI/CD contexts (Domain 3.6).

CLAUDE.md for CI:
  CI-invoked Claude Code reads the SAME project .claude/CLAUDE.md as interactive use.
  This means: document your testing standards, fixtures, and review criteria in CLAUDE.md.
  Your CI review will automatically follow the same quality bar as your interactive work.
  No need to duplicate instructions in CI scripts — CLAUDE.md is shared.
""")


# =====================================================================
# EXAM DISTINCTION SUMMARY
# =====================================================================

def print_exam_summary():
    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 3.6")
    print("=" * 60)
    print("""
Flags and what they do:
  -p / --print       Non-interactive mode — REQUIRED for CI pipelines
  --output-format json  Machine-parseable output — use when pipeline parses output
  --bare             Skips ALL auto-discovery: hooks, skills, MCP, CLAUDE.md
  --append-system-prompt  Appends text to the system prompt for that invocation only (ephemeral)

Settings precedence (highest → lowest):
  1. .claude/settings.local.json    (local overrides, usually gitignored)
  2. .claude/settings.json          (project settings, version-controlled)
  3. ~/.claude/settings.json        (user settings)

Flags that do NOT exist (exam distractors):
  CLAUDE_HEADLESS=true   → does not exist; use -p
  --batch                → does not exist; use -p
  --no-config            → does not exist; use --bare
  --skip-config          → does not exist; use --bare
  --security-only        → does not exist
  --auto-test            → does not exist

Key distinctions:
  -p flag         = non-interactive execution
  --bare          = stripped execution (skips everything, including -p's CLAUDE.md loading)
  Docker          = does NOT isolate config; still auto-discovers
  Independent instance = separate invocation for review; solves self-review bias
  CLAUDE.md for CI = CI reads the same CLAUDE.md; document standards there
""")


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    demo_headless_mode()
    demo_json_output()
    explain_bare_flag()
    explain_review_instance()
    print_exam_summary()
