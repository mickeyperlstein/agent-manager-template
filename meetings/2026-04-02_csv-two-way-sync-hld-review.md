# Meeting: C4 Diagrams and V-Model Levels for devops-bootstrap
Date: 2026-04-02 Time: 06:11

## Participants
- MOD + ARCH: Claude — playing Architect + facilitator
- ARCH: architect — Senior software architect, deep expertise in distributed systems, Node.js, TypeScript, VS Code extensions, event-driven architecture — `~/.claude/agents/architect.md`

## Goal
Finalize the Kanban column flow, artifact levels, and folder structure for the agent-manager-template.

## Relevant Info
- HLD file: `Features/2-HLD/devops-bootstrap/0002-csv-two-way-sync-HLD.md`
- Project: agent-manager-template — a Kanban-as-code governance system for AI coding agents

## Agenda
1. C4 and V-Model mapping
2. HLD vs story/task timing
3. LLD placement
4. Column flow and missing gates
5. Folder/file structure convention

## Notes

- C4 L1/L2 belongs at HLD. C4 L3 belongs at TaskReview (LLD).
- Backlog holds feature stubs only. Stories/tasks are NOT written in Backlog.
- HLD produces task decomposition. Tasks are formally created in the Task column.
- LLD lives inside TaskReview — it is the gate artifact, not a separate column.
- V-Model right leg (tests) is currently implicit — test levels need to be defined in LLD before implementation.
- "Verified" column dropped — test pass + PR review covers it.
- Testing-Agent and Testing-Manual collapsed into single "Test" column (routing is internal).
- HLD agent is the ONE exception to "agents never move stories" — it moves HLD → HLD-Review.
- Folder convention: feature starts as single file, becomes a folder at Task column. HLD travels as sibling.

## Rolling Summary

- Settled C4/V-Model mapping to Kanban columns
- Added HLD-Review gate between HLD and TaskReview
- Added Task column between HLD-Review and TaskReview for task file creation
- Dropped Verified, collapsed Testing into single Test column
- Final flow: Backlog → HLD → HLD-Review → Task → TaskReview → Implementation → Test → Review → Done
- Folder convention established: `{feature}.md` → `{feature}-HLD.md` → `{feature}/` folder from Task onwards
- template branch strategy decided: dev = live project, main = clean template via push_template.sh

## Decisions

1. **Final column flow (9 columns):**
   `Backlog → HLD → HLD-Review → Task → TaskReview → Implementation → Test → Review → Done`

2. **Folder convention:**
   - Backlog: `{feature}.md`
   - HLD / HLD-Review: `{feature}-HLD.md`
   - Task onwards: `{feature}/` folder containing `{feature}-HLD.md` + `0001-{task}.md` files

3. **HLD agent is the only agent that may move a story** (HLD → HLD-Review)

4. **LLD lives in TaskReview** — required artifact before Implementation; written by architect agent per task

5. **Backlog = feature stubs only** — no tasks, no Gherkin, no architecture

6. **Template branch strategy:** `dev` = living project, `main` = clean template; `push_template.sh` syncs dev → main (excludes Features/ and meetings/)

7. **Version bumping:** `push_template.sh` bumps minor version on each template release

## Open Questions

- Should Task column be agent-automated (agent creates task files from HLD) or human-driven?
- Should `{feature}-HLD.md` stay as a sibling through all columns, or move to an archive after TaskReview?
