---
id: 8166be
feature: 0018
epic: b63578
status: Task
type: task
review_gate: yes
---

# Task: Add SOT validation to folders_to_csv.py

## What
Add authority check to `folders_to_csv.py` so it validates the configured SOT before running. If SOT is CSV, the script must refuse to run with a clear error message.

## Scope
- Read `kanban.sot` from `.claude/config.json`
- If `sot == "csv"`, exit with error code 1 and message: "Kanban SOT is 'csv'. Rebuild from folders is forbidden. Use csv_to_folders.py instead."
- If `sot == "folders"`, proceed with current behavior
- Add logging of current SOT before running

## Acceptance Criteria
- [ ] Script reads SOT config at startup
- [ ] Script exits with code 1 if SOT is CSV
- [ ] Error message is clear and actionable
- [ ] Script logs "Kanban SOT is 'X'" before checking
- [ ] Existing folder-to-CSV logic is unchanged when SOT allows it

## Test Conditions
- With `sot: csv`, script exits with error
- With `sot: folders`, script succeeds as before
- Config missing defaults to "csv" (safe default)
- Log message appears in stderr

## Definition of Done
- [ ] Code review approved
- [ ] Script tested with both SOT values
- [ ] Error message is clear
- [ ] No breaking changes to existing behavior when allowed

## Comments

**2026-04-10 — architect (task creation):** Created task stub as part of HLD decomposition for feature 0018.
