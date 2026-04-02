---
id: 385474
title: Review and update folders_to_csv.py
type: task
assignee: architect
review_gate: yes
approved: no
depends_on:
---

## What
Review the existing `template_workflow/scripts/folders_to_csv.py` against the HLD and update it to match: correct column names (1-Backlog through 10-Canceled), `name` field derived from filename, hex id from frontmatter, `depends_on` field, shared schema module.

## Scope
- In: folders_to_csv.py, shared schema module
- Out: csv_to_folders.py (separate task), pre-commit hook

## Acceptance Criteria
- [ ] Scans all columns including 10-Canceled
- [ ] Derives `name` from filename, `state` from folder path
- [ ] Reads hex `id` from frontmatter
- [ ] Reads `depends_on` from frontmatter
- [ ] Uses shared schema module for CSV field order
- [ ] Logs per spec (info/warn/error, structured fields)

## Test Conditions
- Happy path: scan Features/ → CSV reflects correct state, name, id → log: "sync complete" with item_count
- Missing id in frontmatter → log: warn, file skipped
- 10-Canceled folder → items appear in CSV with state = Canceled

## Definition of Done
- [ ] Script passes E2E scenarios from HLD §10
- [ ] All log events present per §6
- [ ] No regressions on existing behavior
