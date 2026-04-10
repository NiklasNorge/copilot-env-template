---
name: fabric.instructions
description: Auto-loads for Microsoft Fabric notebook work.
---

# Microsoft Fabric Notebook Rules

Use these rules when working in Fabric notebooks or Fabric-targeted modules.

## Runtime And Engine Policy

- Python compatibility floor: 3.11
- Prefer 3.12 style when runtime allows
- Default to Polars for transforms in Python runtime
- Use Spark only when distribution is truly required

## Fabric-Specific Conventions

- Use Fabric workspace and Lakehouse path conventions
- Keep `notebookutils` calls at the notebook boundary, not deep in transform logic
- Separate IO/secrets/platform glue from data transforms
- Keep core transforms importable so they can be tested outside notebook cells

## Guardrails

- Avoid row-wise loops for dataframe operations
- Keep schema and quality assertions near load/transform boundaries
- Add test coverage for extracted functions in `src/` modules
- Keep cell order predictable: imports, config, functions, execution

## Prefer Skills

- `microsoft-fabric-notebooks`
- `python-notebook-structure`
- `data-quality-testing`
- `polars-spark-pandas-patterns`
