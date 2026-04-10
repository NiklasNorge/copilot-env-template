# Copilot Instructions for Data Engineering Projects

**Ecosystem**: reusable Copilot bootstrap for data engineering projects  
**Stack**: Python, Polars-first, Python runtime on Fabric or Databricks  
**Scope**: metadata-first; use this file to steer Copilot before scaffolding code

<!-- CUSTOMIZE BEFORE FIRST USE -->

---

## First Steps

1. Edit `project_name`, `tech_stack`, and `key_links` in the YAML below.
2. Customize `docs/DATA-PLATFORM-GUIDE.md` for your environment.
3. Run `/setup-project` to generate the real project structure in the target repository.

```yaml
project_name: "YOUR_PROJECT_NAME"
tech_stack: [Python, Polars, "Python runtime on Fabric/Databricks"]
key_links:
  - "Wiki: [your-link]"
  - "Data dictionary: [your-link]"
  - "Docs: [your-link]"
```

---

## Tools At Your Fingertip

**3 Specialist Agents**
- `@DataQuality`
- `@CodeReviewer`
- `@ProjectScaffolder`

**8 Slash Commands**
- `/setup-project`, `/analyze-data`, `/validate-pipeline`, `/review-code`
- `/organize-notebook`, `/sync-docs`, `/test-this`, `/lesson`

Reference docs:
- `docs/AGENTS.md`
- `docs/PROMPTS.md`

---

## Auto-Loading Context Rules

Context rules load when you open matching file types in the target project:

| When You Open | Loads | For |
|---------------|-------|-----|
| `.py` files | `python.instructions.md` plus data engineering rules | style, imports, types |
| `.ipynb` files | `notebooks.instructions.md` plus data engineering rules | cell organization, extraction |
| `test_*.py` | `testing-and-quality.instructions.md` | TDD and pytest patterns |
| Fabric or Databricks code | `fabric-and-databricks.instructions.md` | runtime and platform guidance |

---

## Repository Role

This repository ships Copilot metadata and reference assets.

It does not guarantee that `src/` and `tests/` already exist. Those are expected to be generated or added after you use `/setup-project` in the target project.

Reference assets included here:
- `.github/agents/`
- `.github/instructions/`
- `.github/prompts/`
- `.github/skills/`
- `pyproject.toml`
- `Makefile`
- `conftest.py`

Treat the Python tooling files as examples for the generated project, not as proof that this repository itself is a runnable app template.

---

## Navigation

- Getting started: `QUICKSTART.md`
- Skills and techniques: `docs/SKILLS.md`
- Agent patterns: `docs/AGENTS.md`
- Slash commands: `docs/PROMPTS.md`
- Platform setup: `docs/SETUP.md` and `docs/DATA-PLATFORM-GUIDE.md`
- Lessons log: `tasks/lessons.md`

---

## Quick Help

- How do I start? Use `/setup-project` or read `QUICKSTART.md`.
- Which agent should I use? See `docs/AGENTS.md`.
- Which command should I use? See `docs/PROMPTS.md`.
- Which platform guidance applies? See `docs/DATA-PLATFORM-GUIDE.md`.
