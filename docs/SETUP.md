---
title: Environment Setup
---

# Environment Setup

This guide is for the project you bootstrap with this repository.

The bootstrap repo itself is metadata-first. If you have not generated or added a real `src/` and `tests/` layout yet, some project-level commands below are not supposed to work yet.

---

## Python Baseline

- Python 3.11 or newer
- Prefer Python 3.12 for local development and new generated projects
- Git
- VS Code with GitHub Copilot and GitHub Copilot Chat

Write code that stays compatible with Python 3.11+, but prefer 3.12-era style and standard-library usage unless a platform runtime requires otherwise.

---

## Base Setup For A Generated Project

### 1. Create A Virtual Environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

Optional platform extras:

```bash
pip install -e ".[dev,databricks]"
pip install -e ".[dev,fabric]"
```

### 3. Verify The Generated Project

Once the project has actual code and tests, run the relevant commands:

```bash
make test
make lint
make format
```

---

## Configuration

Create a `.env` file in the target project if needed:

```bash
ENV=development
DATA_DIR=./data
LOG_LEVEL=DEBUG
DB_HOST=localhost
DB_NAME=dev_db
DB_USER=postgres
DB_PASSWORD=***
```

Do not hardcode credentials. Use environment variables or platform secret stores.

---

## VS Code Setup

Recommended extensions:
- GitHub Copilot
- GitHub Copilot Chat
- Python
- Pylance
- Black Formatter
- Ruff

Example `.vscode/settings.json` for a generated project:

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.analysis.typeCheckingMode": "basic"
}
```

---

## Platform Notes

For Databricks and Fabric specifics, see [DATA-PLATFORM-GUIDE.md](./DATA-PLATFORM-GUIDE.md).

---

## Reference Assets In This Repo

This repository includes:
- [pyproject.toml](../pyproject.toml)
- [Makefile](../Makefile)
- [conftest.py](../conftest.py)

Treat them as reference assets for the generated project. They may need adaptation after `/setup-project` creates the real code layout.
