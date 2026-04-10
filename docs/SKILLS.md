---
title: Skills Library Reference
---

# Skills Library

This template includes reusable skills that shape how Copilot behaves in the project you bootstrap.

The stronger skills in this repo now ship helper scripts, templates, or checklists alongside `SKILL.md`, so they act more like reusable workflow units than static advice files.

---

## Overview

| Skill | Purpose | Typical Use |
|-------|---------|-------------|
| `data-quality-testing` | Validation patterns, assertions, fixtures | Writing quality checks |
| `polars-spark-pandas-patterns` | Framework and platform guidance | Choosing Polars, Pandas, or Spark patterns |
| `notebook-as-code` | Notebook organization and extraction | Converting notebooks into maintainable workflows |
| `auto-doc-sync` | Documentation drift detection | Updating docs after refactors |
| `markdown-notebook-docs` | README and notebook documentation patterns | Writing operational docs |
| `data-pipeline-tdd` | Test-first pipeline workflow | RED-GREEN-REFACTOR for data work |
| `code-review-notebooks` | Review checklists and severity language | Reviewing code before merge |
| `capture-data-eng-lessons` | Structured lesson capture | Feeding learnings back into the template |
| `fabric-databricks-python-runtime` | Platform-specific runtime heuristics | Building Polars-first workflows on Fabric or Databricks |

---

## Categories

Execution-oriented skills:
- `auto-doc-sync`
- `data-quality-testing`
- `data-pipeline-tdd`
- `code-review-notebooks`
- `fabric-databricks-python-runtime`

Reference or manual-process skills:
- `markdown-notebook-docs`
- `capture-data-eng-lessons`

---

## Usage Notes

- Skills apply to the target project, not just this bootstrap repo.
- Skills can support agents or slash commands.
- Not every skill has a dedicated agent in this repository.
- Some skills are intentionally manual-only via frontmatter because they work better as explicit user-invoked aids than as auto-triggered capabilities.

Examples:
- `notebook-as-code` supports `/organize-notebook`
- `auto-doc-sync` supports `/sync-docs`
- `data-quality-testing` supports `@DataQuality` and `/validate-pipeline`

---

## Structure

Typical skill layout:

```text
.github/skills/[skill-name]/
  SKILL.md
  examples/        # optional
  references/      # optional
  templates/       # optional
  scripts/         # optional
```

Each skill folder must contain `SKILL.md` and may optionally include scripts, examples, templates, checklists, or references.

Examples in this repo:
- `auto-doc-sync/doc-scan.py`
- `data-quality-testing/examples/`
- `data-pipeline-tdd/examples/`
- `fabric-databricks-python-runtime/checklists/`

---

## Validation

This repo includes a basic validator for the skill library:

```bash
python scripts/validate_skills.py
```

It checks for:
- missing `SKILL.md`
- missing or malformed frontmatter
- frontmatter `name` that does not match the directory name
- unusually thin skills

---

## Choosing The Right Entry Point

Use an agent when the repo ships one for the task:
- `@DataQuality`
- `@CodeReviewer`
- `@ProjectScaffolder`

Use a slash command when the task is packaged that way:
- `/organize-notebook`
- `/sync-docs`
- `/lesson`

Use a manual-only skill when the workflow is better as an explicit human step:
- `markdown-notebook-docs`
- `capture-data-eng-lessons`

---

## See Also

- [AGENTS.md](./AGENTS.md)
- [PROMPTS.md](./PROMPTS.md)
- [../tasks/lessons.md](../tasks/lessons.md)
