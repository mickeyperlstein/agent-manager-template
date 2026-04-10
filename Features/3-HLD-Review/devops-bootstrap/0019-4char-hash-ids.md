---
id: "0019"
title: Shorten task ID hashes to 4 characters for readability
status: HLD
assignee: architect
review_gate: yes
---

## Story

As a template user, I want task IDs to use 4-character hex hashes instead of 6-character hashes so that file paths and Kanban listings are more readable and easier to remember.

Current: `pubspec-35b799-5d3989-ac402c`  
Target: `pubspec-35b7-5d39-ac40`

## Acceptance Criteria

- [ ] HLD specifies ID format: `{task_name}-{epic_4char}-{feature_4char}-{task_4char}`
- [ ] HLD documents collision risk analysis (65k possibilities per segment)
- [ ] Kanban.md updated with ID length constraint
- [ ] Python hash generation script modified to take first 4 chars instead of 6
- [ ] Script enforces 4-char limit in validation
- [ ] Existing IDs with 6-char hashes can coexist (backward compatible)
- [ ] HLD reviewed for format decision and collision risk acceptance

## Dependencies
- Assumes merge with existing hash generation in feature 0013 (features CLI)

## Notes
- Collision risk acceptable: 65k possibilities per segment (4-char hex)
- Full hash not retained (simplicity > insurance against unlikely collisions)
- Format is hierarchical: epic hash → feature hash → task hash (3-level isolation)
- Backward compatible: existing 6-char IDs can coexist; new generation uses 4-char
