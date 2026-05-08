"""
Domain 1 Exercise 2 — Coordinator / Subagent Architecture
===========================================================
CCA-F Exam Focus:
  - Subagents do NOT inherit coordinator context — pass everything explicitly
  - Parallel subagents: multiple API calls launched, results collected before synthesis
  - Pass structured data (JSON), not conversational prose, between agents
  - Coordinator specifies goals + quality criteria, NOT step-by-step procedures
  - Synthesis is a separate pass — never concatenate raw subagent outputs as final answer

Scenario: A research coordinator that dispatches two specialist subagents in parallel,
then synthesizes their findings into a unified answer.
"""

import anthropic
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

client = anthropic.Anthropic()


# --- Subagent runner (reuses the loop from ex1) ---

def run_subagent(agent_name: str, system_prompt: str, task: str) -> dict:
    """
    Runs a subagent with explicit context injection.
    Returns structured JSON output — not prose.

    Key pattern: context is passed in system_prompt + task message.
    The subagent has NO access to the coordinator's conversation history.
    """
    print(f"  [subagent:{agent_name}] Starting task...")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": task}],
    )

    result_text = response.content[0].text
    print(f"  [subagent:{agent_name}] Done.")
    return {"agent": agent_name, "output": result_text}


# --- Coordinator ---

def coordinator(user_request: str):
    """
    Demonstrates the coordinator pattern:
      1. Decompose the task into scoped subtasks
      2. Dispatch subagents IN PARALLEL (not sequentially)
      3. Collect structured outputs
      4. Run a synthesis pass — never concatenate raw outputs
    """
    print(f"\n--- Coordinator starting ---")
    print(f"Request: {user_request}\n")

    # Step 1: Coordinator decomposes the task
    # In a real system this decomposition could itself be LLM-driven.
    # Here we define it directly for clarity.
    subagent_tasks = [
        {
            "name": "pros-analyst",
            "system": (
                "You are a specialist analyst focused on benefits and advantages. "
                "Your job is to identify the strongest arguments IN FAVOR of the topic. "
                "Return your findings as a JSON object: "
                "{\"topic\": str, \"pros\": [str], \"confidence\": \"high\"|\"medium\"|\"low\"}"
            ),
            "task": f"Analyze the pros of: {user_request}",
        },
        {
            "name": "cons-analyst",
            "system": (
                "You are a specialist analyst focused on risks and drawbacks. "
                "Your job is to identify the strongest arguments AGAINST the topic. "
                "Return your findings as a JSON object: "
                "{\"topic\": str, \"cons\": [str], \"confidence\": \"high\"|\"medium\"|\"low\"}"
            ),
            "task": f"Analyze the cons of: {user_request}",
        },
    ]

    # Step 2: Dispatch subagents IN PARALLEL
    # Key pattern: multiple calls launched simultaneously, not sequentially.
    # In Claude Code this would be multiple Task calls in ONE response turn.
    # Here we use ThreadPoolExecutor to simulate parallel dispatch.
    print("[coordinator] Dispatching subagents in parallel...")
    results = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(
                run_subagent, st["name"], st["system"], st["task"]
            ): st["name"]
            for st in subagent_tasks
        }
        for future in as_completed(futures):
            result = future.result()
            results[result["agent"]] = result["output"]

    print(f"\n[coordinator] All subagents complete. Running synthesis pass...")

    # Step 3: Structured handoff to synthesis subagent
    # Pass structured data (JSON), not raw prose.
    # The synthesis agent receives EXPLICIT context — it cannot see the subagent sessions.
    synthesis_context = json.dumps({
        "original_request": user_request,
        "pros_analysis": results.get("pros-analyst"),
        "cons_analysis": results.get("cons-analyst"),
    }, indent=2)

    synthesis_prompt = (
        "You are a synthesis specialist. You receive structured research from two analysts "
        "and produce a balanced, concise summary for a decision-maker. "
        "Do not just concatenate the inputs — integrate and resolve tensions between them. "
        "Format: 2-3 sentence executive summary, then a bullet list of key tradeoffs."
    )

    final = run_subagent(
        "synthesizer",
        synthesis_prompt,
        f"Synthesize the following research:\n{synthesis_context}",
    )

    print(f"\n--- Final synthesis ---\n{final['output']}")
    return final["output"]


# --- Run it ---

if __name__ == "__main__":
    coordinator("adopting a microservices architecture for a mid-sized engineering team")
