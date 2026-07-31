# Task List — cca-exercises

_Current exercise backlog. Updated by `/sync`._

---

## ▶ Current status (2026-07-30)

**The retake study sprint itself is tracked in `~/Desktop/Ramsey-Brain/docs/task-list.md`** — that's the live, day-to-day plan (mock exams, recall drilling, readiness gates). This file only tracks work specific to *this* project (exercises + `html-resource-guide/`).

- [x] ~~`d2-review.html` full audit + remediation~~ (2026-07-29) — see `docs/memory.md` for detail. 5 fixes (Edit-recovery bug incl. graded quiz answer, `~/.claude.json` path regression, error fields, tool_choice rule, Coordinator tier, API-connector section); quiz 17→21 questions.
- [x] ~~Fix stale Edit-recovery lesson in this project's own `docs/lessons.md`~~ (2026-07-29) — was teaching the same incomplete fact as the old `d2-review.html`.
- [x] ~~Re-audit `CCAF-Scenarios.html`~~ (2026-07-30) — mirrored ~20 new concepts/traps from the wiki `.md` in lockstep; new green "NEW" badge class.
- [x] ~~Build an anti-patterns reference guide~~ (2026-07-30) — new `CCAF-AntiPatterns.html`, all ~21 exam anti-patterns by domain (why-it-fails/do-instead) + quick-reference table.
- [ ] **Consider auditing d1/d3/d4/d5-review.html against the current wiki state** — they were last fully audited 2026-07-14; the wiki has advanced since (D1/D3/D5 content from the 2026-07-29 mock: PostToolUse side-effects, review-capacity-by-risk, batch-vs-sequential worked example; plus D4/D5 tool_choice-single-tool and stratified-sampling-vs-classifier from the 2026-07-30 mock). Not yet done — d2 and the Scenarios/AntiPatterns pages were prioritized instead.
- [ ] ~~Warm up with `quiz me cca` in Ramsey-Brain~~ — superseded; recall drilling has been happening continuously in Ramsey-Brain since 2026-07-14 (68→70-card decks now split across `wiki/cca/recall/`).

---

## Exercise Sprint — Attempt 1 FAILED (670/1000, 2026-05-26) · Retake sprint ongoing, tracked in Ramsey-Brain

### Domain 1 — Agentic Architecture (27%) — COMPLETE
- [x] ex1: Basic agentic loop — check `stop_reason`, append `tool_result` blocks, handle `max_tokens`
- [x] ex1b: Parallel tool calls — multiple tool calls in one response
- [x] ex2: Coordinator + subagents — explicit context passing, parallel Task calls
- [x] ex3: Hooks reference — PreToolUse / PostToolUse patterns (markdown)
- [x] ex4: Tool sequencing — ordered multi-tool orchestration
- [x] ex5: Task decomposition — breaking work across agentic steps
- [x] ex6: Session management (markdown reference)
- [x] Hooks: hook_pre_production_gate, hook_pre_refund_gate, hook_post_pii_trim
- [x] Domain 1 HTML quiz — 12/12 (100%) — D1 mastered
- [ ] Domain 1 practice questions — 15 done 93% (2026-05-19); 5 remaining; miss: generic tool misuse → constrained replacement

### Domain 2 — MCP Tool Design (18%) — EXERCISES COMPLETE
- [x] ex1: Tool descriptions — overlapping tools, disambiguation
- [x] ex2: Tool errors — `isError`, `errorCategory`, `isRetryable` structured responses
- [x] ex3: Tool scope — right-sizing tool granularity
- [x] ex4: MCP config reference — scopes, credential handling (markdown)
- [x] ex5: Output design — structured output formatting
- [ ] Hook: hook_post_output_trim — review only (exists, not explicitly run)
- [x] Config: sample.mcp.json with `${ENV_VAR}` credential pattern
- [x] Domain 2 practice questions — done (2026-05-08, all 5 subdomains; weak spots: 2.1 split generic tools, 2.2 business vs permission, 2.4 MCP resources)

### Domain 3 — Claude Code Workflows (20%) — COMPLETE
- [x] ex1: CLAUDE.md hierarchy — concept walkthrough done (Parts A/B/C); `/memory` bug fixed; 92% on HTML quiz
- [x] ex2: Skills and slash commands — 90% drill (9/10); miss: context:fork framing variation
- [x] ex3: Path-scoped rules — 90% drill (9/10); miss: monorepo directory boundary vs glob distinction
- [x] ex4: Plan mode — 80% drill (8/10); misses: plan mode cannot gate mid-execution (PreToolUse hook), auto-memory location
- [x] ex5: CI/CD headless mode — 70% drill (7/10); misses: prior findings in context (Q3), inline confidence for triage (Q4)
- [x] Domain 3 practice questions — 14/20 (70%) 2026-05-19; re-drill 6/6 (100%); weak spot: probabilistic vs deterministic axis

### Domain 4 — Prompt Engineering (20%) — EXERCISES COMPLETE
- [x] ex1: Few-shot prompting — vague vs explicit criteria vs contrastive examples (4.1, 4.2)
- [x] ex2: Structured output — JSON schema, nullable fields, enum+other, conflict_detected (4.3)
- [x] ex3: tool_choice — auto vs any vs forced, the first-turn-then-auto pattern (4.4)
- [x] ex4: Batch API — submit, poll, correlate via custom_id, failure recovery (4.5)
- [x] ex5: Retry-with-feedback — error feedback loop, retry limits, detected_pattern field (4.3/4.6)
- [x] Domain 4 practice questions — Q21–Q50 complete (90%); 4.5/4.6 drill done (60%); HTML quiz 11/14 (79%); weak spots: any vs auto tool_choice, conflict_detected overconfidence, batch recovery custom_id, batch interval math with retries

### Domain 5 — Context Management (15%) — EXERCISES COMPLETE
- [x] ex1: Long context — lost-in-the-middle, key findings at top, tool output trimming (5.1)
- [x] ex2: Escalation — explicit criteria + few-shot, frustrated user pattern, multi-topic (5.2)
- [x] ex3: Context degradation — API statelessness, scratchpad files, case-facts block (5.4, 5.5)
- [x] ex4: Error propagation — structured errors, coverage annotations, multi-agent recovery (5.3)
- [x] Domain 5 practice questions — 20 done (2026-05-14, 16/20 = 80%; misses: cache_control after compaction, hybrid summarization, JSON manifest crash recovery, PDF full automation vs sampling)
- [x] D5 spot drill — 4/4 (100%) — cache_control, hybrid summarization, JSON manifest, PDF sampling

---

## Practice Exams

- [x] **Practice Exam 1 (Udemy)** — 76% (46/60) taken May 10; weak spots: D4 (67%), D1 (75%)
- [x] **Anthropic Official Practice Exam** — Taken 2026-05-25 (twice); both scores lost to Skilljar platform bug; Anthropic support contacted
- [x] **Practice Exam 2 (Udemy)** — **88% (53/60)** taken May 17; domain breakdown: Context 100%, D3 92%, D1 88%, D4 83%, D2 82%
- [x] **30Q weighted mixed drill** — 24/30 (80%) taken May 20; miss redrill 6/6 (100%)
- [x] **Practice Exam 3 (Udemy)** — 93% (56/60) 2026-05-26 — PASSED (72% threshold); D1 100%, D4 100%, D3 92%, D5 89%, D2 82%

---

## Post-Exam / Retake Prep

### Immediate
- [x] Receive exam results — **FAILED. 670/1000. Passing: 720/1000.**
- [x] Add no-sycophancy rule to CLAUDE.md and memory — done 2026-05-27
- [ ] Follow up with Anthropic support re: lost official mock scores (ticket open)
- [ ] **Register on the new platform + lock in a retake date** (target July 21 – Aug 1, 2026)
- [ ] Get the **official Anthropic practice exam** from the new platform and complete it before sitting (closest proxy to real-exam wording)
- [x] Ask Anthropic support what the "Other" domain covers — **RESOLVED 2026-07-01**: v0.2 exam guide confirms "Other" = D4 (Prompt Engineering & Structured Output); score report mislabeled it. No mystery domain.
- [ ] (Optional) Ask Zain about "Conversational AI Patterns" **wording** — content resolved to D4; only real-exam wording intel still useful

### Retake Research (do before resuming study)
- [x] Identify what "Other" / "Conversational AI Patterns" actually covers — **RESOLVED 2026-07-01**: it IS D4 (score-report mislabel), per v0.2 guide.
- [ ] Find recent test-taker accounts of D3 real exam wording (54% despite 92% practice = wording gap)
- [x] ~~Locate any prep material for "Conversational AI Patterns" content~~ — no longer needed; resolved to D4.

### Retake Prep (superseded — tracked live in Ramsey-Brain `docs/task-list.md` since 2026-07-24)
- [x] ~~D3 deep dive~~ / [x] ~~D2 targeted drill~~ — superseded by the Ramsey-Brain retake sprint's recall-card + mock-exam cycle (2026-07-14 onward). D2 was the priority-drill domain 2026-07-28→29 (20%→60% after remediation); D4 is now the repeat-drill target (100%→67% on the 2026-07-29 mock).
- [x] ~~"Other" / Conversational AI Patterns deep dive~~ — moot; resolved to D4.
- [ ] Archive domain-1/ and domain-2/ exercise notes into Ramsey-Brain wiki
- [ ] Tag any reusable patterns (agentic loop skeleton, hook templates) for future reference
- [ ] Lint check: confirm no literal secrets in any exercise files
- [ ] Sit rested — non-negotiable; do not schedule exam after travel or minimal sleep

---

_Last updated: 2026-07-30 (CCAF-Scenarios.html re-audit + new CCAF-AntiPatterns.html; 3rd mock 907/1000 PASSED in Ramsey-Brain, full 60Q attempt planned 2026-07-31 PM — see Ramsey-Brain task-list.md for the live plan)_
