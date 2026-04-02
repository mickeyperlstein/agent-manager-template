---
id: 3cda27
title: Implement mandatory pre-commit hook
type: task
assignee: architect
review_gate: yes
approved: no
depends_on: 385474, 0640af
---

## What
Implement the mandatory pre-commit hook at `.git/hooks/pre-commit` that runs folders_to_csv.py then csv_to_folders.py on every commit, staging both tasks.csv and any moved files atomically.

## Scope
- In: .git/hooks/pre-commit script, setup.sh integration
- Out: the sync scripts themselves

## Acceptance Criteria
- [ ] Hook runs folders_to_csv.py then csv_to_folders.py on every commit
- [ ] tasks.csv and Features/ are staged after sync
- [ ] Hook is installed by setup.sh
- [ ] Hook failure blocks the commit with a clear error message

## Test Conditions
- Move a file manually → git commit → CSV reflects new column in same commit → log: sync ran
- CSV edit → git commit → file moved + CSV updated atomically → log: sync ran
- Sync error → commit blocked → log: error with reason

## Definition of Done
- [ ] Hook installed and executable
- [ ] setup.sh installs hook on first run
- [ ] Atomic commit verified via E2E test
