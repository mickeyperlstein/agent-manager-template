---
id: 993e26
epic: 23a043
feature: e9245d
title: Update CSV schema and HLD data model
type: task
assignee: agent
review_gate: no
approved: yes
depends_on:
fast_tracked: yes
source: meetings/2026-04-02_agent-work-status-visibility.md
---

## What
Update the CSV schema and HLD data model to add `epic` and `feature` as explicit hex id fields. Update the example row and field table in `Features/4-Task/csv-two-way-sync/0002-csv-two-way-sync-HLD.md`.

## Why fast-tracked
Pure doc update. Decisions made in meeting 2026-04-02. No design needed — schema is fully specified in meeting decisions.

## LLD
In `0002-csv-two-way-sync-HLD.md` §3.1:
- CSV schema line: add `epic` and `feature` after `id`
  - New: `id,epic,feature,state,name,assignee,type,review_required,approved,depends_on`
- Add rows to field table:
  - `epic` | frontmatter | Hex id of the epic this item belongs to
  - `feature` | frontmatter | Hex id of the feature this item belongs to
- Update example row to include epic and feature hex ids
- Update shared schema module note to reflect new field order

## Acceptance Criteria
- [ ] CSV schema line in HLD includes `epic` and `feature` fields
- [ ] Field table has entries for both with source = frontmatter
- [ ] Example row is valid against new schema
