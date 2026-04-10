---
name: /validate-pipeline
description: Run data quality checks on pipeline code or data, identify issues, suggest fixes
---

# Validate Pipeline

**What it does**: Checks pipeline for data quality issues (nulls, duplicates, schema mismatches, etc.) and proposes fixes.

**When to use**:
- Adding quality checks to a pipeline
- Debugging data quality issues
- Before deploying to production

**Example usage**:

```
/validate-pipeline

Checking: src/data/pipelines/load_orders.py
```

**Output you'll get**:
- Missing quality checks identified
- Suggested assertions/validators
- Example test cases
- Severity level (Critical/Major/Minor)
- Link to data-quality-testing skill

**This delegates to**: @DataQuality agent (validation suggestions), @CodeReviewer (code review)
