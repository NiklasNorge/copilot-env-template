---
name: /organize-notebook
description: Restructure a notebook's cells, extract functions, improve readability
---

# Organize Notebook

**What it does**: Analyzes notebook structure and suggests/implements reorganization: cell reordering, function extraction, cleanup.

**When to use**:
- Notebook has 300+ lines (getting unwieldy)
- Cell dependencies unclear
- Repeated code blocks
- Before converting notebook to production pipeline

**Example usage**:

```
/organize-notebook

Analyzing: notebooks/exploratory/sales_analysis.ipynb
```

**Output you'll get**:
- Current structure analysis (cell count, line counts, dependencies)
- Suggested reorganization (imports → config → functions → execution)
- Functions to extract to `.py` (with code)
- Import cleanup recommendations
- Before/after diff

**This delegates to**: @NotebookOrganizer agent (restructure), @CodeReviewer (quality review)
