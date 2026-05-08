"""
CCA-F Domain 2, Exercise 3 -- Tool Scope and Constraints (Subdomain 2.3)

WHAT THIS EXERCISES:
  Scoped, purpose-specific tools are more reliable than broad generic ones.
  Constraints should live IN the tool definition and implementation --
  not in the system prompt.

EXAM PATTERNS:
  CORRECT  -- Replace generic tool with constrained alternative
               (e.g., fetch_url -> load_support_doc with URL validation)
  CORRECT  -- Give each subagent only the tools it needs for its role
  WRONG    -- One generic tool that does everything
  WRONG    -- Enforce scope via system prompt instructions (probabilistic)

STRUCTURE:
  Part A -- Generic fetch_url tool: no constraints, agent can go anywhere
  Part B -- Scoped load_support_doc tool: URL validated at tool level
  Part C -- Too-many-tools problem: 6 overlapping tools vs. 3 focused ones
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
# PART A -- GENERIC TOOL (no constraints)
# Agent can request any URL -- no validation at the tool level.
# System prompt says "only search our docs" but that is probabilistic.
# ==============================================================

GENERIC_TOOLS = [
    {
        "name": "fetch_url",
        "description": (
            "Fetch the content of any web URL. "
            "Use this to retrieve information from web pages."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch"}
            },
            "required": ["url"]
        }
    }
]


def fetch_url_impl(url):
    """Mock: returns different content based on URL."""
    if "support.example.com" in url:
        return {
            "url": url,
            "content": "Support article: How to reset your password. Step 1: ...",
            "source": "official_docs"
        }
    # Agent fetched an outside URL -- scope violation
    return {
        "url": url,
        "content": "External site content -- not from our documentation.",
        "source": "external"
    }


# ==============================================================
# PART B -- SCOPED TOOL (constraints enforced in implementation)
# URL validation happens at the tool level -- not in the prompt.
# If the URL is outside allowed domains, the tool rejects it
# before any fetch occurs.
# ==============================================================

ALLOWED_DOMAINS = ["support.example.com", "docs.example.com"]

SCOPED_TOOLS = [
    {
        "name": "load_support_doc",
        "description": (
            "Load content from the official support documentation. "
            "Only works with support.example.com and docs.example.com URLs. "
            "Use this to answer product questions from official documentation. "
            "Do NOT attempt URLs from external sites -- this tool will reject them."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "A support.example.com or docs.example.com URL"
                }
            },
            "required": ["url"]
        }
    }
]


def load_support_doc_impl(url):
    """
    Scope enforced at the tool level -- not in system prompt.
    Rejects disallowed domains with a structured error.
    """
    allowed = any(domain in url for domain in ALLOWED_DOMAINS)
    if not allowed:
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "description": (
                "This tool only loads content from support.example.com and "
                "docs.example.com. The requested URL is outside allowed domains."
            )
        }
    return {
        "url": url,
        "content": "Support article: How to reset your password. Step 1: ...",
        "source": "official_docs"
    }


# ==============================================================
# PART C -- TOO MANY TOOLS PROBLEM
# 6 narrowly-named tools for simple order operations.
# Overlapping names degrade Claude's selection reliability.
# Consolidate to 3 focused tools with clear boundaries.
# ==============================================================

TOO_MANY_TOOLS = [
    {
        "name": "order_lookup",
        "description": "Look up an order.",
        "input_schema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}
    },
    {
        "name": "order_search",
        "description": "Search for orders.",
        "input_schema": {"type": "object", "properties": {"q": {"type": "string"}}, "required": ["q"]}
    },
    {
        "name": "order_get",
        "description": "Get order information.",
        "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}
    },
    {
        "name": "order_status",
        "description": "Check the status of an order.",
        "input_schema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}
    },
    {
        "name": "order_find",
        "description": "Find orders for a customer.",
        "input_schema": {"type": "object", "properties": {"customer": {"type": "string"}}, "required": ["customer"]}
    },
    {
        "name": "order_details",
        "description": "Get detailed order information.",
        "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}
    }
]

CONSOLIDATED_TOOLS = [
    {
        "name": "get_order_by_id",
        "description": (
            "Get full details for a single order by its ID (format ORD-XXXXX). "
            "Returns items, shipping, tracking, and payment status. "
            "Use ONLY when the customer provides a specific order ID."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"]
        }
    },
    {
        "name": "search_orders_by_criteria",
        "description": (
            "Search for a list of orders by customer name, email, date range, or status. "
            "Use when the customer wants to browse or filter -- not for a specific ID lookup."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_name": {"type": "string"},
                "status": {"type": "string"},
                "date_from": {"type": "string"},
                "date_to": {"type": "string"}
            },
            "required": []
        }
    },
    {
        "name": "get_order_status",
        "description": (
            "Get the current fulfillment status of an order (pending/shipped/delivered/cancelled). "
            "Lightweight -- use when the customer only wants a status update, not full order details."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"]
        }
    }
]


# ==============================================================
# AGENT RUNNER
# ==============================================================

def run_single_turn(user_message, tool_defs, implementations, system=None):
    kwargs = {
        "model": MODEL,
        "max_tokens": 256,
        "tools": tool_defs,
        "messages": [{"role": "user", "content": user_message}]
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)

    for block in response.content:
        if block.type == "tool_use":
            result = implementations.get(block.name, lambda i: {"error": "no impl"})(block.input)
            print(f"  Tool: {block.name}")
            print(f"  Input: {json.dumps(block.input, ensure_ascii=True)}")
            print(f"  Result: {json.dumps(result, ensure_ascii=True)[:120]}...")
            return block.name
    print("  (no tool called)")
    return None


def main():
    print("=" * 60)
    print("EXERCISE 3 -- Tool Scope and Constraints (2.3)")
    print("=" * 60)

    # ---- Part A vs B: scope enforcement ----
    print("\n--- PART A: Generic fetch_url (no constraints) ---")
    print("System prompt says 'only use our docs' -- but that is probabilistic.\n")

    generic_impls = {"fetch_url": lambda i: fetch_url_impl(i["url"])}
    scoped_impls  = {"load_support_doc": lambda i: load_support_doc_impl(i["url"])}

    scope_queries = [
        "Look up the password reset guide at support.example.com/reset",
        "Find information at https://competitor.com/comparison",
    ]
    for q in scope_queries:
        print(f"  Query: {q}")
        run_single_turn(
            q, GENERIC_TOOLS, generic_impls,
            system="Only retrieve content from our official documentation."
        )
        print()

    print("\n--- PART B: Scoped load_support_doc (URL validated in tool) ---")
    print("Constraint is in the tool implementation -- not the system prompt.\n")
    for q in scope_queries:
        print(f"  Query: {q}")
        run_single_turn(q, SCOPED_TOOLS, scoped_impls)
        print()

    # ---- Part C: too many tools ----
    print("\n--- PART C: Too many tools (6) vs. consolidated (3) ---")
    print("6 overlapping order tools degrade selection reliability.\n")
    print(f"  Too-many-tools set ({len(TOO_MANY_TOOLS)} tools):")
    for t in TOO_MANY_TOOLS:
        print(f"    - {t['name']}: {t['description']}")

    print(f"\n  Consolidated set ({len(CONSOLIDATED_TOOLS)} tools):")
    for t in CONSOLIDATED_TOOLS:
        print(f"    - {t['name']}")

    test_q = "What is the status of order ORD-10041?"
    print(f"\n  Query against too-many-tools: {test_q}")
    all_impls = {t["name"]: (lambda i: {"status": "shipped", "order_id": "ORD-10041"}) for t in TOO_MANY_TOOLS}
    run_single_turn(test_q, TOO_MANY_TOOLS, all_impls)

    print(f"\n  Same query against consolidated tools:")
    consol_impls = {t["name"]: (lambda i: {"status": "shipped", "order_id": "ORD-10041"}) for t in CONSOLIDATED_TOOLS}
    run_single_turn(test_q, CONSOLIDATED_TOOLS, consol_impls)

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 2.3")
    print("=" * 60)
    print("""
Scoped tools vs. generic tools:
  CORRECT  -- Constrained tool (URL allowlist enforced IN the tool)
  WRONG    -- Generic tool + system prompt constraint (probabilistic)
  WRONG    -- Generic tool + routing classifier to decide what is allowed

Too-many-tools problem:
  4-5 focused tools = reliable selection
  18 overlapping tools = degraded reliability
  Fix: consolidate overlapping tools, not rename with numbered suffixes

Subagent tool restriction:
  Each subagent gets ONLY the tools relevant to its role
  Web-search subagent: search tools only
  Document-analysis subagent: read tools only
  Report-generation subagent: write tools only
  No cross-specialization access -- scoped per role
""")


if __name__ == "__main__":
    main()
