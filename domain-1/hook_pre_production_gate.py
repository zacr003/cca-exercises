"""
Exercise A — PreToolUse: Block writes to production paths.
Fires before Write or Edit tool calls.
Exits with code 2 (ask user) if the target path contains /production/.

Key fix: Windows paths use backslashes — normalize to forward slashes before checking.
Stdin from Claude Code wraps tool params under "tool_input" key.
"""
import json, sys

hook_data = json.load(sys.stdin)
tool_input = hook_data.get("tool_input", {})
file_path = tool_input.get("file_path", "") or tool_input.get("path", "")

if "/production/" in file_path.replace("\\", "/"):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"Write to production path detected: {file_path}. Approve?"
        }
    }))
    sys.exit(2)

sys.exit(0)
