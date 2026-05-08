"""
CCA-F Domain 2, Exercise 2 -- Tool Error Handling (Subdomain 2.2)

WHAT THIS EXERCISES:
  Structured error responses tell the agent HOW to recover.
  Generic or silent errors leave the agent unable to reason about next steps.

KEY FIELDS:
  isError       -- bool  : true = access/execution failure, false = successful call
  errorCategory -- str   : "transient" | "validation" | "permission"
  isRetryable   -- bool  : true = retry may succeed; false = same params will fail again
  description   -- str   : human-readable, customer-safe (no raw input or PII)

EXAM PATTERNS:
  "0 results" is NOT an error -- it is a successful query returning an empty set
  Timeout      = transient, retryable   -> agent can retry with same params
  Policy error = validation, NOT retryable -> agent should NOT retry identically
  Silent empty = ANTI-PATTERN -> agent thinks call succeeded, hides real failure

STRUCTURE:
  Part A -- correct structured errors for 3 failure modes
  Part B -- anti-pattern: silent suppression
  Part C -- agent handling: watch how Claude reasons about each error type
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
# TOOL DEFINITIONS
# ==============================================================

TOOLS = [
    {
        "name": "search_products",
        "description": (
            "Search the product catalog by keyword. "
            "Returns a list of matching products. "
            "An empty list means no products matched -- it is not an error."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string"}
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "get_inventory_level",
        "description": (
            "Look up current inventory count for a product SKU. "
            "May return a transient error if the inventory service is temporarily unavailable."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sku": {"type": "string", "description": "Product SKU, e.g. WIDGET-01"}
            },
            "required": ["sku"]
        }
    },
    {
        "name": "apply_promo_code",
        "description": (
            "Apply a promotional code to a cart. "
            "Returns success confirmation or a validation error if the code is invalid or expired."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "cart_id":    {"type": "string"},
                "promo_code": {"type": "string"}
            },
            "required": ["cart_id", "promo_code"]
        }
    }
]


# ==============================================================
# PART A -- CORRECT STRUCTURED TOOL IMPLEMENTATIONS
# ==============================================================

def search_products_correct(keyword):
    """
    0 results is a SUCCESS -- not an error.
    The agent should report "nothing found" -- not retry.
    """
    if keyword == "discontinued_item":
        # Successful call, empty result set -- NOT isError
        return {
            "status": "success",
            "results": [],
            "count": 0,
            "message": "No products matched the search criteria."
        }
    return {
        "status": "success",
        "results": [
            {"sku": "WIDGET-01", "name": "Blue Widget", "price": 44.99},
            {"sku": "WIDGET-02", "name": "Red Widget",  "price": 39.99}
        ],
        "count": 2
    }


def get_inventory_level_correct(sku):
    """
    Simulates a transient timeout from the inventory service.
    isRetryable: true -- the agent can retry with the same parameters.
    NOTE: error description never echoes back raw input (HIPAA/PII safety).
    """
    if sku == "WIDGET-99":
        return {
            "isError": True,
            "errorCategory": "transient",
            "isRetryable": True,
            "description": (
                "Inventory service temporarily unavailable. "
                "Please retry the request."
            )
        }
    return {"sku": sku, "quantity_on_hand": 142, "warehouse": "WH-EAST"}


def apply_promo_code_correct(cart_id, promo_code):
    """
    Policy violation (invalid code) = validation error, NOT retryable.
    Retrying with the same invalid code will always fail.
    Description is customer-safe: no raw promo code echoed back.
    """
    if promo_code == "BADCODE":
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "description": (
                "The promotional code entered is not valid or has expired. "
                "Please check the code and try a different one."
            )
        }
    return {
        "status": "success",
        "discount_applied": 10.00,
        "new_cart_total": 79.99
    }


# ==============================================================
# PART B -- ANTI-PATTERN IMPLEMENTATIONS
# Silent suppression: returns empty/success for actual failures.
# The agent cannot distinguish failure from "no results."
# ==============================================================

def get_inventory_level_silent(sku):
    """
    ANTI-PATTERN: returns empty dict on failure instead of isError.
    Agent cannot tell if the service is down or inventory is 0.
    """
    if sku == "WIDGET-99":
        return {}   # <-- agent treats this as a successful empty result
    return {"sku": sku, "quantity_on_hand": 142}


def apply_promo_code_silent(promo_code):
    """
    ANTI-PATTERN: silently returns empty on validation failure.
    Agent may retry indefinitely or report a confusing response.
    """
    if promo_code == "BADCODE":
        return {}   # <-- agent has no signal that this was a policy failure
    return {"status": "success", "discount_applied": 10.00}


# ==============================================================
# AGENT RUNNER
# ==============================================================

CORRECT_IMPLEMENTATIONS = {
    "search_products":    lambda i: search_products_correct(i["keyword"]),
    "get_inventory_level": lambda i: get_inventory_level_correct(i["sku"]),
    "apply_promo_code":   lambda i: apply_promo_code_correct(i["cart_id"], i["promo_code"]),
}

SILENT_IMPLEMENTATIONS = {
    "search_products":    lambda i: search_products_correct(i["keyword"]),  # same
    "get_inventory_level": lambda i: get_inventory_level_silent(i["sku"]),
    "apply_promo_code":   lambda i: apply_promo_code_silent(i.get("promo_code", "")),
}


def run_agent(user_message, implementations, label):
    print(f"\n  [{label}] {user_message}")
    messages = [{"role": "user", "content": user_message}]

    for _ in range(4):  # safety cap -- not the loop termination signal
        response = client.messages.create(
            model=MODEL,
            max_tokens=512,
            tools=TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"  Agent: {block.text.strip()}")
            return

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    fn = implementations.get(block.name)
                    result = fn(block.input) if fn else {"error": "unknown tool"}
                    print(f"  Tool call : {block.name}({json.dumps(block.input, ensure_ascii=True)})")
                    print(f"  Tool result: {json.dumps(result, ensure_ascii=True)}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=True)
                    })
            messages.append({"role": "user", "content": tool_results})


# ==============================================================
# TEST SCENARIOS
# ==============================================================

SCENARIOS = [
    (
        "Search for discontinued_item in the catalog",
        "0 results = success, not an error -- agent should report nothing found"
    ),
    (
        "What is the inventory level for SKU WIDGET-99?",
        "Transient timeout -- isRetryable:true, agent may retry"
    ),
    (
        "Apply promo code BADCODE to cart CART-555",
        "Validation failure -- isRetryable:false, agent should not retry"
    ),
]


def main():
    print("=" * 60)
    print("EXERCISE 2 -- Tool Error Handling (2.2)")
    print("=" * 60)

    print("\n--- PART A: CORRECT structured error responses ---")
    for message, note in SCENARIOS:
        print(f"\n  NOTE: {note}")
        run_agent(message, CORRECT_IMPLEMENTATIONS, "CORRECT")

    print("\n--- PART B: ANTI-PATTERN (silent suppression) ---")
    for message, note in SCENARIOS[1:]:  # skip search -- same impl
        print(f"\n  NOTE: {note}")
        run_agent(message, SILENT_IMPLEMENTATIONS, "SILENT")

    print("\n" + "=" * 60)
    print("EXAM DISTINCTION SUMMARY -- 2.2")
    print("=" * 60)
    print("""
Error response fields:
  isError       : true  = access/execution failure
  errorCategory : "transient"  = network/service issue; retry may work
                  "validation" = bad input or policy; same params will fail
                  "permission" = access denied; not retryable
  isRetryable   : true  = agent can retry with same parameters
                : false = agent must change approach or escalate
  description   : customer-safe -- never echo raw input or PII back

Critical distinctions:
  "0 results" -- NOT isError. Successful query, empty result set.
  Timeout     -- isError:true, errorCategory:"transient", isRetryable:true
  Policy fail -- isError:true, errorCategory:"validation", isRetryable:false

  WRONG: return {} on failure (silent suppression)
         Agent cannot tell failure from empty data
  WRONG: use a confidence score field instead of isRetryable
  WRONG: terminate the whole workflow on a single tool failure
         Return partial results + structured error; let coordinator decide
""")


if __name__ == "__main__":
    main()
