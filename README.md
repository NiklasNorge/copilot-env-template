# Data Engineering Copilot Bootstrap Reference

An opinionated Copilot bootstrap reference for Python notebook engineering on Microsoft Fabric and Databricks.

This repository is metadata-first. Its primary purpose is to provide Copilot agents, prompt files, instructions, and skills that you copy into a real project and then use to scaffold project structure and workflow behavior.

Python policy for generated projects: support Python 3.11+, prefer Python 3.12 by default.

**What you get**
- 3 specialist agents: Data Quality, Code Review, Project Scaffolding
- 10 reusable skills covering validation, documentation, testing, notebook structure, and platform-specific Fabric/Databricks heuristics
- 8 slash commands for common workflows
- Project-level instructions for Python, notebooks, testing, and Fabric/Databricks work
- Reference `pyproject.toml`, `Makefile`, and `conftest.py` assets you can adapt in generated projects

**What this repo is not**
- Not a prebuilt starter application
- Not a repository with shipped `src/` and `tests/` trees
- Not expected to pass app-level lint/test commands before you scaffold a target project
- Not intended to be published as a Python package

## Quick Start

For step-by-step setup, see [QUICKSTART.md](./QUICKSTART.md).

For an existing project, copy the Copilot metadata and the lessons log:

```bash
cp -r /path/to/copilot-env-template/.github ./
mkdir -p tasks
echo "# Lessons Log" > tasks/lessons.md
```

PowerShell equivalent:

```powershell
Copy-Item -Recurse C:\path\to\copilot-env-template\.github .github
New-Item -ItemType Directory -Force tasks | Out-Null
Set-Content tasks\lessons.md "# Lessons Log"
```

Then customize:
- `.github/copilot-instructions.md`
- `docs/DATA-PLATFORM-GUIDE.md`
- Any skill files you want to tune for your team or platform

## Repository Contents

| Path | Purpose |
|------|---------|
| [QUICKSTART.md](./QUICKSTART.md) | Bootstrap flow for a new or existing project |
| [.github/copilot-instructions.md](./.github/copilot-instructions.md) | Root manifest for the Copilot setup |
| [docs/AGENTS.md](./docs/AGENTS.md) | Agent roles and handoff patterns |
| [docs/PROMPTS.md](./docs/PROMPTS.md) | Slash command reference |
| [docs/SKILLS.md](./docs/SKILLS.md) | Skill catalog and customization guidance |
| [docs/SETUP.md](./docs/SETUP.md) | Environment setup for the project you bootstrap |
| [docs/DATA-PLATFORM-GUIDE.md](./docs/DATA-PLATFORM-GUIDE.md) | Fabric and Databricks guidance |
| [docs/GOLDEN-PATH.md](./docs/GOLDEN-PATH.md) | End-to-end notebook-to-tested-pipeline workflow |
| [tasks/lessons.md](./tasks/lessons.md) | Lessons log template |

## Agents And Commands

**Agents**
- `@DataQuality`
- `@CodeReviewer`
- `@ProjectScaffolder`

**Commands**
- `/setup-project`
- `/analyze-data`
- `/validate-pipeline`
- `/organize-notebook`
- `/sync-docs`
- `/review-code`
- `/test-this`
- `/lesson`

See [docs/AGENTS.md](./docs/AGENTS.md) and [docs/PROMPTS.md](./docs/PROMPTS.md) for details.

Prompt files in `.github/prompts/` use `*.prompt.md`.

## How To Use This Template

1. Copy `.github/` into a real project, or clone this repo as the starting point for a new project.
2. Customize `.github/copilot-instructions.md` so Copilot sees your project name, stack, and links.
3. Tune any skills that should reflect your platform conventions.
4. Reload VS Code so Copilot picks up the metadata.
5. Use `/setup-project` to scaffold `src/`, `tests/`, and starter code in the target project.
6. Use the other agents and prompts to iterate on the generated project.

## Reference Assets

This repository includes `pyproject.toml`, `Makefile`, and `conftest.py` as reference assets.

Treat them as examples for the project you generate. They are not evidence that this repository already contains a runnable application.

Important:
- `make test`, `make lint`, and related targets are for generated projects with `src/` and `tests/`
- do not treat this bootstrap repo itself as the runtime target for those commands
- copy/adapt the reference files after `/setup-project` creates the real project layout

## Resources

| Resource | Link |
|----------|------|
| GitHub Copilot Docs | [docs.github.com/copilot](https://docs.github.com/en/copilot) |
| Databricks | [docs.databricks.com](https://docs.databricks.com/en/index.html) |
| Microsoft Fabric | [learn.microsoft.com/fabric](https://learn.microsoft.com/en-us/fabric/) |
| pytest | [docs.pytest.org](https://docs.pytest.org/) |
| Polars | [docs.pola.rs](https://docs.pola.rs/) |
