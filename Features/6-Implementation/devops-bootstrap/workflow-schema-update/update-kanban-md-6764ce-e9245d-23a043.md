---
id: 6764ce
epic: 23a043
feature: e9245d
title: Update KANBAN.md for individual file moves and filename convention
type: task
assignee: agent
review_gate: no
approved: yes
depends_on:
fast_tracked: yes
source: meetings/2026-04-02_agent-work-status-visibility.md
---

## What
Rewrite the folder lifecycle and column table in `KANBAN.md` to reflect that task files move individually (not as a folder unit) from Task onwards, and document the filename convention.

## Why fast-tracked
Pure doc update. Decisions made in meeting 2026-04-02.

## LLD
In `KANBAN.md`:

1. **Folder Lifecycle section** — replace current folder-as-unit block with:
   - Backlog/HLD/HLD-Review: single file moves as before
   - Task onwards: individual task files move independently
   - HLD file stays as reference artifact in the feature folder
   - Add note: `depends_on` controls ordering between tasks

2. **Filename convention** — add a new section:
   ```
   ## Filename Convention
   {name}-{taskid}-{featureid}-{epicid}.md
   - name: human-readable slug
   - taskid, featureid, epicid: short hex (3 bytes, generated at creation)
   ```

3. **Column table** — update File Structure column for Task and beyond to show individual file moves

## Acceptance Criteria
- [ ] Folder lifecycle reflects individual file moves from Task column onwards
- [ ] Filename convention documented with example
- [ ] Column table updated
