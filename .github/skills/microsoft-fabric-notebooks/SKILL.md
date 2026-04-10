---
name: microsoft-fabric-notebooks
description: >-
  Fabric-specific notebook patterns with Python-runtime-first, Polars-first
  defaults. Use for Lakehouse workflows, notebookutils boundaries, and
  cost-aware runtime decisions.
---

# Microsoft Fabric Notebooks

Use this skill when targeting Microsoft Fabric notebooks and Lakehouse workflows.

## Assets

- `checklists/runtime-readiness.md`

## Core Rules

- Prefer Python runtime plus Polars before Spark
- Keep `notebookutils` usage near notebook boundaries
- Keep transforms in importable modules where practical
- Validate output schema and key constraints before persistence

## Typical Use

```text
Scaffold a Fabric notebook workflow that reads Lakehouse parquet, transforms in Polars, validates quality checks, and writes partitioned output.
```
