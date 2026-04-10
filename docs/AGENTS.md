---
title: Agents Reference
---

# Agents Reference

The repo ships three specialist agents for notebook-centric data engineering workflows.

## @DataQuality

Use for:
- schema and constraint validation
- null/duplicate integrity checks
- quality regression tests

Primary skills:
- `data-quality-testing`
- `data-pipeline-tdd`
- `polars-spark-pandas-patterns`
- `microsoft-fabric-notebooks`
- `databricks-notebooks`

## @CodeReviewer

Use for:
- correctness and performance review
- maintainability and extraction guidance
- pre-merge risk checks

Primary skills:
- `python-notebook-code-review`
- `polars-spark-pandas-patterns`

## @ProjectScaffolder

Use for:
- initializing notebook-first project structure
- setting up starter transforms, validators, and tests
- guiding first-step platform choices

Primary skills:
- `python-notebook-structure`
- `data-pipeline-tdd`
- `microsoft-fabric-notebooks`
- `databricks-notebooks`

## Recommended Flow

1. `/setup-project` or `@ProjectScaffolder`
2. `/organize-notebook` for structure and extraction
3. `/validate-pipeline` or `@DataQuality`
4. `/review-code` or `@CodeReviewer`
5. `/lesson` for process capture
