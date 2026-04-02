---
id: s09
title: Create "agent-manager-template" repo  on github using gh cli
status: backlog
assignee: architect
depends_on: nothing
review_gate: yes
---

## Story
As the team, I want a GitHub repo `agent-manager-template` that houses all agent tooling (agent definitions, meeting workflow, CSV sync script, wrappers) so these tools can be maintained independently and consumed as an upstream by any project repo.

## Acceptance Criteria
- [ ] `agent-manager-template` repo created on GitHub (confirm visibility with Mickey)
- [ ] `template_workflow/version.json` present at root of template folder: `{ "version": "1.0.0" }`
- [ ] Version bumped on every breaking change to template structure or config schema
- [ ] Consuming repos can check `template_workflow/version.json` to know which template version they're on
- [ ] Load order documented: agent-manager upstream → template_workflow/ project overrides

## Dependencies
none

## Open Questions
none

