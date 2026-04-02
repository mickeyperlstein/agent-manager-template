# Task

## What is the Task Column?

The **Task** column is where individual task files are created from the HLD decomposition. Each task file must include acceptance criteria, test conditions, and a definition of done — not just scope. This is where the V-Model test design begins.

**Column:** `4-Task` — agent acts when a feature folder arrives here (after human approves HLD).

## Folder Structure

```
Features/4-Task/
  {feature}/
    {feature}-HLD.md          ← HLD as reference (sibling)
    0001-{task-name}.md
    0002-{task-name}.md
```

## Task File Format

```markdown
---
id: "0001"
feature: {feature}
title: Task title
status: task
assignee: architect
review_gate: yes
---

## What
What this task implements (one paragraph).

## Scope
What is explicitly in and out of scope for this task.

## Depends On
List other task ids this task depends on, or "none".

## Acceptance Criteria
Conditions that must be true for this task to be considered done:
- [ ] Condition 1
- [ ] Condition 2
- [ ] Condition 3

## Test Conditions
Black-box E2E scenarios. For each condition, identify every pipeline system the code affects and how you will verify it directly (log, DB query, queue message, cache read, metric in dashboard, etc.).
- Happy path: ... → log: ... / DB: ... / queue: ...
- Key error path: ... → log: ...
- Critical edge case (if any): ...

List all pipeline systems this task writes to or affects: (DB / queue / cache / storage / metrics / ...)

## Definition of Done
- [ ] Code reviewed
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Acceptance criteria verified
- [ ] No open blockers
```

## V-Model Artifacts Produced Here

| V-Model Document | Task Column Equivalent |
|---|---|
| Test Design Spec | Acceptance criteria + test conditions |
| Test Case Spec (draft) | Test conditions list (formalized to Gherkin at TaskReview) |
| RTM entry | Task id linked to feature HLD |

Formal Gherkin and LLD (Test Case Spec finalized) are written at TaskReview. The test conditions here are the input to that process.

## Agent Responsibilities

1. Read `{feature}-HLD.md` → `## Task Decomposition`
2. Create one `.md` file per task
3. For each task: fill in What, Scope, Acceptance Criteria, Test Conditions, Definition of Done
4. Do not write LLD or formal Gherkin yet — that is TaskReview's job

## After Task

Human reviews task list and test conditions, then moves the folder to `5-TaskReview`.
