# Task List — cca-exercises

_Current exercise backlog. Updated by `/sync`._

---

## Exercise Sprint — Attempt 1 FAILED (670/1000, 2026-05-26) · Retake window: July 21 – Aug 1, 2026

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

### Retake Prep (early retake available now; target window July 21 – Aug 1, 2026)
- [ ] D3 deep dive — 54% on real exam; needs real-exam-wording-aligned drill
- [ ] D2 targeted drill — 67% on real exam; consistently weakest domain
- [x] ~~"Other" / Conversational AI Patterns deep dive~~ — moot; resolved to D4. Folded into the D4 deep dive above.
- [ ] Archive domain-1/ and domain-2/ exercise notes into Ramsey-Brain wiki
- [ ] Tag any reusable patterns (agentic loop skeleton, hook templates) for future reference
- [ ] Lint check: confirm no literal secrets in any exercise files
- [ ] Sit rested — non-negotiable; do not schedule exam after travel or minimal sleep

---

_Last updated: 2026-07-07 (timeline sync from Ramsey-Brain — retake window July 21–Aug 1; "Other" = D4 resolution)_
