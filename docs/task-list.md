# Task List — cca-exercises

_Current exercise backlog. Updated by `/sync`._

---

## Active Sprint — CCA-F Exam (Target: 2026-05-27)

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
- [ ] Domain 1 practice questions — 20 from the question bank (HTML quiz done; bank drill pending)

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
- [ ] Domain 3 practice questions — 20 from the question bank (not started)

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
- [ ] D5 spot drill — 4 targeted questions on weak spots; Q1 presented, not yet answered

---

## Practice Exams

- [x] **Practice Exam 1 (Udemy)** — 76% (46/60) taken May 10; weak spots: D4 (67%), D1 (75%)
- [ ] **Anthropic Official Practice Exam** — take before or alongside Exam 2; scenario-based format matches real exam
- [ ] **Practice Exam 2 (Udemy)** — timed, full sim (due: May 18); target weak domains from Exam 1
- [ ] **Practice Exam 3 (Udemy)** — timed, full sim (May 19–21); review every wrong answer

---

## Post-Exam Cleanup

- [ ] Archive domain-1/ and domain-2/ exercise notes into Ramsey-Brain wiki
- [ ] Tag any reusable patterns (agentic loop skeleton, hook templates) for future reference
- [ ] Lint check: confirm no literal secrets in any exercise files

---

_Last updated: 2026-05-16_
