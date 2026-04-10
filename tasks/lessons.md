# Lessons Log — Data Engineering Copilot

This file captures lessons learned from recurring issues, successful patterns, and improvements to future work.

**Format**: Each lesson includes problem, root cause, fix, and tags for pattern detection.

**How to Add a Lesson**: Use `/lesson` in Copilot Chat, or manually add entries following this format.

**Pattern Detection**: When the same issue appears 3+ times, consider filing a GitHub Issue to amend a skill or create a new one.

---

## Template Entry

Copy this format when logging new lessons:

```markdown
## Lesson: [Brief Title — What You Learned]

- **Problem**: [Concise description of what went wrong, was tricky, or surprised you]
- **Root Cause**: [Why did it happen? What was the assumption that failed?]
- **Fix/Solution**: [What you did to resolve it]
- **Prevention**: [How to avoid this next time]
- **Tags**: `tag1`, `tag2` (examples: `pyspark`, `pandas`, `data-quality`, `notebooks`, `testing`, `documentation`, `performance`, `fabric`, `databricks`)
- **Date**: YYYY-MM-DD
- **Reference**: [Optional: link to code, Copilot chat, or docs]

---
```

---

## Example Lessons (These are Not Real — Just Samples)

### Lesson: Empty DataFrames Break Quality Checks

- **Problem**: Pipeline crashed when a data source returned 0 rows
- **Root Cause**: Quality assertions assumed non-empty DataFrames; didn't check row count first
- **Fix/Solution**: Added `assert df.shape[0] > 0` at the beginning of the pipeline; log warning and exit gracefully
- **Prevention**: Always validate row count on load; check for data source downtime
- **Tags**: `data-quality`, `spark`, `error-handling`
- **Date**: 2026-04-10
- **Reference**: `src/data/pipelines/load_daily.py` (line 25)

---

### Lesson: Notebook Cells Too Long & Slow to Debug

- **Problem**: 200-line notebook cell was hard to debug; took 30 min to isolate bug
- **Root Cause**: Mixed data loading, transformation, and validation in one cell
- **Fix/Solution**: Extracted into separate cells + extracted function to `src/data/transforms.py`
- **Prevention**: Max ~50 lines per cell; extract logic >100 lines to `.py` modules
- **Tags**: `notebooks`, `refactoring`, `organization`
- **Date**: 2026-04-09
- **Reference**: Execute `/organize-notebook` when in doubt

---

### Lesson: Docs Out of Sync with Code

- **Problem**: README listed pipeline parameters that changed 2 months ago; confused teammates
- **Root Cause**: No process to sync docs when code changed
- **Fix/Solution**: Added docstring to function, updated README with current parameters
- **Prevention**: Use `@DocsSync` after significant code changes; add to PR checklist
- **Tags**: `documentation`, `process`
- **Date**: 2026-04-08
- **Reference**: Use `/sync-docs` quarterly

---

## Your Lessons (Add Below)

*Your entries will go here. Use `/lesson` in Copilot Chat or copy the template above.*

---

## Pattern Detection — Recurring Issues

Scan this log periodically (weekly/monthly) for patterns:

**Pattern A: Appears 3+ times?**  
→ File GitHub Issue to create/amend a Skill  
→ Update `.github/instructions/*.md`  
→ Suggest new rule or example

**Pattern B: Specific to a tool/platform?**  
→ Update relevant Skill (e.g., `polars-spark-pandas-patterns/SKILL.md`)  
→ Add example to `examples/` folder

**Pattern C: Self-improvement cycle?**  
→ Open Discussion: "Should we change how we handle [pattern]?"  
→ Update `tasks/lessons.md` with resolution

---

## Quick Stats

- **Total Lessons**: 0 (track as you add entries)
- **Most Common Tag**: (Will update as you add entries)
- **Last Updated**: 2026-04-10

---

## How to Use This Log

1. **Add Lessons**: After fixing a bug, learning something, or having a breakthrough → `/lesson` in Copilot Chat
2. **Review Weekly**: Scan for patterns every Friday or sprint end
3. **Act on Patterns**: 3+ occurrences of same issue → Amend a skill or create an issue
4. **Share Wins**: Successful patterns → Consider adding as a new skill or documentation
5. **Evolve**: This log drives continuous improvement of the template

---

## Integration with Self-Improvement

This log feeds the **self-improving** aspect of the template:

```
Issue Found → Lesson Logged → Pattern Detected (3+ entries) → Amend Skill → Better Future Outcomes
```

Over time, you build a personal knowledge base tailored to your team's patterns, pain points, and wins!
