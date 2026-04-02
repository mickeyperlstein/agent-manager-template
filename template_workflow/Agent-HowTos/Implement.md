# Implementation

This system is V-Model driven. All changes to the system are tracked in the Features/ folder structure and synced to tasks.csv.

## What is Implementation?

The **Implementation** column is where actual code is written. A story enters Implementation only after:
- HLD is complete (feature-level design)
- LLD is complete (story-level contracts, sequences, data shapes)
- Gherkin acceptance criteria are written
- CTO has approved (committed the move)

## Primary Input: the LLD

**Read the LLD before writing any code.** The LLD (in the story's `## LLD` section) is the implementation contract — interface signatures, sequence, data shapes, and test plan. The HLD is background context only.

If the LLD is missing or incomplete, do not implement. Route the story back to TaskReview with a comment explaining what's missing.

## What Happens Here

| Activity | Who | Output |
|----------|-----|--------|
| Write tests first (TDD) | Agent | Failing tests per LLD test plan |
| Write code | Agent | Implementation matching LLD contracts |
| Update story file | Agent | Mark acceptance criteria complete |
| Route to testing | Agent | Testing-Agent or Testing-Manual |

## Agent Responsibilities

When a story is in Implementation:

1. **Read the LLD** — this is the contract, not the HLD
2. **Write tests first** — aligned to the LLD test coverage plan
3. **Implement code** — match LLD interfaces exactly; no design changes here
4. **Update story file** — mark each Gherkin scenario pass/fail
5. **Route to testing** — move to Testing-Agent or Testing-Manual

## Implementation Checklist

- [ ] LLD read and understood
- [ ] Tests written (fail before implementation) — per LLD test plan
- [ ] Code follows LLD interface contracts exactly
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass (if applicable)
- [ ] Acceptance criteria (Gherkin) met
- [ ] No shortcuts from LLD design without a documented reason

## After Implementation

Once implementation is complete:
1. Agent routes story to Testing-Agent (automated tests) or Testing-Manual (human QA)
2. Tests verify the implementation against Gherkin scenarios
3. Story moves to Verified when tests pass and human approves

## See Also

- `HLD.md` — Feature design (background context)
- `TaskReview.md` — LLD gate that precedes Implementation
- `Testing-Agent.md` — Automated testing phase
- `Kanban.md` — Full column workflow
