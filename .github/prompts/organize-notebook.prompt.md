---
name: /organize-notebook
description: Restructure notebook cells, extract functions, improve readability and organization
---

# /organize-notebook

**What it does**: Analyzes notebook structure and restructures cells: reordering, function extraction, cleanup, and organization.

**When to use**:
- Notebook has 300+ lines (getting unwieldy)
- Cell dependencies are unclear
- Repeated code blocks across cells
- Before converting notebook to production pipeline
- Notebook logic should move to `.py` modules

**Example usage**:

```
/organize-notebook

Analyzing: notebooks/exploratory/sales_analysis.ipynb
```

**What you'll get**:
- Current structure analysis: cell count, line counts, cell dependencies
- Reorganization proposal: imports → config → helper functions → main execution
- Functions extracted to `.py` (with move suggestions)
- Import cleanup and consolidation recommendations
- Before/after cell order and dependencies
- Suggested refactoring steps

**Typical flow**:
1. You have a messy 400-line notebook
2. Run `/organize-notebook`
3. Get: "Extract 3 functions to `.py`, reorder 8 cells"
4. Apply restructuring
5. Run tests to verify
6. Clean notebook + modular code

**See also**: `@CodeReviewer` for code quality review after organization
