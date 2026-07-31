# Registry — cca-exercises

_Map of all exercise files, configs, and dependencies. Updated by `/sync`._

---

## Directory Map

```
cca-exercises/
├── .claude/
│   ├── settings.json          ← Claude Code hooks (PreToolUse / PostToolUse)
│   ├── settings.local.json    ← Local overrides (gitignored — not committed)
│   └── commands/
│       └── sync.md            ← /sync slash command
├── docs/                      ← Session persistence (this system)
│   ├── memory.md              ← Running context and state
│   ├── lessons.md             ← Conventions and gotchas
│   ├── task-list.md           ← Exercise backlog
│   └── registry.md            ← This file
├── domain-1/                  ← Agentic Architecture exercises (complete)
├── domain-2/                  ← MCP Tool Design exercises (complete)
├── production/                ← Scratch / simulation area
├── .gitignore
└── extract_domain1.sh
```

---

## Exercise Registry

### Domain 1 — Agentic Architecture (`domain-1/`)

| File | Description | Status |
|------|-------------|--------|
| `ex1_agentic_loop.py` | Basic agentic loop: stop_reason, tool_result blocks, max_tokens | Complete |
| `ex1b_parallel_tools.py` | Parallel tool calls in one response | Complete |
| `ex2_coordinator_subagents.py` | Coordinator + 2 subagents, explicit context passing | Complete |
| `ex3_hooks.md` | PreToolUse / PostToolUse hook patterns (reference) | Complete |
| `ex4_tool_sequencing.py` | Ordered multi-tool orchestration | Complete |
| `ex5_task_decomposition.py` | Task decomposition across agentic steps | Complete |
| `ex6_session_management.md` | Session management patterns (reference) | Complete |
| `hook_pre_production_gate.py` | PreToolUse: blocks Write/Edit in production scope | Complete |
| `hook_pre_refund_gate.py` | PreToolUse: intercepts process_refund tool calls | Complete |
| `hook_post_pii_trim.py` | PostToolUse: strips PII from all tool outputs | Complete |

### Domain 2 — MCP Tool Design (`domain-2/`)

| File | Description | Status |
|------|-------------|--------|
| `ex1_tool_descriptions.py` | Overlapping tool descriptions, disambiguation | Complete |
| `ex2_tool_errors.py` | Structured errors: isError, errorCategory, isRetryable | Complete |
| `ex3_tool_scope.py` | Right-sizing tool granularity | Complete |
| `ex4_mcp_config.md` | MCP config scopes and credential handling (reference) | Complete |
| `ex5_output_design.py` | Structured output formatting | Complete |
| `hook_post_output_trim.py` | PostToolUse: trims get_product_details output | Complete |
| `sample.mcp.json` | MCP config template with ${ENV_VAR} credential pattern | Complete |

### Domain 3 — Claude Code Workflows (`domain-3/`)

| File | Description | Status |
|------|-------------|--------|
| `ex1_claude_md.md` | CLAUDE.md hierarchy — 3 scopes, @import, conflict resolution | Complete |
| `ex2_skills_commands.md` | Skills and slash commands — context:fork, allowed-tools, argument-hint | Complete |
| `ex3_path_scoped_rules.md` | Path-scoped rules — YAML paths frontmatter, glob patterns | Complete |
| `ex4_plan_mode.md` | Plan mode — decision framework, iterative refinement, Explore subagent | Complete |
| `ex5_ci_headless.py` | CI/headless mode — -p flag, --output-format json, --bare | Complete |
| `outputs/ex5_output.txt` | ex5 script run output | Complete |

### Domain 4 — Prompt Engineering (`domain-4/`)

| File | Description | Status |
|------|-------------|--------|
| `ex1_few_shot.py` | Few-shot prompting — vague vs explicit vs contrastive examples | Complete |
| `ex2_structured_output.py` | Structured output — JSON schema, nullable fields, enum+other | Complete |
| `ex3_tool_choice.py` | tool_choice — auto vs any vs forced, first-turn-then-auto; bug fixed 2026-05-11 | Complete |
| `ex4_batch_api.py` | Batch API — submit, poll, correlate via custom_id | Complete |
| `ex5_retry_feedback.py` | Retry-with-feedback — error feedback loop, retry limits | Complete |
| `d4_session.json` | Practice question bank session state (not committed) | Active |

### Domain 5 — Context Management (`domain-5/`)

| File | Description | Status |
|------|-------------|--------|
| `ex1_long_context.py` | Long context — lost-in-the-middle, key findings at top | Complete |
| `ex2_escalation.py` | Escalation — explicit criteria + few-shot, frustrated user pattern | Complete |
| `ex3_context_degradation.py` | Context degradation — API statelessness, scratchpad files | Complete |
| `ex4_error_propagation.py` | Error propagation — structured errors, multi-agent recovery | Complete |

### Production / Scratch (`production/`)

| File | Description |
|------|-------------|
| `customer_data.txt` | Sample PII data used in hook_post_pii_trim exercises |
| `test.txt` | Scratch file |

### HTML Resources (`html-resource-guide/`)

| File | Description | Status |
|------|-------------|--------|
| `pre-exam-summary.html` | Pre-exam reference card — mental moves, miss patterns, domain anchors, distinctions table, anti-patterns | Created 2026-05-26 |
| `d1/d3/d4/d5-review.html` | Domain study guides, downstream renderings of the Ramsey-Brain wiki domain pages | Last full audit 2026-07-14 — due for a refresh (wiki has advanced since, incl. D1/D3/D5 content from 2026-07-29 and D4/D5 content from 2026-07-30) |
| `d2-review.html` | Domain 2 study guide | **Fully audited + remediated 2026-07-29** (2nd full audit; 1st was 2026-07-14). Fixed 5 issues (Edit-recovery bug in 5 spots incl. graded quiz answer, `~/.claude.json` path regression, missing error fields, missing tool_choice rule, missing Coordinator tier, missing API-connector section) + expanded quiz 17→21 questions. Confirmed internally consistent (all 4 hardcoded quiz-count bookkeeping spots). |
| `CCAF-Scenarios.html` | Reference for all 6 exam scenarios — domains tested, key concepts, exam traps, clarifying insight per scenario | Created earlier; **re-audited 2026-07-30** against ~2.5 months of wiki growth — ~20 new concepts/traps mirrored from `wiki/cca/CCAF-Scenarios.md` in lockstep, new green "NEW" badge CSS class added |
| `CCAF-AntiPatterns.html` | All ~21 CCA-F exam anti-patterns grouped by domain (D1–D5), each with a why-it-fails box and a do-instead box, plus a quick-reference table | **Created 2026-07-30** — compiled from the v1.0 exam guide's task-statement anti-pattern callouts + domain-page corroborating detail |

### Root (`cca-exercises/`)

| File | Description |
|------|-------------|
| `drill_30q.txt` | Generated 30Q weighted mixed drill questions (temp; regenerated each session) |

---

## External Practice Resources

_Independent third-party prep sites — useful as **weak-spot finders, NOT readiness signals** (see lessons.md: Udemy scores did not predict real-exam performance). Verify answer keys against the domain wiki; do not absorb blindly. The official Anthropic practice exam remains the only trusted readiness proxy._

| Resource | URL | Notes |
|----------|-----|-------|
| CCA Practice Platforms — Readiness Diagnostic | https://www.claudecertifiedarchitects.com/diagnostic/ | Shared in Slack 2026-07-07. Free, no account, 10 scenario Qs across all 5 domains (~5 min). **Verified accurate** vs. official v0.2 guide: domains, weights (27/20/20/18/15), passing score (720/1000), 60-Q format all correct; clearly disclaims Anthropic affiliation. Answer-key quality **unverified** (paid $49 upsell for a 400-Q platform). Use as a diagnostic only. |

---

## Tools & Dependencies

| Tool | Purpose |
|------|---------|
| Python 3.14 | All exercise scripts |
| Anthropic Python SDK | API calls in Domain 1 & 2 exercises |
| Claude Code | Hook execution, /sync command |
| Git Bash | Shell environment (Windows) |

### Python Path (Windows)

```
C:/Program Files/Python314/python
```

Used explicitly in `.claude/settings.json` hook commands.

---

## Hook Configuration (`.claude/settings.json`)

| Hook | Trigger | File |
|------|---------|------|
| PreToolUse | Write\|Edit | `domain-1/hook_pre_production_gate.py` |
| PreToolUse | process_refund | `domain-1/hook_pre_refund_gate.py` |
| PostToolUse | `.*` (all) | `domain-1/hook_post_pii_trim.py` |
| PostToolUse | get_product_details | `domain-2/hook_post_output_trim.py` |

---

_Last updated: 2026-07-30 (CCAF-Scenarios.html re-audit + new CCAF-AntiPatterns.html — see HTML Resources table)_
