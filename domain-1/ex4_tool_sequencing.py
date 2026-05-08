"""
Domain 1 Exercise 4 — Tool Sequencing and Programmatic Prerequisites
=====================================================================
CCA-F Exam Focus (Subdomain 1.4):
  - Prompt instructions alone have non-zero failure rate for hard compliance
  - Programmatic prerequisites: block downstream tools until prerequisite returns verified result
  - Model-driven tool selection (good descriptions) preferred over routing layers / keyword classifiers
  - For complex multi-concern requests: decompose, investigate in parallel, synthesize

Scenario: A financial operations agent that MUST verify customer identity before
processing any refund. Two enforcement approaches are compared:
  A) Prompt-only instruction (soft — probabilistic, can be skipped)
  B) Programmatic gate in the tool itself (hard — deterministic, always enforced)
"""

import anthropic
import json

client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# State tracking — the programmatic prerequisite mechanism
#
# In production: a session store or database record.
# In Claude Code hooks: a temp state file (see ex3_hooks.md Exercise C).
# Here: in-memory flag that persists across tool calls within one agent run.
# ---------------------------------------------------------------------------

class AgentState:
    def __init__(self):
        self.customer_verified = False
        self.verified_customer_id = None

    def reset(self):
        self.customer_verified = False
        self.verified_customer_id = None

state = AgentState()


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def verify_customer(customer_id: str) -> dict:
    """
    Identity verification — must succeed before financial ops are allowed.
    On success, writes to the shared state object (the programmatic prerequisite).
    """
    known_customers = {
        "C-001": {"name": "Alice Johnson", "status": "verified"},
        "C-002": {"name": "Bob Smith",    "status": "flagged"},
        "C-999": {"name": "Unknown",      "status": "not_found"},
    }
    result = known_customers.get(customer_id, {"status": "not_found"})

    # PROGRAMMATIC PREREQUISITE: update shared state on a successful verification.
    # This is the write side of the gate — process_refund reads it.
    if result.get("status") == "verified":
        state.customer_verified = True
        state.verified_customer_id = customer_id
        result["verified"] = True
    else:
        state.customer_verified = False
        state.verified_customer_id = None
        result["verified"] = False

    return result


def process_refund(customer_id: str, amount: float, reason: str) -> dict:
    """
    Issue a refund.

    EXAM PATTERN: The gate is enforced HERE (inside the tool), not only in the
    system prompt. Even if the model ignores the system prompt instruction, this
    check always runs. Prompt instructions = probabilistic. Tool-level gate = deterministic.
    """
    # Read side of the programmatic prerequisite gate
    if not state.customer_verified:
        return {
            "success": False,
            "blocked_by": "prerequisite_gate",
            "error": (
                "PREREQUISITE NOT MET: Customer identity must be verified before processing a refund. "
                "Call verify_customer first and ensure status == 'verified'."
            ),
        }

    if state.verified_customer_id != customer_id:
        return {
            "success": False,
            "blocked_by": "prerequisite_gate",
            "error": (
                f"Customer ID mismatch: verified customer is {state.verified_customer_id}, "
                f"not {customer_id}."
            ),
        }

    if amount > 1000:
        return {
            "success": False,
            "error": "Refund exceeds $1,000 limit — requires manager approval.",
        }

    return {
        "success": True,
        "refund_id": f"REF-{customer_id}-{int(amount)}",
        "customer_id": customer_id,
        "amount": amount,
        "reason": reason,
    }


def get_account_balance(customer_id: str) -> dict:
    """
    Look up account balance.

    NOTE: This tool does NOT require identity verification — it is read-only.
    Model-driven tool selection means the model picks this vs. process_refund
    based on intent, guided by the tool descriptions below.
    Good descriptions eliminate the need for a routing classifier.
    """
    balances = {
        "C-001": {"balance": 2450.00, "currency": "USD"},
        "C-002": {"balance": 150.00,  "currency": "USD"},
    }
    return balances.get(customer_id, {"error": "Account not found"})


TOOLS = {
    "verify_customer":   verify_customer,
    "process_refund":    process_refund,
    "get_account_balance": get_account_balance,
}


# ---------------------------------------------------------------------------
# Tool definitions
#
# EXAM PATTERN: Tool descriptions are what guide model-driven tool selection.
# Clear, distinct descriptions eliminate the need for a routing layer or
# keyword classifier in front of the agent. If you find yourself adding a
# pre-processing classifier, fix the tool descriptions instead.
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "verify_customer",
        "description": (
            "Verify a customer's identity before any financial transaction. "
            "Must be called first, and must return verified=true, before process_refund can succeed. "
            "Use for: refunds, account changes, any sensitive financial operation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID, e.g. C-001",
                }
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "process_refund",
        "description": (
            "Process a refund for a verified customer. "
            "Requires prior successful verify_customer call — will fail with an error if identity is unverified. "
            "Maximum refund: $1,000 USD. For larger amounts, escalate to a manager."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "amount":      {"type": "number", "description": "Refund amount in USD"},
                "reason":      {"type": "string", "description": "Reason for the refund"},
            },
            "required": ["customer_id", "amount", "reason"],
        },
    },
    {
        "name": "get_account_balance",
        "description": (
            "Look up the account balance for a customer. "
            "Does NOT require prior identity verification — safe for read-only inquiries."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
            },
            "required": ["customer_id"],
        },
    },
]


# ---------------------------------------------------------------------------
# Agentic loop (same pattern as ex1)
# ---------------------------------------------------------------------------

def run_agent(user_message: str, label: str = "") -> str:
    messages = [{"role": "user", "content": user_message}]

    system = (
        "You are a financial support agent. "
        "When a customer requests a refund, always verify their identity first via verify_customer. "
        # NOTE: This instruction is the SOFT layer (probabilistic).
        # process_refund enforces the prerequisite programmatically (deterministic).
        # Hard compliance requires both — the tool gate is the safety net.
    )

    print(f"\n{'=' * 60}")
    print(f"TEST: {label}")
    print(f"User: {user_message}")
    print("=" * 60)

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=system,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        stop_reason = response.stop_reason
        print(f"[loop] stop_reason = {stop_reason!r}")

        messages.append({"role": "assistant", "content": response.content})

        if stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")), ""
            )
            print(f"\nAgent: {final_text}")
            return final_text

        if stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            print(f"[loop] Executing {len(tool_use_blocks)} tool(s): {[b.name for b in tool_use_blocks]}")

            tool_results = []
            for block in tool_use_blocks:
                result = TOOLS[block.name](**block.input)
                print(f"  [{block.name}] input={block.input}")
                print(f"           result={result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "user", "content": tool_results})


# ---------------------------------------------------------------------------
# Run the tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # Test 1: Happy path — model selects verify_customer → process_refund (correct sequence)
    state.reset()
    run_agent(
        "I need a $200 refund for customer C-001. Their order arrived broken.",
        label="Happy path — verify then refund",
    )

    # Test 2: Programmatic gate demonstration
    # Even without the model, process_refund blocks if called without verification.
    # This is the key exam point: prompt instructions alone are insufficient.
    print(f"\n{'=' * 60}")
    print("TEST: Direct programmatic gate — bypassing the model entirely")
    print("=" * 60)
    state.reset()  # No verification has occurred
    print("[direct] Calling process_refund without prior verify_customer:")
    blocked = process_refund("C-001", 200.0, "bypass attempt")
    print(f"  Result: {blocked}")
    print(
        "\n  EXAM POINT: The gate fires regardless of what the model does.\n"
        "  System prompt instructions alone cannot guarantee this — the tool can.\n"
    )

    # Test 3: Read-only balance lookup — no verification required
    # Model should select get_account_balance directly, not verify_customer first.
    # This tests model-driven tool selection via good descriptions.
    state.reset()
    run_agent(
        "What is the account balance for customer C-001?",
        label="Read-only request — model selects correct tool without verification",
    )

    # Test 4: Flagged customer — verification fails, refund stays blocked
    state.reset()
    run_agent(
        "Process a $50 refund for customer C-002.",
        label="Flagged customer — verify fails, refund blocked by gate",
    )

    # -----------------------------------------------------------------------
    # Anti-pattern callout (do not implement — for exam awareness only)
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 60}")
    print("ANTI-PATTERN CALLOUT (exam awareness, do not implement)")
    print("=" * 60)
    print("""
  WRONG approach — routing classifier in front of the agent:
    if "refund" in user_message.lower():
        require_verification()
    elif "balance" in user_message.lower():
        skip_verification()

  Why it fails:
    - "Can you cancel and refund order ORD-001?" -> keyword "refund" detected
    - "What does a refund process look like?" -> false positive
    - Keyword routing breaks on paraphrasing, multi-intent requests, and edge cases

  CORRECT approach:
    - Write precise, distinct tool descriptions
    - Let the model select tools based on intent
    - Enforce hard compliance in the tool itself (programmatic gate)
    - Use hooks (PreToolUse) for enforcement at the Claude Code layer
""")
