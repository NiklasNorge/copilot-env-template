---
name: fabric-databricks-python-runtime
description: >-
  Apply Polars-first Python-runtime patterns for Microsoft Fabric and
  Databricks, and decide when not to reach for Spark. Use when scaffolding,
  reviewing, or debugging data workflows on those platforms.
---

# Fabric Databricks Python Runtime

Use this skill when the target project runs on Fabric or Databricks and the default choice should be Python runtime plus Polars.

## Assets In This Skill

- `checklists/runtime-readiness.md`: operational checklist for new pipelines

## Core Rules

- Prefer Python runtime plus Polars before Spark.
- Escalate to Spark only for genuinely distributed workloads.
- Keep platform-specific IO and secret handling isolated from transformation code.
- Optimize for cheap, debuggable, notebook-friendly execution first.

## Typical Usage

```text
Use fabric-databricks-python-runtime to scaffold a daily ingestion job that reads parquet from the lakehouse, transforms with Polars, validates output, and only falls back to Spark if distribution becomes necessary.
```
