---
id: 8bed76
title: Write E2E test suite
type: task
assignee: architect
review_gate: yes
approved: no
depends_on: 385474, 0640af, 3cda27
---

## What
Write the E2E test suite for the csv sync feature. Black-box only — tests verify behavior through log entries and filesystem state. Uses same tooling as production (log reader + filesystem checks).

## Scope
- In: test suite covering all Gherkin scenarios from HLD §10
- Out: unit tests, mocking of internals

## Acceptance Criteria
- [ ] All Gherkin scenarios from HLD §10 implemented as executable tests
- [ ] Each test verifies observable output (log entry + filesystem state)
- [ ] Idempotency scenario covered
- [ ] Auto-progression gate (review_gate + depends_on) covered
- [ ] Collision scenario covered
- [ ] Fallback rglob scenario covered

## Test Conditions
Each test verifies via log + filesystem:
- Run sync twice → second run log: "0 files moved"
- approved=yes, review_gate=yes → no move, no auto-progression log entry
- Collision → error log + file unmoved
- File not at expected path → warn log + file found and moved

## Definition of Done
- [ ] All scenarios pass
- [ ] No internal state assertions
- [ ] Tests run from CI without manual setup
