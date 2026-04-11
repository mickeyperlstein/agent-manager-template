# Meeting

Date: 2026-04-11 Time: 13:07

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
Problem: Current push pollutes main with Features/, meetings/, tasks.csv. Downstream ops manually clean up.
Solution: Replace git add . + unstage with git status → filter → git add. Include untracked files (intentional), exclude specific dirs/files.
Decision: Approved. Proceed to implementation.

## Decisions
**Outcome:** ACCEPTED — Proceed with implementation

**What to build:**
Replace `push_template.py` with new workflow:
1. Use `git status` to capture modified + untracked files
2. Filter against exclusion list (hardcoded at top)
   - Exclusions: Features/, meetings/, tasks.csv, push_template.py, push_template.sh
3. `git add` only filtered list
4. Bump version, commit, push

**Key requirement:** Untracked files MUST be included (solve the main problem)

**Next steps:**
- Implement new push_template.py
- Test with --test flag
- Review exclusion list before merging
