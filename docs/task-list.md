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

### Domain 2 — MCP Tool Design (18%) — EXERCISES COMPLETE
- [x] ex1: Tool descriptions — overlapping tools, disambiguation
- [x] ex2: Tool errors — `isError`, `errorCategory`, `isRetryable` structured responses
- [x] ex3: Tool scope — right-sizing tool granularity
- [x] ex4: MCP config reference — scopes, credential handling (markdown)
- [x] ex5: Output design — structured output formatting
- [ ] Hook: hook_post_output_trim — review only (exists, not explicitly run)
- [x] Config: sample.mcp.json with `${ENV_VAR}` credential pattern
- [ ] Domain 2 practice questions — 60 drilled this session across all 5 subdomains (weak spots: 2.1 split generic tools, 2.2 business vs permission, 2.4 MCP resources)

### Domain 3 — Claude Code Workflows (20%) — EXERCISES COMPLETE
- [x] ex1: CLAUDE.md hierarchy — 3 scopes, concatenation, @import, .claude/rules/, conflict resolution
- [x] ex2: Skills and slash commands — context:fork, allowed-tools, argument-hint, project vs user scope
- [x] ex3: Path-scoped rules — YAML paths frontmatter, glob patterns, vs directory CLAUDE.md
- [x] ex4: Plan mode — decision framework, iterative refinement, Explore subagent
- [x] ex5: CI/CD headless mode — -p flag, --output-format json, --bare, independent review instance
- [ ] Domain 3 practice questions — 50 from the question bank

### Domain 4 — Prompt Engineering (20%) — EXERCISES COMPLETE
- [x] ex1: Few-shot prompting — vague vs explicit criteria vs contrastive examples (4.1, 4.2)
- [x] ex2: Structured output — JSON schema, nullable fields, enum+other, conflict_detected (4.3)
- [x] ex3: tool_choice — auto vs any vs forced, the first-turn-then-auto pattern (4.4)
- [x] ex4: Batch API — submit, poll, correlate via custom_id, failure recovery (4.5)
- [x] ex5: Retry-with-feedback — error feedback loop, retry limits, detected_pattern field (4.3/4.6)
- [ ] Domain 4 practice questions — 50 from the question bank

### Domain 5 — Context Management (15%) — EXERCISES COMPLETE
- [x] ex1: Long context — lost-in-the-middle, key findings at top, tool output trimming (5.1)
- [x] ex2: Escalation — explicit criteria + few-shot, frustrated user pattern, multi-topic (5.2)
- [x] ex3: Context degradation — API statelessness, scratchpad files, case-facts block (5.4, 5.5)
- [x] ex4: Error propagation — structured errors, coverage annotations, multi-agent recovery (5.3)
- [ ] Domain 5 practice questions — 40 from the question bank

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

_Last updated: 2026-05-10_
