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
- [x] `tasks.csv` schema defined: `id, epic, story, state, assignee, column, type, review_gate`
  - `state` (not status): reflects story state (backlog, in-progress, done, etc.)
  - `type`: defaults to `stories` (plural), can be other types (bugs, tasks, etc.)
  - Path auto-built from `{epic}/{type}/` — e.g., `devops-bootstrap/stories/`
- [x] `scripts/folders_to_csv.py` scans `Features/` → rebuilds `tasks.csv` from disk + frontmatter
  - Derives `epic`, `type` from folder path structure
- [x] `scripts/csv_to_folders.py` reads `tasks.csv` → moves files to correct column folders
  - Builds target path from `{epic}/{type}/` columns
- [ ] Script is idempotent (run twice = no change)
- [ ] **Pre-commit hook** registered in `.git/hooks/pre-commit` — runs sync automatically on every commit
- [ ] Commit always contains both the CSV change and the resulting folder moves (atomic)
- [ ] Sync targets defined in `template_workflow/kanban-sync.config.json` — script reads config, syncs to whatever targets are enabled
- [ ] Supported targets: `folders` (always on), `sheets`, `gh-projects`
- [ ] Documented in CONTRIBUTING.md

## Trigger
Pre-commit hook (Option B) — edit CSV → `git commit` → hook runs sync → folders move → both staged in same commit.

## Dependencies
None — this is the foundation everything else builds on.
