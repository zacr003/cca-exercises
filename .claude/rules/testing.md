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
- Never make real API calls in tests — mock all external services
- Assert specific values, not just truthy/falsy (`assert result == 42`, not `assert result`)
