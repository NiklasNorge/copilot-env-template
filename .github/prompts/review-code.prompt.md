---
name: /review-code
description: Structured code review for Python and notebooks with severity-graded feedback
---

# Review Code

**What it does**: Performs detailed code review using a structured checklist: correctness, performance, quality, testing, maintainability. Outputs CRITICAL/MAJOR/MINOR/FYI feedback.

**When to use**:
- Before pushing code
- Getting feedback before PR
- Want to catch issues early

**Example usage**:

```
/review-code

src/data/pipelines/load_orders.py
```

**Output you'll get**:
- Correctness issues (logic errors, edge cases)
- Performance concerns (loops, memory, Spark shuffles)
- Data quality checks (nulls, validation)
- Code standards (PEP 8, type hints, docstrings)
- Testing gaps
- Maintainability suggestions
- Each issue graded: CRITICAL / MAJOR / MINOR / FYI
- "Fix before merge" vs "Nice to have" categorization

**This delegates to**: @CodeReviewer agent (structured review with checklists)
