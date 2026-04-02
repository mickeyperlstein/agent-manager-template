---
id: "0010"
title: Create .cline/ stub wrappers
status: backlog
assignee: architect
depends_on: "0006, 0007"
review_gate: yes — Mickey manually tests each wrapper
---

## Story
As an agent, I want `.cline/` rule/stub files that load agent context from `template_workflow/` so Cline picks up the correct agent persona and project rules from the canonical SOT.

## Acceptance Criteria
- [ ] Research from 0006 confirms exact Cline folder and file format
- [ ] Stub files created per agent under `.cline/` (format TBD by research)
- [ ] Each stub points to or includes content from `template_workflow/agents/<name>.md`
- [ ] Mickey manually activates each agent in Cline and confirms persona loads
- [ ] Manual test steps documented (output from 0006 research)

## Dependencies
- 0006 (research must confirm Cline's exact loading mechanism)
- 0007 (canonical agent files must exist in template_workflow/)

## Notes
Cline has no native "agents" — may use `.clinerules`, custom instructions, or MCP context injection. Research (0006) determines the approach.
