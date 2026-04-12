---
id: baec
epic: 6099
feature: a4c1
title: Integration Testing for Push-to-Template Workflow
type: task
assignee: agent
review_gate: yes
approved: no
depends_on: bb31, 369f
---

## What
Write end-to-end tests for the complete push-to-template workflow: bash wrapper calls push_template.py in cache, artifacts are removed, clean template is pushed to main, and downstream clone gets the clean version.

## Scope
- Test happy path: dev → main with clean template
- Test error path: merge fails (main diverged)
- Test error path: push fails (network/permission)
- Verify downstream clone has no Features/, meetings/, tasks.csv
- Test with bash wrapper and push_template.py integration
- Test can run locally and in CI environment

## Out of Scope
- Unit tests for individual functions
- Performance testing
- Load testing

## Acceptance Criteria
- [ ] Happy path test passes: commits flow dev → cache → main cleanly
- [ ] Error path test: merge failure is caught and reported
- [ ] Error path test: push failure is caught and reported
- [ ] Downstream clone test: fresh clone from main has no dev artifacts
- [ ] Test runs in local environment (bash + Python)
- [ ] Test can be automated in CI/CD (GitHub Actions or similar)
- [ ] Test report shows what was tested and results
- [ ] All Gherkin scenarios from HLD pass

## Test Conditions
**Happy path:** Full workflow dev → main → downstream
- Given: dev branch with features and artifacts, fresh main
- When: bash wrapper runs push_to_template.py
- Then: main has clean template, downstream clone is artifact-free, version bumped

**Error scenario:** Main branch diverged
- Given: main was manually edited
- When: bash wrapper runs
- Then: merge fails, script exits with error, main unchanged

**Error scenario:** Push fails
- Given: origin/main is unreachable
- When: bash wrapper runs
- Then: script detects failure, exits with error code

## Definition of Done
- [ ] Test script written (bash or Python)
- [ ] All 3 scenarios tested (happy + 2 error paths)
- [ ] Test uses real git operations (not mocks)
- [ ] Test verifies Gherkin scenarios pass
- [ ] Test can run locally and in CI
- [ ] Test output is clear and actionable
- [ ] Edge cases documented (what test doesn't cover)
