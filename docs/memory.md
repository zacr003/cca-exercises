# Project Memory — cca-exercises

_Running context and state. Updated by `/sync` at end of each session._

---

## What This Project Is

Hands-on coding exercises for the **CCA-F (Claude Certified Architect Foundations)** exam.
Target exam date: **2026-05-27**.

Each domain maps to a folder of standalone Python scripts (and config/reference files).
Exercises are written for Windows + Git Bash; all Python files include the UTF-8 stdout fix.

The companion wiki lives at `~/Desktop/Ramsey-Brain/` (Obsidian vault).

---

## Current State (as of 2026-05-08)

### Domain Progress

| Domain | Weight | Status | Folder |
|--------|--------|--------|--------|
| 1 — Agentic Architecture | 27% | Complete | `domain-1/` |
| 2 — MCP Tool Design | 18% | Not started | `domain-2/` |
| 3 — Claude Code Workflows | 20% | Not started | `domain-3/` |
| 4 — Prompt Engineering | 20% | Not started | `domain-4/` |
| 5 — Context Management | 15% | Not started | `domain-5/` |

### Exercise Count

| Domain | Files | Notes |
|--------|-------|-------|
| Domain 1 | 7 exercises + 3 hooks | ex1–ex6, hook_pre x2, hook_post x1 |
| Domain 2 | 5 exercises + 1 hook + 1 config | ex1–ex5, hook_post, sample.mcp.json |
| Domain 3 | 0 | Review-only domain (daily Claude Code work) |
| Domain 4 | 0 | Question drilling + targeted exercises |
| Domain 5 | 0 | Question drilling + targeted exercises |

---

## Sprint Milestones

| Date | Milestone |
|------|-----------|
| May 11 (Sun) | Udemy Practice Exam 1 — timed, full sim |
| May 18 (Sun) | Udemy Practice Exam 2 — timed, full sim |
| May 19–21 | Udemy Practice Exam 3 + weak spot review |
| May 26 (Tue) | Refresh day — no new exercises |
| **May 27 (Wed)** | **CCA-F Exam** |

---

## Key File Locations

| Resource | Path |
|----------|------|
| This file | `docs/memory.md` |
| Task list | `docs/task-list.md` |
| File registry | `docs/registry.md` |
| Conventions | `docs/lessons.md` |
| Sync command | `.claude/commands/sync.md` |
| Claude Code hooks config | `.claude/settings.json` |
| Companion wiki | `~/Desktop/Ramsey-Brain/` |

---

## Last Session Summary

_Updated by `/sync` at end of each session._

- 2026-05-07: Domain 1 exercises complete — ex1 (agentic loop), ex1b (parallel tools), ex2 (coordinator/subagents), ex3 (hooks), ex4 (tool sequencing), ex5 (task decomposition), ex6 (session management)
- 2026-05-07: Domain 1 hooks built — hook_pre_production_gate, hook_pre_refund_gate, hook_post_pii_trim
- 2026-05-07: Domain 2 exercises complete — ex1 (tool descriptions), ex2 (tool errors), ex3 (tool scope), ex4 (MCP config reference), ex5 (output design)
- 2026-05-07: Domain 2 hook built — hook_post_output_trim; sample.mcp.json created
- 2026-05-08: docs/ persistence system and /sync command bootstrapped
