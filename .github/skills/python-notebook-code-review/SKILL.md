---
name: python-notebook-code-review
description: >-
  Review Python and notebook code for correctness, performance, maintainability,
  and testing gaps with severity-based findings.
allowed-tools:
  - read
---

# Python Notebook Code Review

Use this skill for read-only review passes over notebooks and extracted modules.

## Review Areas

- correctness and edge cases
- Polars/Spark performance choices
- extraction and maintainability
- missing tests and quality checks

## Severity Output

- CRITICAL: fix before merge
- MAJOR: should fix in PR
- MINOR: worthwhile cleanup
- FYI: optional context
