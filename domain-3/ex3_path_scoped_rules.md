# CCA-F Domain 3, Exercise 3 — Path-Scoped Rules (Subdomain 3.3)

**What this exercises:**
- `.claude/rules/` as a modular alternative to a monolithic CLAUDE.md
- YAML frontmatter `paths:` field with glob patterns
- When to use path-scoped rules vs. directory-level CLAUDE.md
- The key scenario: conventions for files spread across many directories

**Run this in**: Claude Code (open the cca-exercises folder)

---

## Core Concept: The Problem Path-Scoped Rules Solve

Imagine you have test files scattered throughout a codebase — `Button.test.tsx` next to `Button.tsx`,
`api.test.ts` next to `api.ts`, `utils.spec.py` next to `utils.py`.

**A directory CLAUDE.md can't help you here.** It only loads when Claude Code is working in THAT
specific directory. A test file in `/components/` won't see a CLAUDE.md from `/services/`.

**Path-scoped rules solve this.** A rule file in `.claude/rules/` with:
```yaml
paths:
  - "**/*.test.tsx"
  - "**/*.spec.py"
```
...loads ANY TIME Claude Code edits a matching file, regardless of which directory it's in.

**Additional benefit:** path-scoped rules only load when you're working in matching files —
this reduces irrelevant context and saves tokens when working in unrelated areas.

---

## Part A — Create Path-Scoped Rule Files

### Rule 1: Test file conventions (applies to all test files anywhere)

Create `.claude/rules/testing.md`:

```markdown
---
paths:
  - "**/*.test.py"
  - "**/*.spec.py"
  - "**/test_*.py"
---
# Test File Conventions

- Every test function must start with `test_`
- Use pytest fixtures for shared setup — never duplicate setup code across tests
- Test exactly one behavior per test function
- Test edge cases: empty inputs, None/null values, boundary values (0, max, min)
- Never make real API calls in tests — mock all external services
- Assert specific values, not just truthy/falsy (`assert result == 42`, not `assert result`)
- Include one test for the "happy path" and at least one for the error path
```

### Rule 2: API handler conventions (applies to API files)

Create `.claude/rules/api-handlers.md`:

```markdown
---
paths:
  - "domain-4/**/*.py"
  - "domain-5/**/*.py"
---
# Domain 4 and 5 Exercise Conventions

- All API calls must handle the case where the response is empty or None
- Always use the `claude-haiku-4-5-20251001` model for exercises (faster, cheaper)
- Print the model's response after each API call so the output is visible
- Include error handling around `client.messages.create()` calls
```

### Rule 3: Infrastructure conventions (applies to specific paths)

Create `.claude/rules/infrastructure.md`:

```markdown
---
paths:
  - ".claude/**/*"
  - "**/settings.json"
---
# Claude Code Config File Conventions

- Never hardcode API keys or tokens in config files — use ${ENV_VAR} expansion
- All MCP server entries must use environment variable expansion for credentials
- Document the purpose of each hook in a comment above it
```

---

## Part B — Observe the Difference

**Test path-scoped rules vs. directory CLAUDE.md:**

1. Open a file that matches one of your glob patterns (e.g., create `domain-3/test_demo.py`)
2. Ask Claude Code: "What conventions should I follow for this file?"
   → It should mention the testing conventions from `testing.md`
3. Open a non-matching file (e.g., `domain-3/demo.py`)
4. Ask the same question
   → It should NOT mention testing conventions — they're not loaded for this file type

**This is the key behavior:** path-scoped rules are conditional. They load only when relevant.

---

## Part C — Path-Scoped Rules vs. Directory CLAUDE.md

Use this table to choose between them on the exam:

| Situation | Right choice | Why |
|-----------|-------------|-----|
| Test files scattered across many directories | `.claude/rules/testing.md` with `**/*.test.ts` glob | Can't reach files across directories with directory CLAUDE.md |
| Conventions that only apply to the `backend/` directory and its subdirectories | `backend/CLAUDE.md` | Naturally bounded by directory, simpler |
| Terraform conventions applying to `.tf` files in `/infra/`, `/deploy/`, `/modules/` | `.claude/rules/terraform.md` with `**/*.tf` glob | Files span multiple directories |
| API endpoint conventions for `src/api/` only | `src/api/CLAUDE.md` | Clear directory boundary |
| All Python files regardless of location | `.claude/rules/python.md` with `**/*.py` glob | Cross-cutting by file type |

**The frontmatter key is `paths:` — NOT `projects:`, NOT `directories:`**

---

## Exam Trap Table — 3.3

| Trap | Correct Pattern |
|------|----------------|
| Directory CLAUDE.md for test files spread across codebase | Use `.claude/rules/` with `**/*.test.*` glob — directory CLAUDE.md can't reach other directories |
| `projects:` as the frontmatter key | The correct key is `paths:` |
| Relying on Claude to infer which CLAUDE.md section applies | Use explicit glob matching — don't expect the model to reason about which section is relevant |
| Path-scoped rules override directory CLAUDE.md | They don't — all matching sources are concatenated |
| Rules in `.claude/rules/` without `paths:` frontmatter | They load at launch alongside CLAUDE.md — effectively the same as project-level CLAUDE.md |

---

## What to observe

After creating these rule files:
- Edit a `*.test.py` file and ask Claude Code to add a test — it should follow pytest conventions
- Edit a `*.py` file that is NOT a test file — testing conventions should NOT appear
- Run `/memory` — you'll see which rules files are currently loaded for the file you're editing

The conditional loading is the feature. Token-efficient AND context-appropriate.
