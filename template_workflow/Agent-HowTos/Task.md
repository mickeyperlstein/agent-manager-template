# Task

## What is the Task Column?

The **Task** column is where an agent adds LLD + Gherkin + TestPlan to task stubs created by the HLD agent. Each task file already contains: What, Scope, Acceptance Criteria, Test Conditions, and Definition of Done.

**Column:** `4-Task` — agent acts on individual task stub files here.

## Folder Structure

```
Features/4-Task/{epic}/{feature}/
  {feature}-HLD.md                          ← HLD reference, stays here
  {name}-{taskid}-{featureid}-{epicid}.md   ← task stub, agent adds LLD here
  {name}-{taskid}-{featureid}-{epicid}.md
```

## Task File Format

```markdown
---
id: a3f9c1
epic: 23a043
feature: e9245d
title: Task title
type: task
assignee: agent
review_gate: yes
approved: no
depends_on:
---

## What
What this task implements (one paragraph).

## Scope
- In: what is covered
- Out: what is not covered

## Acceptance Criteria
- [ ] Condition 1
- [ ] Condition 2

## Test Conditions
Black-box E2E scenarios. For each: identify every pipeline system affected and how to verify (log, DB query, queue, metric, etc.).
- Happy path: ... → log: ... / DB: ...
- Key error path: ... → log: ...

## Definition of Done
- [ ] LLD written
- [ ] Gherkin covers happy path and key error paths
- [ ] TestPlan written
- [ ] No open blockers

## LLD
(added by Task agent)

## Gherkin
(added by Task agent)

## TestPlan
(added by Task agent)
```

## Agent Responsibilities

1. Read `{feature}-HLD.md` for context
2. For each task stub: add LLD, Gherkin, and TestPlan sections
3. Move the task file to `Features/5-TaskReview/{epic}/{feature}/` when done
4. Do not move files that have unresolved `depends_on` — check those first

## After Task

Human reviews each task file in `5-TaskReview`. When satisfied, commits the move to `6-Implementation`.
