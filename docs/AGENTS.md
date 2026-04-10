---
title: Agents Reference
---

# Agents Reference

This template includes 5 specialist agents, each with a clear role, trigger phrases, and delegation patterns.

---

## 1. DataQuality Agent

**Role**: Data validation, quality testing, debugging data issues.

**When to invoke**:
- "My pipeline has nulls in the ID column — how do I validate that?"
- "Write quality checks for this dataset"
- "Why is my data test failing?"

**What it does**:
- Proposes inline assertions
- Generates pytest fixtures for validation
- Flags data quality anti-patterns
- Suggests validators (pytest plugins, great_expectations)

**Skills it uses**:
- `data-quality-testing` - Validation patterns, fixtures, assertions
- `spark-pandas-best-practices` - Platform-specific validation

**Delegates to**:
- @NotebookOrganizer if validation logic should be extracted to `.py`
- @CodeReviewer for quality review before merge
- @DocsSync to document quality rules

**Typical conversation**:
```
You: "My data has nulls but I'm not checking for them"
Agent: "Here's a validation approach:
  1. Assert non-empty DataFrame
  2. Check key columns for nulls
  3. Add test fixtures
  4. Run tests before pipeline"
```

---

## 2. NotebookOrganizer Agent

**Role**: Restructure notebooks, extract functions, improve clarity.

**When to invoke**:
- "This notebook is 500 lines — help me organize it"
- "Extract this repeated logic to a module"
- "Cell dependencies are unclear"

**What it does**:
- Analyzes cell organization (order, dependencies)
- Proposes cell reordering (imports → config → functions → execution)
- Suggests functions to extract to `.py`
- Refactors for clarity and reusability

**Skills it uses**:
- `notebook-as-code` - Extraction patterns, cell ordering
- `data-pipeline-tdd` - Making logic testable

**Delegates to**:
- @DataQuality if extracted code needs validation
- @CodeReviewer for code quality
- @DocsSync to document extracted modules

**Typical conversation**:
```
You: "This cell is 200 lines with lots of repeated logic"
Agent: "I suggest:
  1. Extract filter_active_orders() to src/transforms.py
  2. Extract validate_orders() to src/validators.py
  3. Import and use in notebook
  4. Tests in tests/test_transforms.py"
```

---

## 3. DocsSync Agent

**Role**: Keep documentation and code in sync, detect drift, propose updates.

**When to invoke**:
- "I refactored this function — update the docs?"
- "Documentation feels outdated"
- "Are these examples still accurate?"

**What it does**:
- Detects doc-code drift (signature changes, renamed parameters, broken examples)
- Proposes documentation updates
- Validates example code (doctest)
- Updates README, docstrings, guides

**Skills it uses**:
- `auto-doc-sync` - Drift detection, update workflow
- `markdown-notebook-docs` - Documentation templates

**Delegates to**:
- @CodeReviewer for code quality of examples
- @NotebookOrganizer if notebook docs need restructuring

**Typical conversation**:
```
You: "I changed the function signature — docs out of date?"
Agent: "Detected drift:
  1. Function now takes 3 params instead of 2
  2. Return type changed
  3. Examples reference old param names
  
Proposed updates:
  - Update docstring with new signature
  - Fix examples in README
  - Run doctest to validate"
```

---

## 4. CodeReviewer Agent

**Role**: Structured code review for Python and notebooks using severity grades.

**When to invoke**:
- "Review my code before I push"
- "Is this efficient?"
- "Did I miss anything?"

**What it does**:
- Checks correctness (logic, edge cases, types)
- Flags performance issues (loops, memory, Spark shuffles)
- Validates data quality checks
- Reviews code standards (PEP 8, type hints, docstrings)
- Tests coverage gaps
- Grades severity: CRITICAL / MAJOR / MINOR / FYI

**Skills it uses**:
- `code-review-notebooks` - Review checklist, severity levels
- `spark-pandas-best-practices` - Platform-specific performance
- `data-quality-testing` - Quality validation

**Delegates to**:
- @NotebookOrganizer if code structure needs improvement
- @DocsSync if docs/examples need updating

**Typical conversation**:
```
You: "Review this transform function"
Agent: "Found issues:
  ✗ CRITICAL: Row-by-row loop will be slow (100K rows)
  ✗ MAJOR: Missing docstring
  ✓ MINOR: Could extract discount constant
  
Fix CRITICAL before merge."
```

---

## 5. ProjectScaffolder Agent

**Role**: Meta-agent for bootstrapping new data engineering projects.

**When to invoke**:
- Starting a new data pipeline project
- Using this template for the first time
- "How do I set up a new project?"

**What it does**:
1. Asks discovery questions:
   - Data source? (CSV, DB, API, streaming)
   - Transformations? (aggregation, dedup, enrichment)
   - Output destination? (Lakehouse, file, API)
   - Quality rules? (constraints, checks)
   - Platform preference? (Pandas, Spark, Fabric, Databricks)

2. Generates:
   - Complete folder structure
   - Starter pipeline code (load_transform_store.py)
   - Test fixtures and templates
   - Quality validators
   - README with setup instructions
   - Customized pyproject.toml, Makefile

**Skills it uses**: All skills (synthesis mode)

**Delegates to**:
- @DataQuality to finalize quality checks
- @CodeReviewer to review generated code
- @NotebookOrganizer if organizing exploratory work

**Typical conversation**:
```
Agent: "I'll help you set up a new project.
Questions:
1. What's your data source?
2. What transformations needed?
3. Output destination?
...

Generated:
✓ Folder structure in project/
✓ Starter pipeline: src/data/pipelines/main.py
✓ Test fixtures: tests/conftest.py
✓ Docs: README.md
Next: Customize DATA-PLATFORM-GUIDE.md for your platform"
```

---

## Agent Coordination & Delegation

### Typical Multi-Agent Flow

**Scenario**: New feature in existing pipeline

1. **You** write code
2. **@CodeReviewer** reviews for quality → finds issues
3. **@CodeReviewer** delegates to @NotebookOrganizer (if structure issue)
4. **NotebookOrganizer** refactors → extracts to `.py`
5. **@DataQuality** reviews new code for validation
6. **@DocsSync** updates README and docstrings
7. Done! Ready to merge.

### When to Call Each Agent

| Question | Agent |
|----------|-------|
| "Is my data valid?" | @DataQuality |
| "Organize this notebook" | @NotebookOrganizer |
| "Docs out of date?" | @DocsSync |
| "Review my code" | @CodeReviewer |
| "Set up new project" | @ProjectScaffolder |

---

## Tips for Working with Agents

1. **Be specific**: "Review my load_orders.py" (better than "review code")
2. **Context**: Share file path or code snippet for faster analysis
3. **Iterate**: Ask follow-up questions; agents learn your preferences
4. **Use skills**: Reference skills in your questions: "Per data-quality-testing skill, did I miss any assertions?"
5. **Accept delegation**: If agent suggests another agent, follow their recommendation

---

## See Also

- [Slash Commands Reference](./PROMPTS.md) - Quick access to agent workflows
- [Skills Library](./SKILLS.md) - Deep dive on each skill
- [Lessons Log](../tasks/lessons.md) - Continuous improvement tracking
