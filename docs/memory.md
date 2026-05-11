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

## Current State (as of 2026-05-10)

### Domain Progress

| Domain | Weight | Status | Folder |
|--------|--------|--------|--------|
| 1 — Agentic Architecture | 27% | Complete | `domain-1/` |
| 2 — MCP Tool Design | 18% | Exercises complete | `domain-2/` |
| 3 — Claude Code Workflows | 20% | In progress — ex1 done, ex2–ex5 remaining | `domain-3/` |
| 4 — Prompt Engineering | 20% | Exercises created, not started | `domain-4/` |
| 5 — Context Management | 15% | Exercises created, not started | `domain-5/` |

### Exercise Count

| Domain | Files | Notes |
|--------|-------|-------|
| Domain 1 | 7 exercises + 3 hooks | ex1–ex6, hook_pre x2, hook_post x1 |
| Domain 2 | 5 exercises + 1 hook + 1 config | ex1–ex5, hook_post, sample.mcp.json |
| Domain 3 | 5 exercises | ex1–ex4 markdown walkthroughs, ex5 Python (CI/headless) |
| Domain 4 | 5 exercises | ex1–ex5 Python — created, not yet run |
| Domain 5 | 4 exercises | ex1–ex4 Python — created, not yet run |

### Practice Exam Results

| Exam | Date | Score | D1 | D2 | D3 | D4 | D5 |
|------|------|-------|----|----|----|----|-----|
| Exam 1 (Udemy) | 2026-05-10 | **76% (46/60)** | 75% | 82% | 83% | 67% | 78% |
| Exam 2 (Udemy) | 2026-05-18 | — | — | — | — | — | — |
| Exam 3 (Udemy) | 2026-05-19–21 | — | — | — | — | — | — |

---

## Sprint Milestones

| Date | Milestone |
|------|-----------|
| ~~May 11 (Sun)~~ May 10 | ✅ Udemy Practice Exam 1 — 76% (46/60) |
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
- 2026-05-07: Domain 2 exercises scaffolded — ex1–ex5 + hook + sample.mcp.json created
- 2026-05-08: docs/ persistence system and /sync command bootstrapped
- 2026-05-08: Domain 2 exercises run — ex1, ex2, ex3, ex5 executed; outputs saved to domain-2/outputs/; ex4 read as markdown reference
- 2026-05-08: Domain 1 Q&A — 37 questions at 84%; Domain 2 Q&A — all 5 subdomains
- 2026-05-08: Study workflow established — walkthrough → run exercise → save output → Q&A
- 2026-05-10: Domain 3 started — ex1 (CLAUDE.md hierarchy) concept walkthrough complete; `/memory` bug fixed in ex1 and d3-review.html (4 spots)
- 2026-05-10: d1-review.html quiz fixed — answers redistributed from 7x B to even A/B/C/D spread
- 2026-05-10: Practice Exam 1 taken — 76% (46/60); weak spots: D4 (67%), D1 (75%)
- 2026-05-10: Sprint plan updated — Week 2 reoriented to D4 priority; target 83%+ on Exam 2
