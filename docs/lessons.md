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

- **Primary (curated)**: `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v3.0.0.json` — 242 questions, tiered T1/T2/T3 (58/115/69). Internally named "Streamlined CCA-F curated curriculum v1" — a curated subset of v2.0.0, not a new source bank. 209 questions pulled from v2.0.0; 33 candidate-authored gap-fillers (`anthropic_vetted: false`). Filter by `curated_tier` for prioritized drilling.
- **Broad bank**: `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v2.0.0.json` — 1,489 questions; use when v3 lacks coverage for a subdomain (e.g., D2=6, D5=11 in v3). Filter by `domain_id` (not `domain`).
- D2 and D5 are thin in the curated bank — source bank limitation, not a coverage fix failure.
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

- Read the question bank JSON **directly** using the Read tool — do not spawn an agent to load it. Spawning an agent adds significant latency.
- **Active bank**: `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v3.0.0.json` (242 curated, tiered). Use for targeted drilling; filter by `curated_tier` (1/2/3) or `domain_id`.
- **Broad bank**: `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v2.0.0.json` (1,489 Qs) — use for subdomain coverage when v3 doesn't have enough questions for a domain.
- Read once per session and keep the relevant questions in context.

---

## In-Chat Question Bank Drill Pattern

- **No Python script needed** for question bank drills. Claude reads the JSON directly, filters by `domain_id`, and presents questions one at a time in chat. **Active bank**: v3.0.0 (`cca_f_question_bank_v3.0.0.json`, 242 curated). Fall back to v2.0.0 (1,489 Qs) if v3 lacks coverage for a subdomain.
- Filter field is `domain_id` (integer, e.g. `5`), not `domain` (string).
- Questions are presented one at a time. User answers; Claude scores and explains immediately before moving to the next.
- 20-question batches are the standard for a domain drill session.
- Queue state (unanswered questions + correct answers) is saved to memory file `d5_question_bank_queue.md` when a session is interrupted mid-drill.

---

## CCA-F Exam Intelligence — v3.0.0 Prep Guide (2026-05-16)

From a passed candidate (784/1000, exam taken 2026-05-13). Apply to every practice session.

### Four mental moves (exam-day discipline)
1. **Click the blue scenario box first** — each question has a collapsed blue scenario context box (upper-right). Easy to miss; questions misread without it. Scenario box → stem → options.
2. **Name the symptom axis before evaluating options** — e.g., "agent forgets custom class after N turns" is attention-dilution, not token-budget. Name it first, then discard options addressing the wrong axis.
3. **Translate behavior to mechanism, not parameter name** — exam describes behavior ("agent cuts off after 10 iterations"), not syntax (`max_turns`). Identify the mechanism; pick the option that addresses it.
4. **"Increase context window" is almost never the answer** for forgetting — attention dilution, recency bias, and compaction-induced loss all produce forgetting without exhausting tokens. Right fixes: few-shot examples, scratchpad re-read, periodic summary injection.

### Stem keyword signal
When stem contains **"must," "always," "guarantee,"** or **"before model sees"** → correct answer is **never a system prompt**. Always a hook, programmatic gate, forced tool selection, or JSON schema + strict:true.

### Fabricated hook names — recurring distractors
`PreToolCall` and `OnToolReturn` do not exist. Only `PreToolUse` and `PostToolUse` are valid. Never select a fabricated hook name.

### Practice exam behavior
The official Anthropic practice exam presents the **same 60 questions every attempt** — only scenario order shuffles. Re-taking it yields zero new coverage. Use the curated bank for fresh questions.

### Exam format (Zain, AI Dept lead, 2026-05-15)
Exam is **broad/situational** — scenario-based reasoning, not syntax recall. Zain's exam did NOT test CLAUDE.md file specifics or commands vs skills distinction. Focus on "what do you do in this situation?" not configuration details.

### The 6 official exam scenarios (4 randomly selected per sitting)

| # | Scenario | Core concepts tested |
|---|----------|---------------------|
| 1 | Customer Support Agent | Tool description disambiguation; escalation criteria + few-shot |
| 2 | Code Gen with Claude Code | `context: fork` for verbose skills; plan mode for architectural changes |
| 3 | Claude Code Configuration | `.claude/rules/` glob paths; cross-directory rule activation |
| 4 | Multi-Agent Research System | Coordinator routes through synthesis; structured error propagation; least-privilege tools |
| 5 | CI/CD Integration | `-p` flag for headless mode; Batch API = latency-tolerant only |
| 6 | Structured Data Extraction | Aggregate metrics mask segment failures; stratified analysis before reducing review |

Source: official exam guide v0.1 (Feb 2025). Sample questions: `~/Desktop/Ramsey-Brain/wiki/syntheses/cca-f-sample-questions.md`.

### Question bank to use going forward
`~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v3.0.0.json` — 242 curated questions, tiered 58/115/69. Filter by `curated_tier` (1/2/3). Use v2.0.0 (`cca_f_question_bank_v2.0.0.json`) for broad subdomain drilling.

### Drift scenarios (rotation hedge — not in official 6)
- Conversational AI Patterns (appeared on n=1 form)
- Long Document Processing
- Agent Skills (Enterprise KM / Developer Tooling / Code Execution)
- Claude for Operations / Agentic Tool Design

---

## MCP Resources vs Tools (CCA-F Exam Critical — surfaced 2026-05-17)

- **Resources** = read-only, reference data (catalogs, policy lists, static configs). No tool call overhead; agent references them directly.
- **Tools** = actions and dynamic lookups that change state or require live computation.
- If an agent repeatedly calls a "list_X" tool for stable reference data → convert to an MCP resource.
- Forcing a first-turn `tool_choice` to load catalogs is wrong — it still burns a tool call turn and doesn't solve the overhead problem.

---

## Extraction Reliability — Missing Source Pattern (CCA-F Exam Critical — surfaced 2026-05-17)

- When a required field is absent because the **source document was never provided**, retrying is harmful — it produces hallucinated values.
- Correct pattern: **detect absence → halt retries → mark incomplete → request the missing document**.
- "Infer from nearby dates" = fabrication. "Retry with explicit prompts" = majority vote on hallucinations. Both are wrong.
- Rule: **missing source is a pipeline input problem, not an extraction problem**.

---

## Subagent Tool Scoping — Least Privilege in Practice (CCA-F Exam Critical — surfaced 2026-05-17)

- **Read-only tools can and should be delegated** to subagents that need them frequently. Forcing coordinator round trips for read-only data is unnecessary latency.
- **State-changing tools** (`process_refund`, `escalate_to_human`, etc.) stay coordinator-only — centralized oversight of actions that modify backend state.
- "Keep all tools coordinator-only" is wrong when it causes avoidable round trips for reads.
- "Give all subagents all tools" eliminates the control layer entirely — wrong.

---

## Session Management — Resume + Targeted Revalidation (surfaced 2026-05-17)

- When files have changed since a named session was last active: **resume the session + revalidate only the changed files**.
- Do NOT start a fresh session — that discards valid prior analysis on unchanged files.
- Do NOT proceed unchanged — stale assumptions on modified files are dangerous.
- A single "confidence score" is not a substitute for targeted revalidation — it doesn't tell you which assumptions are stale.

---

## Structured Output — Two Tools vs anyOf (CCA-F Exam Critical — surfaced 2026-05-18)

- When different activity/entity types need different required fields (e.g., cardio needs time+distance, strength needs reps+weight), **splitting into two tools is stronger than a single tool with an `anyOf` schema**.
- **Two tools** = tool-selection enforcement. The cardio tool structurally cannot accept reps/weight. The model picks the tool; the schema does the rest.
- **anyOf** = right layer, weaker mechanism. Complex conditional schemas are harder for the model to adhere to; failures still hit server-side validation after the call is made (turns into a retry loop).
- Rule: **when you can make it a routing problem, do that — don't make it a schema validation gamble**.

---

## Batch API — Blocking vs Latency-Tolerant (reinforced 2026-05-18, clarified 2026-05-20)

The single criterion: **does something block on this completing right now?**

- Pre-merge CI checks → block developers → **synchronous**
- Nightly test generation → runs overnight, nobody is waiting → **Batch**
- Weekly security audits → scheduled, not blocking → **Batch**

Common miss: treating "nightly" as synchronous because it's automated. Nightly = latency-tolerant. If a developer isn't waiting on it, it's Batch.

**Exam signal for Batch API eligibility (clarified 2026-05-20):**
The exam uses an **explicitly stated hard deadline** as the signal for synchronous, not the operational window.
- Hard deadline named (e.g., "must complete by Tuesday 9am") → check if 24h window leaves buffer; if not → **synchronous**
- No hard deadline stated (e.g., "nightly", "weekly", "runs overnight") → **Batch API eligible**
- Real-world concern ("nightly window is only 12 hours") is valid in ops but irrelevant on the exam — the exam grades against the documented rule, not operational constraints.

---

## D3 Exam Traps — Surfaced 2026-05-19

**Probabilistic vs. deterministic axis** — the single most common D3 miss pattern:
- `PostToolUse` hook = automatic, harness-enforced, fires after every tool call ✓
- CLAUDE.md instruction = probabilistic, model can forget or skip ✗
- Slash command = requires manual user invocation, not automatic ✗
- When stem says "automatically" or "without adding to every prompt" → hook is the answer

**Prior findings in context for re-review runs (3.6):**
- When a re-review produces duplicate findings on already-fixed code: include prior findings in context and instruct Claude to report only new/still-unaddressed issues
- Post-processing string-match filters are brittle — small wording changes evade dedup and don't help Claude understand what was fixed
- Rule: **in-context awareness beats downstream filters**

**Interacting problems → single message (3.5):**
- When two failures share a code path (e.g., same helper function), fixing them sequentially risks introducing another regression on the shared path
- Signal: "the regression was introduced by Claude's previous fix" = interacting
- Signal: "fixing one won't affect the other" = independent → sequential
- Rule: **shared code path = single message**

**Generic tool misuse → constrained replacement (D1/D3 crossover):**
- When a generic tool (e.g., `fetch_url`) is being misused (agent uses it as a backdoor search), the fix is a constrained replacement (`load_document` that validates URL format)
- Domain-blocklists are brittle; prompt instructions are bypassable
- Routing around it (through coordinator) doesn't enforce the constraint at the call site
- Rule: **structural enforcement at the tool level, not routing or instructions**

**Constraint elimination technique (Q7 pattern):**
- When a question lists a stakeholder constraint ("no filtering before developer review"), scan all options first and eliminate any that violate the constraint before reading explanations
- A and C both filtered findings → eliminated immediately regardless of how reasonable they sounded

---

## Explicit Criteria vs Few-Shot Examples — Decision Rule (locked in 2026-05-26)

When the problem is **missing definition** → explicit criteria first
- "Check that comments are accurate" → not actionable → add: "flag when claimed behavior contradicts actual code behavior"
- "Classify sentiment" → undefined → add: "classify as negative when message expresses dissatisfaction regardless of tone"

When the problem is **inconsistent application of a known target** → few-shot examples
- Detailed instructions don't consistently work → switch to examples
- Prose produces different interpretations each turn → concrete input/output examples

**The sequence:** missing definition → criteria → inconsistency persists → examples → never "more instructions"

**Exam signal table:**
- "Vague instruction", "doesn't define what qualifies" → explicit criteria
- "Instructions already added, still inconsistent", "prose produces different results" → few-shot examples
- "Detailed instructions don't consistently work" → few-shot examples

---

## Prerequisite Gates for Required Workflow Ordering (surfaced 2026-05-26)

- When a step must always happen before a downstream step: **coordinator-side prerequisite gate** that blocks the downstream Task call until the required artifact exists
- Prompt instructions alone have a non-zero failure rate for required ordering — not acceptable for guaranteed compliance
- Parsing natural language signals ("complete", "ready") to determine loop behavior = documented anti-pattern
- PreToolUse hook = blocks a tool until a condition is met (single agent)
- Coordinator prerequisite gate = blocks a subagent Task call until upstream artifact is confirmed

---

## Coordinator Decomposition Coverage (surfaced 2026-05-26)

- When broad codebase/research coverage is incomplete despite all subagents completing: the **coordinator's decomposition was too narrow**
- Subagents did their jobs — they only covered what the coordinator assigned them
- Fix: revise coordinator planning to identify ALL plausible entry points before delegating
- Strengthening synthesis to "infer missing workflows" produces confident fabrication — not a fix

---

## Stratified Sampling Before Reducing Review (surfaced 2026-05-26)

- Aggregate accuracy metrics (e.g., 97% overall) can mask concentrated errors in specific segments
- Before reducing reviewer coverage: stratified random sampling across topic, source type, and report section
- Detects hidden error rates and novel failure patterns that aggregate metrics miss
- Reviewing only low-confidence claims assumes high-confidence = no errors — incorrect

---

## Plan Mode Triggers (reinforced 2026-05-26)

Use plan mode when:
- Large-scale changes affecting many files
- Multiple valid implementation approaches exist
- Architectural decisions need to be made
- Task requirements are ambiguous or underspecified

Do NOT start with direct execution and switch to plan mode later — costs rework.

---

## CI Structured Output — `--output-format json --json-schema` (surfaced 2026-05-26)

- For reliable CI automation, use `--output-format json` + `--json-schema` flags
- Guarantees field names and types programmatically — stronger than prompt instructions
- Stronger prompt wording is still probabilistic; schema flags are deterministic
- Regex parsing on variable markdown output is fragile — replace with structured output flags

---

## PostToolUse Hook vs Wrapper Tools — Normalization Pattern (surfaced 2026-05-25)

- When normalizing data from mixed-format tools (some third-party, unmodifiable): **PostToolUse hook is more maintainable than wrapper tools**
- Hook = one centralized transformation layer, works on all tools including third-party
- Wrapper tools = two strategies (modify owned + wrap third-party) = two places to maintain, inconsistent architecture
- The deciding criterion is **maintainability**, not correctness — both approaches work; hook wins on maintenance burden
- Trap: C (wrapper tools) sounds like clean architecture but creates dual strategy when third-party tools are involved

---

## Tool Misrouting — Fix Descriptions First (reinforced 2026-05-25)

- Consistent wrong tool selection → **examine and fix tool descriptions first**, always
- Overlapping descriptions (near-identical wording) → rename + rewrite at source; don't add routing layers or classifiers
- Pre-routing classifiers and few-shot examples both treat the symptom; description fix eliminates the root cause
- Examining descriptions is the diagnostic step; rewriting is the fix

---

## Coordinator Pattern — Hub-and-Spoke Benefits (reinforced 2026-05-25)

- The primary advantage of routing through a coordinator (vs. direct subagent-to-subagent): **centralized visibility, consistent error handling, controlled information flow**
- Not serialization, not batching, not automatic retry — those are distractors
- Hub-and-spoke = coordinator sees everything, handles errors in one place, decides what each subagent receives

---

## Edit Fallback — Non-Unique Anchor (surfaced 2026-05-26 drill)

- When `Edit` fails because the anchor text appears multiple times in the file: **do not Grep + replace-all**
- Correct pattern: `Read` the full file → identify the intended block by surrounding context → `Write` the complete corrected file
- Grep + replace-all changes every occurrence — violates the requirement to change only one
- Retrying `Edit` with broader text still doesn't guarantee hitting the right occurrence
- Rule: **ambiguous anchor → full-file Read + Write**

---

## -p / --print vs --output-format json (CI interactivity — reinforced 2026-05-26 drill)

- **`-p` / `--print`** = non-interactive execution mode — Claude Code processes prompt, writes output, exits. Fixes CI hangs caused by interactive mode.
- **`--output-format json`** = structured output format for machine parsing. Does NOT change whether the process waits for input.
- These solve different problems. A CI hang = interactivity issue = use `--print`. Machine-parseable output = use `--output-format json`. Both can be combined when both are needed.
- Trap: `--output-format json` sounds like it controls process behavior — it does not.

---

## Passing Threshold — Confirmed 2026-05-26

- **720/1000 (72%) to pass the real CCA-F exam**
- Colleagues passing at 749, 780, 791 — no scores above 800 observed in this cohort
- The "90% required" framing circulating pre-exam is **incorrect**
- Practice exam scores of 80%+ are comfortably above threshold

---

## D5 Exam Traps — Surfaced 2026-05-14

- **cache_control after compaction**: Compaction replaces conversation history with a new summary block. That block is new content — no cache hit. Fix: explicitly add a `cache_control` breakpoint to the compaction block so future requests hit the cache. Without it, every post-compaction request is a cache miss.
- **Hybrid summarization (5.4)**: Correct pattern is summarize older messages + keep recent ones verbatim. Summarizing *every turn* (including recent ones) is lossy and unnecessary. Vector search retrieves but doesn't retain — not the same as summarization.
- **JSON manifest for crash recovery (5.4)**: When a subagent crashes, the fix is a periodic JSON manifest (goal + processed files + key entities) the coordinator injects on resume. Re-establishing a connection (API keys, session tokens) does not restore *state*.
- **PDF automation in tiered review (5.5)**: If a source meets the accuracy target, fully automate it. Stratified sampling on a source that already clears the threshold is unnecessary overhead — it's a monitoring pattern, not an initial design choice.
- **CCA-F study resources**: Topics not in exercises → `docs.anthropic.com` (prompt caching, long context best practices). Question bank explanations (if present in JSON) are the fastest targeted review per miss.
