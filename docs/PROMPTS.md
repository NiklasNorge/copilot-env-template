---
title: Prompt Files Reference
---

# Prompt Files

Workspace prompt files are in `.github/prompts/` and use `*.prompt.md`.

## Active Prompt Files

- `setup-project.prompt.md`
- `analyze-data.prompt.md`
- `validate-pipeline.prompt.md`
- `organize-notebook.prompt.md`
- `sync-docs.prompt.md`
- `review-code.prompt.md`
- `test-this.prompt.md`
- `lesson.prompt.md`

## Command Mapping

| Slash Command | Prompt File |
|---|---|
| `/setup-project` | `setup-project.prompt.md` |
| `/analyze-data` | `analyze-data.prompt.md` |
| `/validate-pipeline` | `validate-pipeline.prompt.md` |
| `/organize-notebook` | `organize-notebook.prompt.md` |
| `/sync-docs` | `sync-docs.prompt.md` |
| `/review-code` | `review-code.prompt.md` |
| `/test-this` | `test-this.prompt.md` |
| `/lesson` | `lesson.prompt.md` |

## Notes

- Prompt files are task templates and should stay concise.
- Keep platform-specific logic in skills or instruction files, not duplicated in every prompt.
