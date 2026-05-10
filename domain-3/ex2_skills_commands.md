# CCA-F Domain 3, Exercise 2 — Skills and Slash Commands (Subdomain 3.2)

**What this exercises:**
- The difference between skills and CLAUDE.md rules
- Creating project-scoped vs user-scoped slash commands
- SKILL.md frontmatter: `context`, `allowed-tools`, `argument-hint`
- Why `context: fork` matters for verbose skills
- How to customize a skill personally without affecting teammates

**Run this in**: Claude Code (open the cca-exercises folder)

---

## Core Concept: Three Ways to Give Claude Instructions

| Mechanism | When it activates | Scope | Use for |
|-----------|------------------|-------|---------|
| CLAUDE.md / rules | Always, automatically | Project or user | Universal standards (always-on) |
| Slash commands | When you type `/command` | Project or user | Quick team workflows |
| Skills | When you type `/skill-name` | Project or user | Complex isolated tasks |

**The key distinction tested on the exam:**
- **CLAUDE.md** = always-loaded universal standards. "Use 4 spaces for indentation" belongs here.
- **Skills** = on-demand task-specific workflows. "Run a full security audit of this module" belongs here.
- **Don't use skills for always-on conventions** — that's CLAUDE.md/rules territory.

---

## Part A — Slash Commands

Slash commands are simple: a markdown file in `.claude/commands/` becomes a `/command` you can type.

### Project-scoped command (shared with team)

Create `.claude/commands/review.md`:

```markdown
Review the current file for bugs, security issues, and logic errors.

Focus on:
- Null/None handling and type mismatches
- Unhandled error paths
- Hardcoded values that should be configuration
- Missing input validation

Skip: minor style issues, formatting preferences, naming conventions.

Output format: one finding per line — [SEVERITY] location: description
```

After creating this file, type `/review` in Claude Code. It runs the review instructions
against whatever file you're currently working in.

**Exam trap:** A developer creates `/review` in `~/.claude/commands/review.md` and expects
teammates to have it after pulling. They won't — user-scoped commands are machine-local.
To share with the team, the file must be in `.claude/commands/` (project-level, version-controlled).

### User-scoped command (personal only)

Create `~/.claude/commands/standup.md`:

```markdown
Summarize my recent git activity (last 24 hours) as a standup update.
Format: Yesterday / Today / Blockers
Keep it under 5 bullet points total.
```

This command is only available on your machine — perfect for personal workflows you don't
want to impose on teammates.

---

## Part B — Skills

Skills are more powerful than commands because they support frontmatter configuration.

### SKILL.md frontmatter fields (these are the ONLY documented fields — know them cold)

```markdown
---
context: fork          # "fork" = run in isolated sub-agent context (default: inline)
allowed-tools:         # restrict which tools the skill can use
  - Read
  - Grep
  - Glob
argument-hint: "Path to the module to analyze"   # prompts for params when invoked without args
---
```

**What these do:**

| Field | What it does | When to use it |
|-------|-------------|----------------|
| `context: fork` | Runs skill in an isolated sub-agent; verbose output stays OUT of your main session | Always for exploration/analysis skills that produce a lot of output |
| `allowed-tools` | Restricts which tools the skill can call | When you want a skill to be read-only (no Write, no Edit) |
| `argument-hint` | Shows a prompt "Enter: [hint]" when you invoke without arguments | When the skill needs a specific input to work |

**Exam trap:** `model: haiku` is NOT a documented SKILL.md frontmatter field. Only `context`, `allowed-tools`, and `argument-hint` are valid.

### Create a code analysis skill

Create `.claude/skills/analyze/SKILL.md`:

```markdown
---
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
argument-hint: "Directory or file to analyze"
---
# Code Analysis Skill

Analyze the specified path. Report:
1. What this code does (2-3 sentences)
2. Key functions or classes and their purpose
3. Dependencies (imports used)
4. Potential issues or concerns
5. Test coverage gaps (files or functions with no corresponding tests)

Be specific — reference actual function names, not general descriptions.
```

Now invoke it: `/analyze domain-1/`

**Watch what happens:**
- `context: fork` means the verbose analysis output goes into a sub-agent, not your main session
- Your main conversation context stays clean — only the final summary comes back
- Without `context: fork`, a deep analysis of 10 files would fill your context window with exploration output

---

## Part C — Personal Skill Customization

What if you want a slightly different version of a team skill, just for yourself?

**Wrong approach:** Add an `override: true` field to your SKILL.md. This field does NOT exist.

**Correct approach:** Create a skill in `~/.claude/skills/` with a DIFFERENT name.

```
.claude/skills/analyze/SKILL.md      <- team's version (shared via git)
~/.claude/skills/analyze-verbose/SKILL.md  <- your personal version (different name, machine-local)
```

The different name means both can coexist without conflict. Your teammates keep `/analyze`;
you get `/analyze-verbose` with your personal tweaks.

---

## Part D — Skills vs. CLAUDE.md: The Exam Question Pattern

The exam presents a scenario and asks whether to use skills or CLAUDE.md. Use this framework:

| Scenario | Answer | Why |
|---------|--------|-----|
| "Enforce that all functions have docstrings" | CLAUDE.md | Always-on standard |
| "Run a security audit of this module" | Skill | On-demand, invoked explicitly |
| "Add 'use TypeScript strict mode' to team standards" | CLAUDE.md | Team convention, always applies |
| "Generate a PR description from git diff" | Skill (or command) | Task-specific, invoked when needed |
| "Keep PII out of log statements" | CLAUDE.md | Always-on enforcement |
| "Analyze test coverage for a specific directory" | Skill | Specific task, produces verbose output |

---

## Exam Trap Table — 3.2

| Trap | Correct Pattern |
|------|----------------|
| `model: haiku` in SKILL.md frontmatter | Not a valid field — only `context`, `allowed-tools`, `argument-hint` |
| `override: true` to personalize a team skill | Doesn't exist — create a personal variant with a different name in `~/.claude/skills/` |
| User-scoped commands shared via git pull | `~/.claude/commands/` is machine-local — use `.claude/commands/` for team commands |
| Skills for always-on convention enforcement | That's CLAUDE.md or `.claude/rules/` — skills are on-demand |
| `context: fork` is just "quiet mode" | It runs the skill in an isolated sub-agent — verbose output never enters the main session |
| argument-hint replaces positional `$1` `$2` params | `argument-hint` prompts for a single input — for complex parameterization, keep it simple |
