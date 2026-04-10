---
name: code-review-notebooks
description: >-
  Review Python and notebook code for correctness, performance, maintainability,
  and testing gaps. Use when you want a structured read-only review pass with
  severity-based findings.
allowed-tools:
  - read
---

# Code Review Notebooks

Use this skill for structured review work, especially when code has moved between notebooks and modules or when data-processing logic needs a correctness and performance pass.

## Review Areas

- correctness and edge cases
- performance and unnecessary row-wise work
- maintainability and extraction candidates
- missing tests
- data-quality blind spots

## Output Style

- CRITICAL: fix before merge
- MAJOR: should fix in the PR
- MINOR: worthwhile cleanup
- FYI: useful but optional context
