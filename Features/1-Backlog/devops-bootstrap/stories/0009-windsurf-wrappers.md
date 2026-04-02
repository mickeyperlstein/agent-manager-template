---
id: "0009"
title: Create .windsurf/workflows/ stub wrappers
status: backlog
assignee: architect
depends_on: s05
review_gate: yes — Mickey manually tests each wrapper
---

## Story
As an agent, I want `.windsurf/workflows/<name>.md` stub files that point to `template_workflow/workflows/` so Windsurf loads skills/workflows from the canonical SOT.

## Acceptance Criteria
- [ ] `template_workflow/workflows/meeting.md` created (canonical, sourced from perli_old windsurf version)
- [ ] `.windsurf/workflows/meeting.md` stub points to canonical
- [ ] Mickey manually tests meeting workflow via `/meeting` command
- [ ] Pattern documented so future workflows follow same stub convention

## Dependencies
- s05 (template_workflow structure must exist)

## Notes
Source for canonical meeting.md: `perli_old/.windsurf/workflows/meeting.md` (more complete than commands-skills version).
Mickey tests manually before done.
