# Meeting

Date: 2026-04-11 Time: 13:07 — **RESUMED 2026-04-12 18:45**

## Participants
- MOD + ARCH: Claude Haiku 4.5 — playing Architect + facilitator
- (none yet)

## Topic
Selective git push workflow — prevent unwanted directories from reaching main

## Goal
Decide on implementation approach for selective git add filtering to replace `git add .`

## Relevant Info
see push_template.py for existing state

**Problem Statement:**
Current push uses `git add .` which includes `features/`, `meetings/`, `reviews/`, and other excluded directories in the commit. These reach main, and downstream ops must manually delete folders and files from the website repo — creating manual cleanup work and mess.

**Recommended Solution:**
Instead of `git add .` followed by removal, use `git status` to show a line-by-line list of changes. Filter out excluded items (meetings/, features/, etc.) from the output, then `git add` only the approved lines. This gives us both flexibility and explicit exclusion control.

**Why it matters:**
- Prevents unwanted artifacts from polluting main
- Gives teams explicit control over what gets pushed
- No downstream cleanup needed
- Small difference, big impact

## Agenda
- Review problem and proposed solution
- Discuss implementation approach (filtering logic, exclusion list)
- Decide on approach
- Any blockers or alternatives?

## Notes
- ARCH: Reviewed current push_template.py approach (git add . then unstage exclusions) — backwards, error-prone
- ARCH: Your proposal (git status → filter → git add approved) is cleaner, more direct
- Clarified: Include untracked files in the filter (that's the point), but exclude Features/, meetings/, tasks.csv, push_template.py, push_template.sh
- Exclusion list will be hardcoded at top of script for user review

## Rolling Summary
**Phase 1 (2026-04-11):**
Problem: Current push pollutes main with Features/, meetings/, tasks.csv. Downstream ops manually clean up.
Solution: Replace git add . + unstage with git status → filter → git add. Include untracked files (intentional), exclude specific dirs/files.
Decision: Approved. Proceed to implementation.

**Phase 2 (2026-04-12 - RESUMED):**
Implementation revealed new issues:
- Current git status approach may not be detecting changes correctly
- Question: should main branch be in separate folder for push operations?
- Unclear how files will actually move during push
- Need to reconsider git methodology: git status vs git diff --files or other approach

## Decisions
**Phase 1 Outcome (REJECTED):** git status → filter → git add approach doesn't work
- Problem: Changes are already committed, git status shows nothing
- Repo is 4+ commits ahead of remote, but working tree is clean

**Phase 2 Outcome (ACCEPTED):** Separate main cache + merge approach

**What to build:**
Automated push-to-template script:
1. Maintain local cache folder with clean checkout of main
2. Merge dev into main cache: `git merge --ff-only dev`
3. Remove dev artifacts: `git rm -r Features/ meetings/ tasks.csv push_to_template.py push_template.sh`
4. Commit removal: `git commit -m "chore: remove dev-only artifacts"`
5. Push to origin/main
6. Report what was pushed

**Key architecture decisions:**
- Main is release-only (no manual edits, script-only pushes)
- Dev stays full project (Features/, meetings/, tasks.csv intact)
- Cache folder is clean source of truth for main
- Script is deterministic, CI-friendly, can be called from GitHub Actions

**Exclusions on main:**
- Features/
- meetings/
- tasks.csv
- push_to_template.py
- push_template.sh

**Next steps:**
- Create feature: push-to-template automation (high priority, HLD-ready)
- Implement script with error handling
- Test in CI workflow
- Document deployment process
