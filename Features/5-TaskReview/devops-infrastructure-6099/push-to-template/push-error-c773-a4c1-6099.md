---
id: c773
epic: 6099
feature: a4c1
title: Push & Error Handling
type: task
assignee: architect
review_gate: no
depends_on: "5829"
---

## Task: Push & Error Handling

**What:** Implement git push and idempotent failure recovery.

**Acceptance Criteria:**
- [ ] `git push origin HEAD:main` executes
- [ ] On failure: exit(1), no partial state
- [ ] Error message logged to stderr
- [ ] Idempotent: safe to retry (transitory cache resets)
- [ ] Reports on success: commits merged, artifacts removed

**Definition of Done:**
- [x] Function: push_to_main() implemented
- [x] Error handling tested (3/3 tests: success, failure no origin, stderr logging)
