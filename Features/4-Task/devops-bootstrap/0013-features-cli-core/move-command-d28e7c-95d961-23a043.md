---
id: "d28e7c"
epic: "23a043"
feature: "95d961"
title: features move command
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Implement the `features move <filepath> <target-column>` command for moving task files between Kanban columns.

## Scope
- Create `template_workflow/features/commands/move.py`
- Implement move command with args: filepath, target-column
- Read source file frontmatter to extract epic/feature
- Build destination path: `Features/{column}/{epic}/{feature}/{filename}`
- Execute `git mv` + `mkdir -p` as needed
- Update file frontmatter: `column: {target}` field

## Acceptance Criteria
- [ ] `features move <file> <column>` moves file to correct column folder
- [ ] Command uses `git mv` (not just `mv`)
- [ ] Destination directories created as needed
- [ ] Frontmatter `column` field updated to target column
- [ ] Rejects paths outside Features/ with clear error
- [ ] Validates target column is valid (1-9 format)

## Test Conditions
- Create test file in 4-Task, move to 6-Implementation
- Verify file exists at destination
- Verify frontmatter column field updated
- Verify git history shows rename
- Test invalid path outside Features/ → error

## Definition of Done
- Move command fully implemented
- All AC met
- Tests pass
