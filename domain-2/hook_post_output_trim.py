"""
CCA-F Domain 2, Exercise 5 -- PostToolUse Hook: Output Trimming

WHAT THIS DOES:
  Intercepts get_product_details tool results BEFORE Claude processes them.
  Strips internal/noisy fields and injects only business-relevant content.

EXAM PATTERN:
  PostToolUse hooks cannot replace the raw tool result -- they can only
  inject additionalContext alongside it. For true output replacement,
  trimming must happen inside the tool implementation itself.
  This hook demonstrates the additionalContext injection pattern.

  ANTI-PATTERN: hook returns BOTH formatted summary AND raw output
                -> model still sees all the raw noise

CONFIGURATION (add to .claude/settings.json):
  {
    "PostToolUse": [
      {
        "matcher": "get_product_details",
        "hooks": [
          {
            "type": "command",
            "command": "\"C:/Program Files/Python314/python\" C:/Users/zac.ramsey/Desktop/cca-exercises/domain-2/hook_post_output_trim.py"
          }
        ]
      }
    ]
  }
"""

import sys
import json

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

BUSINESS_FIELDS = {"product_id", "name", "price", "in_stock", "category", "description"}

NOISE_FIELDS = {
    "internal_sku", "warehouse_bin", "last_audit_ts", "audit_by",
    "db_row_version", "shard_key", "etag", "query_plan_hash",
    "query_duration_ms", "cache_hit", "replica_id", "index_seek_count",
    "raw_sql_params", "internal_flags"
}


def main():
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    # PostToolUse passes tool_response at top level
    tool_response = hook_data.get("tool_response", {})

    # Try to parse the tool result content
    content = tool_response.get("content", "")
    if isinstance(content, list):
        # content array format
        text_parts = [
            block.get("text", "") for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        raw_text = " ".join(text_parts)
    else:
        raw_text = str(content)

    try:
        result = json.loads(raw_text)
    except (json.JSONDecodeError, ValueError):
        # Not JSON -- nothing to trim
        sys.exit(0)

    if not isinstance(result, dict):
        sys.exit(0)

    # Identify which noise fields are present
    found_noise = [k for k in result if k in NOISE_FIELDS]

    if not found_noise:
        # Nothing to trim
        sys.exit(0)

    # Build trimmed summary
    trimmed = {k: v for k, v in result.items() if k in BUSINESS_FIELDS}

    context = (
        f"NOTE FROM OUTPUT TRIMMER: The raw tool result contained "
        f"{len(found_noise)} internal/system fields that were stripped "
        f"({', '.join(found_noise[:5])}{'...' if len(found_noise) > 5 else ''}). "
        f"Business-relevant summary: {json.dumps(trimmed, ensure_ascii=True)}"
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
