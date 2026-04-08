---
id: "0013"
title: features CLI — core (column moves + ID generation)
status: backlog
assignee: architect
depends_on: none
review_gate: yes
---

## Story
As an agent, I need a sandboxed CLI (`python -m features`) that handles all permission-sensitive workflow operations inside `Features/` — so I can move task files between columns and generate hex IDs with a single user `allow` grant instead of per-operation prompts.

## Acceptance Criteria
- [ ] `features move <filepath> <target-column>` — moves a task file to the correct column folder, constrained to `Features/` tree; rejects any path outside `Features/` with a clear error
- [ ] `features new-id [task|feature|epic]` — generates a collision-free 3-byte hex ID, prints to stdout
- [ ] `features clean` — deletes all files with `state: marked-for-deletion` in frontmatter, inside `Features/` only
- [ ] Startup guard: script prints warning and asserts all target paths are within `Features/` before any operation
- [ ] Single `allow` on `python -m features` covers all the above operations for agents
- [ ] Entrypoint: `template_workflow/features/__main__.py`
- [ ] Documented in KANBAN.md under "Column Move Protocol"

## Trigger
Agents need column moves but may not have shell `mv`/`rm` permission. This CLI provides a safe, bounded, always-allowable alternative.

## Dependencies
None.

## Comments
**2026-04-02 — MOD+ARCH (meeting: agent-work-status-visibility):** Decided in continuation session. Replaces the write+mark-for-deletion workaround. PM confirmed: ship safe ops first, gate git behind a separate story.
