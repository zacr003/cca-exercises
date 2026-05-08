# Domain 1 Exercise 6 — Session Management and Parallelism

CCA-F Exam Focus (Subdomain 1.7):
- `fork_session` — independent branches from a shared analysis baseline
- `--resume [session-name]` — continuing a named session across work sessions
- **Resume vs. fresh start** decision framework
- **Explore subagent** pattern — isolate verbose discovery, return summaries
- `"Task"` must be in `allowedTools` for a coordinator to spawn subagents
- `stop_reason: "max_tokens"` with incomplete `tool_use` → raise `max_tokens` and retry

---

## Concept 1 — `fork_session`: Independent Branches from a Shared Baseline

### What it does
`fork_session` creates a copy of the current session state so two independent
investigation branches can proceed without contaminating each other.

### When to use it
Use when you have reached a shared understanding of the codebase and need to
explore **two or more divergent options** — e.g., comparing refactoring approaches,
or evaluating two competing API designs.

### Claude Code command

```bash
# Inside a Claude Code session, after shared analysis is complete:
/fork_session refactor-option-a
/fork_session refactor-option-b
```

Each fork starts from the same session snapshot. Changes in one fork do not
appear in the other. This is the correct tool for divergent exploration.

### Scenario

> You have explored the `OrderService` class and understand its structure.
> Now you want to compare two refactoring strategies:
>   A) Extract a `RefundPolicy` class
>   B) Convert to a dataclass + validators pattern
>
> Fork at this point. Option A exploration in one session, Option B in another.
> Compare results without cross-contamination.

### Common trap
Running both explorations in a single session = findings from Option A bleed
into Option B analysis. The model's context contains mixed reasoning and produces
inconsistent comparisons.

---

## Concept 2 — `--resume [session-name]`: Continuing a Named Session

### What it does
`--resume` continues a previously named Claude Code session, restoring the prior
conversation context, tool results, and investigation state.

### When to use it
Use when prior tool results are **still current** and you are picking up where
you left off within the same investigation.

### Claude Code command

```bash
# Start a named session
claude --session-name order-service-audit

# Resume it next work session (same day or next day if files unchanged)
claude --resume order-service-audit
```

### Resume vs. Fresh Start — the exam decision framework

| Condition | Use |
|-----------|-----|
| Files are **unchanged** since last session | `--resume` — prior tool results are still valid |
| You remember where you left off | `--resume` — no need to re-explore |
| Files have **changed significantly** since last session | Fresh start — prior tool results are stale |
| Prior tool results reference code that no longer exists | Fresh start — stale results cause hallucination |
| It has been days and the codebase has been active | Fresh start + inject a written summary of prior findings |

### When resuming: target the update
When you resume and only a few files changed, tell the session specifically
what changed rather than asking it to re-explore everything:

```
/resume order-service-audit
"Since last session, only order_service.py changed — the cancel_order method 
was refactored. Re-read that method only. Prior findings on api_gateway.py 
and user_service.py are still valid."
```

This preserves valid context while refreshing only the stale parts.

---

## Concept 3 — Explore Subagent Pattern

### What it does
A dedicated "Explore" subagent runs verbose discovery (reading many files,
running searches) and returns **only a concise summary** to the coordinator.

This keeps the main session's context clean — the raw tool output from 14
file reads does not flood the coordinator's context window.

### Why it matters
Without the Explore subagent pattern:
- Every `Read`, `Grep`, and `Glob` result lands in the coordinator's context
- After exploring a large codebase, the coordinator's effective context for
  reasoning is significantly reduced by raw tool noise
- The model's attention dilutes across verbose output

With the Explore subagent:
- Verbose discovery happens in an isolated session
- The coordinator receives a tight JSON summary
- The coordinator's context stays focused on reasoning and decision-making

### Python implementation (simulates the pattern)

```python
import anthropic
import json
from concurrent.futures import ThreadPoolExecutor

client = anthropic.Anthropic()

# Simulated file contents (in production, the subagent reads these via tools)
CODEBASE = {
    "user_service.py": "class UserService: ...",
    "order_service.py": "class OrderService: ...",
    "api_gateway.py": "def handle_request(...): ...",
}

def explore_subagent(scope: str, files: dict) -> dict:
    """
    Isolated discovery subagent.
    Receives explicit context (scope + file contents).
    Returns a tight JSON summary — NOT raw tool output.
    
    EXAM PATTERN:
      - Subagent has NO access to coordinator session history
      - Context must be injected explicitly (scope, file contents)
      - Return structured JSON, not prose (precise handoff for coordinator)
    """
    file_dump = "\n\n".join(
        f"=== {name} ===\n{content}" for name, content in files.items()
    )
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=(
            "You are an exploration specialist. Read the provided source files and "
            "return a concise structured summary. Do not include raw file content in your output. "
            "Return JSON: {\"files_reviewed\": [str], \"key_patterns\": [str], "
            "\"entry_points\": [str], \"risks\": [str]}"
        ),
        messages=[{
            "role": "user",
            "content": f"Scope: {scope}\n\nFiles to explore:\n{file_dump}"
        }]
    )
    return json.loads(response.content[0].text)


def coordinator_with_explore_subagent():
    """
    Coordinator that uses an Explore subagent to isolate discovery noise.
    """
    print("[coordinator] Dispatching Explore subagent for discovery...")
    
    # Explore subagent runs in isolation — all verbose discovery stays there
    summary = explore_subagent(
        scope="Identify entry points and authorization risks",
        files=CODEBASE
    )
    
    print(f"[coordinator] Received summary from Explore subagent: {summary}")
    # Coordinator now reasons over the SUMMARY, not raw tool output
    # Its context stays focused for downstream decision-making
    return summary
```

---

## Concept 4 — `allowedTools` Must Include `"Task"`

### The rule
For a coordinator agent to spawn subagents using the `Task` tool, `"Task"` must
be in the `allowedTools` list for that coordinator's invocation.

If `"Task"` is omitted, the coordinator cannot dispatch subagents —
it silently falls back to single-agent execution.

### Example (Claude Code SDK / programmatic invocation)

```python
# WRONG — coordinator cannot spawn subagents
response = client.messages.create(
    model="claude-opus-4-6",
    tools=[web_search_tool, read_file_tool],   # "Task" missing
    ...
)

# CORRECT — coordinator can spawn subagents
response = client.messages.create(
    model="claude-opus-4-6",
    tools=[web_search_tool, read_file_tool, task_tool],  # "Task" included
    ...
)
```

### In claude headless mode

```bash
# WRONG
claude -p "Research and summarize..." --allowedTools "WebSearch,Read"

# CORRECT
claude -p "Research and summarize..." --allowedTools "WebSearch,Read,Task"
```

---

## Concept 5 — `stop_reason: "max_tokens"` with Incomplete `tool_use`

This is covered in Subdomain 1.1 and ex1, but appears in session management
context too: if a coordinator response is truncated mid-tool-use block, the
entire response (including the partial `tool_use`) must be handled.

### What happens
The API returns `stop_reason: "max_tokens"` and the response content may contain
a partial or incomplete `tool_use` block — the tool was requested but the arguments
were cut off.

### Correct handling

```python
if stop_reason == "max_tokens":
    # Do NOT treat this as end_turn
    # Do NOT try to parse partial tool_use blocks
    print(f"[loop] Response truncated — raising max_tokens and retrying")
    max_tokens *= 2
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": [{
        "type": "text",
        "text": "Your response was truncated. Please continue."
    }]})
    continue  # back to top of the loop
```

### Exam trap
Treating `"max_tokens"` the same as `"end_turn"` and returning the partial
response as the final answer. `"max_tokens"` always means truncation.

---

## Exam Traps Summary — Subdomain 1.7

| Trap | Correct Pattern |
|------|----------------|
| Running divergent explorations in one session | `fork_session` to create independent branches |
| Always resuming regardless of file staleness | Evaluate: resume if files unchanged, fresh start if stale |
| Not telling the resumed session what changed | Explicitly state which files changed on resume |
| Explore subagent returns raw file content | Return a tight JSON summary — not raw tool output |
| `"Task"` missing from `allowedTools` | Always include `"Task"` if the coordinator needs to spawn subagents |
| Treating `stop_reason: "max_tokens"` as completion | Raise `max_tokens` and retry — it is always truncation |
