"""
Exercise B — PostToolUse: Flag email addresses in tool results.
Fires after any tool call, before the model processes the result.

Exam note: PostToolUse cannot replace the raw tool result — it injects
additionalContext alongside it. The model sees the context AND the result.
For true PII prevention, sanitize at the source (the tool itself).

Exit 0 + hookSpecificOutput = model sees additionalContext injected.
"""
import json, re, sys

hook_data = json.load(sys.stdin)
tool_response = hook_data.get("tool_response", {})
response_str = json.dumps(tool_response)

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
found = EMAIL_RE.findall(response_str)

if found:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"PII WARNING: This tool result contained {len(found)} email address(es). Treat as [REDACTED] and do not repeat them."
        }
    }))

sys.exit(0)
