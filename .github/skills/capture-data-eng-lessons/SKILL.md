---
name: capture-data-eng-lessons
description: >-
  Meta-skill for capturing lessons learned from recurring issues, successful patterns,
  and improvements. Drives self-improvement through structured observation and pattern detection.
---

# Capture Data Engineering Lessons

## When to Use

- **After fixing a bug**: Log what went wrong and how you fixed it
- **After learning something**: Unexpected behavior? Gotcha? Log it
- **Weekly review**: Scan for patterns (3+ same issue = recurring problem)
- **Continuous improvement**: Lessons → amendments to skills/processes

---

## Lesson Format

Use this structure for each entry in `tasks/lessons.md`:

```markdown
## Lesson: [Brief Title]

- **Problem**: [What went wrong? What was confusing? What took time?]
- **Root Cause**: [Why did it happen? What assumption failed?]
- **Fix/Solution**: [What worked? How did you resolve it?]
- **Prevention**: [How to avoid this next time? What rule should we have?]
- **Tags**: `tag1`, `tag2`, `tag3` (see tags below)
- **Date**: YYYY-MM-DD
- **Reference**: [Optional link: code file, Copilot chat, docs]

---
```

---

## Example Lessons

### Example 1: Data Quality Issue

```markdown
## Lesson: Nulls Crashed Data Quality Checks

- **Problem**: Pipeline failed silently when a data source returned null values in the ID column
- **Root Cause**: Quality assertions assumed non-empty DataFrames; didn't check for nulls first
- **Fix/Solution**: Added explicit null check early in pipeline:
  ```python
  assert df[["id", "date"]].isnull().sum().sum() == 0, "Nulls in key columns"
  ```
- **Prevention**: Always validate constraints BEFORE transform; don't assume clean data
- **Tags**: `data-quality`, `spark`, `assumptions`, `error-handling`
- **Date**: 2026-04-09
- **Reference**: `src/data/pipelines/load_daily.py` line 25

---
```

### Example 2: Performance Issue

```markdown
## Lesson: Row-by-Row Loop Too Slow for 1M Row Dataset

- **Problem**: Took 5 minutes to process daily data; was using `.apply()` on 1M rows
- **Root Cause**: Didn't know pandas `.apply()` is row-by-row (not vectorized)
- **Fix/Solution**: Replaced:
  ```python
  # SLOW
  df['discount'] = df.apply(lambda row: row['amount'] * 0.9, axis=1)
  
  # FAST
  df['discount'] = df['amount'] * 0.9
  ```
- **Prevention**: For Pandas on 10k+ rows: use vectorized operations, avoid `.apply()`
- **Tags**: `pandas`, `performance`, `vectorization`
- **Date**: 2026-04-08
- **Reference**: Copilot suggested the fix; learned about vectorization

---
```

### Example 3: Documentation Issue

```markdown
## Lesson: Outdated README Confused Teammate

- **Problem**: README had old pipeline steps; teammate followed old instructions
- **Root Cause**: Refactored pipeline 2 months ago but didn't update README
- **Fix/Solution**: Updated README with current steps, added timestamp "Last Updated: 2026-04-07"
- **Prevention**: After code changes, update docs immediately; add "Last Updated" to all guides
- **Tags**: `documentation`, `maintenance`, `communication`  
- **Date**: 2026-04-07
- **Reference**: `README.md` and `.github/copilot-instructions.md`

---
```

---

## Tags Reference

Use tags to categorize lessons for pattern detection:

| Tag | When | Examples |
|-----|------|----------|
| `data-quality` | Data validation, null handling, constraints | "Nulls crashed assertions", "Duplicates found" |
| `spark` | PySpark-specific issue | "Memory error on collect", "Shuffle too slow" |
| `pandas` | Pandas-specific issue | "Row-by-row loop slow", "dtype mismatch" |
| `notebooks` | Notebook organization, structure | "Cell dependencies unclear", "Extracted function" |
| `documentation` | Doc drift, unclear guides | "README outdated", "Docstring missing" |
| `testing` | Test coverage, edge cases | "Test didn't catch null", "Added fixture" |
| `performance` | Speed, memory efficiency | "Loop too slow", "Memory inefficient" |
| `error-handling` | Exception handling, debugging | "Silent failure", "Unhelpful error message" |
| `assumptions` | Unspoken assumptions that failed | "Assumed schema stable", "Assumed no duplicates" |
| `fabric` | Microsoft Fabric-specific | "Lakehouse path error", "SDK behavior" |
| `databricks` | Databricks-specific | "Cluster config issue", "Unity Catalog" |
| `communication` | Team/process miscommunication | "Unclear requirements", "No handoff notes" |
| `config` | Configuration management | "Hardcoded value", "Missing env var" |
| `process` | Process improvements | "No code review", "Manual steps needed" |

---

## Workflow: Capture & Review

### Weekly Review

**Thursday end-of-day ritual** (15 minutes):

1. Open `tasks/lessons.md`
2. Scan last week's entries
3. Look for patterns: same issue 2+ times? → Potential rule amendment

```markdown
## Pattern Detected (Draft)

**Issue**: Row-by-row loops slow on large data  
**Occurrences**: 3 times in past month  
- Lesson 1: .apply() on 1M rows took 5 min
- Lesson 2: .loc[] loop on aggregation
- Lesson 3: for-loop in validation

**Recommendation**: Add rule to skills/spark-pandas-best-practices/SKILL.md  
"Always vectorize operations on DataFrames > 10k rows. Avoid .apply(), .loc[], for-loops."

**Action**: File GitHub issue "Enhancement: Vectorization rules for >10k row operations"
```

### Monthly Review (1-2 hours)

1. Read all lessons from past month
2. Identify top 3 problem areas
3. Update relevant skills with new patterns
4. Update `.github/copilot-instructions.md` if new rule applies broadly

### Pattern Detection Criteria

| Pattern Type | Threshold | Action |
|--------------|-----------|--------|
| Same root cause | 3+ occurrences | Amend skill or create GitHub issue |
| New anti-pattern discovered | Any (if important) | Add to code review checklist |
| Process bottleneck | 2+ mentions | Propose workflow change |
| Tool limitation | 2+ mentions | Consider tool switch or workaround |

---

## From Lessons to Skill Amendments

### Scenario: Data Quality Pattern Emerges

**Lessons logged**:
- Lesson 1: "Nulls in ID column broke pipeline"
- Lesson 2: "Forgot to check for empty DataFrame"
- Lesson 3: "Duplicate IDs slipped through"

**Detected pattern**: Quality checks incomplete

**Skill amendment**:

In `skills/data-quality-testing/SKILL.md`, add new section:

```markdown
## Critical Checks Checklist

Always validate these BEFORE any transform:

1. [ ] DataFrame not empty: `assert df.shape[0] > 0`
2. [ ] Key columns not null: `assert df[["id"]].isnull().sum().sum() == 0`
3. [ ] No duplicate keys: `assert df["id"].duplicated().sum() == 0`
4. [ ] Expected columns present: `assert all(col in df.columns for col in EXPECTED)`
5. [ ] Correct data types: [dtype enforcement]
```

**Update `.github/copilot-instructions.md`**:

```markdown
### Data Quality Standard

All pipelines include these inline checks:

\`\`\`python
# After load
assert df.shape[0] > 0, "Empty data"
assert set(df.columns) == EXPECTED_SCHEMA, "Schema mismatch"
assert df[KEYS].isnull().sum().sum() == 0, "Nulls in key columns"
\`\`\`
```

---

## Preventing Recurrence

After logging a lesson and identifying a pattern:

### Document the Rule

```markdown
**Rule**: Always check for nulls in key columns before transform

**Why**: Nulls silently break downstream logic; fail fast instead

**Where to enforce**: 
- In skill: data-quality-testing/SKILL.md
- In instructions: .github/copilot-instructions.md § Data Quality
- In code review: Check off box "Key columns validated"

**How Copilot helps**: 
- Agents suggest this during code review
- Agents prompt: "Have you validated nulls?"
```

### Train Copilot

When agents ask "Have you validated data quality?":

**You say**: "Yes, I checked nulls and duplicates per [skill-name]"

**Copilot learns**: This is a consistent rule; mention it proactively next time

---

## Anti-Patterns in Lesson Capture

### ❌ Too Vague

```markdown
# BAD
- **Problem**: Things were slow
- **Fix**: Made it faster
- **Tags**: `performance`

# GOOD
- **Problem**: Pipeline took 5 minutes; .apply() loop on DataFrame[1M rows]
- **Fix**: Replaced df.apply(lambda...) with vectorized df[col] * factor
- **Tags**: `pandas`, `performance`, `vectorization`
```

### ❌ Missing Prevention

```markdown
# BAD
- **Problem**: Forgot to deploy docs
- **Fix**: Deployed docs

# GOOD
- **Problem**: README outdated after code refactor; teammate confused
- **Root Cause**: No process to sync docs after code changes
- **Prevention**: After every code change, scan for docs that reference changed logic
```

---

## Integration with GitHub Issues

When pattern emerges → Create GitHub issue:

```markdown
**Title**: "Recurrent: Data quality checks incomplete"

**Description**:
Lessons #3, #5, #12 all involve incomplete validation:
- Nulls not checked
- Empty data not caught  
- Duplicates missed

**Proposal**: Amend `data-quality-testing` skill with mandatory checklist

**Action**: Update skill + update .github/copilot-instructions.md
```

---

## References

- [Retrospectives Guide](https://www.retrium.com/resources/guides)
- [Data Quality Frameworks](https://greatexpectations.io/)
- [Continuous Improvement (Kaizen)](https://en.wikipedia.org/wiki/Kaizen)
