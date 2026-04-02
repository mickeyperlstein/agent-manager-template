# Testing-Agent

## What is Testing-Agent?

The **Testing-Agent** column is for automated testing by AI agents. After implementation, stories enter here to verify they work correctly against the Gherkin scenarios and LLD test plan.

## When to Test

**Column:** `Testing-Agent` (Features/5-Testing-Agent/)

Stories are tested when:
- Implementation is complete
- Code is ready for verification
- Tests can be automated (not requiring human judgment)

## V-Model Test Levels

Tests should cover all levels defined in the story's LLD test coverage plan:

| V-Model Level | Test Type | Verifies |
|---|---|---|
| Code | Unit tests | Individual functions match LLD interface contracts |
| Component | Integration tests | Components interact correctly per LLD sequence |
| Container | Smoke / contract tests | End-to-end flow through containers |
| Requirements | Acceptance tests | Gherkin scenarios pass |

## What Happens Here

| Activity | Who | Output |
|----------|-----|--------|
| Run unit tests | Agent | Pass/fail results |
| Run integration tests | Agent | Pass/fail results |
| Run e2e / acceptance tests | Agent | Gherkin scenario results |
| Check coverage | Agent | Coverage report |
| Verify acceptance criteria | Agent | Gherkin checklist completion |
| Route forward | Agent | Next column decision |

## Insufficient Tests

If the existing tests don't cover edge cases, negative paths, or critical failure modes that you identify:

1. Add `**Rejected by Tester:** insufficient tests — [reason]` at the top of the story file
2. Add the missing scenarios in Gherkin format at the end of `## Acceptance Criteria`
3. Add a comment explaining why (dated, with your role)
4. Route the story to `Testing-Manual` instead of Verified

Do not route to Verified with known gaps.

## Agent Responsibilities

When a story is in Testing-Agent:

1. **Run all tests** — Unit, integration, e2e per LLD test plan
2. **Verify Gherkin scenarios** — Each scenario must pass explicitly
3. **Report results** — Document pass/fail in story comments
4. **Route forward**:
   - All pass → Verified
   - Needs human QA or has gaps → Testing-Manual
   - Fail → Back to Implementation with failure details

## Testing Checklist

- [ ] Unit tests pass (per LLD coverage plan)
- [ ] Integration tests pass (per LLD coverage plan)
- [ ] E2E / acceptance tests pass (Gherkin scenarios)
- [ ] Coverage meets threshold
- [ ] No regressions introduced
- [ ] All Gherkin scenarios explicitly verified

## After Testing-Agent

Once automated testing passes:
1. Story moves to Verified (human approval)
2. Or routes to Testing-Manual if human QA needed
3. Human verifies and approves for PR

## See Also

- `Implement.md` — Coding phase that precedes testing
- `TaskReview.md` — LLD and Gherkin defined here
- `Kanban.md` — Full column workflow
