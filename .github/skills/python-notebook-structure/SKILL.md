---
name: python-notebook-structure
description: >-
  Organize Python notebooks for clarity, extraction, and testability. Use when
  a notebook is growing, logic needs extraction to modules, or cell order has
  become hard to maintain.
allowed-tools:
  - read
  - write
---

# Python Notebook Structure

Use this skill to keep notebooks consistent and extraction-friendly.

## Structure Standard

1. Imports
2. Configuration and constants
3. Pure transform and validation functions
4. Orchestration cell
5. Diagnostics and outputs

## Extraction Rules

- Extract reusable logic to modules under `src/`
- Keep notebook cells thin wrappers around module functions
- Move platform-specific helpers (`dbutils`, `notebookutils`) to boundary code
- Add tests for extracted logic immediately
