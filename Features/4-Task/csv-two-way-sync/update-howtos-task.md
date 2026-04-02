---
id: 73df4b
title: Update Agent-HowTos to reflect new frontmatter schema
type: task
assignee: architect
review_gate: yes
approved: no
depends_on: fd2dbd
---

## What
Update all `template_workflow/Agent-HowTos/` files to reflect the finalized frontmatter schema: hex id, `depends_on` field, `approved`/`review_gate` valid values (yes/no), `state` removed, `type` values.

## Scope
- In: all Agent-HowTos/*.md frontmatter templates and examples
- Out: script logic, CSV schema

## Acceptance Criteria
- [ ] Backlog.md: hex id generation instructions, depends_on field
- [ ] Task.md: hex id, depends_on in template
- [ ] HLD.md: hex id in examples
- [ ] TaskReview.md, Implement.md, Test.md: frontmatter examples consistent
- [ ] No sequential ids (0001, 0002) remaining in any HowTo template

## Test Conditions
- Human reads Backlog.md → knows exactly how to generate a hex id and fill depends_on
- Agent reads Task.md → creates task file with correct frontmatter fields

## Definition of Done
- [ ] All HowTo frontmatter templates updated
- [ ] No stale field names (state, feature, sequential ids)
