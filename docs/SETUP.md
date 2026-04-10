---
title: Environment Setup
---

# Environment Setup

This guide covers setting up the development environment for this data engineering project.

---

## Prerequisites

- **Python**: 3.8+ (check with `python --version`)
- **Git**: For version control
- **VS Code**: With GitHub Copilot extension

---

## Local Development Setup

### 1. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n data-eng python=3.10
conda activate data-eng
```

### 2. Install Dependencies

```bash
# Install core + dev dependencies
pip install -e ".[dev]"

# Or install specific platforms
pip install -e ".[dev,databricks]"    # For Databricks
pip install -e ".[dev,fabric]"        # For Fabric
```

### 3. Verify Installation

```bash
# Run tests
make test-quick

# Run linter
make lint

# Format code
make format
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (add to `.gitignore`):

```bash
# Platform config
ENV=development
DATA_DIR=./data
LOG_LEVEL=DEBUG

# Database (if applicable)
DB_HOST=localhost
DB_NAME=dev_db
DB_USER=postgres
DB_PASSWORD=***

# API Keys (store securely!)
# Never hardcode credentials — use environment variables or secret managers
```

### For Databricks

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure authentication
databricks configure --token
# (Enter host URL and token from workspace)
```

### For Fabric

```bash
# Install Fabric SDK
pip install microsoft-fabric

# Authenticate with Azure
# Use VS Code "Microsoft account" extension
```

---

## IDE Setup (VS Code)

### Extensions

- **GitHub Copilot** (GitHub.copilot)
- **GitHub Copilot Chat** (GitHub.copilot-chat)
- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Black Formatter** (ms-python.black-formatter)
- **Ruff** (charliermarsh.ruff)

### Recommended Settings

Add to `.vscode/settings.json`:

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
  "python.linting.ruffEnabled": true,
  "python.analysis.typeCheckingMode": "basic"
}
```

---

## Running Tests

```bash
# All tests with coverage
make test

# Quick test (no coverage)
make test-quick

# Watch mode (re-run on file change)
make test-watch

# Unit tests only
make test-unit

# Integration tests only
make test-integration

# Specific test file
pytest tests/unit/test_transforms.py -v
```

---

## Common Issues

### Issue: ModuleNotFoundError on import

```bash
# Solution: Install in editable mode
pip install -e "."
```

### Issue: Databricks connection timeout

```bash
# Solution: Check host and token
databricks configure --token
# Verify in ~/.databrickscfg
```

### Issue: Fabric authentication fails

```bash
# Solution: Clear Azure CLI cache
az account clear
# Then re-authenticate
```

---

## Further Reading

- [pyproject.toml](../pyproject.toml) - Dependencies and configuration
- [Makefile](../Makefile) - Available commands
- `.github/instructions/` - Coding standards (auto-loaded by file type)
