# Test

## Philosophy

A small, focused E2E suite beats hundreds of granular unit tests. The goal is regression protection — making sure nothing that worked before is broken. Aim for ~30 well-chosen E2E scenarios, not a test pyramid.

Unit tests are only worth writing for genuinely complex, isolated logic (e.g. a pure parsing function). Everything else: E2E.

## E2E Approach: Black-Box + Observable Output

Tests are **black-box only** — test the SUT from the outside. No knowledge of internals, no assertions on private state or implementation details.

Every assertion must be observable via one or more of:
- **Logs** (preferred) — structured entry confirming what happened
- **DB / storage artifact** — query the database or filesystem to confirm the write actually occurred
- **Harness** — for UI changes where visual output must be captured

For server-side tests, logs and DB artifacts should align — the log says "I wrote X" and the DB confirms X is there. A test only passes when all expected observability points match.

If you can't verify a test by reading logs, querying an artifact, or harness output — it is not a valid test.

## Tooling and Pipeline Coverage

Use the same tools for testing as production monitoring. If the project has Grafana, a passing E2E test means the metric shows up in Grafana — not just that the code ran.

**Every system in the pipeline that the code affects must be tested directly as black-box:**
- Writes to DB → query the DB
- Publishes to a queue → consume from the queue and verify the message
- Writes to cache → read from the cache
- Emits a metric → verify it in the monitoring dashboard (Grafana, etc.)
- Writes to object storage → read back the artifact
- Produces a log → read the log

If the code touches it, the test verifies it. No exceptions for "that's someone else's system." If it's in your pipeline, it's in your E2E.

## What is the Test Column?

The agent verifies the implementation against the E2E scenarios defined in the task files.

**Column:** `7-Test`

## Agent Responsibilities

1. Run E2E scenarios from each task's `## Acceptance Criteria`
2. Verify each scenario by reading logs or harness output — not internal state
3. Check for regressions — does anything that worked before still work?
4. Route forward:
   - All pass → move folder to `8-Review`
   - Needs human judgment (UX, visual) → flag for human, leave in Test
   - Fail → move folder back to `6-Implementation` with failure notes in task file

## Checklist

- [ ] Each scenario verified via logs or harness output
- [ ] No assertion on internal state or implementation details
- [ ] Regression suite passes
- [ ] No known gaps
- [ ] Failure notes written if routing back to Implementation

## After Test

Agent moves folder to `8-Review`.
