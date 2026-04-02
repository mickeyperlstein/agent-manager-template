---
epic: 23a043
feature: bd72df
id: 0640af
title: Review and update csv_to_folders.py
type: task
assignee: architect
review_gate: yes
approved: no
depends_on: 385474
---

## What
Review the existing `template_workflow/scripts/csv_to_folders.py` against the HLD and update it: correct auto-progression map (new 9+1 column names), gate requires `review_gate=no` AND `approved=yes`, `depends_on` blocks progression if dependencies not Done, shared schema module.

## Scope
- In: csv_to_folders.py, auto-progression logic, dependency gate
- Out: folders_to_csv.py, pre-commit hook

## Acceptance Criteria
- [ ] Auto-progression map matches HLD: Backlog→HLD→HLD-Review→Task→TaskReview→Implementation→Test→Review→Done
- [ ] Auto-progression blocked if `review_gate=yes`
- [ ] Auto-progression blocked if any `depends_on` item is not in Done
- [ ] Uses shared schema module
- [ ] Logs per spec

## Test Conditions
- Happy path: approved=yes, review_gate=no, no deps → file moves to next column → log: "auto-progression applied"
- Blocked by review_gate: approved=yes, review_gate=yes → file does not move
- Blocked by dependency: depends_on item not in Done → file does not move → log: warn "blocked by dependency"
- Collision at target → log: error, file unmoved

## Definition of Done
- [ ] All Gherkin scenarios from HLD §10 pass
- [ ] Dependency gate tested
- [ ] No regressions
