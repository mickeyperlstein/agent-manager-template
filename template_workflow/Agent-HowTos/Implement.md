# Implementation

## What is Implementation?

The agent writes code from the LLD using test-driven development (TDD). Code is complete when unit + integration + E2E tests all pass. A task enters here only after LLD and acceptance criteria exist and a human has approved.

**Column:** `6-Implementation`

## Testing Philosophy

**Unit tests (TDD):** Write test first, then code to pass it. Test LLD interfaces and contracts.

**Integration + E2E tests:** A small, focused suite (~30 well-chosen scenarios) beats hundreds of granular unit tests. Goal: regression protection — make sure nothing that worked before is broken.

**Black-box testing only:** Test the system from the outside. No knowledge of internals, no assertions on private state. Every assertion must be observable via:
- **Logs** (preferred) — structured entry confirming what happened
- **DB/storage artifact** — query database or filesystem to confirm writes
- **Harness** — for UI changes where visual output must be captured

If you can't verify a test by reading logs, querying an artifact, or harness output — it is not a valid test.

## Primary Input: the LLD

**Read the LLD before writing any code.** The LLD in each task file is the contract — interfaces, sequences, data shapes. The HLD is background context.

If LLD is missing, route back to TaskReview with a comment.

## Agent Responsibilities

1. **Read** `{feature}-HLD.md` — especially `## Logging & Monitoring` (context + observability contract)
2. **Read** each task's `## LLD` (implementation contract)
3. **Write unit tests first** (TDD) — test the LLD interfaces before implementing
4. **Implement** — match LLD interfaces exactly
5. **Implement logging and monitoring** — structured log entries and metrics per HLD spec
6. **Write integration + E2E tests** — verify via logs, DB artifacts, metrics per the HLD observability spec; verify Gherkin scenarios pass
7. **Update task file** — mark acceptance criteria complete
8. **Route to Review** when all tests pass (unit + integration + E2E)

## Checklist

- [ ] Unit tests written first (TDD) — test LLD interfaces before code
- [ ] Code matches LLD interface contracts exactly
- [ ] HLD `## Logging, Monitoring & Tracing` section implemented
- [ ] Every log entry is meaningful — answers a question someone would ask during an incident; no noise logs
- [ ] Distributed traces instrumented per HLD spec
- [ ] Metrics emitted per HLD spec
- [ ] Integration tests pass — components interact per LLD sequence
- [ ] E2E tests pass — Gherkin scenarios verified; observable outputs match (logs, DB, metrics)
- [ ] Unit + Integration + E2E test suites all pass
- [ ] No shortcuts from LLD without a documented reason
- [ ] Acceptance criteria marked complete
- [ ] Implementation Artifacts section filled in (source files, test files, branch, PR/commit)

## After Implementation

Agent moves task file to `7-Review` when all tests pass.
