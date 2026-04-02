---
id: "0008"
title: Create .claude/agents/ stub wrappers
status: backlog
assignee: architect
depends_on: s05
review_gate: yes — Mickey manually tests each wrapper
---

## Story
As an agent, I want `.claude/agents/<name>.md` stub files that point to `template_workflow/agents/` so Claude Code loads the correct agent definition from the canonical SOT.

## Acceptance Criteria
- [ ] One stub per agent (6 total) in `.claude/agents/`
- [ ] Stub contains correct frontmatter (name, description, model, color)
- [ ] Stub body directs Claude to load canonical file from `template_workflow/agents/<name>.md`
- [ ] Mickey manually invokes each agent and confirms it loads correctly
- [ ] No agent logic duplicated in stubs — SOT is template_workflow only

## Dependencies
- s05 (canonical files must exist before stubs point to them)

## Notes
Mickey tests each wrapper manually before this story is marked done.
