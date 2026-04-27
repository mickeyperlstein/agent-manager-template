# Column: TaskReview (5-TaskReview)

**What:** LLD review gate. Human reviews task files and commits move to Implementation.

**When to work here:** Human reviews each task file that arrives from Task column.

**Agent role:** None — the work was done in Task column. Files auto-move here by agent after LLD/Gherkin/TestPlan added.

---

## What is an LLD?

A task-level spec at C4 Level 3 (Component):
- Interface contracts (function signatures, API shapes)
- Sequence diagrams (call order, error paths)
- Data shapes (input/output types, validation)
- Test coverage plan (unit / integration / container)

---

## LLD Template

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

---

## TaskReview Checklist

- [ ] LLD written for every task file
- [ ] Gherkin covers happy path and key error paths
- [ ] No open questions blocking implementation
- [ ] Human has committed the move to Implementation

---

## For Non-Technical Reviewers

Focus on the plain-English summary in each task file — does the plan make sense? The LLD detail is there for completeness; you are not expected to read every line.

---

## After TaskReview

Human commits the move of the task file to `Features/6-Implementation/{epic}/{feature}/`. Agent reads LLD as the implementation contract. Each task file moves independently — no need to wait for all tasks to be reviewed before implementation starts on unblocked ones.
