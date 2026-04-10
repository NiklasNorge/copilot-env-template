# QUICKSTART: New Data Engineering Project — 10 Minutes ⚡

This guide walks you through setting up a new data engineering project using this template.

---

## Step 1: Clone or Copy (2 min)

### Option A: Start Fresh

```bash
git clone https://github.com/NiklasNorge/copilot-env-template.git my-data-project
cd my-data-project

# Optional: Remove template history, start fresh
rm -rf .git
git init
git add .
git commit -m "Initial: Data engineering project with Copilot"
```

### Option B: Add to Existing Project

```bash
# Copy everything from the template
cp -r /path/to/copilot-env-template/.github ./
cp /path/to/copilot-env-template/skills.md ./
cp /path/to/copilot-env-template/.github/copilot-instructions.md ./

# Create tasks folder if it doesn't exist
mkdir -p tasks
echo "# Lessons Log\n" > tasks/lessons.md

# Add to git
git add .github/ skills.md tasks/lessons.md
git commit -m "feat: Add Copilot data engineering template"
```

---

## Step 2: Customize (4 min)

### Edit `.github/copilot-instructions.md` — SETUP REQUIRED Section

Open the file and find the **SETUP REQUIRED** block (near the top). Fill in:

```yaml
project_name: "my-analytics-pipeline"          ← Your project name
tech_stack:
  - Python (core)
  - "PySpark"                                   ← Choose: PySpark or Pandas
  - "Databricks"                                ← Choose: Databricks or Fabric
primary_focus:
  - "Data pipelines"                            ← Your focus
key_links:
  - "Wiki: https://wiki.company.com/data"
  - "Data dict: [link]"
```

**Keep the rest of the file as-is** (standards, conventions, folder structure).

### Edit `skills/data-quality-testing/SKILL.md`

Open and customize:
- **Testing framework**: pytest ✅ (already set), or change to `great_expectations`
- **Assertion patterns**: Replace generic examples with your actual quality rules
- **Example schema**: Use your actual table schemas

### Edit `skills/spark-pandas-best-practices/SKILL.md`

Choose your platform:
- **PySpark**: Uncomment Spark sections, comment out Pandas
- **Pandas**: Uncomment Pandas sections, comment out Spark

*Keep data validation sections — those apply to both.*

### Edit `docs/DATA-PLATFORM-GUIDE.md`

Add platform-specific details:

```markdown
## Databricks Setup (if using Databricks)
- **Cluster**: Python 3.10+, Spark 3.3+
- **Catalog**: Use Unity Catalog with pattern: `workspace.schema.table`
- **Config**: Store secrets in `utils/config.py`, fetch from Secrets API
- **Example**: [link to your workspace wiki]

## Fabric Setup (if using Fabric)
- **Lakehouse**: `/Shared/your_lakehouse`
- **Default Schema**: `dbo` or custom
- **Config**: Environment variables + Fabric SDK
- **Example**: [link to your Fabric workspace]
```

---

## Step 3: Reload VS Code (30 sec)

Close VS Code completely, then reopen your project. Copilot agents should now appear in the Copilot Chat dropdown.

```bash
# Or restart VS Code: Ctrl+Shift+P → "Developer: Reload Window"
```

---

## Step 4: Test It Works (2 min)

### Test 1: Invoke an Agent

1. Open Copilot Chat (Ctrl+L or Cmd+L)
2. Look for the **agent** dropdown (top-left of chat)
3. Select **@ProjectScaffolder**
4. Type: `Create a folder structure for a daily ETL pipeline`
5. ✅ Should respond with folder suggestions + sample code

### Test 2: Use a Slash Command

1. In Copilot Chat, type: `/setup-project`
2. ✅ Should present setup wizard

### Test 3: Check File-Type Instructions

1. Create a new file: `src/data/sample_pipeline.py`
2. Open it in VS Code
3. In Copilot Chat, type: `How should I structure this file?`
4. ✅ Should reference Python + data engineering conventions from `.github/instructions/`

---

## Step 5: Create Your First Pipeline (Use as Template)

In Copilot Chat, select `@ProjectScaffolder` and adapt this prompt:

```
Create a new pipeline for: [your data source]
Requirements:
- Load from [source: CSV/database/API]
- Transform: [describe transformations]
- Validate: [quality checks you need]
- Output: [destination]
Tech: PySpark (or Pandas)
```

Copilot will:
1. Generate folder structure
2. Create sample code (load → transform → validate → store)
3. Generate pytest tests
4. Suggest CI/CD setup

---

## Step 6: Capture Your First Lesson (Optional but Recommended)

After your first successful pipeline or bug fix:

```
Copilot Chat → /lesson
```

Answer:
- **Problem**: What went wrong? (or what was tricky?)
- **Root Cause**: Why did it happen?
- **Fix**: How did you solve it?
- **Tags**: `pyspark`, `data-quality`, `notebooks`

This logs to `tasks/lessons.md`. Later, patterns become new skills or rule amendments.

---

## 📂 Your Project Structure (After Customization)

```
my-data-project/
├── .github/
│   ├── copilot-instructions.md       ✅ CUSTOMIZED
│   ├── agents/                       (5 agents, ready to use)
│   ├── instructions/                 (auto-loading per file type)
│   ├── skills/                       (8 skills, with customized SKILL.md files)
│   └── prompts/                      (8 slash commands)
├── skills.md                         ✅ Ready (auto-discovered)
├── tasks/
│   └── lessons.md                    ✅ Empty (ready for lessons)
├── docs/
│   ├── DATA-PLATFORM-GUIDE.md        ✅ CUSTOMIZED
│   ├── AGENTS.md
│   ├── SKILLS.md
│   ├── PROMPTS.md
│   ├── SETUP.md
│   ├── PIPELINE-CATALOG.md
│   └── DECISIONS.md
├── src/
│   ├── data/
│   │   ├── pipelines/
│   │   ├── validators/
│   │   └── fixtures/
│   ├── notebooks/
│   │   ├── exploratory/
│   │   ├── reports/
│   │   └── templates/
│   └── utils/
├── tests/
├── pyproject.toml                    (ready to use)
├── Makefile                          (ready: make test, make lint, etc.)
└── .gitignore                        (ready)
```

---

## 🚀 Next: Start Coding

You're ready! Pick one:

### 1. Build a Small Pipeline (10 min)

```bash
Copilot Chat → @ProjectScaffolder

"Create a simple ETL pipeline:
 - Read data from tests/data/sample.csv
 - Add a 'processed_date' column
 - Validate: no nulls in ID
 - Save to src/data/pipelines/transformed.csv"
```

### 2. Write Tests for an Existing Function

```bash
Copilot Chat → /test-this

"Generate tests for: [paste function code]"
```

### 3. Organize & Refactor a Notebook

```bash
Copilot Chat → @NotebookOrganizer

"Reorganize my notebook to separate Logic, Tests, and Execution"
```

### 4. Validate a Dataset

```bash
Copilot Chat → /analyze-data

"Analyze tests/data/sample.csv and flag any anomalies"
```

---

## ✅ Checklist

- [ ] Cloned/copied template
- [ ] Customized `.github/copilot-instructions.md` (SETUP REQUIRED section)
- [ ] Customized `skills/data-quality-testing/SKILL.md`
- [ ] Customized `skills/spark-pandas-best-practices/SKILL.md`
- [ ] Customized `docs/DATA-PLATFORM-GUIDE.md`
- [ ] Reloaded VS Code
- [ ] Tested an agent (should work)
- [ ] Tested a slash command (should work)
- [ ] Created first pipeline OR logged first lesson
- [ ] ✨ Ready to build!

---

## 🆘 Troubleshooting

### Agents not appearing in Copilot Chat dropdown?

1. Check: `.github/agents/` folder exists with `.md` files
2. Verify: VS Code settings has `"chat.instructionsFilesLocations": [".github/instructions"]`
3. Fix: Reload VS Code (`Ctrl+Shift+P` → Reload Window)

### Instructions not loading when I open a `.py` file?

1. Verify: `.github/instructions/python.instructions.md` exists
2. Check: File path matches trigger pattern (e.g., `src/**/*.py`)
3. Fix: Copilot may need a 30-sec delay; try reopening file

### Slash commands not appearing?

1. Check: `.github/prompts/` has the files you want
2. Verify: File names match command you're typing (e.g., `/analyze-data` → `analyze-data.prompt.md`)
3. Fix: Type `/` and wait for suggestions to populate

### Skills not loading?

1. Verify: `skills.md` exists at repo root
2. Check: Each skill folder has a `SKILL.md` file
3. Fix: `skills.md` may have broken links — verify skill paths

### Still stuck?

- Check [docs/AGENTS.md](./docs/AGENTS.md)
- Check [docs/SKILLS.md](./docs/SKILLS.md)
- Open an issue on GitHub

---

## 📖 Further Reading

- **Full README**: [README.md](./README.md) — Overview & workflows
- **Agents Guide**: [docs/AGENTS.md](./docs/AGENTS.md) — What each agent does
- **Skills Guide**: [docs/SKILLS.md](./docs/SKILLS.md) — Deep-dive on each skill
- **Platform Guide**: [docs/DATA-PLATFORM-GUIDE.md](./docs/DATA-PLATFORM-GUIDE.md) — Fabric & Databricks specifics
- **Lessons Guide**: [tasks/lessons.md](../tasks/lessons.md) — Self-improvement workflow

---

**You're all set! 🎉 Start your first pipeline now.**
