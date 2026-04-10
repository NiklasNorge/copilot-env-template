# QUICKSTART: Bootstrap A New Data Engineering Project

This repository is a metadata-first bootstrap. You use it to install Copilot behavior into a real project, then let Copilot scaffold code and structure from there.

## Step 1: Choose Your Bootstrap Mode

### Option A: Start A New Project From This Repo

```bash
git clone https://github.com/NiklasNorge/copilot-env-template.git my-data-project
cd my-data-project
```

At this point you have the Copilot metadata and reference assets. You do not yet have a generated `src/` or `tests/` tree.

### Option B: Add Copilot Metadata To An Existing Project

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

If you also want the reference project assets, copy these as needed:
- `pyproject.toml`
- `Makefile`
- `conftest.py`
- `docs/`

## Step 2: Customize The Bootstrap Metadata

### Edit `.github/copilot-instructions.md`

Update the YAML block near the top:

```yaml
project_name: "my-analytics-pipeline"
tech_stack: [Python, Polars, Databricks]
key_links:
  - "Wiki: https://wiki.company.com/data"
  - "Data dictionary: https://wiki.company.com/data-dictionary"
  - "Runbook: https://wiki.company.com/runbook"
```

### Edit Skills You Intend To Rely On

Common first edits:
- `.github/skills/data-quality-testing/SKILL.md`
- `.github/skills/polars-spark-pandas-patterns/SKILL.md`
- `.github/skills/auto-doc-sync/SKILL.md`

Adapt examples, quality rules, and platform-specific guidance to your environment.

### Edit `docs/DATA-PLATFORM-GUIDE.md`

Document the target platform details your team actually uses, such as:
- Databricks cluster/runtime versions
- Fabric Lakehouse conventions
- Secret management patterns
- Internal links and runbooks

## Step 3: Reload VS Code

Reload VS Code after copying and editing the metadata so Copilot reloads the `.github` configuration.

## Step 4: Verify The Bootstrap Works

Success criteria for this repository are metadata-oriented:

1. Copilot agents appear in chat.
2. Slash commands appear when you type `/`.
3. File-type instructions load when you open relevant files.

### Check Agents

Expected agents in this repo:
- `@DataQuality`
- `@CodeReviewer`
- `@ProjectScaffolder`

### Check Commands

Expected commands:
- `/setup-project`
- `/analyze-data`
- `/validate-pipeline`
- `/organize-notebook`
- `/sync-docs`
- `/review-code`
- `/test-this`
- `/lesson`

### Check File-Type Instructions

Open a Python file in your target project and ask Copilot how it should be structured. It should reference the conventions in `.github/instructions/`.

## Step 5: Scaffold The Real Project

Use `@ProjectScaffolder` or `/setup-project` to generate the actual project structure.

Example prompt:

```text
Create a new pipeline project.

Requirements:
- Source: daily CSV export from S3
- Transformations: deduplicate on order_id, standardize timestamps, derive processed_date
- Output: parquet files in the analytics lakehouse
- Quality checks: no nulls in order_id, valid status values, row count should not drop by more than 5 percent
- Platform: Databricks with Python runtime
```

Expected outcome:
- Copilot proposes or generates `src/` and `tests/`
- starter pipeline modules
- test fixtures
- validation patterns
- setup guidance for the generated project

## Step 6: Apply The Reference Assets

After scaffolding the real project, decide which reference assets from this repo you want to adopt:
- `pyproject.toml`
- `Makefile`
- `conftest.py`
- `docs/SETUP.md`

These files are examples for generated projects. They are not meant to imply that this repository itself is already a runnable application.

## Step 7: Capture Lessons

Use `/lesson` after you solve recurring problems or establish new patterns. Store those in `tasks/lessons.md` and use them to improve the skills over time.

## Troubleshooting

### Agents do not appear

Check that `.github/agents/` exists and reload VS Code.

### Commands do not appear

Check that `.github/prompts/` contains the command files and type `/` in Copilot Chat to trigger suggestions.

### Instructions do not seem active

Check that `.github/instructions/` exists and open a matching file type such as `.py` or `.ipynb`.

### You expected `src/` or `tests/` to exist already

That is not the contract of this repository. Those are expected to be created by `/setup-project` or by copying the reference assets into your target project.

## Further Reading

- [README.md](./README.md)
- [docs/AGENTS.md](./docs/AGENTS.md)
- [docs/PROMPTS.md](./docs/PROMPTS.md)
- [docs/SKILLS.md](./docs/SKILLS.md)
- [docs/DATA-PLATFORM-GUIDE.md](./docs/DATA-PLATFORM-GUIDE.md)
