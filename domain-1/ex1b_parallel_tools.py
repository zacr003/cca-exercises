"""
Domain 1 Exercise 1b — Agentic Loop with Parallel Tool Calls
=============================================================
CCA-F Exam Focus:
  - Model may return MULTIPLE tool_use blocks in a single response
  - Execute ALL tool_use blocks before the next API call
  - Return ALL tool_result blocks in ONE user message (not one per tool)
  - tool_use_id links each result back to its specific request — never mix them up
  - Parallel execution (ThreadPoolExecutor) is an optimization;
    correctness only requires all results in ONE message

New pattern vs. ex1:
  ex1 always had one tool call per turn.
  Here, a broad request causes the model to call multiple tools simultaneously.
  The loop logic is identical — only the number of tool_use blocks changes.

Scenario: A travel planning agent with three independent tools.
A broad "plan my trip" request triggers all three tools in a single model turn.
"""

import anthropic
import json
from concurrent.futures import ThreadPoolExecutor

client = anthropic.Anthropic()

# --- Fake tool implementations ---

def check_flights(origin: str, destination: str, date: str) -> dict:
    flights = {
        ("NYC", "LAX", "2026-06-01"): {"available": True, "price": 342, "airline": "Delta", "duration": "5h 30m"},
        ("NYC", "LAX", "2026-06-15"): {"available": True, "price": 289, "airline": "United", "duration": "5h 45m"},
        ("NYC", "MIA", "2026-06-01"): {"available": True, "price": 178, "airline": "American", "duration": "3h 10m"},
    }
    key = (origin.upper(), destination.upper(), date)
    return flights.get(key, {"available": False, "reason": "No flights found for this route/date"})


def check_hotels(city: str, check_in: str, check_out: str) -> dict:
    hotels = {
        ("LAX", "2026-06-01", "2026-06-05"): [
            {"name": "The Standard", "price_per_night": 189, "rating": 4.2},
            {"name": "Ace Hotel", "price_per_night": 215, "rating": 4.5},
        ],
        ("MIA", "2026-06-01", "2026-06-05"): [
            {"name": "The Betsy", "price_per_night": 299, "rating": 4.7},
            {"name": "Freehand Miami", "price_per_night": 145, "rating": 4.1},
        ],
    }
    key = (city.upper(), check_in, check_out)
    return hotels.get(key, {"available": False, "reason": "No hotels found for these dates"})


def get_weather_forecast(city: str, date: str) -> dict:
    forecasts = {
        ("LAX", "2026-06-01"): {"condition": "Sunny", "high": 78, "low": 62},
        ("MIA", "2026-06-01"): {"condition": "Partly cloudy", "high": 85, "low": 74},
    }
    key = (city.upper(), date)
    return forecasts.get(key, {"condition": "Unknown", "high": None, "low": None})


TOOLS = {
    "check_flights": check_flights,
    "check_hotels": check_hotels,
    "get_weather_forecast": get_weather_forecast,
}

TOOL_DEFINITIONS = [
    {
        "name": "check_flights",
        "description": "Check flight availability and pricing between two cities on a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "3-letter origin city code, e.g. NYC"},
                "destination": {"type": "string", "description": "3-letter destination city code, e.g. LAX"},
                "date": {"type": "string", "description": "Travel date in YYYY-MM-DD format"},
            },
            "required": ["origin", "destination", "date"]
        }
    },
    {
        "name": "check_hotels",
        "description": "Check hotel availability and rates in a city for given check-in and check-out dates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "3-letter city code, e.g. LAX"},
                "check_in": {"type": "string", "description": "Check-in date in YYYY-MM-DD format"},
                "check_out": {"type": "string", "description": "Check-out date in YYYY-MM-DD format"},
            },
            "required": ["city", "check_in", "check_out"]
        }
    },
    {
        "name": "get_weather_forecast",
        "description": "Get the weather forecast for a city on a specific date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "3-letter city code, e.g. LAX"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
            },
            "required": ["city", "date"]
        }
    }
]


# --- Tool executor (extracted so it works with ThreadPoolExecutor.map) ---

def execute_tool(block) -> dict:
    """Execute a single tool_use block and return a tool_result dict."""
    tool_fn = TOOLS[block.name]
    result = tool_fn(**block.input)
    print(f"  [{block.name}] input={block.input} -> result={result}")
    return {
        "type": "tool_result",
        "tool_use_id": block.id,   # ties this result back to the specific tool_use block
        "content": json.dumps(result),
    }


# --- Agentic loop ---

def run_agent(user_message: str, max_tokens: int = 1024) -> str:
    messages = [{"role": "user", "content": user_message}]

    print(f"\n{'='*60}")
    print(f"User: {user_message}\n")

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        stop_reason = response.stop_reason
        print(f"[loop] stop_reason = {stop_reason!r}")

        if stop_reason == "max_tokens":
            print(f"[loop] Truncated - raising max_tokens to {max_tokens * 2}")
            max_tokens *= 2
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": [
                {"type": "text", "text": "Your response was truncated. Please continue."}
            ]})
            continue

        messages.append({"role": "assistant", "content": response.content})

        if stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")), ""
            )
            print(f"\nAgent: {final_text}".encode("ascii", errors="replace").decode("ascii"))
            return final_text

        if stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            count = len(tool_use_blocks)
            print(f"[loop] Model requested {count} tool(s): {[b.name for b in tool_use_blocks]}")

            # KEY PATTERN: Run all tools in parallel, collect ALL results,
            # then return them in ONE user message.
            #
            # Wrong approach (do NOT do this):
            #   for block in tool_use_blocks:
            #       messages.append({"role": "user", "content": [one_result]})  # WRONG
            #
            # Correct approach: collect all, send once.
            with ThreadPoolExecutor(max_workers=count) as executor:
                tool_results = list(executor.map(execute_tool, tool_use_blocks))

            print(f"[loop] Returning {len(tool_results)} result(s) in ONE message")
            messages.append({"role": "user", "content": tool_results})


# --- Run it ---

if __name__ == "__main__":
    # Test 1: Narrow request — single tool call (baseline, same as ex1)
    run_agent("What flights are available from NYC to LAX on June 1st 2026?")

    # Test 2: Broad request — should trigger flight + hotel in parallel (2 tools, 1 turn)
    run_agent(
        "I want to fly from NYC to LAX on June 1st 2026 and stay for 4 nights. "
        "What are my flight and hotel options?"
    )

    # Test 3: Full plan request — should trigger all 3 tools in parallel (3 tools, 1 turn)
    run_agent(
        "Plan my trip: NYC to LAX on June 1st 2026, staying until June 5th. "
        "I need flights, hotels, and what the weather will be like."
    )
