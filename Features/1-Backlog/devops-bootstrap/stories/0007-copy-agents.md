---
id: "0007"
title: Copy agent files to template_workflow/agents/
status: backlog
assignee: architect
depends_on: s02
review_gate: yes
---

## Story
As the team, I want all agent definitions copied from `perli_old` into `template_workflow/agents/` (the canonical SOT) so agents are available in the new repo.

## Acceptance Criteria
- [ ] `template_workflow/agents/` created
- [ ] All 6 agents copied: architect, mobile_developer, automated_tester, pm, data_science_agent, china_sourcing_expert
- [ ] Memory paths inside each file updated to point to new repo location
- [ ] `template_workflow/agents/agent-memory/<agent>/` dirs created with `.gitkeep`
- [ ] Mickey reviews each copied file before wrappers are created (s06, s07)

## Dependencies
- s02 (repo must exist to push)

## Notes
Source: `perli_old/template_workflow/agents/*.md`
