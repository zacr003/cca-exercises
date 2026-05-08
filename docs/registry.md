# Registry — cca-exercises

_Map of all exercise files, configs, and dependencies. Updated by `/sync`._

---

## Directory Map

```
cca-exercises/
├── .claude/
│   ├── settings.json          ← Claude Code hooks (PreToolUse / PostToolUse)
│   ├── settings.local.json    ← Local overrides (not committed)
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
| _(none yet)_ | Review-only domain; exercises added if weak spots surface | — |

### Domain 4 — Prompt Engineering (`domain-4/`)

| File | Description | Status |
|------|-------------|--------|
| _(none yet)_ | Targeted exercises based on practice exam results | — |

### Domain 5 — Context Management (`domain-5/`)

| File | Description | Status |
|------|-------------|--------|
| _(none yet)_ | Targeted exercises based on practice exam results | — |

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

_Last updated: 2026-05-08_
