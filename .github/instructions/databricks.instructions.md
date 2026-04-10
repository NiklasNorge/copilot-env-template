---
name: databricks.instructions
description: Auto-loads for Databricks notebook work.
---

# Databricks Notebook Rules

Use these rules when working in Databricks notebooks or Databricks-targeted modules.

## Runtime And Engine Policy

- Python compatibility floor: 3.11
- Prefer 3.12 style when runtime allows
- Default to Polars in Python-friendly workloads
- Use PySpark when you need distributed execution, large joins, or cluster-native operations

## Databricks-Specific Conventions

- Keep `dbutils` usage at notebook boundaries
- Separate platform/IO/secrets code from transform code
- Keep transform functions importable and testable from modules
- Use clear table/path conventions and avoid hidden path assumptions

## Guardrails

- Avoid `.collect()` on large datasets unless justified
- Keep quality assertions on key columns and row-count expectations
- Add tests for extraction code moved from notebook cells
- Prefer explicit runtime decisions in comments when Spark is required

## Prefer Skills

- `databricks-notebooks`
- `python-notebook-structure`
- `data-quality-testing`
- `polars-spark-pandas-patterns`
