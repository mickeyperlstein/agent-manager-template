---
id: 9868d2
feature: 0018
epic: b63578
status: Task
type: task
review_gate: yes
---

# Task: Add SOT validation to csv_to_folders.py

## What
Add authority check to `csv_to_folders.py` so it validates the configured SOT before running. If SOT is Folders, the script must refuse to run with a clear error message.

## Scope
- Read `kanban.sot` from `.claude/config.json`
- If `sot == "folders"`, exit with error code 1 and message: "Kanban SOT is 'folders'. Sync from CSV is forbidden. Use folders_to_csv.py instead."
- If `sot == "csv"`, proceed with current behavior
- Add logging of current SOT before running

## Acceptance Criteria
- [ ] Script reads SOT config at startup
- [ ] Script exits with code 1 if SOT is Folders
- [ ] Error message is clear and actionable
- [ ] Script logs "Kanban SOT is 'X'" before checking
- [ ] Existing CSV-to-folders logic is unchanged when SOT allows it

## Test Conditions
- With `sot: folders`, script exits with error
- With `sot: csv`, script succeeds as before
- Config missing defaults to "csv" (safe default)
- Log message appears in stderr

## Definition of Done
- [ ] Code review approved
- [ ] Script tested with both SOT values
- [ ] Error message is clear and actionable
- [ ] No breaking changes to existing behavior when allowed

## Comments

**2026-04-10 — architect (task creation):** Created task stub as part of HLD decomposition for feature 0018.
