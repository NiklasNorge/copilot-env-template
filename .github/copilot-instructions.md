# Copilot Instructions for Data Engineering Projects

**Ecosystem**: Reusable, portable Copilot setup for solo data engineers  
**Stack**: Python, Polars (primary), Python runtime on Fabric/Databricks  
**Auto-loads**: Context rules + skills per file type

<!-- CUSTOMIZE BEFORE FIRST USE -->

---

## 🚀 First Steps (5 min)

1. Edit `project_name`, `tech_stack`, `key_links` in the YAML below
2. Customize: `docs/DATA-PLATFORM-GUIDE.md` (your platform)
3. Run `/setup-project` to auto-generate folder structure

```yaml
project_name: "YOUR_PROJECT_NAME"
tech_stack: [Python, Polars, "Python runtime on Fabric/Databricks"]
key_links:
  - "Wiki: [your-link]"
  - "Data dictionary: [your-link]"
  - "Docs: [your-link]"
```

---

## 🤖 Tools at Your Fingertip

**3 Specialist Agents** (Copilot Chat):
- `@DataQuality` — Validate data, write quality tests, catch anomalies
- `@CodeReviewer` — Structured code review with severity grading
- `@ProjectScaffolder` — Bootstrap new projects (discovery → scaffold → handoff)

**8 Slash Commands** (Type `/` in Chat):
- `/setup-project`, `/analyze-data`, `/validate-pipeline`, `/review-code`
- `/organize-notebook`, `/sync-docs`, `/test-this`, `/lesson`

**Full reference**: [docs/AGENTS.md](../docs/AGENTS.md), [docs/PROMPTS.md](../docs/PROMPTS.md)

---

## 📋 Auto-Loading Context Rules

Context rules load automatically when you open specific file types:

| When You Open | Loads | For |
|---------------|-------|-----|
| `.py` files | `python.instructions.md` + data eng rules | Style, imports, types |
| `.ipynb` files | `notebooks.instructions.md` + data eng rules | Cell org, extraction |
| `test_*.py` | `testing-and-quality.instructions.md` | TDD, pytest patterns |
| Databricks/Fabric | `fabric-and-databricks.instructions.md` | Python runtime + Polars |

**Details**: `.github/instructions/` directory

---

## 📁 Project Layout

```
PROJECT_ROOT/
├── .github/
│   ├── copilot-instructions.md    ← This file (root manifest)
│   ├── agents/ + instructions/ + skills/ + prompts/
├── docs/                          ← Guides: AGENTS, SKILLS, PROMPTS, SETUP, DATA-PLATFORM-GUIDE
├── src/data/pipelines/            ← ETL code
├── src/data/validators/           ← Quality checks
├── src/notebooks/                 ← Analysis & reports
├── tests/unit/ + tests/integration/
└── pyproject.toml, Makefile, conftest.py
```

Run `/setup-project` to auto-generate `src/` + `tests/` structure.

---

## 📚 Navigation

- **Getting Started**: [QUICKSTART.md](../QUICKSTART.md) or `/setup-project`
- **Skills & Techniques**: [docs/SKILLS.md](../docs/SKILLS.md)
- **Agent Patterns**: [docs/AGENTS.md](../docs/AGENTS.md)
- **Slash Commands**: [docs/PROMPTS.md](../docs/PROMPTS.md)
- **Platform Setup**: [docs/SETUP.md](../docs/SETUP.md) + [docs/DATA-PLATFORM-GUIDE.md](../docs/DATA-PLATFORM-GUIDE.md)
- **Learn & Improve**: [tasks/lessons.md](../tasks/lessons.md)

---

## ❓ Quick Help

- **How do I start?** → `/setup-project` or [QUICKSTART.md](../QUICKSTART.md)
- **I'm stuck** → Use `@DataQuality` or `@CodeReviewer` agents
- **Platform questions?** → [docs/DATA-PLATFORM-GUIDE.md](../docs/DATA-PLATFORM-GUIDE.md)
- **Which tool to use?** → [docs/SKILLS.md](../docs/SKILLS.md)


