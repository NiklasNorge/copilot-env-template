# Copilot Instructions for Notebook Engineering

Opinionated bootstrap for Python notebook work on Microsoft Fabric and Databricks.

## Baseline

- Python compatibility floor: 3.11
- Preferred style target: 3.12
- Dataframe policy: Polars first, PySpark when distributed execution is required

## Project Setup

Update this block before using the bootstrap:

```yaml
project_name: "YOUR_PROJECT_NAME"
platform: "Fabric or Databricks"
tech_stack: [Python, Polars, PySpark]
key_links:
  - "Wiki: [your-link]"
  - "Runbook: [your-link]"
```

## Agents

- `@DataQuality`
- `@CodeReviewer`
- `@ProjectScaffolder`

## Prompt Files

Prompt files live in `.github/prompts/` and use the `*.prompt.md` naming convention.

## Auto-Loaded Instructions

- `python.instructions.md`
- `notebooks.instructions.md`
- `testing-and-quality.instructions.md`
- `fabric.instructions.md`
- `databricks.instructions.md`

## Skills

Skills live in `.github/skills/` and are used for deeper, task-specific workflows with optional helper assets.

## Navigation

- `QUICKSTART.md`
- `docs/GOLDEN-PATH.md`
- `docs/AGENTS.md`
- `docs/PROMPTS.md`
- `docs/SKILLS.md`
