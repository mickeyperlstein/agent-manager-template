# TaskReview

## What is TaskReview?

**TaskReview** is the LLD review gate. Individual task files arrive here from `Task` (agent moves them after adding LLD + Gherkin + TestPlan). A human reviews each file and commits the move to Implementation.

## Who Acts Here

**Human** reviews each task file. No agent action required at this column — the work was done in Task.

**For non-technical reviewers:** focus on the plain-English summary in each task file — does the plan make sense? The LLD detail is there for completeness; you are not expected to read every line.

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

Human commits the move of the task file to `Features/6-Implementation/{epic}/{feature}/`. Agent reads LLD as the implementation contract. Each task file moves independently — no need to wait for all tasks to be reviewed before implementation starts on unblocked ones.
