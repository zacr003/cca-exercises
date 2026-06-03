# cca-exercises Project Standards

## Code Style
- All Python files must include a module-level docstring
- Use snake_case for all variable and function names
- Do not use print() for debug output — use comments instead

## Exercise Format
- Every exercise file must have an EXAM DISTINCTION SUMMARY section at the bottom
- Fake/mock data goes at the top of the file, before the functions that use it
- All exercises use `claude-haiku-4-5-20251001` as the model — faster and cheaper for practice

## Error Handling
- All API calls must handle the case where the response is empty or None
- Print the model's response after each API call so output is visible when running

## Exam Readiness — Honesty Rule

NEVER tell the user they are ready to sit an exam unless ALL of the following are confirmed:
- All critical practice scores are in hand (missing scores = a blocker, not a footnote)
- No significant content gaps remain unresolved
- The user is rested — exhaustion is a hard risk, not a minor caveat

If any of these are missing, say so explicitly. Do not let strong scores on one source paper over unresolved gaps elsewhere. Do not let timeline pressure or momentum override an honest assessment.

If asked "am I ready?", answer with what is confirmed AND what is still unknown. Positive reinforcement for effort is fine. Optimism about readiness when the data doesn't support it is not.

This rule exists because Claude told the user he was ready on 2026-05-26 — the user was sleep-deprived, the official mock score was never received, and an entire exam domain had no prep material. He failed. Do not repeat this.

@import .claude/rules/testing.md
