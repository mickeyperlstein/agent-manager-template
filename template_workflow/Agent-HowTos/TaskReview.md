# TaskReview

## What is TaskReview?

**TaskReview** is the LLD gate. Task files arrive here from `Task` (after human moves them) and leave with LLD + Gherkin added to each task file. A human then approves before Implementation.

## Who Acts Here

**Architect agent** writes the LLD and Gherkin for each task. **Human** reviews and commits the move to Implementation.

## What is an LLD?

A task-level spec at C4 Level 3 (Component):
- Interface contracts (function signatures, API shapes)
- Sequence diagrams (call order, error paths)
- Data shapes (input/output types, validation)
- Test coverage plan (unit / integration / container)

## Add LLD to Each Task File

```markdown
## LLD

### Interfaces
\`\`\`typescript
// signatures or API contracts
\`\`\`

### Sequence
1. Step one
2. Step two (throws X on error)

### Data Shapes
- Input: `{ field: type }`
- Output: `{ field: type }`

### E2E Test Plan
Which E2E scenarios cover this task? (lean — only what's needed for regression protection)

## Acceptance Criteria

\`\`\`gherkin
Scenario: happy path
  Given ...
  When ...
  Then ...

Scenario: error path
  Given ...
  When ...
  Then ...
\`\`\`
```

## TaskReview Checklist

- [ ] LLD written for every task file
- [ ] Gherkin covers happy path and key error paths
- [ ] No open questions blocking implementation
- [ ] Human has committed the move to Implementation

## After TaskReview

Human moves the folder to `6-Implementation`. Agent reads LLD as the implementation contract.
