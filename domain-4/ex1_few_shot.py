"""
CCA-F Domain 4, Exercise 1 — Few-Shot Prompting (Subdomains 4.1, 4.2)
======================================================================

WHAT THIS EXERCISES:
  When detailed instructions alone produce inconsistent results, the fix is
  concrete few-shot examples — NOT stronger instructions.

  Two key concepts tested together here:
    4.1 -- Explicit criteria over vague instructions (fix false positives)
    4.2 -- Few-shot examples as the most effective disambiguation technique

KEY RULES:
  - 2-4 TARGETED contrastive examples > 10-15 unambiguous typical examples
  - Examples must show reasoning for WHY one choice was made over an alternative
  - Grouping examples by tool/category does NOT teach discrimination
  - Contrastive and adjacent examples DO teach discrimination
  - "Be more conservative" is a vague instruction that does not move classification
  - Explicit criteria with examples = the correct fix

STRUCTURE:
  Part A -- Vague instruction: inconsistent severity classification
  Part B -- Explicit criteria only: better but still misses edge cases
  Part C -- Explicit criteria + few-shot examples: consistent and accurate
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
# TEST CASES: Code snippets for classification
# Each has an expected severity for comparison
# =====================================================================

CODE_SAMPLES = [
    {
        "code": "user_input = request.args.get('id')\nquery = f'SELECT * FROM users WHERE id = {user_input}'",
        "expected": "CRITICAL",
        "why": "SQL injection vulnerability — user input directly in query string"
    },
    {
        "code": "x = 1\ny = 2\nresult = x + y  # adds two numbers",
        "expected": "OK",
        "why": "Comment accurately describes code behavior"
    },
    {
        "code": "def calculate_total(items):\n    # Returns the average\n    return sum(item.price for item in items)",
        "expected": "HIGH",
        "why": "Comment says 'average' but code returns sum — misleading"
    },
    {
        "code": "password = 'admin123'  # temporary password",
        "expected": "CRITICAL",
        "why": "Hardcoded credential in source code"
    },
    {
        "code": "# TODO: add error handling\nresult = int(user_input)",
        "expected": "MEDIUM",
        "why": "Missing error handling acknowledged but not yet added"
    },
]


# =====================================================================
# PART A: VAGUE INSTRUCTION (problem — inconsistent output)
# =====================================================================

VAGUE_SYSTEM = """You are a code review tool. Review the code snippet and classify any issues.

Be conservative and only flag high-confidence issues.
Severity levels: CRITICAL, HIGH, MEDIUM, LOW, OK

Return JSON: {"severity": "...", "issue": "..."}"""

# =====================================================================
# PART B: EXPLICIT CRITERIA (better — but still misses edge cases)
# =====================================================================

EXPLICIT_CRITERIA_SYSTEM = """You are a code review tool. Classify code issues using these EXACT criteria:

CRITICAL: Flag when ANY of these are present:
  - User input directly concatenated into SQL queries (SQL injection)
  - Credentials, passwords, or API keys hardcoded as string literals
  - Authentication or authorization completely missing for sensitive operations

HIGH: Flag when:
  - A comment describes different behavior than what the code actually does
  - Error handling is absent for operations that will fail on invalid input

MEDIUM: Flag when:
  - A TODO comment notes a known missing feature that affects correctness
  - A variable name is actively misleading about what it holds

OK: Return when none of the above apply.

Return JSON: {"severity": "CRITICAL|HIGH|MEDIUM|LOW|OK", "issue": "one sentence description or 'No issue'"}"""

# =====================================================================
# PART C: EXPLICIT CRITERIA + FEW-SHOT EXAMPLES (correct approach)
# =====================================================================
# The few-shot examples are CONTRASTIVE:
#   - They show ambiguous cases and WHY the decision was made
#   - They are adjacent (not grouped by category)
#   - They demonstrate the exact reasoning needed for edge cases

FEW_SHOT_SYSTEM = """You are a code review tool. Classify code issues using these criteria:

CRITICAL: SQL injection, hardcoded credentials, missing auth on sensitive ops
HIGH: Comment contradicts actual code behavior
MEDIUM: TODO noting a known correctness gap
OK: No issue

EXAMPLES (study these carefully — they show how to handle ambiguous cases):

Example 1:
Code: name = request.form['name']
      print(f"Hello, {name}")
Severity: OK
Reasoning: User input is used only for display output — no database query, no security operation.
This looks suspicious but is actually safe in this context.

Example 2:
Code: user_id = request.args.get('id')
      result = db.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
Severity: CRITICAL
Reasoning: User input is DIRECTLY concatenated into a SQL string — classic SQL injection.
The difference from Example 1: this goes into a database query, not just display.

Example 3:
Code: def get_items():
      # Returns sorted items
      return items  # items is already unsorted
Severity: HIGH
Reasoning: Comment claims behavior (sorted) that the code does not deliver.
This is the comment-contradicts-code pattern.

Example 4:
Code: def get_items():
      # Returns items
      return sorted_items
Severity: OK
Reasoning: Even though variable name has 'sorted' prefix, the comment accurately
describes what is returned. No contradiction.

Example 5:
Code: # TODO: validate email format
      user.email = email_input
Severity: MEDIUM
Reasoning: Developer acknowledged the gap (TODO) but hasn't fixed it yet.
The missing validation affects correctness, but the intent is documented.

Return JSON: {"severity": "CRITICAL|HIGH|MEDIUM|OK", "issue": "one sentence or 'No issue'"}"""


# =====================================================================
# RUNNER
# =====================================================================

def classify_code(code: str, system_prompt: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Review this code:\n\n```\n{code}\n```"}]
    )
    text = response.content[0].text.strip()
    # Try to extract JSON from the response
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except json.JSONDecodeError:
        pass
    return {"severity": "PARSE_ERROR", "issue": text[:100]}


def run_classification_test(system_prompt: str, label: str):
    print(f"\n--- {label} ---")
    correct = 0
    for sample in CODE_SAMPLES:
        result = classify_code(sample["code"], system_prompt)
        severity = result.get("severity", "?")
        match = "OK" if severity == sample["expected"] else "MISS"
        if match == "OK":
            correct += 1
        # Truncate code for display
        code_preview = sample["code"].replace("\n", " | ")[:60]
        print(f"  [{match}] Expected={sample['expected']:8s} Got={severity:8s} | {code_preview}")
    print(f"  Score: {correct}/{len(CODE_SAMPLES)}")
    return correct


def main():
    print("=" * 60)
    print("EXERCISE 1 -- Few-Shot Prompting (4.1, 4.2)")
    print("=" * 60)
    print("Same 5 code snippets classified with three different prompts.")
    print("Watch how accuracy changes.\n")

    score_a = run_classification_test(VAGUE_SYSTEM, "PART A: Vague instruction ('be conservative')")
    score_b = run_classification_test(EXPLICIT_CRITERIA_SYSTEM, "PART B: Explicit criteria only")
    score_c = run_classification_test(FEW_SHOT_SYSTEM, "PART C: Explicit criteria + few-shot examples")

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 4.1 / 4.2")
    print("=" * 60)
    print(f"""
Scores:
  Part A (vague):          {score_a}/{len(CODE_SAMPLES)}
  Part B (explicit only):  {score_b}/{len(CODE_SAMPLES)}
  Part C (criteria + examples): {score_c}/{len(CODE_SAMPLES)}

Key rules:
  WRONG  "Be more conservative" -- vague; model has no concrete definition
  WRONG  "Only report high-confidence issues" -- vague; 'high-confidence' is undefined
  WRONG  10-15 unambiguous typical examples -- targets easy cases, not the edge cases causing errors
  WRONG  Grouped examples (all CRITICALs, then all HIGHs) -- doesn't teach discrimination between similar cases
  CORRECT Explicit categorical criteria -- defines the boundary
  CORRECT 2-4 targeted contrastive examples -- show reasoning for ambiguous edge cases

The contrastive pattern (Examples 1 & 2 above):
  Show two similar-looking cases that get DIFFERENT classifications, and explain WHY.
  This teaches the model what the boundary IS, not just what "typical" looks like.

High false positive rates in one category (e.g., 'comment accuracy'):
  CORRECT: Temporarily DISABLE that category while improving its criteria
  WRONG:   Apply uniform strictness reduction (penalizes accurate categories too)
  WRONG:   Switch to a more capable model (doesn't fix the prompt quality issue)
""")


if __name__ == "__main__":
    main()
