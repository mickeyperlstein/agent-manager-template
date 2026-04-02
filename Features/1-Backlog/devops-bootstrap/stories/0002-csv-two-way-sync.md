---
id: "0002"
title: CSV two-way sync with folder structure
status: backlog
assignee: architect
depends_on: none
review_gate: yes
---

## Story
As the team, we want a single `tasks.csv` at repo root that stays in sync with the `Features/` folder structure — so editing the CSV moves/creates/renames files, and moving files updates the CSV.

## Acceptance Criteria
- [ ] `tasks.csv` schema defined: `id, epic, feature, story, status, assignee, column, type, review_gate`
- [ ] `scripts/kanban-csv-sync.sh` reads CSV → creates/moves story files to correct column folder
- [ ] Same script run in reverse: walks `Features/` folder → rebuilds CSV from file frontmatter
- [ ] Script is idempotent (run twice = no change)
- [ ] **Pre-commit hook** registered in `.git/hooks/pre-commit` — runs sync automatically on every commit
- [ ] Commit always contains both the CSV change and the resulting folder moves (atomic)
- [ ] Sync targets defined in `template_workflow/kanban-sync.config.json` — script reads config, syncs to whatever targets are enabled
- [ ] Supported targets: `folders` (always on), `sheets`, `gh-projects`
- [ ] Example config:
  ```json
  {
    "version": "1.0.0",
    "targets": {
      "folders": true,
      "sheets": { "enabled": true, "spreadsheet_id": "..." },
      "gh-projects": { "enabled": false, "project_number": 1 }
    }
  }
  ```
- [ ] Documented in CONTRIBUTING.md

## Trigger
Pre-commit hook (Option B) — edit CSV → `git commit` → hook runs sync → folders move → both staged in same commit.

## Dependencies
None — this is the foundation everything else builds on.
