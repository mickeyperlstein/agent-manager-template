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

**Why:** Current push strategy is using git status where it should be comparing between branches, and instead of complex branching diffs and reinventing git it makes more sense to just use the correct git workflow of checkout from main to a temp upsert then pull changes from dev  and then the existing script will work as planned because status will be "dirty'

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

## Architecture & Layer Responsibilities

**Two-layer design: Bash wrapper + Python core**

```
┌─────────────────────────────────────────────────┐
│  push_template.sh (BASH wrapper)                │
│  ├─ Check/create cache folder                  │
│  ├─ git clone origin (if missing)              │
│  ├─ git checkout main                          │
│  ├─ git fetch origin                           │
│  ├─ git pull origin/main                       │
│  └─ Call: python3 push_template.py             │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│  push_template.py (PYTHON core logic)           │
│  ├─ git merge --ff-only dev/dev                │
│  ├─ git status → filter allowed files          │
│  ├─ git add allowed_files_only                 │
│  ├─ git commit -m "chore: merge dev..."        │
│  └─ git push origin HEAD:main                  │
└─────────────────────────────────────────────────┘
```

**Why this split?**
- Bash handles infrastructure (clone, checkout, pull) — simple, transparent, shell-native
- Python handles filtering logic (merge, filter, commit, push) — business logic, testable, recoverable

**Invariant:** Cache always starts clean (Bash ensures this). Python only does merge+filter+commit+push.

**Layer boundary rule:** No `git init` in Python. No filtering logic in Bash. Respect the split.

## Acceptance Criteria

- [ ] Script creates/updates main cache folder safely
- [ ] `git merge --ff-only` works and fails gracefully if not fast-forward
- [ ] Removes all 5 artifact types: Features/, meetings/, tasks.csv, push_to_template.py, push_template.sh and allows adding to this list i a central simple fashion
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
- Then: `git merge --ff-only` fails; script exits with error; no push happens log / stderr show error for user

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
    Then Features/ is not in  main
    And meetings/ is not in main
    And tasks.csv is not in main
    And push_to_template.py is not in main
    And push_template.sh is not in main
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
testing can be human run or automated via basic bash
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

---

# Review 2026-04-14

## Participants
- Presenter: architect (Claude Haiku)
- Reviewer: senior-architect (Claude Opus)
- MOD: Claude Haiku

## Questions & Answers

**Q (Senior Architect):** Cache state management — how do you handle stale/corrupted cache, filesystem wipes, or main branch divergence?

**A (Presenter):** Cache is transitory (reset each run). Procedure: stash → fetch → pull → operate → stash pop. If anything fails, cache is reset on next run. Idempotent design means safe to retry.

**Q (Senior Architect):** Artifact removal strategy — filtering git status only stages changes, doesn't remove pre-existing artifacts on main.

**A (Presenter):** Whitelist approach: `git status` → filter excluded items → `git add allowed_files_only` → commit → push. Artifacts never get staged, so they're implicitly excluded. Pre-existing artifacts on main will be gone because they're not in the merge.

**Q (Senior Architect):** Push failure recovery — what if push fails mid-flight after removal commit?

**A (Presenter):** Idempotent design: exit(1), nothing committed to main, dev branch unaffected. On retry: cache resets and runs again safely.

## Rolling Summary

- HLD designs automated push-to-template script with safety-first approach
- Cache is transitory, resets each run (stash→fetch→pull→operate→stash pop)
- Artifact filtering via whitelist: only stage allowed files, artifacts are implicitly excluded
- Idempotent: safe to retry on any failure
- Three critical architectural concerns addressed and resolved
- Design is CI-friendly and deployable

## Decisions & Clarifications

**✅ Cache Folder Location:** Default to `~/Documents/agent-manager-template-release/`

**✅ Artifact Removal:** Whitelist approach — `git status` → filter → `git add allowed` → commit → push

**✅ Failure Recovery:** Idempotent (exit 1, safe retry)

**✅ Logging:** Simple stdout/stderr (CI standard, human-readable)

**✅ CI Integration:** Single script entry point, idempotent

**Outcome: ACCEPTED** — HLD is architecturally sound and ready for task decomposition

Kanban movement: 3-HLD-Review → ready for task creation in 4-Task
