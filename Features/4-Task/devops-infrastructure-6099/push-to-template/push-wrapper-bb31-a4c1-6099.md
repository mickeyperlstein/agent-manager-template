---
id: bb31
epic: 6099
feature: a4c1
title: Bash Wrapper for Cache Management
type: task
assignee: agent
review_gate: yes
approved: no
depends_on:
---

## What
Create bash script that manages the push-to-template workflow: checkout main into a cache folder, merge dev, execute push_template.py from the clean environment, and clean up.

## Scope
- Check if cache folder exists; create or update it
- Checkout main branch cleanly into cache
- Merge dev into cache (using `git merge --ff-only`)
- Execute push_template.py from cache directory
- Handle errors: exit loudly if merge fails
- Clean up cache folder after push (or keep for next run?)
- Script is callable manually and from CI/CD

## Out of Scope
- Modifying push_template.py logic
- Complex error recovery
- Multi-branch support (only dev → main)

## Acceptance Criteria
- [ ] Script accepts command-line arguments (cache folder path, optional flags)
- [ ] Cache folder is created/updated cleanly on each run
- [ ] `git merge --ff-only` is called; fails gracefully if not fast-forward
- [ ] push_template.py runs from cache directory with correct PATH
- [ ] Script exits with error code on merge failure; no push happens
- [ ] Script reports what push_template.py did (files pushed, version bumped)
- [ ] Can be called manually: `bash push_wrapper.sh`
- [ ] Can be called from GitHub Actions with env vars

## Test Conditions
**Happy path:** Fresh cache, merge succeeds, push succeeds
- Given: cache folder doesn't exist, dev has commits ahead of main
- When: `bash push_wrapper.sh` runs
- Then: cache folder created, dev merged, push_template.py executes, files pushed to main

**Error path:** Merge fails (main diverged)
- Given: main was manually edited
- When: `bash push_wrapper.sh` runs
- Then: `git merge --ff-only` fails, script exits with error, no push happens

## Definition of Done
- [ ] Script written and tested locally
- [ ] Cache folder lifecycle is clean (create, use, keep or remove)
- [ ] Merge failure is detected and reported clearly
- [ ] push_template.py executes successfully in cache environment
- [ ] Script works in both local and CI environments
- [ ] No hardcoded paths; all configurable via args/env vars
- [ ] Error messages are helpful and actionable
