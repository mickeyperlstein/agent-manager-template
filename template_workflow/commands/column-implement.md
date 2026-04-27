# Column: Implementation (6-Implementation)

**What:** Agent writes code from the LLD using test-driven development (TDD). Code is complete when unit + integration + E2E tests all pass.

**When to work here:** Agent acts after LLD and acceptance criteria exist and human has approved in TaskReview.

---

## Primary Input: the LLD

**Read the LLD before writing any code.** The LLD in each task file is the contract — interfaces, sequences, data shapes. The HLD is background context.

**Verify LLD clarity BEFORE writing code:**
1. **`layer:` field** — Is it BASH, PYTHON, JS? Does that match the HLD Architecture section?
2. **`file_to_modify:` field** — Which existing file? Are you editing it, or creating new?
3. **Responsibilities section** — What does this layer own, what does it NOT own?
4. **Assumptions section** — What state is the system in before this task runs?

**If any are missing or unclear:** Route back to TaskReview with: "LLD incomplete — please clarify: layer designation, file target, and layer boundaries."

---

## Testing Philosophy

**Unit tests (TDD):** Write test first, then code to pass it. Test LLD interfaces and contracts.

**Integration + E2E tests:** A small, focused suite (~30 well-chosen scenarios) beats hundreds of granular unit tests. Goal: regression protection — make sure nothing that worked before is broken.

**Black-box testing only:** Test the system from the outside. No knowledge of internals, no assertions on private state. Every assertion must be observable via:
- **Logs** (preferred) — structured entry confirming what happened
- **DB/storage artifact** — query database or filesystem to confirm writes
- **Harness** — for UI changes where visual output must be captured

If you can't verify a test by reading logs, querying an artifact, or harness output — it is not a valid test.

---

## Agent Responsibilities

1. **Read** `{feature}-HLD.md` — especially `## Logging & Monitoring` (context + observability contract)
2. **Read** each task's `## LLD` (implementation contract)
3. **Write unit tests first** (TDD) — test the LLD interfaces before implementing
4. **Implement** — match LLD interfaces exactly
5. **Implement logging and monitoring** — structured log entries and metrics per HLD spec
6. **Write integration + E2E tests** — verify via logs, DB artifacts, metrics per the HLD observability spec; verify Gherkin scenarios pass
7. **Update task file** — mark acceptance criteria complete
8. **Route to Review** when all tests pass (unit + integration + E2E)

---

## Checklist

- [ ] Unit tests written first (TDD) — test LLD interfaces before code
- [ ] Tests are clean flows — one test with multiple assertions, not many tests with repeated setup/teardown
- [ ] Code is DRY — no duplication, reuse logic, delete dead code, minimize LOC
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

---

## After Implementation

Agent moves task file to `8-Review` when all tests pass.
