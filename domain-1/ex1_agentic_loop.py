"""
Domain 1 Exercise 1 — Basic Agentic Loop
=========================================
CCA-F Exam Focus:
  - stop_reason is the ONLY termination signal (never parse text)
  - Execute ALL tool_use blocks when stop_reason == "tool_use"
  - Return ALL tool_result blocks in ONE user message before the next API call
  - tool_result blocks must come FIRST in the content array
  - stop_reason == "max_tokens" means truncation, not completion — raise max_tokens and retry

Scenario: A simple customer support agent that can look up order status and issue refunds.
"""

import anthropic
import json

client = anthropic.Anthropic()

# --- Fake tool implementations ---

def get_order_status(order_id: str) -> dict:
    orders = {
        "ORD-001": {"status": "shipped", "eta": "2026-05-08"},
        "ORD-002": {"status": "delivered", "date": "2026-05-04"},
        "ORD-003": {"status": "processing"},
    }
    return orders.get(order_id, {"error": "Order not found"})


def issue_refund(order_id: str, amount: float) -> dict:
    if amount > 500:
        return {"success": False, "reason": "Refund exceeds $500 limit — requires manager approval"}
    return {"success": True, "refund_id": f"REF-{order_id}", "amount": amount}


# Map tool names to functions
TOOLS = {
    "get_order_status": get_order_status,
    "issue_refund": issue_refund,
}

# --- Tool definitions for the API ---

TOOL_DEFINITIONS = [
    {
        "name": "get_order_status",
        "description": "Look up the current status and delivery information for a customer order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, e.g. ORD-001"}
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "issue_refund",
        "description": "Issue a refund for a delivered or problematic order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID to refund"},
                "amount": {"type": "number", "description": "Refund amount in USD"}
            },
            "required": ["order_id", "amount"]
        }
    }
]

# --- Agentic loop ---

def run_agent(user_message: str, max_tokens: int = 1024) -> str:
    """
    Runs the agentic loop until stop_reason == 'end_turn'.

    Key patterns demonstrated:
      1. Check stop_reason — never check text content
      2. Execute ALL tool_use blocks in a single round
      3. Return ALL tool_result blocks in ONE user message
      4. Handle max_tokens by raising the limit and retrying
    """
    messages = [{"role": "user", "content": user_message}]

    print(f"\n--- Agent starting ---")
    print(f"User: {user_message}\n")

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # PATTERN 1: Check stop_reason — this is the ONLY termination signal
        # Never do: if "I have completed" in response.content[-1].text
        stop_reason = response.stop_reason
        print(f"[loop] stop_reason = {stop_reason!r}")

        # PATTERN 4: Handle max_tokens — this is truncation, not completion
        if stop_reason == "max_tokens":
            print(f"[loop] Response truncated — raising max_tokens from {max_tokens} to {max_tokens * 2}")
            max_tokens *= 2
            # Add the partial response and retry
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": [
                {"type": "text", "text": "Your response was truncated. Please continue."}
            ]})
            continue

        # Add assistant response to message history
        messages.append({"role": "assistant", "content": response.content})

        # PATTERN 2: stop_reason == "end_turn" means the agent is done
        if stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")), ""
            )
            print(f"\nAgent: {final_text}")
            return final_text

        # PATTERN 2 continued: stop_reason == "tool_use" — execute tools
        if stop_reason == "tool_use":
            # Collect ALL tool_use blocks (there may be more than one)
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            print(f"[loop] Executing {len(tool_use_blocks)} tool(s): {[b.name for b in tool_use_blocks]}")

            # PATTERN 3: Build ALL tool_result blocks, then return in ONE user message
            # tool_result blocks must appear FIRST in the content array
            tool_results = []
            for block in tool_use_blocks:
                tool_fn = TOOLS[block.name]
                result = tool_fn(**block.input)
                print(f"  [{block.name}] input={block.input} -> result={result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            # Return ALL results in ONE message — tool_result blocks first
            messages.append({"role": "user", "content": tool_results})


# --- Run it ---

if __name__ == "__main__":
    # Test 1: Simple status lookup
    run_agent("What's the status of order ORD-001?")

    # Test 2: Refund within limit
    run_agent("I need a refund of $150 for order ORD-002, it arrived damaged.")

    # Test 3: Refund exceeding limit — agent should surface the business rule
    run_agent("Please refund $600 for order ORD-001.")
