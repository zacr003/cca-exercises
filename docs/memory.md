# Project Memory — cca-exercises

_Running context and state. Updated by `/sync` at end of each session._

---

## What This Project Is

Hands-on coding exercises for the **CCA-F (Claude Certified Architect Foundations)** exam.
Attempt 1: **2026-05-26 — FAILED. 670/1000. Passing threshold: 720/1000.**
Retake: **early retake available now** — the platform migration (confirmed 2026-07-01) waived the 6-month wait. Target window: **July 21 – Aug 1, 2026.** Cert validity once passed: **12 months** from award date. (The original 6-month-wait eligibility of 2026-11-21 is now superseded.)

Each domain maps to a folder of standalone Python scripts (and config/reference files).
Exercises are written for Windows + Git Bash; all Python files include the UTF-8 stdout fix.

The companion wiki lives at `~/Desktop/Ramsey-Brain/` (Obsidian vault).

---

## Current State (as of 2026-07-30)

**⚠️ Retake study sprint is tracked primarily in the companion wiki (`~/Desktop/Ramsey-Brain/`), not here.** This project's own docs/ fell behind (last touched 2026-07-07) while the actual retake grinding — recall-card system, mock exams, domain-page corrections — happened in Ramsey-Brain's `docs/` + `wiki/` + `log.md`. For the full day-by-day retake narrative, read Ramsey-Brain's `docs/memory.md` "Last Session Summary" and `log.md`. This file's job is narrower: track this project's own artifacts (exercises + `html-resource-guide/`).

**Retake sprint status, briefly:** Attempt 1 failed 670/1000 (2026-05-26). Three claudecertificationguide.com mocks: 2026-07-28 = 714/1000 NOT PASSED (D2 20% the whole gap); 2026-07-29 = 720/1000 PASSED (D2 jumped to 60%, D4 dipped to 67%); **2026-07-30 = 907/1000 PASSED, 89%** — big jump, D1/D2/D3 all 100%, D5 now the standalone weakest domain (60%). Still the smaller 28-question "quick exam" variant; the stated readiness gate (56/60) targets the full 60-question version, **planned for 2026-07-31 afternoon**. Real CCA-F retake not yet booked — confidence-gated for Sat 2026-08-01 or Mon 2026-08-03.

**`html-resource-guide/d2-review.html` fully audited + remediated 2026-07-29** — was stale since the 2026-07-14 refresh, teaching an incomplete Edit-recovery fact that had already cost real mock-exam points.

**`CCAF-Scenarios.html` re-audited 2026-07-30** against ~2.5 months of wiki growth (mirrored from the Ramsey-Brain `.md` in lockstep — ~20 new concepts/traps across all 6 scenarios, green "NEW" badge added). **New file `CCAF-AntiPatterns.html` created 2026-07-30** — all ~21 exam anti-patterns grouped by domain (why-it-fails / do-instead per entry) plus a quick-reference table, matching the existing guide's visual style.

## Prior State (as of 2026-07-07)

### Domain Progress

| Domain | Weight | Status | Folder |
|--------|--------|--------|--------|
| 1 — Agentic Architecture | 27% | Complete — D1 HTML quiz 12/12 (100%) | `domain-1/` |
| 2 — MCP Tool Design | 18% | Exercises complete | `domain-2/` |
| 3 — Claude Code Workflows | 20% | Complete — exercises done; practice drill 14/20 (70%); weak spot: probabilistic vs deterministic axis | `domain-3/` |
| 4 — Prompt Engineering | 20% | Exercises complete; Q21–Q50 done (90%); 4.5/4.6 drill done (60%); HTML quiz 11/14 (79%) | `domain-4/` |
| 5 — Context Management | 15% | Exercises complete; bank drill done — 16/20 (80%); weak spots: cache_control after compaction, hybrid summarization, JSON manifest crash recovery | `domain-5/` |

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
| D4 Q21–Q50 drill | 2026-05-13 | **90% (27/30)** | — | — | — | 90% | — |
| D4 4.5/4.6 drill | 2026-05-13 | **60% (6/10)** | — | — | — | 60% | — |
| D5 question bank drill | 2026-05-14 | **80% (16/20)** | — | — | — | — | 80% |
| D4 HTML quiz | 2026-05-13 | **79% (11/14)** | — | — | — | 79% | — |
| Exam 2 (Udemy) | 2026-05-17 | **88% (53/60)** | 88% | 82% | 92% | 83% | 100% |
| T1 targeted drill (5.4/4.2/1.5/4.3) | 2026-05-18 | **85% (17/20)** | — | — | — | — | — |
| D3 bank drill | 2026-05-19 | **70% (14/20)** | — | — | 70% | — | — |
| D3 re-drill (6 misses) | 2026-05-19 | **100% (6/6)** | — | — | 100% | — | — |
| D1 bank drill (15 Qs) | 2026-05-19 | **93% (14/15)** | 93% | — | — | — | — |
| 30Q weighted mixed drill | 2026-05-20 | **80% (24/30)** | 75% | 80% | 83% | 83% | 80% |
| 30Q miss redrill (6 Qs) | 2026-05-20 | **100% (6/6)** | — | — | — | — | — |
| Sparq Q bank (coworker site) | 2026-05-25 | **84% (52/62)** | 80% | 100% | 80% | 73% | 100% |
| D4 in-chat drill | 2026-05-25 | **90% (9/10)** | — | — | — | 90% | — |
| D4 HTML quiz (re-run) | 2026-05-25 | **71% (10/14)** | — | — | — | 71% | — |
| Anthropic Official Mock (attempt 1) | 2026-05-25 | Score lost — Skilljar platform bug | — | — | — | — | — |
| Anthropic Official Mock (attempt 2) | 2026-05-25 | Score lost — Skilljar platform bug | — | — | — | — | — |
| Exam 3 (Udemy) | Not taken — skipped | — | — | — | — | — | — |
| Targeted D4 drill (in-chat) | 2026-05-26 | **90% (9/10)** | — | — | — | 90% | — |
| Mixed drill #1 (in-chat) | 2026-05-26 | **80% (8/10)** | — | — | — | — | — |
| Mixed drill #2 (in-chat) | 2026-05-26 | **100% (10/10)** | — | — | — | — | — |
| Mixed drill #3 (in-chat) | 2026-05-26 | **100% (10/10)** | — | — | — | — | — |
| Exam 3 (Udemy) | 2026-05-26 | **93% (56/60) — PASSED** | 100% | 82% | 92% | 100% | 89% |
| Miss-pattern drill (in-chat) | 2026-05-26 | **100% (5/5)** — Read+Write, stratified sampling, -p/--print | — | — | — | — | — |
| **CCA-F Real Exam** | **2026-05-26** | **FAILED — 670/1000 (67%)** | 75% | 67% | 54% | 33% ("Other") | 75% |

---

## Sprint Milestones

| Date | Milestone |
|------|-----------|
| ~~May 11 (Sun)~~ May 10 | ✅ Udemy Practice Exam 1 — 76% (46/60) |
| May 18 (Sun) | Udemy Practice Exam 2 — timed, full sim |
| May 21 (Thu) | Birthday drill — 30Q mixed |
| May 22–24 | Wedding — off |
| May 25 (Mon) | Anthropic Official Mock + Udemy Exam 3 if time permits |
| **May 26 (Tue)** | **✅ CCA-F Exam — taken; awaiting results** |

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

_Updated by `/sync` at end of each session. Keeps the 3-5 most recent entries; older entries archived to `docs/memory-archive.md` (first rotation: 2026-07-30)._

- 2026-07-30: **CCAF-Scenarios.html re-audit + new CCAF-AntiPatterns.html, alongside a 3rd mock exam PASSED 907/1000 in Ramsey-Brain.** No exercise work this session — activity was in `html-resource-guide/`. (1) The companion wiki's `CCAF-Scenarios.md` (untouched since 2026-05-17) was re-audited against ~2.5 months of growth and gained ~20 new concepts/traps across all 6 scenarios; mirrored here into `CCAF-Scenarios.html` in lockstep (new green "NEW" badge CSS class). (2) Built a new standalone reference, `CCAF-AntiPatterns.html` — every exam anti-pattern (~21) grouped by domain with a why-it-fails box and a do-instead box per entry, plus a quick-reference table, matching the existing guide's sidebar-nav visual pattern. (3) Meanwhile in Ramsey-Brain: a weakest-domain recall drill (D2/D3/D4) ran, then the user took a 3rd mock exam and **passed 907/1000 (89%)**, up from 720 the prior night — D1/D2/D3 all 100%, D5 now the standalone weakest domain (60%). Full detail lives in Ramsey-Brain's `docs/memory.md` and `log.md` per this project's standing convention. Full 60Q mock attempt planned for 2026-07-31 afternoon.
- 2026-07-29: **`d2-review.html` full audit + remediation, then real payoff on a mock exam.** Followed the established audit method (whole-file diff vs. the Ramsey-Brain wiki's `domain-2-mcp-tool-design.md`, not just the one known gap — per the "spot-fixing ≠ auditing" lesson from the 2026-07-14 D2 near-miss). Found and fixed: the Edit-recovery bug in 5 locations including the quiz's own graded answer key (Q8, now correctly rewards expand-context/`replace_all` as the first step, not Read+Write); a regression of the previously-caught `~/.claude/mcp.json`→`~/.claude.json` wrong path; missing `customerFriendlyMessage`/`suggestedAction` error fields; missing `tool_choice` force-then-revert-to-`auto` rule; missing "Coordinator" tool-count tier; missing API-level MCP Connector `authorization_token` section. Quiz expanded 17→21 questions (4 new, covering both of D2's flagged weak patterns). First drill on the fixed quiz: **18/21 (86%)** — 2 of 3 misses were genuine net-new content gaps (SSE-startup-reachability, rate-limiting-server-side), now carded on the wiki side. Then the user retook the **claudecertificationguide.com mock and passed: 720/1000** (up from 714 the prior day) — D2 jumped 20%→60%, direct payoff from this remediation. A live mistake from earlier in that Ramsey-Brain session (batch-vs-sequential feedback ordering) was also caught against the mock's own answer key and corrected on the wiki. Also fixed this project's own `docs/lessons.md`, which still taught the old incomplete Edit-recovery fact — same bug, different file, now corrected everywhere. Recall cards, source pages, and domain-page content all updated on the Ramsey-Brain side; this file and `task-list.md`/`registry.md` brought back in sync here.
- 2026-07-07: **Timeline sync from Ramsey-Brain** (auditing/cleanup only — no study work yet). Reconciled stale status across all docs: Attempt 1 failed 670/1000; **early retake now available** (platform migration waived the 6-month wait), target window **July 21 – Aug 1, 2026** (was 2026-11-21). **"Other" / "Conversational AI Patterns" resolved = D4** (v0.2 exam guide; score-report mislabel, no mystery domain) — closed the related research tasks in task-list and corrected lessons.md. Confirmed 12-month cert validity. Study resumes 7/8 or 7/9, D4/D3 priority. Note: Ramsey-Brain now has 47 recall cards seeded (run "quiz me cca" there).

_Older entries (2026-05-07 through 2026-06-03) archived to `docs/memory-archive.md`._
