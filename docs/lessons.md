# Lessons — cca-exercises Conventions

_Rules and gotchas specific to this project. Updated by `/sync`._

---

## Python Environment

- **UTF-8 fix**: Every `.py` exercise file includes `sys.stdout.reconfigure(encoding='utf-8')` immediately after imports. Required on Windows to avoid encoding errors when printing Unicode or emoji characters.
- **Python path**: Hooks in `settings.json` use the full absolute path: `C:/Program Files/Python314/python`. Do not rely on `python` or `python3` aliases in hook commands — they may not resolve correctly in the Claude Code hook execution environment.
- **Standalone scripts**: Exercise files are not modules. They run top-to-bottom as `python ex1_agentic_loop.py`. No `if __name__ == "__main__"` guard is strictly required, but including it is fine.

---

## Hook Conventions

- Hook files are named `hook_pre_<purpose>.py` (PreToolUse) and `hook_post_<purpose>.py` (PostToolUse).
- `settings.json` lives at the **cca-exercises root** — not inside domain folders. Claude Code reads it from the project root.
- `settings.local.json` is for local overrides and is not committed.
- Hook commands in `settings.json` use Windows-style paths with forward slashes and quote the Python executable: `"C:/Program Files/Python314/python"`.

---

## MCP / Credential Rules (CCA-F Exam Critical)

- MCP configs must use **`${ENV_VAR}` expansion only** for credentials — never literal token values.
- The Sparq Module 3 examples show literal PAT values in `mcp.json` env blocks. **Those examples are exam-incorrect.** The CCA-F exam requires `${ENV_VAR}` syntax.
- `sample.mcp.json` in `domain-2/` uses the correct pattern and is the reference implementation.

---

## Exercise File Conventions

- Exercises that are reference/config work (no runnable Python) use `.md` format: `ex3_hooks.md`, `ex4_mcp_config.md`, `ex6_session_management.md`.
- Runnable exercises use `.py` format.
- Output files (`ex5_output.txt`) are produced by exercise runs — not hand-authored.

---

## Git

- `hook_debug.log` is excluded via `.gitignore` — it grows large and is not useful in history.
- `__pycache__/` and `*.pyc` are excluded.
- `.env` files are excluded — never commit API keys.

---

## Study Session Workflow (Standard for All Domains)

Each subdomain follows this sequence — do not skip steps:

1. **Concept walkthrough** — Claude explains key concepts, distinctions, and traps for the subdomain
2. **Run the exercise** — execute the `.py` file and capture output
3. **Save output** — write results to `domain-X/outputs/exY_output.txt` so it can be reviewed alongside the code
4. **Multiple choice Q&A** — drill questions from the question bank on that subdomain before moving on

This applies to every subdomain across all domains. For reference-only exercises (`.md` files), skip the run step and go directly to Q&A.

**Output file location:** `domain-X/outputs/exY_output.txt` (create the `outputs/` folder per domain as needed)

---

## Known Gotchas

- The `production/` folder contains `customer_data.txt` with sample PII used by the `hook_post_pii_trim` exercise. This is fake/sample data only — never put real PII here.
- `extract_domain1.sh` is a utility script for extracting domain-1 exercise content; not part of the exercise sequence.
