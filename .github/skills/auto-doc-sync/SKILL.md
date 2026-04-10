---
name: auto-doc-sync
description: >-
  Detect documentation drift after code changes, compare Python signatures to
  docs, and update README or docstring examples. Use when refactors may have
  made docs stale and you want a repeatable scan-first workflow.
allowed-tools:
  - read
  - write
  - shell(python:*)
---

# Auto-Doc Sync

Use this skill when code changed and you need to verify that docstrings, README examples, and API usage notes still match the implementation.

## Assets In This Skill

- `doc-scan.py`: scans Python files and Markdown docs for obvious drift
- `examples/README-doc-section.md`: sample section style for code-backed docs

## Workflow

1. Run `python .github/skills/auto-doc-sync/doc-scan.py <path-to-code>`.
2. Review drift findings:
   - missing docstrings
   - missing type hints
   - Markdown references to stale function signatures
3. Update the docstring first.
4. Update README or docs examples second.
5. Re-run the scan to confirm the drift is gone.

## Typical Usage

```text
The transform signature changed. Use auto-doc-sync to scan src/ and docs/ for stale references, then propose exact doc updates.
```

## Principles

- Code is the source of truth.
- Docstrings and type hints should be updated before downstream docs.
- Examples should be runnable, not decorative.
- Drift should be detected mechanically when possible.

## Notes

- The helper script is intentionally lightweight. It catches the common cases first.
- If the codebase uses generated docs, update the source comments and examples rather than editing generated output.
