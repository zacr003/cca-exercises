"""
Domain 1 Exercise 5 — Task Decomposition Strategies
====================================================
CCA-F Exam Focus (Subdomain 1.6):
  - Prompt chaining (fixed sequential pipeline): predefined steps, each output feeds the next
    → Use when the steps are KNOWN upfront
  - Dynamic adaptive decomposition: subtasks generated from what is discovered at each step
    → Use when the scope is UNKNOWN upfront (open-ended investigation)
  - Large reviews: per-file LOCAL pass + separate CROSS-FILE integration pass
    → Local pass catches: SQL injection, null checks, unused imports, off-by-one (per-file issues)
    → Cross-file pass catches: inconsistent API contracts, authorization gaps spanning services
  - Single-pass on all files = attention dilution, inconsistent depth, missed bugs
  - Coordinator instructions should specify GOALS + quality criteria, NOT step-by-step procedures

Scenario: A code review agent reviewing a three-file Python codebase.
Both decomposition strategies are demonstrated and contrasted.
"""

import anthropic
import json

client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Fake codebase — three files with deliberate local AND cross-file issues
#
# Local issues (caught per-file):
#   - user_service.py: SQL injection in get_user and update_role
#   - order_service.py: missing null/bounds check before index access
#
# Cross-file issues (only visible across files):
#   - api_gateway.py calls order_svc.get_orders(order_id) — wrong arg (should be user_id)
#   - api_gateway.py: no authorization check before cancel_order or update_role
#   - Both of these are invisible if you review each file in isolation
# ---------------------------------------------------------------------------

FAKE_FILES = {
    "user_service.py": """\
class UserService:
    def get_user(self, user_id):
        # BUG (local): SQL injection — user_id interpolated directly
        return db.query(f"SELECT * FROM users WHERE id = {user_id}")

    def update_role(self, user_id, new_role):
        # BUG (local): no validation on new_role; SQL injection risk
        db.execute(f"UPDATE users SET role = '{new_role}' WHERE id = {user_id}")
        return True
""",
    "order_service.py": """\
class OrderService:
    def get_orders(self, user_id):
        # Returns list of order dicts: [{id, user_id, amount, status}]
        return db.query(f"SELECT * FROM orders WHERE user_id = {user_id}")

    def cancel_order(self, order_id):
        # BUG (local): order[0] will throw if no orders found — no bounds check
        # BUG (cross-file): no check that order belongs to the requesting user
        order = self.get_orders(order_id)
        if order[0]['status'] != 'pending':
            raise ValueError("Can only cancel pending orders")
        db.execute(f"UPDATE orders SET status = 'cancelled' WHERE id = {order_id}")
""",
    "api_gateway.py": """\
from user_service import UserService
from order_service import OrderService

user_svc = UserService()
order_svc = OrderService()

def handle_request(endpoint, user_id, params):
    if endpoint == '/orders':
        # BUG (cross-file): passes order_id but get_orders expects user_id
        return order_svc.get_orders(int(params.get('order_id')))
    elif endpoint == '/cancel':
        # BUG (cross-file): no authorization — any user can cancel any order
        return order_svc.cancel_order(params['order_id'])
    elif endpoint == '/role':
        # BUG (cross-file): no admin check — any user can escalate their own role
        return user_svc.update_role(user_id, params['role'])
""",
}


# ---------------------------------------------------------------------------
# STRATEGY 1: Prompt Chaining (fixed sequential pipeline)
#
# Step 1 → Step 2 → Step 3 (each output feeds the next)
# Steps are KNOWN before we start — this is the defining characteristic.
# Appropriate for predictable, structured reviews like this one.
#
# ANTI-PATTERN: single pass on all three files at once.
# Why it fails: attention dilutes across files, local+cross-file concerns
# blur together, and the model produces inconsistent depth across files.
# ---------------------------------------------------------------------------

def review_with_prompt_chaining() -> dict:
    """
    Fixed three-step pipeline:
      Step 1 — Per-file local analysis (run on each file; parallel in a real system)
      Step 2 — Cross-file integration pass (depends on Step 1 output)
      Step 3 — Final severity ranking (depends on Steps 1 + 2)
    """
    print("\n" + "=" * 60)
    print("STRATEGY 1: Prompt Chaining (fixed sequential pipeline)")
    print("Steps are known upfront: per-file -> cross-file -> ranking")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 1: Per-file LOCAL analysis
    # Each file reviewed independently. Only local issues in scope.
    # In production: dispatch these in parallel (ThreadPoolExecutor / multiple Task calls).
    # ------------------------------------------------------------------
    print("\n[Step 1] Per-file local analysis (sequential here, parallel in production)")
    per_file_results: dict[str, str] = {}

    for filename, code in FAKE_FILES.items():
        print(f"  Analyzing {filename}...")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=(
                "You are a code reviewer focused exclusively on LOCAL issues within a single file. "
                "Check for: SQL injection, missing input validation, null/index errors, unused imports. "
                "Do NOT comment on cross-file API contracts or authorization — those are out of scope here. "
                "Return valid JSON only: "
                '{"file": "<filename>", "local_issues": [{"line_hint": "<code snippet>", '
                '"issue": "<description>", "severity": "high"|"medium"|"low"}]}'
            ),
            messages=[{
                "role": "user",
                "content": f"Review for local issues only:\n\nFile: {filename}\n```python\n{code}\n```",
            }],
        )
        per_file_results[filename] = response.content[0].text
        print(f"    Done.")

    # ------------------------------------------------------------------
    # Step 2: CROSS-FILE integration pass
    # Receives Step 1 output + full source. Only cross-file concerns in scope.
    # This step would be meaningless without Step 1's scoped context first.
    # ------------------------------------------------------------------
    print("\n[Step 2] Cross-file integration pass (depends on Step 1 output)")

    integration_context = json.dumps({
        "per_file_findings": per_file_results,
        "full_source": FAKE_FILES,
    }, indent=2)

    integration_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=(
            "You are a code reviewer focused exclusively on CROSS-FILE integration issues. "
            "You receive per-file local findings and the full source. "
            "Check for: inconsistent API contracts between files, authorization gaps that span services, "
            "data model mismatches, violated invariants across services. "
            "Do NOT repeat local issues already captured. "
            "Return valid JSON only: "
            '{"integration_issues": [{"files_involved": ["<file>"], '
            '"issue": "<description>", "severity": "high"|"medium"|"low"}]}'
        ),
        messages=[{
            "role": "user",
            "content": f"Find cross-file integration issues:\n{integration_context}",
        }],
    )

    integration_results = integration_response.content[0].text
    print("  Done.")

    # ------------------------------------------------------------------
    # Step 3: Final severity ranking
    # Consumes both Step 1 and Step 2 outputs — synthesizes a prioritized list.
    # ------------------------------------------------------------------
    print("\n[Step 3] Final severity ranking (depends on Steps 1 + 2)")

    ranking_context = json.dumps({
        "local_findings": per_file_results,
        "integration_findings": integration_results,
    }, indent=2)

    ranking_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=(
            "You receive local and cross-file code review findings. "
            "Produce the top 5 issues to fix, ranked by severity and exploitability. "
            "Return valid JSON only: "
            '{"top_issues": [{"rank": <int>, "issue": "<description>", '
            '"severity": "high"|"medium"|"low", "files": ["<file>"]}]}'
        ),
        messages=[{
            "role": "user",
            "content": f"Rank these findings:\n{ranking_context}",
        }],
    )

    print("  Done.")
    return {
        "strategy": "prompt_chaining",
        "per_file": per_file_results,
        "integration": integration_results,
        "ranking": ranking_response.content[0].text,
    }


# ---------------------------------------------------------------------------
# STRATEGY 2: Dynamic Adaptive Decomposition
#
# Subtasks are GENERATED based on what is discovered at each step.
# Steps are NOT known upfront — this is the defining characteristic.
# Appropriate for open-ended investigations (security audits, incident triage)
# where the scope expands or contracts based on findings.
#
# EXAM TRAP: Using adaptive decomposition for a structured, predictable task
# adds unnecessary complexity. And using prompt chaining for an open-ended task
# means you might miss scope that wasn't anticipated at design time.
# ---------------------------------------------------------------------------

def review_with_adaptive_decomposition(investigation_goal: str) -> dict:
    """
    Adaptive three-step pattern:
      Step 1 — Triage: identify highest-risk areas (drives everything downstream)
      Step 2 — Generate targeted subtasks from triage findings (adaptive — not predefined)
      Step 3 — Execute the adaptively-generated subtasks
    """
    print("\n" + "=" * 60)
    print("STRATEGY 2: Dynamic Adaptive Decomposition")
    print("Subtasks are GENERATED from findings — scope is discovered, not predefined")
    print("=" * 60)
    print(f"\nInvestigation goal: {investigation_goal}")

    # ------------------------------------------------------------------
    # Step 1: Triage — determine the highest-risk areas
    # The output of this step determines what subtasks exist in Step 2.
    # This is what makes it "adaptive" — you cannot write Step 2 until Step 1 runs.
    # ------------------------------------------------------------------
    print("\n[Step 1] Triage — identifying highest-risk investigation areas")

    triage_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=(
            "You are a security triage specialist. Given a codebase description and investigation goal, "
            "identify the 2-3 highest-risk areas to focus on. "
            "Return valid JSON only: "
            '{"priority_areas": [{"area": "<name>", "reason": "<why risky>", "files": ["<file>"]}]}'
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Investigation goal: {investigation_goal}\n\n"
                "Files available:\n"
                "- user_service.py: manages users and role assignment\n"
                "- order_service.py: manages orders and cancellations\n"
                "- api_gateway.py: routes all external requests, handles authorization\n"
            ),
        }],
    )

    triage_result = triage_response.content[0].text
    print(f"  Triage findings: {triage_result[:300]}...")

    # ------------------------------------------------------------------
    # Step 2: Generate subtasks from triage output
    # These subtasks could NOT have been written before Step 1 ran.
    # In a full system, each subtask result might generate further subtasks (recursive).
    # ------------------------------------------------------------------
    print("\n[Step 2] Generating targeted subtasks from triage findings")

    subtask_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=(
            "Based on security triage findings, generate specific, testable investigation subtasks. "
            "Each subtask should be narrowly scoped. "
            "Return valid JSON only: "
            '{"subtasks": [{"task_id": <int>, "task": "<description>", '
            '"target_file": "<file>", "what_to_check": "<specific check>"}]}'
        ),
        messages=[{
            "role": "user",
            "content": f"Generate investigation subtasks from this triage:\n{triage_result}",
        }],
    )

    subtasks_text = subtask_response.content[0].text
    print(f"  Generated subtasks: {subtasks_text[:300]}...")

    # ------------------------------------------------------------------
    # Step 3: Execute adaptively-generated subtasks
    # The subtasks fed here were unknown before Step 1.
    # ------------------------------------------------------------------
    print("\n[Step 3] Executing adaptive subtasks against source code")

    execution_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=(
            "You are a security analyst. Execute the given investigation subtasks against the provided source code. "
            "For each subtask: describe what you found and rate severity. "
            "Return valid JSON only: "
            '{"findings": [{"task_id": <int>, "subtask": "<task>", '
            '"finding": "<what was found>", "severity": "high"|"medium"|"low"|"none"}]}'
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Execute these subtasks:\n{subtasks_text}\n\n"
                f"Source code:\n{json.dumps(FAKE_FILES, indent=2)}"
            ),
        }],
    )

    print("  Done.")
    return {
        "strategy": "adaptive_decomposition",
        "triage": triage_result,
        "subtasks": subtasks_text,
        "findings": execution_response.content[0].text,
    }


# ---------------------------------------------------------------------------
# Run both strategies and print the exam distinction
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # Strategy 1: Prompt chaining — structured, predictable code review
    chaining_result = review_with_prompt_chaining()
    print(f"\n[Prompt chaining] Final ranking:\n{chaining_result['ranking']}")

    # Strategy 2: Adaptive decomposition — open-ended security investigation
    adaptive_result = review_with_adaptive_decomposition(
        "open-ended security audit — find authorization bypass and injection vulnerabilities"
    )
    print(f"\n[Adaptive] Final findings:\n{adaptive_result['findings']}")

    # -----------------------------------------------------------------------
    # Exam distinction summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY")
    print("=" * 60)
    print("""
Prompt chaining (Strategy 1):
  - Steps are KNOWN before execution starts
  - Each step's output explicitly feeds the next
  - Per-file LOCAL pass -> cross-file INTEGRATION pass -> ranking
  - Use for: predictable multi-aspect reviews, structured pipelines
  - Exam phrase: "fixed sequential pipeline"

Dynamic adaptive decomposition (Strategy 2):
  - Steps are GENERATED from what is discovered
  - Triage findings determine which subtasks exist
  - Use for: open-ended investigation, unknown scope upfront
  - Exam phrase: "generate subtasks based on what is discovered at each step"

Single-pass on all files (ANTI-PATTERN — do not do this):
  - Attention dilutes across 14+ files
  - Local and cross-file issues blend together
  - Inconsistent review depth, missed bugs, contradictory feedback
  - Fix: split into per-file pass + separate cross-file integration pass
""")
