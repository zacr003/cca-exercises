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
| `ex1_tool_descriptions.py` | Overlapping tool descriptions, disambiguation | Not started |
| `ex2_tool_errors.py` | Structured errors: isError, errorCategory, isRetryable | Not started |
| `ex3_tool_scope.py` | Right-sizing tool granularity | Not started |
| `ex4_mcp_config.md` | MCP config scopes and credential handling (reference) | Not started |
| `ex5_output_design.py` | Structured output formatting | Not started |
| `hook_post_output_trim.py` | PostToolUse: trims get_product_details output | Not started |
| `sample.mcp.json` | MCP config template with ${ENV_VAR} credential pattern | Not started |

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

_Last updated: 2026-05-13_
