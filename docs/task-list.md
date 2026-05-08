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
- [ ] Domain 1 practice questions — 60–80 from the question bank

### Domain 2 — MCP Tool Design (18%) — NOT STARTED
- [ ] ex1: Tool descriptions — overlapping tools, disambiguation
- [ ] ex2: Tool errors — `isError`, `errorCategory`, `isRetryable` structured responses
- [ ] ex3: Tool scope — right-sizing tool granularity
- [ ] ex4: MCP config reference — scopes, credential handling (markdown)
- [ ] ex5: Output design — structured output formatting
- [ ] Hook: hook_post_output_trim
- [ ] Config: sample.mcp.json with `${ENV_VAR}` credential pattern
- [ ] Write 2 overlapping MCP tool descriptions, differentiate both, test with ambiguous queries
- [ ] Domain 2 practice questions — 60 from the question bank

### Domain 3 — Claude Code Workflows (20%) — Review Only
- [ ] Review domain-3 page in Ramsey-Brain wiki
- [ ] Domain 3 practice questions — 50 from the question bank
- [ ] Optional: 1–2 exercises if weak spots surface from practice exams

### Domain 4 — Prompt Engineering (20%)
- [ ] Domain 4 practice questions — 50 from the question bank
- [ ] Optional: targeted exercises based on practice exam weak spots

### Domain 5 — Context Management (15%)
- [ ] Domain 5 practice questions — 40 from the question bank
- [ ] Optional: targeted exercises based on practice exam weak spots

---

## Practice Exams (Udemy)

- [ ] **Practice Exam 1** — timed, full sim (due: Sunday May 11); log score + weak domains
- [ ] **Practice Exam 2** — timed, full sim (due: Sunday May 18); target weak domains from Exam 1
- [ ] **Practice Exam 3** — timed, full sim (May 19–21); review every wrong answer

---

## Post-Exam Cleanup

- [ ] Archive domain-1/ and domain-2/ exercise notes into Ramsey-Brain wiki
- [ ] Tag any reusable patterns (agentic loop skeleton, hook templates) for future reference
- [ ] Lint check: confirm no literal secrets in any exercise files

---

_Last updated: 2026-05-08_
