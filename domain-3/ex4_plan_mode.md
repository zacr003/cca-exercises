# CCA-F Domain 3, Exercise 4 — Plan Mode vs. Direct Execution (Subdomain 3.4)

**What this exercises:**
- When to use plan mode vs. direct execution
- The iterative refinement pattern in plan mode
- The Explore subagent for verbose discovery
- PreToolUse hooks for mid-execution gating (what plan mode cannot do)

**Run this in**: Claude Code

---

## Core Concept: What Plan Mode Actually Does

Plan mode tells Claude Code to **explore and design, but not modify source files.**
Claude can read files, run shell commands to explore, and write out a plan — but will not
edit your code until you switch back to execution mode.

Think of it like this:
- **Plan mode** = an architect who walks through your building and draws blueprints
- **Direct execution** = a contractor who walks in and starts changing things immediately

You want the architect first when the job is complex. For replacing a light bulb, just call the contractor.

---

## Part A — The Decision Framework

Use this table on the exam. Memorize the two columns:

| Use Plan Mode | Use Direct Execution |
|--------------|---------------------|
| Refactoring across 20+ files | Fixing a single bug with a clear stack trace |
| Migrating from REST to GraphQL | Adding one input validation check |
| Architectural decision with tradeoffs | Updating a config value |
| Multiple valid approaches (need to compare) | Change where scope and approach are obvious |
| Unknown dependencies across the codebase | Single-file modification with clear requirement |
| Security-sensitive multi-component change | Updating a dependency version (usually) |
| New authentication system | Adding a date validation to one form field |
| Restructuring a monolith into services | Fixing a typo in an error message |

**The quick test:** "Do I know exactly what to change and where?" → Direct execution.
"Do I need to explore first?" → Plan mode.

---

## Part B — The Iterative Refinement Pattern

**Common exam trap:** Using plan mode as a one-shot oracle.

Wrong mental model:
```
1. Activate plan mode
2. Claude generates a plan
3. Switch to execution
```

Correct mental model:
```
1. Activate plan mode
2. Claude generates a plan
3. YOU give feedback: "This approach doesn't account for X"
4. Claude revises the plan
5. You give more feedback if needed
6. THEN switch to execution once the plan is satisfactory
```

Plan mode is iterative. The value is in the back-and-forth before any code changes.
Starting direct execution and realizing you need to rethink the approach = costly rework.

**Exam trap:** Expecting plan mode to pause mid-execution at a specific step.
Plan mode = safe exploration BEFORE execution. It does not gate steps DURING execution.
For mid-execution gating, use a **PreToolUse hook** instead.

---

## Part C — The Explore Subagent

For large codebases, there's a related pattern: the **Explore subagent**.

When Claude Code reads 30 files to understand a codebase, all that output goes into the
main conversation's context window. After deep exploration, your context is full of file
contents and there's no room left for the actual implementation work.

**The Explore subagent solves this:**
- Spawns a sub-agent to handle the verbose discovery
- The sub-agent returns only a concise summary to the main session
- Your main conversation context stays clean

This is similar to `context: fork` for skills — the principle is the same: isolate verbose
output from the session that needs to do the real work.

**How to invoke:** In Claude Code, ask something like:
"Use the Explore subagent to analyze the domain-1 directory and summarize what each file does."

Compare: ask without the Explore subagent on a 10-file directory. Watch your context fill up.
Then try with Explore — you get a clean summary instead.

---

## Part D — Hands-On: Try Plan Mode

In Claude Code with the cca-exercises project open, try these:

### Scenario 1: Use direct execution (appropriate)
Ask Claude Code: "Add a `--verbose` flag to ex1_agentic_loop.py that prints each tool call's input."
→ This is a clear, single-file, well-scoped change. Direct execution is correct. Plan mode would be waste.

### Scenario 2: Use plan mode (appropriate)
Ask Claude Code: "I want to add error handling to every exercise file in domain-1 that doesn't already have try/except blocks. Plan how you'd approach this without making any changes yet."
→ This spans multiple files with unknown scope. Plan mode first to see the strategy.
→ Give feedback on the plan before switching to execution.

### Scenario 3: Spot the wrong choice
"A developer activates plan mode to add a single print statement to a function."
→ Wrong choice. Direct execution is the right tool for a one-line, clear-scope change.
→ Plan mode for this wastes 3 minutes of exploration before making a one-line edit.

---

## Exam Trap Table — 3.4

| Trap | Correct Pattern |
|------|----------------|
| Plan mode gates steps mid-execution | No — plan mode is for before execution; use PreToolUse hook for mid-execution gating |
| Plan mode is used once, generates plan, done | Plan mode is iterative — refine the plan through conversation before executing |
| Direct execution for complex multi-file changes | Use plan mode — direct execution on complex changes risks costly rework |
| Plan mode for a single-file bug fix | Direct execution — plan mode overhead isn't justified |
| "Plan mode pauses before each file edit" | Plan mode does not touch source files at all; it only reads and writes a plan |
