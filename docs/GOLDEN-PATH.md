---
title: Golden Path
---

# Golden Path: Notebook To Tested Pipeline

This is the intended end-to-end workflow for this repo.

## 1. Scaffold

Use:
- `/setup-project`

Outcome:
- notebook and module skeleton
- validator placeholder
- test skeleton

## 2. Build In Notebook First

Use:
- `/organize-notebook`
- `python-notebook-structure`

Rules:
- keep notebook cell order consistent
- keep transforms pure where possible
- isolate platform APIs (`notebookutils` or `dbutils`)

## 3. Extract Stable Logic

Move reusable logic to `src/` modules.

Add tests using:
- `data-pipeline-tdd`
- `data-quality-testing`

## 4. Validate Output Contracts

Use:
- `/validate-pipeline`
- `@DataQuality`

Minimum checks:
- schema columns and types
- non-null keys
- uniqueness constraints
- row-count sanity

## 5. Platform Pass

Fabric-targeted work:
- apply `microsoft-fabric-notebooks`

Databricks-targeted work:
- apply `databricks-notebooks`

Keep Polars first and escalate to PySpark only when distributed execution is needed.

## 6. Review And Finalize

Use:
- `/review-code`
- `@CodeReviewer`
- `/sync-docs`

Then log recurring lessons with:
- `/lesson`
