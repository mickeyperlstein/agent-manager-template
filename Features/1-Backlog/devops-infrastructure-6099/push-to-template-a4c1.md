---
id: a4c1
epic: 6099
feature: a4c1
title: Push-to-Template Automation Script
type: feature
assignee: architect
review_gate: yes
approved: no
priority: high
depends_on:
---

## Feature

**What:** Automated script that maintains a clean checkout of main branch, merges dev commits, removes dev-only artifacts, and pushes clean template to origin/main. Replaces manual git filtering and .gitignore complexity.

**Why:** Current push strategy pollutes main with template project artifacts (Features/, meetings/, tasks.csv). Downstream users get confused/unusable template. Script cleanly separates dev (full project) from main (clean distribution).

**Scope:**
- Python script: `push_to_template.py`
- Maintains local cache folder with clean main checkout
- Git merge dev into cache (fast-forward only)
- Remove dev artifacts: Features/, meetings/, tasks.csv, push_to_template.py, push_template.sh
- Commit removal and push to origin/main
- Error handling: fail loudly if main was manually edited
- CI-friendly: callable from GitHub Actions or manual runs
- Report: what was pushed, what was removed

**Out of Scope:**
- Handling merge conflicts (main is release-only, shouldn't happen)
- Cherry-picking specific commits
- Rewriting history

## Acceptance Criteria

- [ ] Script creates/updates main cache folder safely
- [ ] `git merge --ff-only` works and fails gracefully if not fast-forward
- [ ] Removes all 5 artifact types: Features/, meetings/, tasks.csv, push_to_template.py, push_template.sh
- [ ] Commits removal with clear message
- [ ] Pushes to origin/main successfully
- [ ] Reports what was pushed (commit count, files removed)
- [ ] Can be called manually: `python3 push_to_template.py`
- [ ] Can be called from CI with env vars for branch/version
- [ ] Handles errors (missing origin, permission issues, etc.)

## Test Conditions

**Happy path:** New commits on dev, push to clean main
- Given: dev has 3 new commits ahead of main
- When: `python3 push_to_template.py` runs
- Then: Features/, meetings/, tasks.csv removed; 1 commit pushed to origin/main; report shows "3 commits merged, 5 artifacts removed"

**Error path:** Someone manually edited main
- Given: main was edited directly (not fast-forward)
- When: `python3 push_to_template.py` runs
- Then: `git merge --ff-only` fails; script exits with error; no push happens

**Error path:** Push fails (permission, network)
- Given: origin/main is unreachable
- When: `python3 push_to_template.py` runs
- Then: Script detects git push failure; reports error; exits non-zero

## Gherkin

```gherkin
Feature: Push template artifacts to clean main branch

  Scenario: Push new commits to main, removing dev artifacts
    Given dev branch has 3 commits ahead of main
    And Features/ contains 60 Kanban items
    And meetings/ contains 5 meeting files
    And tasks.csv has 57 rows
    When I run: python3 push_to_template.py
    Then Features/ is removed from main
    And meetings/ is removed from main
    And tasks.csv is removed from main
    And push_to_template.py is removed from main
    And push_template.sh is removed from main
    And 1 deletion commit is pushed to origin/main
    And script reports: "3 commits merged, 5 artifacts removed"

  Scenario: Prevent pushing if main was manually edited
    Given main has been manually edited (not fast-forward)
    When I run: python3 push_to_template.py
    Then git merge --ff-only fails
    And no commits are pushed to origin/main
    And script exits with error: "Main branch diverged; manual intervention required"

  Scenario: Report error if push fails
    Given origin/main is unreachable
    When I run: python3 push_to_template.py
    Then script detects git push failure
    And exits with non-zero code
    And logs the error reason
```

## Definition of Done

- [ ] Script written and tested locally
- [ ] All Gherkin scenarios pass (happy + error paths)
- [ ] Cache folder is safely created/updated (no overwrites)
- [ ] Fast-forward-only merge prevents accidental overwrites of main
- [ ] All 5 artifacts are reliably removed
- [ ] Commit message is clear and traceable
- [ ] Error handling: fails gracefully with helpful messages
- [ ] Works with GitHub Actions (documented env vars)
- [ ] Works with manual runs (documented usage)
- [ ] README updated: describe push process, how to run script
- [ ] Tested end-to-end: dev → main → downstream clone is clean
