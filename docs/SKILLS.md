---
title: Skills Library Reference
---

# Skills Library

This repo keeps a notebook-first, platform-explicit skill set.

## Core Skills

| Skill | Purpose |
|---|---|
| `python-notebook-structure` | Consistent notebook layout and extraction |
| `data-quality-testing` | Validators, fixtures, and quality test patterns |
| `data-pipeline-tdd` | RED-GREEN-REFACTOR for transforms and pipelines |
| `polars-spark-pandas-patterns` | Engine choice and performance patterns |
| `python-notebook-code-review` | Structured notebook/module code review |
| `auto-doc-sync` | Drift detection between code and docs |

## Platform Skills

| Skill | Purpose |
|---|---|
| `microsoft-fabric-notebooks` | Fabric-specific notebook/runtime guidance |
| `databricks-notebooks` | Databricks-specific notebook/runtime guidance |

## Manual-Only Skills

| Skill | Purpose |
|---|---|
| `capture-data-eng-lessons` | Lessons log process |
| `notebook-doc-templates` | Documentation template pack |

## Skill Structure

Each skill directory must contain `SKILL.md` and may include optional assets:
- examples
- templates
- checklists
- helper scripts

## Validation

Run:

```bash
python scripts/validate_skills.py
```

This checks naming, frontmatter, and minimum structural quality.
