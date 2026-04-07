---
id: "db4eaa"
epic: "23a043"
feature: "95d961"
title: Git utilities module
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Create `utils/git.py` with git operation wrappers for the features CLI git commands.

## Scope
- `git_stage_features()` — stage all files under Features/, return list
- `git_get_staged_files()` — return currently staged files
- `git_commit(message, files)` — commit with message
- `git_push()` — push current branch
- `git_get_last_commit_files()` — return files from last commit
- `git_revert_last_commit()` — revert last commit
- `git_unstage_files(files)` — unstage specific files

## Acceptance Criteria
- [ ] All functions implemented in `utils/git.py`
- [ ] Functions handle git errors gracefully
- [ ] All functions have docstrings
- [ ] Returns proper data types (List[Path], bool)

## Test Conditions
- Test each function with real git operations
- Verify error handling works
- Verify return types are correct

## Definition of Done
- `utils/git.py` complete
- All AC met
- Tests pass
