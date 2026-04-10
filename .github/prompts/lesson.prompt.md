---
name: /lesson
description: Log a lesson learned from a problem, fix, or discovery
---

# Lesson

**What it does**: Structured lesson capture. You describe a problem/discovery and it formats it into the lessons log, checks for patterns, and suggests skill updates if needed.

**When to use**:
- Fixed a recurring issue
- Encountered unexpected behavior
- Learned a new pattern
- Weekly self-improvement

**Example usage**:

```
/lesson

Problem: Row-by-row loop too slow on large dataset
```

**Output you'll get**:
- Formatted lesson entry ready for `tasks/lessons.md`
- Pattern detection (3+ similar issues? → Suggests skill amendment)
- Suggested GitHub issue if pattern detected
- Link to relevant skill for deep dive
- Self-improvement stats (lessons this week, patterns this month)

**Output format**:
```markdown
## Lesson: [Title]
- **Problem**: ...
- **Root Cause**: ...
- **Fix**: ...
- **Prevention**: ...
- **Tags**: `tag1`, `tag2`
- **Date**: YYYY-MM-DD
```

**This delegates to**: Internal logging system (no agent, just formatting)
