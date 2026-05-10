"""
CCA-F Domain 5, Exercise 2 — Escalation and Human-in-the-Loop (Subdomain 5.2)
===============================================================================

WHAT THIS EXERCISES:
  When to escalate to a human and when NOT to. The exam tests this heavily with
  scenario questions. Knowing the correct trigger (and the wrong ones) is critical.

ESCALATION TRIGGERS (valid):
  1. Customer EXPLICITLY requests a human agent -> honor immediately, no investigation first
  2. Policy is AMBIGUOUS or SILENT on the customer's specific situation -> escalate
  3. INABILITY TO MAKE MEANINGFUL PROGRESS after reasonable attempts -> escalate

DO NOT ESCALATE based on:
  - Customer emotion or frustration alone (sentiment != complexity)
  - Self-reported confidence scores (poorly calibrated)
  - Multi-topic messages (handle each with appropriate tools)
  - "Case complexity" if the issue has a clear resolution

FRUSTRATED USER PATTERN (heavily tested):
  Frustrated, but issue is SOLVABLE -> acknowledge + offer resolution first
  Only escalate if customer REITERATES wanting a human after the offer

STRUCTURE:
  Part A -- Explicit criteria in system prompt (with few-shot examples)
  Part B -- Scenario tests: watch how the agent handles each trigger type
  Part C -- The frustrated user pattern in detail
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
# TOOLS AVAILABLE TO THE SUPPORT AGENT
# =====================================================================

SUPPORT_TOOLS = [
    {
        "name": "lookup_order",
        "description": "Look up order status and details by order ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "process_refund",
        "description": "Process a refund for a delivered order. Maximum automated amount: $500.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "amount":   {"type": "number", "description": "Refund amount in USD"}
            },
            "required": ["order_id", "amount"]
        }
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Transfer the case to a human agent with a structured summary. "
            "Use when: customer explicitly requests a human, policy gap exists, "
            "or unable to resolve after reasonable attempts."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason":     {"type": "string", "description": "Why escalating"},
                "summary":    {"type": "string", "description": "What was investigated and attempted"},
                "recommended_action": {"type": ["string", "null"]}
            },
            "required": ["reason", "summary"]
        }
    }
]


# =====================================================================
# SYSTEM PROMPT: EXPLICIT ESCALATION CRITERIA + FEW-SHOT EXAMPLES
# =====================================================================
# This is the CORRECT approach. Vague instructions like "escalate complex cases"
# produce inconsistent behavior. Explicit criteria + examples are the fix.

SUPPORT_SYSTEM_PROMPT = """You are a customer support agent. Your goal is to resolve issues
directly whenever possible, and escalate to a human only when appropriate.

ESCALATION CRITERIA — escalate when ANY of these apply:
  1. Customer EXPLICITLY asks for a human agent or manager -> escalate immediately
  2. Policy is SILENT or AMBIGUOUS on the customer's specific request -> escalate
  3. You have made reasonable attempts and cannot make meaningful progress -> escalate

DO NOT ESCALATE based on:
  - Customer frustration or emotional tone alone
  - "This seems complex" without a specific policy gap or failure to progress
  - Self-reported confidence (if you can look up an answer, do so)

FRUSTRATED USER PATTERN:
  If customer is frustrated but the issue is within your capability:
    Step 1: Acknowledge their frustration empathetically
    Step 2: Offer to resolve the issue
    Step 3: ONLY escalate if they explicitly reiterate wanting a human after your offer

EXAMPLES:

Example 1 — RESOLVE (standard refund):
  Customer: "My order ORD-001 arrived broken. I want a refund."
  Action: Look up order -> process refund if eligible
  Do NOT escalate: this is a standard operation within your capability

Example 2 — ESCALATE (customer requests human):
  Customer: "I want to speak to a manager about this."
  Action: escalate_to_human immediately with summary of the situation
  Do NOT attempt to resolve first: explicit request for human = immediate escalation

Example 3 — RESOLVE FIRST (frustrated but solvable):
  Customer: "This is ridiculous! I've been waiting 3 weeks for my refund!"
  Action: Acknowledge frustration, then look up refund status and resolve
  Do NOT escalate: frustration alone is not an escalation trigger
  Only escalate if: after you offer resolution, they reiterate wanting a human

Example 4 — ESCALATE (policy gap):
  Customer: "Can you match the price I found on a competitor's website?"
  Action: escalate_to_human — our policy covers own-site adjustments, not competitor matching
  This is a policy gap: the policy doesn't address this specific request"""


# =====================================================================
# MOCK TOOL IMPLEMENTATIONS
# =====================================================================

def handle_tool(name: str, tool_input: dict) -> dict:
    if name == "lookup_order":
        order_id = tool_input.get("order_id", "")
        if order_id == "ORD-001":
            return {"order_id": "ORD-001", "status": "delivered", "amount": 89.99,
                    "item": "Blue Widget", "eligible_for_refund": True}
        return {"error": "Order not found"}

    if name == "process_refund":
        amount = tool_input.get("amount", 0)
        if amount > 500:
            return {"error": "Refund exceeds $500 automated limit. Must escalate to human."}
        return {"success": True, "refund_id": f"REF-{tool_input.get('order_id', '?')}",
                "amount": amount, "processing_time": "2-3 business days"}

    if name == "escalate_to_human":
        return {"escalated": True, "ticket_id": "TKT-99999",
                "message": "Case transferred to human agent."}

    return {"error": "Unknown tool"}


# =====================================================================
# AGENT RUNNER
# =====================================================================

def run_support_agent(customer_message: str, label: str):
    """Runs the support agent for one customer message and shows what it does."""
    print(f"\n  [{label}]")
    print(f"  Customer: {customer_message}")

    messages = [{"role": "user", "content": customer_message}]

    for _ in range(4):  # safety cap
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=SUPPORT_SYSTEM_PROMPT,
            tools=SUPPORT_TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text = next((b.text for b in response.content if hasattr(b, "text")), "")
            print(f"  Agent:    {text.strip()[:150]}")
            return

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = handle_tool(block.name, block.input)
                    print(f"  Tool:     {block.name}({json.dumps(block.input, ensure_ascii=True)[:60]})")
                    if block.name == "escalate_to_human":
                        print(f"  --> ESCALATED: {block.input.get('reason', '')}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=True)
                    })
            messages.append({"role": "user", "content": tool_results})


# =====================================================================
# TEST SCENARIOS
# =====================================================================

SCENARIOS = [
    (
        "My order ORD-001 arrived broken. I need a refund.",
        "Standard refund — SHOULD RESOLVE (not escalate)"
    ),
    (
        "I want to speak to a manager right now.",
        "Explicit human request — SHOULD ESCALATE IMMEDIATELY"
    ),
    (
        "This is completely unacceptable! I've been waiting weeks! "
        "I demand this fixed immediately!",
        "Frustrated but no explicit escalation request — SHOULD ACKNOWLEDGE + RESOLVE"
    ),
    (
        "Can you match the price I found on Amazon for this product?",
        "Policy gap (competitor pricing not covered) — SHOULD ESCALATE"
    ),
    (
        "I want a refund AND I want to update my shipping address AND "
        "I have a question about my loyalty points.",
        "Multi-topic — SHOULD HANDLE EACH (not escalate due to complexity)"
    ),
]


def main():
    print("=" * 60)
    print("EXERCISE 2 -- Escalation and Human-in-the-Loop (5.2)")
    print("=" * 60)
    print("Watch which tool the agent calls for each scenario.")
    print("escalate_to_human = escalation; process_refund or lookup_order = resolving\n")

    print("--- System prompt uses explicit criteria + few-shot examples ---")
    print("(See SUPPORT_SYSTEM_PROMPT in the code for the full prompt)\n")

    for message, label in SCENARIOS:
        run_support_agent(message, label)

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 5.2")
    print("=" * 60)
    print("""
Valid escalation triggers:
  1. Customer explicitly requests human agent -> honor IMMEDIATELY (no investigation first)
  2. Policy is ambiguous or silent on the specific request -> escalate
  3. Unable to make meaningful progress after reasonable attempts -> escalate

Do NOT escalate based on:
  Customer emotion / frustration alone (sentiment != complexity)
  Self-reported confidence scores (poorly calibrated)
  Multi-topic messages (handle each with appropriate tools)
  "Case is complex" without a specific gap or failure to progress

Frustrated user pattern (exam favorite):
  Frustrated + issue is solvable -> acknowledge empathetically + offer to resolve
  Only escalate if customer REITERATES wanting a human after your offer
  NOT: escalate immediately because they sound angry
  NOT: ignore the frustration and just process the request

Multiple customer matches:
  When lookup returns multiple accounts for "John Smith" -> ask for additional identifier
  (email, phone, order number) to determine which account is correct
  WRONG: select the most recent account via heuristic
  WRONG: select the highest-value account

Structured handoff summary fields (customer support context):
  customer_id, root_cause, refund_amount, recommended_action
  Do NOT: attach raw conversation transcript (human must reconstruct context)
  Do: compile structured summary the human agent can act on immediately

Fix for miscalibrated escalation (agent escalating too much or too little):
  Add explicit escalation criteria with few-shot examples to system prompt
  WRONG: add confidence threshold auto-escalation (self-reported confidence is unreliable)
  WRONG: deploy sentiment classifier (frustration != complexity)
""")


if __name__ == "__main__":
    main()
