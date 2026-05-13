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

## Current State (as of 2026-05-13)

### Domain Progress

| Domain | Weight | Status | Folder |
|--------|--------|--------|--------|
| 1 — Agentic Architecture | 27% | Complete | `domain-1/` |
| 2 — MCP Tool Design | 18% | Exercises complete | `domain-2/` |
| 3 — Claude Code Workflows | 20% | Complete — all exercises done; practice Qs not started | `domain-3/` |
| 4 — Prompt Engineering | 20% | Exercises complete; practice Qs in progress (20/50, 80%) | `domain-4/` |
| 5 — Context Management | 15% | Exercises complete; 20 bank Qs queued (paused at Q1) | `domain-5/` |

### Exercise Count

| Domain | Files | Notes |
|--------|-------|-------|
| Domain 1 | 7 exercises + 3 hooks | ex1–ex6, hook_pre x2, hook_post x1 |
| Domain 2 | 5 exercises + 1 hook + 1 config | ex1–ex5, hook_post, sample.mcp.json |
| Domain 3 | 5 exercises + 1 outputs dir | ex1–ex4 markdown walkthroughs, ex5 Python (CI/headless); all complete |
| Domain 4 | 5 exercises | ex1–ex5 Python — all run; ex3 bug fixed (tool_choice object format) |
| Domain 5 | 4 exercises | ex1–ex4 Python — all run 2026-05-12 |

### Practice Exam Results

| Exam | Date | Score | D1 | D2 | D3 | D4 | D5 |
|------|------|-------|----|----|----|----|-----|
| Exam 1 (Udemy) | 2026-05-10 | **76% (46/60)** | 75% | 82% | 83% | 67% | 78% |
| D4 question bank drill | 2026-05-11 | **80% (16/20)** | — | — | — | 80% | — |
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

- 2026-05-13: D3 all 5 exercises complete — ex2 (skills/commands, 90%), ex3 (path-scoped rules, 90%), ex4 (plan mode, 80%), ex5 (CI/headless, 70%); all concept walkthroughs + drills done
- 2026-05-13: D3 weak spots — plan mode cannot gate mid-execution (PreToolUse hook is the answer); prior findings in context for re-review runs; inline confidence for triage efficiency
- 2026-05-13: ex5_ci_headless.py fixed — UTF-8 reconfigure added; domain-3/outputs/ex5_output.txt created
- 2026-05-13: .claude/settings.local.json added to .gitignore and untracked from git
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
- 2026-05-11: D4 all 5 exercises run — ex1 (few-shot), ex2 (structured output), ex3 (tool_choice), ex4 (batch API), ex5 (retry feedback); 14/15 on exercise Q&A
- 2026-05-11: ex3_tool_choice.py bug fixed — bare strings ("auto","any") replaced with object format ({"type":"auto"}) per API requirement
- 2026-05-11: d4-review.html updated — Ex6 Multi-Instance Review tab added; quiz expanded 12→14 questions
- 2026-05-11: D4 question bank drill started — 20/50 done (80%); misses: Q3 system prompt keyword bias, Q5 parallel decomp vs few-shot, Q12 batch polling backoff, Q20 detected_pattern as string
- 2026-05-11: Question bank v2.0.0 located at ~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v2.0.0.json (1,489 Qs; 333 D4)
- 2026-05-12: D5 all 4 exercises complete — ex1 (long context), ex2 (escalation), ex3 (context degradation), ex4 (error propagation); all walkthroughs + runs + Q&A done
- 2026-05-12: D5 exercise Q&A scores — ex1: 2/3, ex2: 2/3, ex3: 3/3, ex4: 3/3; weak spots: empty result vs. error distinction (5.3), handoff summary content (5.2)
- 2026-05-12: D5 bank question drill — 20 random questions pulled and saved to memory; paused at Q1 (none answered yet); in-chat drill format (no Python script)
- 2026-05-12: In-chat question bank drill pattern established — Claude reads JSON directly, filters by domain_id, presents one question at a time; no Python script required
