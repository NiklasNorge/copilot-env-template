---
name: data-pipeline-tdd
description: >-
  Apply RED-GREEN-REFACTOR to data transformations and pipeline modules. Use
  when starting new pipeline logic, fixing a regression, or extracting notebook
  code into tested modules with concrete starter test templates.
allowed-tools:
  - read
  - write
  - shell(pytest:*)
---

# Data Pipeline TDD

Use this skill when you want tests to define the pipeline contract before implementation hardens around accidental behavior.

## Assets In This Skill

- `examples/test_transform_red.py`: starter RED test for a pure transformation
- `examples/test_notebook_extraction.py`: starter test for logic extracted from a notebook

## Workflow

1. Write the smallest failing test that describes the desired behavior.
2. Implement the minimal code to pass.
3. Refactor only after the behavior is covered.
4. Add edge cases for nulls, empties, and bad input.
5. Promote any bug reproduction test into the permanent suite.

## Typical Usage

```text
Use data-pipeline-tdd to write failing tests for a deduplicate_orders transform before implementing the transform itself. Start from the RED template and then add edge-case coverage.
```

## Principles

- Test behavior, not incidental implementation.
- Prefer input-to-output contracts over private-step assertions.
- Use fixtures to avoid repeating synthetic datasets.
- Extraction from notebooks should produce importable, testable modules.
