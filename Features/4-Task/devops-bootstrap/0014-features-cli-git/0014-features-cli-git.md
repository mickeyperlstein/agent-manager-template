---
id: "0014"
title: features CLI — git (Features/-scoped git operations)
status: backlog
assignee: architect
depends_on: "0013"
review_gate: yes
---

## Story
As an agent, I need scoped git operations that only touch files inside `Features/` — so I can stage, commit, and push workflow changes autonomously without needing broad shell git access or risking commits that include unintended files.

## Acceptance Criteria
- [ ] `features git stage` — stages only files under `Features/` (equivalent to `git add Features/`)
- [ ] `features git commit -m "<message>"` — commits only if all staged files are inside `Features/`; rejects commit if any staged file is outside `Features/`
 - if files are outside featues git it will log the files, remove them from the staging, commit and return the files logged into the staging
- [ ] `features git push` — pushes current branch; only proceeds if last commit touches only `Features/` files
- [ ] Out-of-bounds guard: any operation that would touch files outside `Features/` handled by the log method described above
- [ ] Rollback: `features git undo` — reverts the last Features/-scoped commit (git revert, not reset)
- [ ] Single `allow` on `template_features_cli.py as skill or, can be mcp - open question
- [ ] Documented in KANBAN.md

## Trigger
Agents need to commit and push column moves without broad git permissions. Scoped git ensures autonomous operation stays within workflow boundaries.

## Dependencies
- `0013` (features CLI core) — shared boundary guard and CLI entrypoint extension for git

## Comments
**2026-04-02 — MOD+ARCH (meeting: agent-work-status-visibility):** Decided in continuation session. Split from 0013 on PM recommendation — git has different risk surface, failure modes, and test matrix. Needs own rollback strategy.