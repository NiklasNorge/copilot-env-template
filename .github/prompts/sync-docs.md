---
name: /sync-docs
description: Check and update documentation for code changes, fix doc-code drift
---

# Sync Docs

**What it does**: Detects documentation drift (docs out of sync with code), proposes updates, validates examples.

**When to use**:
- After code refactoring
- Before merging
- Documentation feels stale
- Examples might be broken

**Example usage**:

```
/sync-docs

Checking drift between code and docs
```

**Output you'll get**:
- Detected drift issues (function signature changed, parameters renamed, etc.)
- Broken examples identified
- Proposed doc updates (with diffs)
- Updated docstrings
- Suggested README changes
- Re-validated example code

**This delegates to**: @DocsSync agent (drift detection), @CodeReviewer (code quality)
