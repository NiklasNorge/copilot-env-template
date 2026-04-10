# Data Engineering Copilot + Project Template 🚀

A **reusable, portable Copilot ecosystem** for solo data engineers working with Python, Polars, Microsoft Fabric, and Databricks.

**What You Get**:
- ✅ 5 specialist agents (Data Quality, Notebooks, Docs Sync, Code Review, Project Setup)
- ✅ 8 reusable skills (data validation, documentation, testing, notebook organization)
- ✅ Lightweight governance (suggestions, no enforced gates)
- ✅ Self-improving lessons log for capturing recurring patterns
- ✅ Platform-aware guidance for Fabric & Databricks (Python runtime preferred)
- ✅ Polars-first, Python runtime on cloud platforms

**Use Case**: Build new data engineering projects faster by cloning this template, customizing 4 files, and inheriting the entire Copilot ecosystem.

---

## 🚀 Quick Start

**→ For a 10-minute step-by-step setup, see [QUICKSTART.md](./QUICKSTART.md)**

For existing projects, copy `.github/` and customize:

```bash
cp -r /path/to/copilot-env-template/.github ./
cp /path/to/copilot-env-template/.github/copilot-instructions.md ./.github/
mkdir -p tasks && echo "# Lessons Log" > tasks/lessons.md
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **[QUICKSTART.md](./QUICKSTART.md)** | 10-min setup guide: clone, customize, test |
| **[.github/copilot-instructions.md](./.github/copilot-instructions.md)** | Root manifest (customize SETUP section) |
| **[docs/AGENTS.md](./docs/AGENTS.md)** | What each agent does + delegation patterns |
| **[docs/SKILLS.md](./docs/SKILLS.md)** | Deep-dive on 8 skills with examples |
| **[docs/DATA-PLATFORM-GUIDE.md](./docs/DATA-PLATFORM-GUIDE.md)** | Fabric & Databricks specifics |
| **[docs/SETUP.md](./docs/SETUP.md)** | Environment setup (Python, Databricks, Fabric) |
| **[tasks/lessons.md](./tasks/lessons.md)** | Self-improvement log (auto-updated)

---

## 🤖 Agents & Commands at a Glance

**Agents**: `@DataQuality`, `@NotebookOrganizer`, `@DocsSync`, `@CodeReviewer`, `@ProjectScaffolder`

**Commands**: `/setup-project`, `/analyze-data`, `/validate-pipeline`, `/organize-notebook`, `/sync-docs`, `/review-code`, `/test-this`, `/lesson`

→ See **[docs/AGENTS.md](./docs/AGENTS.md)** and **[docs/PROMPTS.md](./docs/PROMPTS.md)** for details

---

## � Advanced: Model Context Protocol (MCP)

For integrating external systems (databases, APIs, calendars) with Copilot:
- See [MCP Documentation](https://modelcontextprotocol.io/)
- Copilot can now connect to data sources, tools, and workflows via MCP
- **Future enhancement**: Consider MCP for live data validation or platform integration

---

## 📖 Guides & Workflows

**Getting Started**:
- Clone/copy template → Customize 4 files → Reload VS Code (see [QUICKSTART.md](./QUICKSTART.md))

**Common Workflow Examples**:

1. **Start a new pipeline**: `@ProjectScaffolder` → Generates structure, code, tests
2. **Validate data**: `@DataQuality` → Writes assertions + pytest fixtures
3. **Test-driven development**: `/test-this` → Generates RED test, you write code, Copilot suggests REFACTOR
4. **Keep docs in sync**: `@DocsSync` → Scans for drifts, proposes updates
5. **Code review**: `@CodeReviewer` or `/review-code` → Structured feedback
6. **Log lessons**: `/lesson` → Captures recurring patterns for future reference

---

## 🔧 Local Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .
make test                # or: pytest tests/
make format             # or: black src/ tests/
```

See `Makefile` for all commands.

---

## 🎓 Resources

| Resource | Link |
|----------|------|
| GitHub Copilot Docs | [docs.github.com/copilot](https://docs.github.com/en/copilot) |
| Awesome Copilot | [github.com/awesome-copilot](https://github.com/github/awesome-copilot) |
| Databricks | [docs.databricks.com](https://docs.databricks.com/en/index.html) |
| Microsoft Fabric | [learn.microsoft.com/fabric](https://learn.microsoft.com/en-us/fabric/) |
| pytest | [docs.pytest.org](https://docs.pytest.org/) |
| Polars | [docs.pola.rs](https://docs.pola.rs/) |
