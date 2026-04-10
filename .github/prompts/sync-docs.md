---
name: /sync-docs
description: Check and update documentation when code changes, fix doc-code drift
---

# /sync-docs

**What it does**: Detects documentation drift (docs out of sync with code), proposes fixes, validates examples.

**When to use**:
- After code refactoring or function changes
- Before merging code changes
- Documentation feels stale or examples are broken
- You've changed function signatures, parameters, or behavior

**Example usage**:

```
/sync-docs

Checking drift between code and docs...
```

**What you'll get**:
- Drift detection: Function signatures changed? Parameters renamed? Examples outdated?
- Broken examples identified and fixed
- Proposed documentation updates (copy-paste ready diffs)
- Updated docstrings with parameter changes
- Suggested README/example fixes with working code
- Validation: "This example now produces: [output]"

**Typical flow**:
1. You refactor a function
2. Run `/sync-docs`
3. Get back: "Found 3 doc drift issues" + proposed updates
4. Apply the diffs, run tests
5. Done

**See also**: `@CodeReviewer` for code-quality review after doc updates
