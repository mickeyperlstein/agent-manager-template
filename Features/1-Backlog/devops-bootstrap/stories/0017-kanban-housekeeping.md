---
id: "0017"
title: Kanban housekeeping — auto-prune empty folders and move stragglers
status: backlog
assignee: architect
depends_on: "0015"
review_gate: no
---

## Story

Every time an agent reads the Kanban board (at startup), the board should be automatically cleaned before they plan work. This prevents stragglers (HLD files stuck in 2-HLD when tasks exist in 4-Task) and empty epic folders (left behind after all features move forward).

The housekeeping should:
1. Prune empty epic folders (test with `rmdir`)
2. Detect and fix stragglers (features in wrong stage)
3. Report what was cleaned

This runs as Step 1a of every startup protocol (after reading KANBAN.md, before reading tasks.csv).

## Scope — What Housekeeping Fixes

| Situation | Action |
|-----------|--------|
| Empty epic folder (`Features/{col}/{epic}/` with no `.md` files) | Prune with `rmdir` |
| HLD file in 2-HLD + corresponding task folder in 4-Task | Move HLD + stub to 4-Task |
| HLD file in 3-HLD-Review + corresponding task folder in 4-Task | Move to 4-Task |
| Completed HLD in 2-HLD (has `-HLD.md`) but no 4-Task folder yet | Move both to 3-HLD-Review (ready for review) |
| Same filename in two stages (e.g., `0015-*.md` in both 2-HLD and 3-HLD-Review) | Remove the earlier-stage copy |

## Acceptance Criteria

- [ ] Protocol file written at `template_workflow/commands/housekeeping-protocol.md`
- [ ] Agent triggers created:
  - [ ] `.claude/commands/housekeeping.md`
  - [ ] `.windsurf/workflows/housekeeping.md`
- [ ] Housekeeping integrated into startup sequence:
  - [ ] `template_workflow/commands/start-protocol.md` — Step 1a
  - [ ] `agent-manager-claude.md` — Step 1a in startup protocol
  - [ ] `agent-manager-cline.md` — Step 1a in startup protocol
- [ ] `/housekeeping` command is executable and reports:
  - Number of folders pruned
  - Number of files moved + their paths
  - Number of duplicates removed
- [ ] Manual test: place a straggler HLD file, run `/housekeeping`, confirm it moves

## Output

- `template_workflow/commands/housekeeping-protocol.md` — canonical protocol
- `.claude/commands/housekeeping.md` — Claude trigger
- `.windsurf/workflows/housekeeping.md` — Windsurf trigger
- Updated startup protocols in 3 files

## Notes

Runs every session. Idempotent — second run on same board should find it clean.
Uses `git mv` for file organization, reports changes but does not commit (human commits).
