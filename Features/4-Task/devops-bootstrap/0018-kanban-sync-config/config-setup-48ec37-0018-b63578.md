---
id: 48ec37
feature: 0018
epic: b63578
status: Task
type: task
review_gate: yes
---

# Task: Create default config with SOT setting

## What
Create `.claude/config.json` with default `kanban.sot: csv` setting. This is the single source of truth indicator that sync scripts will check.

## Scope
- Create `.claude/config.json` if it doesn't exist
- Add `kanban: { sot: "csv" }` structure
- Document the setting in the file as a comment
- Verify sync scripts can read the config

## Acceptance Criteria
- [ ] `.claude/config.json` exists at repo root
- [ ] Contains valid JSON with `kanban.sot` set to `"csv"`
- [ ] Scripts successfully read the config value
- [ ] Default matches documented behavior in Kanban.md

## Test Conditions
- Config file is valid JSON (no parse errors)
- Value can be read by Python using json module
- Changing value to "folders" works without error

## Definition of Done
- [ ] File created with correct structure
- [ ] Code review approved
- [ ] Manual verification that scripts read the setting

## Comments

**2026-04-10 — architect (task creation):** Created task stub as part of HLD decomposition for feature 0018.
