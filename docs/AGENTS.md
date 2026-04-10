---
title: Agents Reference
---

# Agents Reference

This template ships 3 specialist agents. They are intended to guide work in the project you bootstrap, not to imply that this repository already contains a full generated codebase.

---

## 1. @DataQuality

**Role**: data validation, quality testing, and anomaly debugging.

**When to use it**
- Validate pipeline outputs
- Add quality checks to transformations
- Investigate nulls, duplicates, schema drift, or broken assumptions

**What it does**
- checks schemas, types, keys, and null handling
- suggests assertions and fixtures
- proposes regression tests for data bugs
- pushes toward testable quality rules

**Skills it uses**
- `data-quality-testing`
- `data-pipeline-tdd`
- `polars-spark-pandas-patterns`
- `fabric-databricks-python-runtime`

---

## 2. @CodeReviewer

**Role**: structured code review with severity-based feedback.

**When to use it**
- Review a change before merge
- Check for correctness or performance problems
- Look for edge cases and maintainability issues

**What it does**
- reviews correctness, performance, maintainability, and testing gaps
- grades issues as CRITICAL, MAJOR, MINOR, or FYI
- focuses on review, not general project scaffolding

**Skills it uses**
- `code-review-notebooks`
- `polars-spark-pandas-patterns`

---

## 3. @ProjectScaffolder

**Role**: bootstrap orchestration for a new project.

**When to use it**
- Start a new pipeline project
- Convert this metadata repo into a real project structure
- Run the `/setup-project` workflow

**What it does**
1. asks a small set of discovery questions
2. summarizes requirements back to you
3. proposes or generates `src/`, `tests/`, and starter modules
4. hands off follow-up work to the specialist agents

**Skills it uses**
- `notebook-as-code`
- `data-pipeline-tdd`
- `fabric-databricks-python-runtime`

---

## Coordination Model

Recommended flow for a new project:

1. Use `@ProjectScaffolder` or `/setup-project` to create the real project layout.
2. Use `@DataQuality` or `/validate-pipeline` to add quality checks.
3. Use `@CodeReviewer` or `/review-code` for review before merge.
4. Use `/lesson` when you discover a pattern worth preserving.

---

## Notes

- Notebook organization and doc synchronization are available as slash-command workflows in this repo.
- This repo does not currently ship dedicated `@NotebookOrganizer` or `@DocsSync` agent files.

---

## See Also

- [PROMPTS.md](./PROMPTS.md)
- [SKILLS.md](./SKILLS.md)
- [SETUP.md](./SETUP.md)
