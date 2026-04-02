---
id: "0012"
title: Create demo meeting stub (prefilled save-as template)
status: backlog
assignee: architect
depends_on: s07
review_gate: yes
---

## Story
As any agent, I want a prefilled meeting stub template so that starting a new meeting produces a properly structured file without manual setup — matching what we did in the 2026-04-02 sessions.

## Acceptance Criteria
- [ ] `template_workflow/templates/meeting-stub.md` created with all sections prefilled with placeholders
- [ ] Sections: Participants, Goal, Relevant Info, Agenda, Notes, Rolling Summary, Decisions, Action Items
- [ ] Meeting workflow (s07) uses this template as its base when `/meeting` is invoked
- [ ] Saving meeting produces correctly named file: `meetings/YYYY-MM-DD_slug.md`
- [ ] Tested end-to-end: invoke `/meeting`, confirm stub loads, confirm save works

## Dependencies
- s07 (meeting workflow must be wired up first)
