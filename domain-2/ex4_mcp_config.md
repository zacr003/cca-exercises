# CCA-F Domain 2, Exercise 4 -- MCP Configuration and Credentials (Subdomain 2.4)

This exercise is reference + hands-on config work. MCP configuration lives in
Claude Code (not the Python SDK), so there are no runnable Python files here.
Read each section, then examine the config examples.

---

## Core Concept: Two Scopes of MCP Configuration

| Scope | File | Shared? | Use For |
|-------|------|---------|---------|
| Project | `.mcp.json` (repo root) | Yes -- version-controlled | Team tooling, shared servers |
| User | `~/.claude.json` | No -- machine-local | Personal/experimental servers |

**Exam trap**: Putting a personal experimental server in `.mcp.json` exposes it to
all teammates via version control. Personal servers belong in `~/.claude.json`.

---

## Config A: Correct `.mcp.json` with Environment Variable Expansion

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-jira"],
      "env": {
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}",
        "JIRA_BASE_URL": "${JIRA_BASE_URL}"
      }
    }
  }
}
```

**Key point**: `${GITHUB_TOKEN}` is resolved from the shell environment at runtime.
The literal token value is never written into the file.

**Exam trap**: Hardcoding the token value directly:
```json
"GITHUB_TOKEN": "ghp_actualTokenValueHere"   <-- WRONG: never do this
```
This value is committed to version control and visible to everyone with repo access.

---

## Config B: WRONG -- Hardcoded Credentials

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_abc123realtoken"
      }
    }
  }
}
```

**Why this fails**: Anyone who clones the repo gets the token. If the repo is public,
the token is exposed immediately. Even in private repos, it violates least-privilege.

---

## Config C: allowedTools Pattern for MCP Servers

MCP tool names follow the pattern: `mcp__<servername>__<toolname>`

To permit all tools from the `github` server:
```json
{
  "allowedTools": ["mcp__github__*"]
}
```

To permit only specific tools:
```json
{
  "allowedTools": [
    "mcp__github__create_pull_request",
    "mcp__github__list_issues"
  ]
}
```

**Exam trap**: `"allowedTools": ["github__*"]` -- missing the `mcp__` prefix.
The full pattern is always `mcp__<servername>__<toolname>`.

---

## Config D: Defense-in-Depth -- PreToolUse Hook + Server-Side Allowlist

For domain restriction (e.g., only allow searches on your own docs site):

**Layer 1** -- MCP server implementation: validate requested domain before fetching.
**Layer 2** -- PreToolUse hook: block the tool call if the domain is not in an allowlist.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__websearch__fetch",
        "hooks": [
          {
            "type": "command",
            "command": "\"C:/Program Files/Python314/python\" domain-2/hook_pre_domain_check.py"
          }
        ]
      }
    ]
  }
}
```

**Exam trap**: `mcp_domain_allowlist` as an API parameter -- this does NOT exist.
Domain restriction requires server-side logic + PreToolUse hook, not an API flag.

---

## Config E: Bedrock vs. Direct API

| Deployment | Env Var | Notes |
|-----------|---------|-------|
| Direct API | `ANTHROPIC_API_KEY` | Standard usage |
| Amazon Bedrock | `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials | NOT `ANTHROPIC_API_KEY` |

```bash
# Bedrock -- CORRECT
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_PROFILE=my-bedrock-profile
claude

# Bedrock -- WRONG
export ANTHROPIC_API_KEY=sk-...   # Anthropic key has no effect on Bedrock
```

---

## Hands-On: Examine the Sample Config

Open `sample.mcp.json` in this directory. It shows:
1. Two MCP servers configured with env var expansion
2. Correct `allowedTools` patterns
3. A commented-out example of the WRONG approach (hardcoded token)

To use in a real project, copy it to the project root as `.mcp.json` and set
the corresponding environment variables before launching Claude Code.

---

## Exam Trap Table -- 2.4

| Trap | Correct Pattern |
|------|----------------|
| Hardcode token in `.mcp.json` | `${ENV_VAR}` expansion -- never commit raw secrets |
| Personal server in `.mcp.json` | Personal servers go in `~/.claude.json` |
| `allowedTools: ["github__*"]` | Pattern requires `mcp__` prefix: `"mcp__github__*"` |
| `mcp_domain_allowlist` API param | Does not exist; use server-side allowlist + PreToolUse hook |
| `ANTHROPIC_API_KEY` for Bedrock | Use `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials |
| One `.mcp.json` for all envs | Separate configs per env, or use env var values that differ per env |
