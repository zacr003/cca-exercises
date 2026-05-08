
# Domain 1 Exercise 3 — Hooks (PreToolUse + PostToolUse)

Hooks run in **Claude Code**, not the Python SDK.
This file is your reference for configuring and testing them.

---

## What hooks do

| Hook | When it fires | What it can do |
|------|--------------|----------------|
| `PreToolUse` | Before a tool executes | Allow, deny, ask user, or modify the input (`updatedInput`) |
| `PostToolUse` | After a tool executes | Transform the result before the model sees it |

Key distinction: hooks give you **deterministic guarantees**. Prompt instructions give you probabilistic compliance. For business rules that must always hold, use hooks.

---

## Exercise A — PreToolUse: Block writes to production paths

### Goal
Gate any `Write` or `Edit` tool call that targets a path containing `/production/` — require explicit approval.

### Config (`.claude/settings.json` in your project)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c \"echo '$CLAUDE_TOOL_INPUT' | python C:/Users/zac.ramsey/Desktop/cca-exercises/domain-1/hook_pre_production_gate.py\""
          }
        ]
      }
    ]
  }
}
```

### Hook script: `hook_pre_production_gate.py`

```python
import json, sys

tool_input = json.load(sys.stdin)
file_path = tool_input.get("file_path", "") or tool_input.get("path", "")

if "/production/" in file_path:
    # Exit code 2 = ask the user
    print(json.dumps({
        "decision": "ask",
        "reason": f"Write to production path detected: {file_path}. Approve?"
    }))
    sys.exit(2)

# Exit code 0 = allow
sys.exit(0)
```

### What to observe
- Edit a file outside `/production/` → proceeds without interruption
- Edit a file inside `/production/` → Claude Code pauses and prompts for approval
- This is **programmatic enforcement**, not a system prompt instruction

---

## Exercise B — PostToolUse: Trim PII from tool results

### Goal
Strip email addresses from any tool result before the model processes it.

### Config addition to `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c \"echo '$CLAUDE_TOOL_RESULT' | python C:/Users/zac.ramsey/Desktop/cca-exercises/domain-1/hook_post_pii_trim.py\""
          }
        ]
      }
    ]
  }
}
```

### Hook script: `hook_post_pii_trim.py`

```python
import json, re, sys

tool_result = json.load(sys.stdin)
result_str = json.dumps(tool_result)

# Redact email addresses
cleaned = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED]', result_str)

print(cleaned)
sys.exit(0)
```

### Critical exam trap
PostToolUse PII trimming only strips the **current tool result**.
PII already in conversation history from earlier turns is NOT affected.
For full PII hygiene, you need to sanitize at the source (the tool itself), not just the hook.

---

## Exercise C — PreToolUse: Programmatic prerequisite gate

### Goal
Block `process_refund` from executing until `get_customer` has already been called and returned a verified result. This is the "identity verification before financial operations" pattern.

### Concept
Rather than writing "always verify identity before processing refunds" in your system prompt (probabilistic), you track tool call state programmatically and deny the downstream tool if the prerequisite hasn't been met.

### Approach in Claude Code
Use a `PreToolUse` hook on `process_refund` that checks a state file written by a `PostToolUse` hook on `get_customer`.

**PostToolUse on `get_customer`:** writes `{"verified": true, "customer_id": "..."}` to a temp file.

**PreToolUse on `process_refund`:** reads the temp file. If it doesn't exist or `verified != true`, deny with a clear message.

```python
# hook_pre_refund_gate.py
import json, sys
from pathlib import Path

STATE_FILE = Path("/tmp/customer_verification.json")

if not STATE_FILE.exists():
    print(json.dumps({
        "decision": "deny",
        "reason": "Cannot process refund: customer identity has not been verified. Call get_customer first."
    }))
    sys.exit(1)

state = json.loads(STATE_FILE.read_text())
if not state.get("verified"):
    print(json.dumps({
        "decision": "deny",
        "reason": "Customer verification incomplete. Re-run get_customer."
    }))
    sys.exit(1)

sys.exit(0)  # allow
```

---

## Exam traps to internalize from these exercises

| Trap | Correct pattern |
|------|----------------|
| "Add a system prompt rule: never write to /production/" | PreToolUse hook with `permissionDecision: "ask"` |
| "PostToolUse PII hook keeps history clean" | No — only the current result is cleaned |
| "Add a verification reminder in the system prompt" | Programmatic gate (PreToolUse) blocking downstream tool |
| "Use a Delete tool to remove files" | No Delete tool exists — use `Bash` with `rm` |
