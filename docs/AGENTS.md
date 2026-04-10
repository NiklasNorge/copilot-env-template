---
title: Agents Reference
---

# Agents Reference

This template includes **3 specialist agents**, each with a clear, focused role.

---

## 1. @DataQuality

**Role**: Data validation, quality testing, debugging data anomalies.

**When to invoke**:
- "Validate my pipeline output"
- "Write tests for this transformation"
- "My data has nulls where it shouldn't"
- "Set up quality checks for this table"

**What it does**:
- Checks schema: structure, types, cardinality
- Validates null/key integrity
- Ensures idempotency (pipeline safe to run twice)
- Generates pytest fixtures and assertions
- Flags data quality anti-patterns
- Suggests test-first approach (RED-GREEN-REFACTOR)

**Specialization**:
- **Schema First**: Validates structure before data
- **Aggressive Validation**: Null checks, uniqueness, row counts, business rules
- **Testability Focus**: Everything is assertable and automatable
- **NOT**: Exploratory analysis, visualizations, ad-hoc queries

**Skills it uses**:
- `data-quality-testing` - Assertions, pytest patterns, validators
- `data-pipeline-tdd` - Test-first for data pipelines
- `spark-pandas-best-practices` - Platform-specific validation

**Typical conversation**:
```
You: "Check my ETL output (Spark table with id, amount, date, status)"
Agent: 
  1. Asks: "Constraints? Unique id? Nulls allowed? Valid statuses?"
  2. You answer
  3. Agent generates:
     - Assert schema
     - Assert id is unique
     - Assert no nulls in critical columns
     - Assert date format
     - pytest fixture with edge cases
     - "Ready to run in CI/CD"
```

---

## 2. @CodeReviewer

**Role**: Structured code review with severity grades.

**When to invoke**:
- "Review my code before I push"
- "Is this efficient?"
- "Did I miss any edge cases?"

**What it does**:
- Checks **correctness**: Logic, edge cases, null handling, types
- Flags **performance**: Vectorization, partitioning, memory leaks
- Validates **standards**: PEP 8, type hints, docstrings, error handling
- Reviews **maintainability**: Naming, single responsibility, extractability
- Grades severity: **CRITICAL** (fix before merge) → **MAJOR** → **MINOR** → **FYI**

**Specialization**:
- **Narrow Focus**: Code review only (not testing suggestions, not docs, not reorganization)
- **Consistent Stance**: Same checklist every time, no mood swings
- **Default Reviewer**: Go-to for Python and notebook code quality
- **NOT**: Suggesting test refactors (ask `@DataQuality`), reorganizing notebooks (use `/organize-notebook`), updating docs (use `/sync-docs`)

**Skills it uses**:
- `code-review-notebooks` - Review checklist, severity levels
- `spark-pandas-best-practices` - Platform-specific optimization

**Typical conversation**:
```
You: "Review this transformation function"
Agent:
  ✗ CRITICAL: Row loop over 1M rows — vectorize with apply()
  ✗ MAJOR: No error handling if column missing
  ○ MINOR: Magic number 0.1 should be constant
  ✓ FYI: Type hints suggested for clarity
  
  → Fix CRITICAL before merge
```

---

## 3. @ProjectScaffolder

**Role**: Entrypoint agent for bootstrapping new projects (orchestration only).

**When to invoke**:
- Starting a new data pipeline project
- Using this template for the first time
- "/setup-project" command

**What it does**:
1. **Discovery**: Asks 4-5 key questions about your project goal
2. **Plan**: Summarizes requirements back to you
3. **Scaffold**: Generates folder structure + starter code
4. **Handoff**: "Now use `@DataQuality` for tests" or "`@CodeReviewer` for review"

**Specialization**:
- **Orchestrator Only**: Bootstrap → handoff (not universal build-everything)
- **Focused Scope**: Discovery → scaffold → delegate (not full implementation)
- **Knows When to Stop**: Generates skeleton, hands off to specialists
- **NOT**: Implementing full pipelines, debugging, organizing notebooks

**Discovery Questions** (Always Asks):
1. What's the data source? (CSV, DB, API, Spark, streaming?)
2. What transformations? (filter, join, aggregate, pivot?)
3. Where's the output? (Parquet, Lakehouse, database?)
4. What defines success? (Row count, quality rules, refresh frequency?)
5. Platform preference? (Local Python, PySpark, Fabric, Databricks?)

**Generates**:
- Folder structure (src/, tests/, etc.)
- Starter pipeline skeleton
- Test fixtures and `conftest.py`
- README with setup instructions
- Customized `.github/copilot-instructions.md`

**Skills it uses**:
- `notebook-as-code` - Project structure patterns
- `data-pipeline-tdd` - Test-first bootstrap patterns

**Typical conversation**:
```
User: "/setup-project"
Agent: "Let's bootstrap your project."
  "1. What's your data source?"
  "2. What transformations?"
  ...
  
Agent generates:
  ✓ Folder structure
  ✓ src/data/pipelines/main.py (skeleton)
  ✓ tests/ (with fixtures)
  ✓ README.md
  
  "Next: Customize pyproject.toml, then run `/validate-pipeline` 
   to set up quality checks with @DataQuality"
```

---

## Agent Coordination

### Recommended Flow: New Feature

1. **You** write code
2. **@CodeReviewer** reviews → suggests improvements
3. **@DataQuality** adds/reviews quality checks
4. **@CodeReviewer** final pass
5. Done! Ready to merge

### When to Use Each Agent

| Question | Agent | Or Use Command |
|----------|-------|-----------------|
| "Validate my data?" | @DataQuality | `/validate-pipeline` |
| "Review my code?" | @CodeReviewer | `/review-code` |
| "Set up new project?" | @ProjectScaffolder | `/setup-project` |
| "Organize this notebook?" | — | `/organize-notebook` |
| "Docs out of date?" | — | `/sync-docs` |

### When to Use Prompt Commands Instead

- **`/organize-notebook`**: One-off task (restructure cells, extract functions)
- **`/sync-docs`**: One-off task (detect drift, update docs)
- **`/analyze-data`**: One-off task (explore dataset)
- **`/test-this`**: One-off task (generate tests)
- **`/lesson`**: Capture learnings

---

## Tips for Working with Agents

1. **Be specific**: "Review `src/data/load.py`" (better than "review code")
2. **Share context**: Paste code or file paths for faster analysis
3. **Iterate**: Ask follow-up questions; agents learn your preferences
4. **Use skills**: Reference skills in your questions for more detail
5. **Use Commands for bounded tasks**: `/organize-notebook` is faster than `@ProjectScaffolder` if you just need cell reordering

---

## See Also

- [Slash Commands Reference](./PROMPTS.md) - Quick commands for specific workflows
- [Skills Library](./SKILLS.md) - Deep dive on each skill
- [Setup Guide](./SETUP.md) - Environment setup for agents
