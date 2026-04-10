---
title: Skills Library Reference
---

# Skills Library

This template includes 8 reusable skills that guide best practices for data engineering, code quality, documentation, and self-improvement.

---

## Overview

| Skill | Purpose | When to Use |
|-------|---------|------------|
| **data-quality-testing** | Validation patterns, assertions, fixtures | Writing quality checks for pipelines |
| **spark-pandas-best-practices** | Platform optimization (Spark vs Pandas) | Choosing framework, optimizing large data |
| **notebook-as-code** | Cell organization, extraction, testability | Organizing notebooks, converting to production |
| **auto-doc-sync** | Keeping code & docs synchronized | Updating docs after code changes |
| **markdown-notebook-docs** | Documentation structure & templates | Writing READMEs, data dictionaries |
| **data-pipeline-tdd** | Test-driven development for pipelines | Writing tests before code (RED-GREEN-REFACTOR) |
| **code-review-notebooks** | Code review checklists, severity levels | Reviewing code before merge |
| **capture-data-eng-lessons** | Structured lesson capture, pattern detection | Logging problems & solutions, improving processes |

---

## 1. Data Quality Testing

**File**: `.github/skills/data-quality-testing/SKILL.md`

**What it teaches**:
- When to validate data (before every transform)
- How to write assertions and fixtures
- Anti-patterns to avoid (silent failures)
- Platform-specific validation (Pandas vs PySpark)

**Key sections**:
- Inline assertions checklist
- pytest fixture patterns
- Data quality test suite example
- Common issues & fixes

**When to reference**:
- "My data quality tests are failing"
- "How do I validate nulls in a DataFrame?"
- "What should I check for every pipeline?"

**Skills link**: Ask @DataQuality agent or `/validate-pipeline` command

---

## 2. Spark & Pandas Best Practices

**File**: `.github/skills/spark-pandas-best-practices/SKILL.md`

**What it teaches**:
- When to choose PySpark vs Pandas (size, platform)
- Spark optimization (partitioning, broadcast joins, caching)
- Pandas optimization (vectorization, dtype, memory)
- Migration path from Pandas to Spark
- Platform-specific (Databricks, Fabric)

**Key sections**:
- Decision tree (dataset size → choose framework)
- PySpark patterns (partition, broadcast, cache, column pruning, avoid collect)
- Pandas patterns (vectorization, dtype, memory efficiency, groupby)
- Platform configs (Databricks cluster, Fabric Lakehouse)
- Anti-patterns (row-by-row loops, unnecessary collect)

**When to reference**:
- "Should I use Spark or Pandas?"
- "Why is my Spark query so slow?"
- "How do I vectorize this Pandas operation?"
- "What cluster settings should I use?"

**Skills link**: Ask @CodeReviewer or check performance in `/review-code`

---

## 3. Notebook as Code

**File**: `.github/skills/notebook-as-code/SKILL.md`

**What it teaches**:
- Notebook cell ordering standard (imports → config → functions → execution)
- When to extract logic to `.py` modules
- Making notebook logic testable
- Migration path (exploratory → organized → modular → scheduled)
- Platform-specific (Databricks dbutils, Fabric notebookutils)

**Key sections**:
- Cell organization template
- Extraction patterns (when to extract, before/after examples)
- Testability checklist (make dependencies injectable)
- Platform-specific magic (%autoreload, dbutils)
- Anti-patterns (unclear dependencies, 500+ line notebooks)

**When to reference**:
- "This notebook is 300 lines — where do I start?"
- "How do I make this logic testable?"
- "Should I extract this to a module?"

**Skills link**: Ask @NotebookOrganizer agent or `/organize-notebook` command

---

## 4. Auto-Doc Sync

**File**: `.github/skills/auto-doc-sync/SKILL.md`

**What it teaches**:
- Documenting with type hints & docstrings
- Detecting doc-code drift (signatures, parameters, return types)
- Validation workflow (after code change → update docs → test examples)
- Automation opportunities (Sphinx, pytest --doctest)
- Anti-patterns (outdated READMEs, broken examples)

**Key sections**:
- Docstring-first workflow
- Drift detection checklist
- Update workflow with examples
- Automation (Sphinx, doctest)
- Anti-patterns

**When to reference**:
- "I updated this function — docs are out of date?"
- "Are these examples still accurate?"
- "How do I automate doc updates?"

**Skills link**: Ask @DocsSync agent or `/sync-docs` command

---

## 5. Markdown & Notebook Docs

**File**: `.github/skills/markdown-notebook-docs/SKILL.md`

**What it teaches**:
- README templates (purpose, owner, quick start, overview, data flow, quality checks, troubleshooting)
- Data dictionary templates (schema, meanings, constraints, business rules)
- API documentation templates
- Notebook markdown guidance (when to document sections)
- Best practices (explain WHY not WHAT, use examples, link related)

**Key sections**:
- README template (fill-in-the-blank)
- Data dictionary template
- API docs template
- Notebook markdown guidance
- Best practices & examples

**When to reference**:
- "How do I structure a README?"
- "What goes in a data dictionary?"
- "When should I add markdown sections?"

**Skills link**: Reference when writing docs (no specific agent)

---

## 6. Data Pipeline TDD

**File**: `.github/skills/data-pipeline-tdd/SKILL.md`

**What it teaches**:
- RED-GREEN-REFACTOR workflow for data pipelines
- Step 1: Write failing test (RED)
- Step 2: Write minimal code to pass test (GREEN)
- Step 3: Refactor without breaking tests (REFACTOR)
- Fixture patterns for reusable test data
- Complete pipeline test suite example

**Key sections**:
- RED-GREEN-REFACTOR cycle with examples
- Happy path tests & edge cases & error cases
- Fixtures for reusable test data
- Full pipeline test suite pattern
- Anti-patterns (testing implementation vs behavior)

**When to reference**:
- "How do I write tests BEFORE code?"
- "What test cases do I need?"
- "How do I organize test fixtures?"

**Skills link**: Ask @CodeReviewer or `/test-this` command

---

## 7. Code Review Notebooks

**File**: `.github/skills/code-review-notebooks/SKILL.md`

**What it teaches**:
- Code review checklist (correctness, performance, quality, testing, maintainability)
- Severity levels (CRITICAL / MAJOR / MINOR / FYI)
- Anti-patterns to flag (silent data loss, unreadable names, untestable code)
- Example review conversation
- Self-review checklist

**Key sections**:
- Review checklist (6 categories)
- Severity levels table with actions
- Example review with feedback
- Anti-patterns & how to flag them
- Self-review checklist (before pushing)

**When to reference**:
- "How do I review code effectively?"
- "What should I look for in a code review?"
- "Is this a CRITICAL or MAJOR issue?"

**Skills link**: Ask @CodeReviewer agent or `/review-code` command

---

## 8. Capture Data Engineering Lessons

**File**: `.github/skills/capture-data-eng-lessons/SKILL.md`

**What it teaches**:
- Lesson format (problem, root cause, fix, prevention, tags)
- Tag system for categorization (data-quality, spark, performance, etc.)
- Weekly review workflow
- Pattern detection (3+ occurrences → amendment)
- How to amend skills based on lessons
- Integration with GitHub issues

**Key sections**:
- Lesson format template with examples
- Tags reference (data-quality, spark, notebooks, documentation, testing, etc.)
- Weekly review workflow (15 minutes)
- Pattern detection criteria
- From lessons to skill amendments (workflow)
- GitHub issues integration

**When to reference**:
- "How do I capture a lesson learned?"
- "What should I do when I see a pattern?"
- "How do I improve the template over time?"

**Skills link**: Ask `/lesson` slash command

---

## How Skills Are Structured

Each skill folder contains:

```
.github/skills/[skill-name]/
├── SKILL.md                # Main skill documentation
├── examples/               # Code examples (Python files)
└── references/             # External links, templates
```

---

## Progressive Disclosure

When Copilot references a skill:
1. **Brief mention** with trigger phrases (fast, context-aware)
2. **On demand**: Full SKILL.md loaded when you ask for details
3. **Examples/References**: Available in `examples/` and `references/` folders

This keeps your context window lean while providing deep expertise when needed.

---

## Customization

To customize a skill for your project:

1. **Edit the skill file**: `.github/skills/[skill-name]/SKILL.md`
2. **Add examples**: Store `.py` files in `examples/` specific to your platform (Fabric/Databricks)
3. **Add references**: Link to your internal docs in `references/`
4. **Update agents**: Modify agent instructions (`.github/agents/`) to reference your customizations

---

## Learning Path

**New to project?**
1. Start with **notebook-as-code** (if you're organizing notebooks)
2. Then **spark-pandas-best-practices** (choosing your framework)
3. Then **data-quality-testing** (validating data)

**Setting up a new pipeline?**
1. **data-pipeline-tdd** (write tests first)
2. **spark-pandas-best-practices** (choose framework)
3. **data-quality-testing** (add validation)

**Improving processes?**
1. **code-review-notebooks** (set standards)
2. **capture-data-eng-lessons** (track improvements)
3. Amend other skills based on lessons

---

## See Also

- [Agents Reference](./AGENTS.md) - Who to ask for help
- [Slash Commands Reference](./PROMPTS.md) - Quick access workflows
- [Lessons Log](../tasks/lessons.md) - What the team learned
