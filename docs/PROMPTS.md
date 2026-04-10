---
title: Slash Commands Quick Reference
---

# Slash Commands

Type `/` in Copilot Chat and select one of these commands for quick-access workflows.

---

## Quick Command Matrix

| Command | What It Does | When to Use | Agent |
|---------|-------------|-----------|-------|
| `/analyze-data` | Explore dataset, flag anomalies, suggest visualizations | New dataset investigation | @DataQuality |
| `/validate-pipeline` | Check data quality, suggest assertions, run tests | Adding quality checks | @DataQuality |
| `/organize-notebook` | Restructure cells, extract functions, improve readability | Notebook >300 lines | @NotebookOrganizer |
| `/sync-docs` | Check doc-code drift, update docs, validate examples | After code refactoring | @DocsSync |
| `/review-code` | Structured code review, severity-graded feedback | Before pushing code | @CodeReviewer |
| `/test-this` | Generate test cases with fixtures, doctest-ready | Adding test coverage | @CodeReviewer |
| `/setup-project` | Bootstrap new project with folder structure & starter code | New pipeline project | @ProjectScaffolder |
| `/lesson` | Capture lesson learned, check patterns, suggest improvements | After fixing a bug/learning | Logging system |

---

## Command Details

### `/analyze-data`

**Purpose**: Quick dataset exploration

**Use case**: "I just loaded a new dataset — what's in it?"

**Output**:
- Shape & dtypes
- Missing values
- Statistics (min, max, mean, std)
- Top values per column
- Anomaly flags
- Visualization suggestions

**Example**:
```
/analyze-data

File: sales_data_2026_Q1.csv
Shape: (100000, 12)
Memory: ~8 MB

Nulls detected in region (0.5%)
Revenue has outliers (max $500K vs median $5K)
...suggested visualizations...
```

---

### `/validate-pipeline`

**Purpose**: Check & strengthen data quality in a pipeline

**Use case**: "Does my pipeline have enough quality checks?"

**Output**:
- Missing assertions identified
- Suggested validators
- Test fixtures template
- Example tests
- Severity assessment

**Example**:
```
/validate-pipeline

Checking: src/data/pipelines/load_orders.py

Missing checks:
- ✗ CRITICAL: No null validation on key columns
- ✗ MAJOR: No schema validation
- ✓ MINOR: Could add duplicate check

Suggested assertions:
  assert df[["id", "date"]].isnull().sum().sum() == 0
  assert set(df.columns) == EXPECTED_SCHEMA
  ...
```

---

### `/organize-notebook`

**Purpose**: Restructure a messy notebook

**Use case**: "This notebook is 600 lines — help me clean it up"

**Output**:
- Current structure analysis
- Reorganization plan (imports → config → functions → execution)
- Functions to extract with code
- Import cleanup
- Before/after diff

**Example**:
```
/organize-notebook

File: notebooks/sales_analysis.ipynb
Current state: 18 cells, 650 lines
Issues: Unclear dependencies, repeated filters, mixed logic

Suggested reorganization:
✓ Cell 1: Imports (pandas, logging, config)
✓ Cell 2: Configuration (BATCH_SIZE, MIN_DATE)
✓ Cell 3: Extract filter_active & validate functions
✓ Cell 4: Main execution
✓ Cell 5: Analysis/visualization

Extracted to .py:
  - filter_active_orders (20 lines) → src/filters.py
  - validate_schema (15 lines) → src/validators.py

Diff:
  - Remove: 18 cells
  + Create: 6 organized cells
  + Create: src/filters.py, src/validators.py
  + Create: tests/test_filters.py
```

---

### `/sync-docs`

**Purpose**: Update documentation after code changes

**Use case**: "I refactored this function — docs are probably out of date"

**Output**:
- Detected drift issues
- Proposed updates with diffs
- Re-validated examples
- Updated docstrings

**Example**:
```
/sync-docs

Comparing code vs documentation...

Detected drift:
1. Function signature changed (added 'rate' param)
2. Return type updated (dict → DataFrame)
3. Examples use old signature

Proposed updates:

In docstring:
  OLD: def apply_discount(amount: float) -> float:
  NEW: def apply_discount(amount: float, rate: float = 0.1) -> dict:

In README:
  OLD: `result = apply_discount(100)`
  NEW: `result = apply_discount(100, rate=0.15)`

Actions:
  ✓ Update docstring (src/transforms.py:15)
  ✓ Fix README examples (docs/README.md)
  ✓ Re-validate doctest (passing)
```

---

### `/review-code`

**Purpose**: Structured code review with severity grading

**Use case**: "Before I push, any issues I should fix?"

**Output**:
- Categorized feedback (Correctness, Performance, Quality, Testing, Maintainability)
- Severity grades per issue (CRITICAL / MAJOR / MINOR / FYI)
- "Fix before merge" vs "Nice to have"

**Example**:
```
/review-code

File: src/data/pipelines/load_orders.py

✗ CRITICAL (Fix before merge):
  1. Row-by-row loop on 1M row DataFrame (line 42)
     - Current: for i in range(len(df)): df.loc[i, 'discount'] = ...
     - Issue: Will take >5 minutes
     - Fix: Use vectorized df['discount'] = df['amount'] * 0.9

✗ MAJOR (Fix in PR):
  2. Missing null validation (line 15)
     - Add: assert df[["id"]].isnull().sum().sum() == 0
  3. Hardcoded value (line 18)
     - Extract: DISCOUNT_RATE = 0.1

✓ MINOR (Consider fixing):
  4. Could use type hints on function params
  5. Docstring could expand on business logic

✓ FYI (No action):
  6. Good use of logging
  7. Validation pattern follows best practices
```

---

### `/test-this`

**Purpose**: Generate test cases for a function

**Use case**: "I need to add tests for this function — what should I test?"

**Output**:
- Happy path tests (normal input)
- Edge case tests (empty, nulls, boundaries)
- Error tests (invalid input, types)
- Reusable fixtures
- Pytest-ready code

**Example**:
```
/test-this

Function: src/transforms.py::apply_discount

Generated test cases:

# Happy path
def test_apply_discount_basic():
    result = apply_discount(100.0)
    assert result == 90.0

# Edge cases
def test_apply_discount_zero_amount():
    result = apply_discount(0.0)
    assert result == 0.0

def test_apply_discount_custom_rate():
    result = apply_discount(100.0, rate=0.2)
    assert result == 80.0

# Error cases
def test_apply_discount_invalid_type():
    with pytest.raises(TypeError):
        apply_discount("not a number")

# Test suite
class TestApplyDiscount:
    def test_idempotent(self): ...
    def test_preserves_dtype(self): ...

Fixture:
@pytest.fixture
def sample_amounts():
    return [100.0, 200.0, 150.0]
```

---

### `/setup-project`

**Purpose**: Bootstrap a new data engineering project

**Use case**: "I'm starting a new pipeline — where do I start?"

**Output**:
- Interactive discovery questions
- Generated folder structure
- Starter pipeline code
- Test templates
- Customized pyproject.toml

**Example**:
```
/setup-project

Questions:
1. What's your data source? → CSV file
2. Key transformations? → Aggregation by region + deduplication
3. Output? → Lakehouse table
4. Quality requirements? → No nulls in ID, no duplicates
5. Platform preference? → Databricks

Generated:
✓ Folder structure (src/data/pipelines, tests/, docs/)
✓ Starter code: src/data/pipelines/main.py
✓ Validators: src/data/validators.py
✓ Tests: tests/test_pipeline.py
✓ Docs: README.md with data dictionary
✓ Config: pyproject.toml, Makefile, .gitignore

Next steps:
1. Customize README with business context
2. Update DATA-PLATFORM-GUIDE.md for Databricks
3. Run: make test
4. Deploy: databricks jobs run-now --job-id X
```

---

### `/lesson`

**Purpose**: Capture & learn from issues

**Use case**: "Just fixed a recurring issue — want to document it"

**Output**:
- Formatted lesson entry (ready for `tasks/lessons.md`)
- Pattern detection (3+ occurrences → suggests amendments)
- GitHub issue suggestion (if pattern found)
- Link to relevant skill

**Example**:
```
/lesson

Problem: Row-by-row loop too slow on large dataset

---

Generated lesson:

## Lesson: Vectorization Critical for >100K Rows

- **Problem**: Pipeline took 5 minutes; row-by-row loop on 1M row DataFrame
- **Root Cause**: Used df.apply() instead of vectorized operations
- **Fix**: Replaced df.apply() with np.vectorize or direct column math
- **Prevention**: Always vectorize on DataFrames > 10k rows; benchmark loops

Tags: `pandas`, `performance`, `vectorization`
Date: 2026-04-09

---

Pattern detected! This is the 3rd occurrence:
- Lesson #3: Row-by-row loop (this one)
- Lesson #7: .apply() on large data
- Lesson #12: for-loop in aggregation

Recommendation: Amend spark-pandas-best-practices/SKILL.md
with explicit "Vectorization Rules for >10K Rows"

GitHub issue suggested: "Add vectorization warning to code review checklist"
```

---

## Typical Workflows

### "I'm starting a new project"
```
/setup-project
  ↓ (asks 5 discovery questions)
  ↓ generates folder structure, code, docs
Then:
  /organize-notebook (if exploratory work needs tidying)
  /sync-docs (before first merge)
```

### "I found a bug in my pipeline"
```
/validate-pipeline
  ↓ suggests quality checks to catch the bug
/test-this
  ↓ generate regression test
Then:
  /review-code (before pushing fix)
  /lesson (capture prevention rule)
```

### "Notebook is getting messy"
```
/organize-notebook
  ↓ suggests structure, extraction
Then:
  /review-code (new extracted functions)
  /sync-docs (document extracted modules)
```

---

## Tips

1. **Be specific**: `/review-code` + file path or code snippet
2. **Reference context**: "Per data-quality-testing skill, did I miss..."
3. **Iterate**: Ask follow-ups; commands build on each other
4. **Read output fully**: Scroll to see all suggestions
5. **Follow recommendations**: Commands often suggest next steps

---

## See Also

- [Agents Reference](./AGENTS.md) - Who/what to ask
- [Skills Library](./SKILLS.md) - Deep dive on each topic
