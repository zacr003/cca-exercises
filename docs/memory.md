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

## Current State (as of 2026-07-29)

**⚠️ Retake study sprint is tracked primarily in the companion wiki (`~/Desktop/Ramsey-Brain/`), not here.** This project's own docs/ fell behind (last touched 2026-07-07) while the actual retake grinding — recall-card system, mock exams, domain-page corrections — happened in Ramsey-Brain's `docs/` + `wiki/` + `log.md`. For the full day-by-day retake narrative, read Ramsey-Brain's `docs/memory.md` "Last Session Summary" and `log.md`. This file's job is narrower: track this project's own artifacts (exercises + `html-resource-guide/`).

**Retake sprint status, briefly:** Attempt 1 failed 670/1000 (2026-05-26). Two claudecertificationguide.com mocks taken one day apart: 2026-07-28 = 714/1000 NOT PASSED (D2 20% the whole gap); **2026-07-29 = 720/1000 PASSED** (D2 jumped to 60%, D4 dipped to 67% — new drill target). This is the smaller 28-question "quick exam" variant; the stated readiness gate (56/60) targets the full 60-question version, not yet confirmed. Real CCA-F retake not yet booked — confidence-gated for Sat 2026-08-01 or Mon 2026-08-03.

**`html-resource-guide/d2-review.html` fully audited + remediated 2026-07-29** (see Last Session Summary below) — was stale since the 2026-07-14 refresh, teaching an incomplete Edit-recovery fact that had already cost real mock-exam points.

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

_Updated by `/sync` at end of each session._

- 2026-07-29: **`d2-review.html` full audit + remediation, then real payoff on a mock exam.** Followed the established audit method (whole-file diff vs. the Ramsey-Brain wiki's `domain-2-mcp-tool-design.md`, not just the one known gap — per the "spot-fixing ≠ auditing" lesson from the 2026-07-14 D2 near-miss). Found and fixed: the Edit-recovery bug in 5 locations including the quiz's own graded answer key (Q8, now correctly rewards expand-context/`replace_all` as the first step, not Read+Write); a regression of the previously-caught `~/.claude/mcp.json`→`~/.claude.json` wrong path; missing `customerFriendlyMessage`/`suggestedAction` error fields; missing `tool_choice` force-then-revert-to-`auto` rule; missing "Coordinator" tool-count tier; missing API-level MCP Connector `authorization_token` section. Quiz expanded 17→21 questions (4 new, covering both of D2's flagged weak patterns). First drill on the fixed quiz: **18/21 (86%)** — 2 of 3 misses were genuine net-new content gaps (SSE-startup-reachability, rate-limiting-server-side), now carded on the wiki side. Then the user retook the **claudecertificationguide.com mock and passed: 720/1000** (up from 714 the prior day) — D2 jumped 20%→60%, direct payoff from this remediation. A live mistake from earlier in that Ramsey-Brain session (batch-vs-sequential feedback ordering) was also caught against the mock's own answer key and corrected on the wiki. Also fixed this project's own `docs/lessons.md`, which still taught the old incomplete Edit-recovery fact — same bug, different file, now corrected everywhere. Recall cards, source pages, and domain-page content all updated on the Ramsey-Brain side; this file and `task-list.md`/`registry.md` brought back in sync here.
- 2026-07-07: **Timeline sync from Ramsey-Brain** (auditing/cleanup only — no study work yet). Reconciled stale status across all docs: Attempt 1 failed 670/1000; **early retake now available** (platform migration waived the 6-month wait), target window **July 21 – Aug 1, 2026** (was 2026-11-21). **"Other" / "Conversational AI Patterns" resolved = D4** (v0.2 exam guide; score-report mislabel, no mystery domain) — closed the related research tasks in task-list and corrected lessons.md. Confirmed 12-month cert validity. Study resumes 7/8 or 7/9, D4/D3 priority. Note: Ramsey-Brain now has 47 recall cards seeded (run "quiz me cca" there).
- 2026-05-13: D4 HTML quiz 11/14 (79%); misses: any vs auto tool_choice, conflict_detected overconfidence, batch recovery resubmit only failed custom_ids
- 2026-05-13: D1 HTML quiz 12/12 (100%) — D1 fully mastered
- 2026-05-13: D4 Q21–Q50 drill complete — 27/30 (90%); misses: enum+detail field pattern (Q32), retry-with-feedback vs blind retry (Q46)
- 2026-05-13: D4 4.5/4.6 focused drill — 6/10 (60%); misses: batch interval math with retries, batch multi-turn limitation, structured disagreement vs majority vote; Q4 flagged as unreliable question bank content
- 2026-05-13: Clarified plan mode ≠ extended thinking — plan mode is Claude Code /plan (read-only); extended thinking is API feature thinking:{type:"enabled",budget_tokens:N}
- 2026-05-13: Clarified command vs skill — commands in .claude/commands/ (no frontmatter); skills in .claude/skills/ (optional frontmatter: context:fork, allowed-tools, argument-hint); /sync is a command, not a skill
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
- 2026-05-18: "v3.0.0" bank received from Zain — internally named "Streamlined CCA-F curated curriculum v1"; generated 2026-05-15 FROM the existing v2.0.0 source bank (1,489 Qs); file at `~/Desktop/Ramsey-Brain/raw/cca_f_question_bank_v3.0.0.json`; ingested into Ramsey-Brain
- 2026-05-18: 209 of 242 Qs are pulled directly from v2.0.0; 33 are candidate-authored gap-fillers (`anthropic_vetted: false`); D2=6 and D5=11 because the source bank was thin there — not a fix failure
- 2026-05-18: Genuine new value: tier labeling (T1=58 highest-leverage + 4 confirmed near-verbatim matches, T2=115, T3=69 rotation hedge) and 33 candidate-authored Qs; not a new source bank
- 2026-05-18: Prep guide §3 priority drill order: 5.4 → 4.2 → 1.5 → 4.3 → 5.2 → 1.4 → 1.3 → 1.2 → 3.2
- 2026-05-18: Exam-day mental moves (§5): (1) click scenario box first, (2) name failure axis before reading options, (3) behavior → mechanism not parameter, (4) "increase context window" is almost never right for forgetting
- 2026-05-19: D3 bank drill — 14/20 (70%); re-drill 6/6 (100%); weak spot: probabilistic vs deterministic axis (hooks over CLAUDE.md/slash commands, in-context over filters, constrained tools over generic); pattern also showed in D1 Q14 miss
- 2026-05-19: D1 bank drill (15 Qs) — 14/15 (93%); miss: generic tool misuse fix = replace with constrained alternative (load_document instead of fetch_url), not route around it; D1 is strongest domain
- 2026-05-20: 30Q weighted mixed drill — 24/30 (80%); miss redrill 6/6 (100%); misses: MCP resources vs mandatory tool_choice (resources = on-demand, not forced round-trip), composite tools vs prompt-level parallel batching, tool description fix beats routing layer, subagents + scratchpad for long sessions, Batch API nightly = latency-tolerant
- 2026-05-20: Exam intel from coworker: "Conversational AI Patterns" section (~15 Qs) appeared on live exam — not in Udemy, Skilljar, or Anthropic docs; logged as drift scenario; no actionable prep material found
- 2026-05-26: **CCA-F real exam taken (afternoon).** All 4 scenarios were covered in prep. Official wording differs from Udemy and Anthropic practice exams but not harder. A couple guesses; overall confident. Results expected 7–10 days.
- 2026-05-26: Miss-pattern drill 5/5 (100%) — locked in: Read+Write fallback for non-unique Edit; stratified sampling for rare-segment failures; -p/--print for CI interactivity (not --output-format json).
- 2026-05-26: pre-exam-summary.html created in html-resource-guide/; covers all 3 miss patterns, key distinctions table, domain anchors, anti-pattern hit list.
- 2026-05-26: Udemy Practice Exam 3 — 93% (56/60) PASSED. Agentic Architecture 100%, Prompt Engineering 100%, Claude Code Config 92%, Context Management 89%, Tool Design 82%. Taking break then sitting real exam.
- 2026-05-26: Explicit criteria vs examples distinction locked in — missing definition → criteria first; criteria clear but inconsistent → examples; prose failing → skip to examples
- 2026-05-26: Three targeted in-chat drills — 90%, 100%, 100% — all patterns from mock misses corrected
- 2026-05-26: **REAL EXAM TODAY (afternoon).** Confirmed passing threshold: 720/1000 (72%). Colleagues passing at 749, 780, 791 — "90% required" framing was incorrect.
- 2026-05-26: Key miss patterns from mock runs — PostToolUse hook beats wrapper tools for normalization (centralized, one place, covers third-party); tool misrouting → fix descriptions first; prose failing → examples not more instructions; coordinator = centralized visibility + error handling + info control
- 2026-05-26: Anthropic support emailed re: lost mock scores — Skilljar platform bug on both attempts
- 2026-06-03: Cleanup sync — committed pending 2026-05-27 post-exam changes (failed result 670/1000, retake planning, honesty rule added to CLAUDE.md). No new prep work this session.
- 2026-05-25: Co-worker post-exam intel — "why not how" exam; Anthropic worldview is the answer key; watch outcome keywords ("effective," "reduces," "what type of change"); human-interaction Qs default to Anthropic oversight/transparency/escalation philosophy; light on mechanistic/config questions; DO NOT use Sparq machine (IT blocks proctoring app)
- 2026-05-25: Sparq study site (https://sparq-study.alemadlei.tech/) — quiz runner built by coworker; user loaded this repo's question bank into it; no standalone question bank, it drills whatever JSON you load
- 2026-05-20: Exam schedule revised — target sit date moved to Tuesday May 26; Anthropic Official Mock on Monday May 25; Udemy Exam 3 if time permits Monday
- 2026-05-19: D3 key miss patterns — PostToolUse hook for auto-test (not slash command), prior findings in context for re-review runs (not string-match filters), interacting problems → single message (shared code path is the signal), inline confidence for triage (constraint elimination: stakeholders rejected filtering → A/C both wrong)
- 2026-05-18: T1 targeted drill (5.4/4.2/1.5/4.3) — 17/20 (85%); misses: Q5 Batch routing (nightly=latency-tolerant=Batch), Q11 nullable fields (required fields with no source = hallucination pressure), Q18 two-tools vs anyOf (tool-selection enforcement beats within-schema conditionality)
- 2026-05-17: D5 spot drill complete — 4/4 (100%); cache_control after compaction, hybrid summarization, JSON manifest crash recovery, PDF stratified sampling all solid
- 2026-05-17: Udemy Practice Exam 2 — 88% (53/60), up +12 from Exam 1 (76%); D5 100%, D3 92%, D1 88%, D4 83%, D2 82%
- 2026-05-17: Wrong answer drill — 7/7 (100%); concepts: stop_reason loop, MCP resources vs tools, missing source detection, session resume+revalidation, subagent tool scoping, skills vs commands, schema vs semantic validation
- 2026-05-17: Official Anthropic mock exam found — same 60 Qs every attempt (order shuffles); treat as one-time calibration; save for May 24–25
- 2026-05-16: Reviewed 6 official exam scenarios + 12 official sample questions from exam guide; 4 of 6 scenarios randomly selected per sitting; 720/1000 to pass
- 2026-05-16: Exam intel from Zain (AI Dept lead, passed CCA-F) — exam is broad/situational, not syntax-detail; his exam did NOT test CLAUDE.md specifics or commands vs skills distinction; scenario-based reasoning is the format
- 2026-05-16: Zain uploading a new curated question bank (1,489-question bank too large to get through before exam)
- 2026-05-16: D5 spot review concept anchors done — cache_control after compaction, hybrid summarization, JSON manifest crash recovery, PDF/stratified sampling; Q1 drill presented but not answered (user unavailable)
- 2026-05-14: D5 question bank drill complete — 16/20 (80%); misses: Q5 (cache_control breakpoint after compaction), Q6 (PDF full automation vs stratified sampling), Q9 (hybrid summarization), Q19 (JSON manifest for crash recovery vs reconnection)
- 2026-05-14: D5 weak spots to review before Exam 2 — prompt caching mechanics (cache_control after compaction), hybrid summarization pattern, JSON manifest crash recovery; resource: docs.anthropic.com prompt caching section
