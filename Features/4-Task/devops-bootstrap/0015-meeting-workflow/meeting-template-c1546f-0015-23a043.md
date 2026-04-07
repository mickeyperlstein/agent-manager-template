---
id: "c1546f"
title: Create meeting file template
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

Create `template_workflow/templates/meeting-stub.md` — the prefilled meeting file template used by the protocol in Step 2.

This absorbs the scope of story 0012 (meeting stub template).

Must include all sections from the HLD meeting file format:
- Header: Meeting title, Date, Time
- Participants (with MOD + role format)
- Topic
- Goal
- Relevant Info (with working meeting variant: Prior Discussion sub-section)
- Agenda
- Notes (with working meeting variant: Prior Discussion + Meeting Notes sub-sections)
- Rolling Summary
- Decisions

Use placeholder tokens (e.g., `<topic>`, `<participant>`) that the protocol fills in at runtime.

## Acceptance Criteria

- [ ] File exists at `template_workflow/templates/meeting-stub.md`
- [ ] All sections from HLD meeting file format are present
- [ ] Placeholder tokens are clear and self-documenting
- [ ] Works for both default and working meeting modes
- [ ] 0012 can be closed as superseded

## Comments
**2026-04-07 — Architect (Task creation):** Task stub created from approved HLD. Absorbs scope of 0012.
**2026-04-07 — Agent (Implementation):** Created `template_workflow/templates/meeting-stub.md` with all sections: Participants (MOD format), Topic, Goal, Relevant Info, Agenda, Notes, Rolling Summary, Decisions. Uses self-documenting placeholder tokens. Ready for TaskReview.
