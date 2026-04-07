---
id: "2d7440"
epic: "23a043"
feature: "95d961"
title: Update KANBAN.md with Column Move Protocol
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Add a "Column Move Protocol" section to KANBAN.md documenting the features CLI for agents.

## Scope
- Add section to KANBAN.md explaining the `features` CLI
- Document each command: move, new-id, clean
- Include example usage for agents
- Reference the CLI as the preferred method for column moves

## Acceptance Criteria
- [ ] New "Column Move Protocol" section in KANBAN.md
- [ ] Documents `features move`, `features new-id`, `features clean`
- [ ] Includes example commands for common operations
- [ ] Explains why this exists (single allow grant)

## Test Conditions
- Read KANBAN.md → verify section exists
- Verify all three commands documented
- Verify examples are correct

## Definition of Done
- KANBAN.md updated with protocol section
- All AC met
