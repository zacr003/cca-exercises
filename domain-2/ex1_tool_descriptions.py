"""
CCA-F Domain 2, Exercise 1 -- Tool Descriptions and Selection (Subdomain 2.1)

WHAT THIS EXERCISES:
  Tool descriptions are the PRIMARY mechanism Claude uses for tool selection.
  Overlapping or vague descriptions cause misrouting. Fix BOTH overlapping
  tools -- not just one.

EXAM PATTERNS:
  CORRECT  -- Rename + rewrite BOTH tool descriptions to eliminate overlap
  WRONG    -- Fix only one description
  WRONG    -- Add few-shot routing examples as a first step
  WRONG    -- Add a routing classifier / pre-processing layer
  WRONG    -- tool_choice:"auto" with stronger prompts to force a specific tool

STRUCTURE:
  Part A -- BAD descriptions: overlapping, vague -> misrouting
  Part B -- GOOD descriptions: renamed, differentiated, explicit boundaries -> correct routing
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


# ==============================================================
# PART A -- BAD TOOL DEFINITIONS
# Both tools deal with orders. Descriptions are vague and overlap.
# Claude cannot reliably distinguish when to use which.
# ==============================================================

BAD_TOOLS = [
    {
        "name": "find_orders",
        "description": "Find orders for a customer. Use this to look up order information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_order",
        "description": "Get order details. Use this to retrieve information about an order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order identifier"}
            },
            "required": ["order_id"]
        }
    }
]


# ==============================================================
# PART B -- GOOD TOOL DEFINITIONS
# BOTH tools are renamed AND rewritten. Explicit "when to use"
# and "when NOT to use" sections eliminate all overlap.
# ==============================================================
#
# EXAM TRAP: Improving only find_orders still leaves get_order
# vague. Both descriptions must establish the boundary.

GOOD_TOOLS = [
    {
        "name": "search_orders_by_criteria",
        "description": (
            "Search for a list of orders using partial customer information. "
            "Use this when the customer provides a name, email, date range, or "
            "status filter and wants to browse multiple matching orders. "
            "Returns a summary list -- not full item or shipping detail. "
            "Do NOT use this when the customer provides a specific order ID "
            "such as ORD-XXXXX -- use get_order_by_id for that instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_name": {"type": "string"},
                "status_filter": {
                    "type": "string",
                    "enum": ["all", "pending", "shipped", "delivered", "cancelled"]
                },
                "date_from": {"type": "string", "description": "YYYY-MM-DD"},
                "date_to":   {"type": "string", "description": "YYYY-MM-DD"}
            },
            "required": []
        }
    },
    {
        "name": "get_order_by_id",
        "description": (
            "Retrieve complete details for exactly one order using a specific order ID. "
            "Use this ONLY when the customer provides a specific order ID in the "
            "format ORD-XXXXX. Returns full detail: line items, shipping address, "
            "tracking number, and payment status. "
            "Do NOT use this for browsing or searching across multiple orders -- "
            "use search_orders_by_criteria for that instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Specific order ID in format ORD-XXXXX"
                }
            },
            "required": ["order_id"]
        }
    }
]


# ==============================================================
# MOCK TOOL IMPLEMENTATIONS
# ==============================================================

def handle_tool(name, tool_input):
    if name in ("find_orders", "search_orders_by_criteria"):
        return {
            "results": [
                {"order_id": "ORD-10041", "status": "shipped",   "total": 89.99},
                {"order_id": "ORD-10038", "status": "delivered", "total": 42.00}
            ],
            "count": 2
        }
    if name in ("get_order", "get_order_by_id"):
        return {
            "order_id": tool_input.get("order_id", "ORD-10041"),
            "status": "shipped",
            "items": [{"sku": "WIDGET-01", "qty": 2, "price": 44.99}],
            "shipping_address": "123 Main St, Anytown USA",
            "tracking": "1Z999AA10123456784"
        }
    return {"error": "unknown tool"}


def run_single_turn(user_message, tool_defs):
    """Run one user turn and report which tool was selected."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        tools=tool_defs,
        messages=[{"role": "user", "content": user_message}]
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.name, block.input
    return None, {}


# ==============================================================
# TEST QUERIES
# Clear intent: first 2 are list/search, last 2 are ID lookup.
# With bad descriptions, routing is unreliable.
# With good descriptions, routing is consistent.
# ==============================================================

QUERIES = [
    ("What orders has Jane Smith placed recently?",      "search"),
    ("Show me all pending orders from the last 7 days",  "search"),
    ("Pull up order ORD-10041 for me",                   "id_lookup"),
    ("I need the details on order ORD-10038",             "id_lookup"),
]


def run_section(label, tool_defs):
    print(f"\n--- {label} ---")
    for query, expected_type in QUERIES:
        tool_name, tool_input = run_single_turn(query, tool_defs)
        marker = ""
        if tool_name is None:
            marker = "  (no tool called)"
        print(f"  [{expected_type:9s}] Query  : {query}")
        print(f"              Tool   : {tool_name}{marker}")
        print(f"              Input  : {json.dumps(tool_input, ensure_ascii=True)}")
        print()


def main():
    print("=" * 60)
    print("EXERCISE 1 -- Tool Descriptions and Selection (2.1)")
    print("=" * 60)
    print("Same 4 queries run against BAD tools, then GOOD tools.")
    print("Watch for routing inconsistency in Part A.\n")

    run_section("PART A: BAD descriptions (overlapping, vague)", BAD_TOOLS)
    run_section("PART B: GOOD descriptions (renamed, differentiated)", GOOD_TOOLS)

    print("=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 2.1")
    print("=" * 60)
    print("""
Problem: two overlapping tools causing misrouting

  CORRECT  Rename + rewrite BOTH descriptions
           - Add 'when to use' section
           - Add 'do NOT use when' section
           - Make the boundary explicit in the name itself

  WRONG    Fix only one description
           - The unfixed tool still creates ambiguity

  WRONG    Add few-shot routing examples first
           - Examples add token overhead without fixing root cause
           - Descriptions are the primary signal; fix those first

  WRONG    Add a routing classifier
           - Over-engineered; bypasses LLM natural language understanding
           - Claude already routes by description -- use that

  WRONG    tool_choice:'auto' + stronger prompts to force a tool
           - 'auto' still allows text-only response with no tool call
           - Use tool_choice:'any' to guarantee SOME tool is called
           - Use tool_choice:{'type':'tool','name':'X'} to force SPECIFIC tool
""")


if __name__ == "__main__":
    main()
