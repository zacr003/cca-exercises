# CCA-F Domain 3, Exercise 1 — CLAUDE.md Configuration Hierarchy (Subdomain 3.1)

**What this exercises:**
- The three scopes of CLAUDE.md and what each one is for
- How all discovered files are CONCATENATED (not overriding)
- How conflict resolution actually works (more specific scope wins)
- The `@import` syntax for modular configs
- The `.claude/rules/` directory as an alternative to one giant file
- The `/memory` command for diagnosing which files are loaded
- The 200-line size target

**Run this in**: Claude Code (open the cca-exercises folder in Claude Code to test)

---

## Core Concept: Three Scopes

Think of CLAUDE.md files like layers of instructions, stacked on top of each other:

```
~/.claude/CLAUDE.md          <- Layer 1: YOUR personal preferences (machine-local, not shared)
./CLAUDE.md or .claude/CLAUDE.md  <- Layer 2: TEAM standards (committed to git, shared)
./some-subdirectory/CLAUDE.md     <- Layer 3: AREA-specific context (auto-loaded when working there)
```

**All three load simultaneously and are concatenated — they do NOT override each other.**
If two rules at the same scope conflict, Claude picks one arbitrarily. Eliminate same-scope conflicts.

**Exam trap:** A new team member isn't getting the right behavior. Why?
→ The instructions are in `~/.claude/CLAUDE.md` (user-level, machine-local). They never got shared.
→ Fix: move them to the project-level `.claude/CLAUDE.md` which is version-controlled.

---

## Part A — Examine the Hierarchy

### Step 1: Look at what this project already has

Open the `cca-exercises/` folder in Claude Code, then ask Claude directly:
```
Which CLAUDE.md files are you currently loading?
```
Claude Code will report all active CLAUDE.md files from its context. `/memory` opens the CLAUDE.md for editing — it does NOT list loaded files.

### Step 2: Create a project-level CLAUDE.md

Create `.claude/CLAUDE.md` in the `cca-exercises/` root with this content:

```markdown
# cca-exercises Project Standards

## Code Style
- All Python files must include a module-level docstring
- Use snake_case for all variable and function names
- Do not use print() for debug output — use comments instead

## Exercise Format
- Every exercise file must have an EXAM DISTINCTION SUMMARY section at the bottom
- Fake/mock data goes at the top of the file, before the functions that use it
```

Now ask Claude Code to create a new Python file. Watch whether it follows these standards.

### Step 3: Create a directory-level CLAUDE.md

Create `domain-3/CLAUDE.md` with content specific to D3 exercises:

```markdown
# Domain 3 Exercises — Additional Context

These exercises focus on Claude Code configuration concepts, not Python SDK patterns.
Most exercises are markdown walkthroughs, not runnable Python scripts.

When generating Python files for this domain, keep them minimal — the goal is to
demonstrate the config concept, not build production code.
```

Now navigate to the `domain-3/` directory in Claude Code and ask it to generate something.
The domain-3 CLAUDE.md should also be active alongside the project-level one.

---

## Part B — @import and .claude/rules/

### The problem: CLAUDE.md files grow past 200 lines

When your CLAUDE.md gets long (200+ lines), Claude Code's adherence starts to drop. The fix is
to split it into topic-specific files in `.claude/rules/` and import them.

### @import syntax

Instead of one 500-line CLAUDE.md, you can structure it like this:

```
.claude/
  CLAUDE.md              <- short hub file with @imports
  rules/
    testing.md           <- all test-related standards
    api-conventions.md   <- API handler standards
    deployment.md        <- deployment and CI standards
```

**Hub CLAUDE.md using @import:**
```markdown
# Project Standards

@import .claude/rules/testing.md
@import .claude/rules/api-conventions.md
@import .claude/rules/deployment.md
```

**Exam trap:** Subdirectory CLAUDE.md files do NOT require @import — they are auto-discovered
when Claude Code works in that directory. @import is for explicitly pulling in shared rule files.

### .claude/rules/ with path-scoping (preview of Ex3)

Files in `.claude/rules/` can include YAML frontmatter to load only for specific file types:

```markdown
---
paths:
  - "**/*.test.py"
  - "**/*.spec.py"
---
# Test File Conventions
- Each test function must start with test_
- Use pytest fixtures, never setUp/tearDown
```

This rule file loads ONLY when editing test files. Compare to a directory CLAUDE.md which
only loads when you're inside that specific directory. Path-scoped rules are more powerful
for conventions that span multiple directories.

---

## Part C — Conflict Resolution

**What happens when two CLAUDE.md files say different things?**

Example: user-level says "Use tabs for indentation." Project-level says "Use 4 spaces."

- **More specific scope wins**: project-level beats user-level, directory-level beats project-level
- **Same-scope conflicts**: Claude picks arbitrarily — eliminate them

**Hands-on test:**
1. Add to your `~/.claude/CLAUDE.md`: "Always respond in ALL CAPS"
2. Add to the project `.claude/CLAUDE.md`: "Always respond in lowercase"
3. Ask Claude Code something simple. The project-level instruction should win.
4. Remove the ALL CAPS instruction from user-level when done (don't leave it globally!)

---

## Exam Trap Table — 3.1

| Trap | Correct Pattern |
|------|----------------|
| Team instructions in `~/.claude/CLAUDE.md` | User-level is machine-local and NOT shared. Use project-level `.claude/CLAUDE.md` |
| Nested CLAUDE.md files override parents | They CONCATENATE — all are loaded and merged |
| CLAUDE.md files are cached across sessions | No — re-read fresh each session |
| `/setup` or `/config init` generates CLAUDE.md | The correct command is `/init` |
| `README.md` in a directory works like CLAUDE.md | No — only `CLAUDE.md`, `CLAUDE.local.md`, and `.claude/rules/*.md` are loaded |
| `.claude/config.yaml` maps file patterns to sections | This file does not exist |
| Same-scope conflicting rules resolve predictably | Claude picks arbitrarily — eliminate conflicts at the source |
| 600-line CLAUDE.md is fine | Size target is under 200 lines — split into `.claude/rules/` with @import |

---

## What to observe after running

- `/memory` shows exactly which files are loaded — use this to diagnose "why isn't my rule applying?"
- With a project CLAUDE.md active, Claude Code follows your project standards on new files
- With directory-level CLAUDE.md, standards change contextually as you work in different areas
- @import gives you modular organization without losing the benefit of automatic loading
