---
title: Slash Commands Quick Reference
---

# Slash Commands

Type `/` in Copilot Chat to trigger these metadata-driven workflows.

These commands are meant to help you scaffold or improve the target project. They should not be read as a promise that this repository already contains the generated code examples shown below.

---

## Command Matrix

| Command | What It Does | When To Use |
|---------|--------------|-------------|
| `/analyze-data` | Explore a dataset and flag anomalies | Investigating a new dataset |
| `/validate-pipeline` | Suggest quality checks and tests | Hardening a pipeline |
| `/organize-notebook` | Restructure a notebook and extract logic | Cleaning up notebook workflows |
| `/sync-docs` | Detect doc-code drift and propose updates | After refactors |
| `/review-code` | Review code with severity-based findings | Before merge |
| `/test-this` | Generate test cases and fixtures | Adding or improving tests |
| `/setup-project` | Scaffold the real project structure | Starting a new project |
| `/lesson` | Capture a lesson learned | After a fix or repeated issue |

---

## `/setup-project`

Primary bootstrap workflow for this repository.

Expected outcome:
- creates or proposes `src/` and `tests/`
- adds starter pipeline modules
- suggests validation and test structure
- points you to the reference assets you may want to adopt

Example prompt:

```text
/setup-project

Create a daily ETL project for order exports.
Use Databricks with Python runtime.
Read CSV from cloud storage, standardize timestamps, validate keys, and write parquet output.
```

---

## `/validate-pipeline`

Use this after code exists in the target project.

Typical output:
- missing assertions
- suggested validators
- test fixture ideas
- severity of the quality gaps

---

## `/organize-notebook`

Use this when exploratory work has become hard to follow.

Typical output:
- a cell ordering plan
- extraction candidates for `.py` modules
- test targets for the extracted logic

---

## `/sync-docs`

Use this after implementation changes.

Typical output:
- outdated signatures or examples
- README or docstring edits to make
- validation steps for examples or doctests

Note: this repo does not currently ship a dedicated `@DocsSync` agent. Use the command directly.

---

## `/review-code`

Use this for a structured review pass.

Typical output:
- correctness issues
- performance issues
- maintainability issues
- testing gaps

---

## `/test-this`

Use this when you want Copilot to propose a focused test plan for a function, transformation, or module.

Typical output:
- happy path tests
- edge cases
- invalid-input cases
- reusable fixtures

---

## `/analyze-data`

Use this for first-pass data exploration.

Typical output:
- schema and dtypes
- null patterns
- summary statistics
- anomaly flags

---

## `/lesson`

Use this to capture a recurring problem and fold it back into the bootstrap process.

Typical output:
- a lesson entry for `tasks/lessons.md`
- candidate tags
- suggestions for which skill or instruction file should be improved

---

## See Also

- [AGENTS.md](./AGENTS.md)
- [SKILLS.md](./SKILLS.md)
