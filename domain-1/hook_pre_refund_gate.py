"""
Exercise C — PreToolUse: Block process_refund until get_customer has verified identity.
Fires before process_refund tool calls.

Uses a state file written by a PostToolUse hook on get_customer.
If the state file is missing or unverified, the refund is denied.

Exit 2 + permissionDecision deny = hard block (tool cannot execute).
State file uses Windows TEMP directory for cross-platform compatibility.
"""
import json, sys, os
from pathlib import Path

STATE_FILE = Path(os.environ.get("TEMP", "C:/Windows/Temp")) / "customer_verification.json"

if not STATE_FILE.exists():
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Cannot process refund: customer identity has not been verified. Call get_customer first."
        }
    }))
    sys.exit(2)

state = json.loads(STATE_FILE.read_text())
if not state.get("verified"):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Customer verification incomplete. Re-run get_customer."
        }
    }))
    sys.exit(2)

sys.exit(0)
