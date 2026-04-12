---
id: 369f
epic: 6099
feature: a4c1
title: Enhance push_template.py for Cache Workflow
type: task
assignee: agent
review_gate: yes
approved: no
depends_on: bb31
---

## What
Review and enhance existing push_template.py to work seamlessly in the cache folder workflow. Ensure it handles the git status correctly when run from a pre-merged environment, and add any missing CLI flags or error handling.

## Scope
- Verify push_template.py works when run from cache folder (after merge)
- Ensure exclusion list is complete and correct
- Add `--cache-mode` flag or env var if needed
- Improve error messages for clarity
- Test version bumping in cache context
- Ensure `--force` flag behavior is intentional (currently uses `git push --force`)

## Out of Scope
- Rewriting the core filtering logic
- Changing the commit message format
- Modifying version.json location or format

## Acceptance Criteria
- [ ] push_template.py runs successfully in cache folder after merge
- [ ] All 5 exclusions work correctly: Features/, meetings/, tasks.csv, push_template.py, push_template.sh
- [ ] Version bump works and updates version.json correctly
- [ ] Error handling: clear messages for git command failures
- [ ] `--test` flag still works for dry-run
- [ ] Script reports: commit count merged, files removed, version bumped
- [ ] Works with env vars for CI/CD integration

## Test Conditions
**Happy path:** Run in cache with dirty status from merge
- Given: cache folder with merged commits (new files from dev)
- When: `python3 push_template.py` runs
- Then: Features/, meetings/, tasks.csv excluded; other files staged; commit pushed to main

**Error path:** Script failure in cache
- Given: git commands fail (permission, network)
- When: `python3 push_template.py` runs
- Then: Script detects failure and exits with non-zero code

## Definition of Done
- [ ] Script tested in cache folder workflow
- [ ] Exclusion list verified against HLD spec
- [ ] Version bump confirmed in version.json
- [ ] Error messages are clear and actionable
- [ ] `--test` mode still works (no mutations)
- [ ] Documentation updated for cache workflow assumptions
- [ ] Works with bash wrapper integration
