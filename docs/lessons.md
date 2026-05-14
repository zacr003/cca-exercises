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
- `.claude/settings.local.json` is excluded — added 2026-05-13. Local overrides only; was accidentally tracked before.

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

## /memory Command Behavior

- `/memory` **opens** the active CLAUDE.md for editing — it does NOT list loaded files.
- To diagnose which CLAUDE.md and rules files are currently loaded, ask Claude directly: "Which CLAUDE.md files are you currently loading?"
- The d3-review.html and ex1_claude_md.md originally had this wrong — both corrected 2026-05-10.

---

## tool_choice API Format

- `tool_choice` must always be an **object**, not a bare string. The Anthropic SDK rejects bare strings with a 400 error.
- Correct: `{"type": "auto"}`, `{"type": "any"}`, `{"type": "tool", "name": "X"}`, `{"type": "none"}`
- Wrong: `"auto"`, `"any"`, `"none"`
- Discovered 2026-05-11 when ex3_tool_choice.py failed on first run. Fixed in that file.

### tool_choice Exam Trap — `any` vs `auto`

- **`auto`** — model may call a tool OR return plain text; tool call is optional
- **`{"type": "any"}`** — model **must** call a tool, picks which one from available tools
- Use `any` when: document type unknown, multiple valid tools, extraction is required
- Use `auto` when: tool call is optional and text response is acceptable
- Forced selection `{"type": "tool", "name": "X"}` requires knowing the right tool in advance

---

## Structured Output — Semantic Validation Trap

- JSON schema validates **syntax only** (field names, types, required fields)
- Cross-field consistency (e.g., total = sum of line items) must be checked in **application-layer code**
- `conflict_detected` field relies on the model setting it correctly — always add your own semantic validation
- Rule: **schema = syntax; your code = semantics**

---

## Question Bank Location

- Full question bank: `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v2.0.0.json`
- 1,489 questions total; filter by `domain_id` (not `domain`) for per-domain drills
- D4: 333 questions across subdomains 4.1–4.6
- Session state saved to `domain-X/dX_session.json` (not committed — transient)
- Resume a drill by reading `dX_session.json` for `current` index and `score`

---

## Known Gotchas

- The `production/` folder contains `customer_data.txt` with sample PII used by the `hook_post_pii_trim` exercise. This is fake/sample data only — never put real PII here.
- `extract_domain1.sh` is a utility script for extracting domain-1 exercise content; not part of the exercise sequence.
- Question bank drills: **20 questions per domain** is the standard batch size. Updated 2026-05-14 (previously 60 for D2, 50 for D3, 60–80 for D1 — all reduced to 20).

---

## Question Bank Drill — Interruption Handling

- When the user asks a question mid-drill (e.g., "what domain is this from?"), answer it and then **re-show the full question** before continuing. Do not just say "still waiting on your answer" — the user may not have the question visible anymore.

---

## Commands vs Skills (CCA-F Exam Critical)

- **Commands** = markdown files in `.claude/commands/` — no frontmatter, no isolation, injected into current session on invocation
- **Skills** = markdown files in `.claude/skills/` — optional frontmatter: `context: fork`, `allowed-tools`, `argument-hint`; `context: fork` runs in isolated sub-agent
- Both are invoked with `/name` syntax — they feel identical from the outside
- `/sync` is a **command**, not a skill (lives in `~/.claude/commands/sync.md`)
- Only three valid SKILL.md frontmatter fields: `context: fork`, `allowed-tools`, `argument-hint` — `model:` and `override:` do not exist

---

## Plan Mode vs Extended Thinking (CCA-F Exam Critical)

- **Plan mode** = Claude Code feature activated by `/plan` or `Shift+Tab` — read-only, no file changes, used for pre-execution review
- **Extended thinking** = Anthropic API feature — `thinking: {type: "enabled", budget_tokens: N}` — deeper internal reasoning before responding
- These are completely separate features at different layers — conflating them costs exam points
- Module 2 (Sparq) calls `/plan` "extended thinking mode" — **use CCA-F language ("plan mode") in exam context**

---

## Batch API — Key Formulas (4.5)

- **Max submission interval** = SLA − batch processing window (24h)
  - Example: 30h SLA → max interval = 30 − 24 = 6 hours
- **With retries**: interval + (24h × number of passes) ≤ SLA; retry batch submits immediately after first batch completes
  - Example: 60h SLA, 2 passes → interval + 48 ≤ 60 → max interval = 12 hours
- **Batch API cannot do multi-turn tool calling** — two-step workflows (extract then validate) require two sequential batches
- **Batch = latency-tolerant, non-blocking workloads** — never use for blocking CI checks or synchronous workflows

---

## Question Bank Drill — Loading Method

- Read the question bank JSON **directly** using the Read tool — do not spawn an agent to load it. Spawning an agent adds significant latency. The file is at `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v2.0.0.json`. Read it once per session and keep the relevant questions in context.

---

## In-Chat Question Bank Drill Pattern

- **No Python script needed** for question bank drills. Claude reads the JSON directly (`~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v2.0.0.json`), filters by `domain_id`, and presents questions one at a time in chat.
- Filter field is `domain_id` (integer, e.g. `5`), not `domain` (string).
- Questions are presented one at a time. User answers; Claude scores and explains immediately before moving to the next.
- 20-question batches are the standard for a domain drill session.
- Queue state (unanswered questions + correct answers) is saved to memory file `d5_question_bank_queue.md` when a session is interrupted mid-drill.
