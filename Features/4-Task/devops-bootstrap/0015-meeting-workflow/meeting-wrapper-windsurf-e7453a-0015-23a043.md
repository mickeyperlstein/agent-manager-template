---
id: "e7453a"
title: Create Windsurf meeting wrapper stub
type: task
epic: devops-bootstrap
feature: "0015"
feature_name: meeting-workflow
status: TaskReview
assignee: agent
depends_on: ["3075d4"]
review_gate: yes
---

## Scope

Create `.windsurf/workflows/meeting.md` — thin wrapper stub that points to the canonical protocol.

Follow the established pattern from `.windsurf/workflows/start.md`:
- Direct the agent to read `template_workflow/commands/meeting-protocol.md` in full
- Pass through arguments
- No workflow logic in the stub itself

## Acceptance Criteria

- [ ] File exists at `.windsurf/workflows/meeting.md`
- [ ] Follows same pattern as `.windsurf/workflows/start.md`
- [ ] `/meeting` command works in Windsurf and loads the canonical protocol
- [ ] Arguments are passed through correctly

## Comments
**2026-04-07 — Architect (Task creation):** Task stub created from approved HLD.
**2026-04-07 — Agent (Implementation):** Created `.windsurf/workflows/meeting.md`. Follows same pattern as `start.md` — points to canonical protocol with frontmatter description. Ready for TaskReview.
