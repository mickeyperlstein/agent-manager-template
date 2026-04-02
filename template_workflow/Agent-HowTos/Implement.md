# Implementation

## What is Implementation?

The agent writes code from the LLD. A task enters here only after LLD and acceptance criteria exist and a human has approved.

**Column:** `6-Implementation`

## Primary Input: the LLD

**Read the LLD before writing any code.** The LLD in each task file is the contract — interfaces, sequences, data shapes. The HLD is background context.

If LLD is missing, route back to TaskReview with a comment.

## Agent Responsibilities

1. **Read** `{feature}-HLD.md` — especially `## Logging & Monitoring` (context + observability contract)
2. **Read** each task's `## LLD` (implementation contract)
3. **Implement logging and monitoring first** — structured log entries and metrics are not optional add-ons
4. **Implement** — match LLD interfaces exactly
5. **Write E2E tests** — verify via logs, DB artifacts, metrics per the HLD observability spec
6. **Update task file** — mark acceptance criteria complete
7. **Route to Test** when done

## Checklist

- [ ] HLD `## Logging, Monitoring & Tracing` section read and implemented
- [ ] Every log entry is meaningful — answers a question someone would ask during an incident; no noise logs
- [ ] Distributed traces instrumented per HLD spec
- [ ] Metrics emitted per HLD spec
- [ ] Code matches LLD interface contracts
- [ ] E2E tests verify observable outputs (logs, DB, metrics)
- [ ] No shortcuts from LLD without a documented reason
- [ ] Acceptance criteria marked complete

## After Implementation

Agent moves folder to `7-Test`.
