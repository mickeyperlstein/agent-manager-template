---
id: "95f4b4"
epic: "23a043"
feature: "95d961"
title: features clean command
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Implement the `features clean` command for bulk deletion of files marked for deletion.

## Scope
- Create `template_workflow/features/commands/clean.py`
- Walk `Features/` directory tree for all `.md` files
- Parse frontmatter, collect files where `state: marked-for-deletion`
- Execute `git rm` for tracked files, `rm` for untracked
- Print summary of deleted files

## Acceptance Criteria
- [ ] `features clean` deletes all files with `state: marked-for-deletion`
- [ ] Uses `git rm` for tracked files
- [ ] Uses `rm` for untracked files
- [ ] Prints count of deleted files
- [ ] Prints list of deleted file paths

## Test Conditions
- Create test files with `state: marked-for-deletion` in frontmatter
- Run `features clean`
- Verify files deleted
- Verify git status shows deletions
- Verify output shows correct count

## Definition of Done
- Clean command fully implemented
- All AC met
- Tests pass
