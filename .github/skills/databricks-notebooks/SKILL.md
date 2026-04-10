---
name: databricks-notebooks
description: >-
  Databricks-specific notebook patterns with Polars-first defaults and clear
  PySpark escalation rules. Use for dbutils boundaries, cluster-aware
  transformations, and robust notebook-to-module extraction.
---

# Databricks Notebooks

Use this skill when targeting Databricks notebooks or Databricks jobs.

## Assets

- `checklists/runtime-readiness.md`

## Core Rules

- Prefer Polars for Python-runtime-friendly workloads
- Escalate to PySpark for distributed joins or very large compute-heavy flows
- Keep `dbutils` usage at notebook boundaries
- Keep extraction paths clear so transform logic is testable in modules

## Typical Use

```text
Build a Databricks notebook flow that reads Delta data, applies Polars-first transforms where possible, falls back to Spark only when distributed execution is required, then validates output.
```
