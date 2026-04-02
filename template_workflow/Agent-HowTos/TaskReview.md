# TaskReview

## What is TaskReview?

**TaskReview** is the LLD gate. Stories arrive here from HLD and leave with:
- A Low Level Design (LLD) per story — interface contracts, sequence diagrams, data shapes (C4 L3)
- Gherkin acceptance criteria
- CTO sign-off (commit to move to Implementation)

No story may enter Implementation without a completed LLD and Gherkin.

## Who Acts Here

**Architect agent** writes the LLD and Gherkin for each story. **CTO (human)** reviews and commits the move to Implementation.

The architect agent reads the HLD, decomposes each story into an LLD, and writes Gherkin. The CTO is the approval gate — no story moves to Implementation without a human commit.

## What is an LLD?

A **Low Level Design** is a story-level spec that makes the story implementable without ambiguity. It lives at C4 Level 3 (Component).

LLD answers:
- **Interface contracts**: function signatures, API shapes, event schemas
- **Sequence diagrams**: call order, async vs sync, error paths
- **Data shapes**: input/output types, validation rules, edge cases
- **Test level mapping**: which tests verify this story (unit / integration / container)

## LLD Document Structure

Add an `## LLD` section to the story file:

```markdown
## LLD

### Interfaces
\`\`\`typescript
// function/method signatures or API contracts
\`\`\`

### Sequence
1. Caller does X
2. Component A does Y (throws Z on error)
3. Component B does W

### Data Shapes
- Input: `{ field: type, ... }`
- Output: `{ field: type, ... }`

### Test Coverage Plan
| Test Level | What to verify |
|------------|----------------|
| Unit | Individual function behavior |
| Integration | Component A ↔ Component B contract |
| Container | End-to-end flow through containers |
```

## Gherkin Requirements

Every story must have at least one `Given / When / Then` scenario before leaving TaskReview.

```gherkin
Feature: [story title]

  Scenario: [happy path]
    Given [precondition]
    When [action]
    Then [expected outcome]

  Scenario: [error path]
    Given [precondition]
    When [action that fails]
    Then [expected error behavior]
```

Gherkin goes in the story file under `## Acceptance Criteria`.

## TaskReview Checklist

- [ ] LLD written (interfaces, sequence, data shapes)
- [ ] Test coverage plan defined per V-Model level
- [ ] Gherkin scenarios cover happy path and key error paths
- [ ] No open questions blocking implementation
- [ ] CTO has committed the move to Implementation

## After TaskReview

Once CTO approves:
- Story moves to `Implementation`
- Agent reads the LLD as primary implementation spec
- HLD is background context; LLD is the contract

## See Also

- `HLD.md` — Feature design phase that precedes TaskReview
- `Implement.md` — Implementation phase that follows
- `Kanban.md` — Full column workflow
