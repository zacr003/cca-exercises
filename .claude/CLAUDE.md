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

@import .claude/rules/testing.md
