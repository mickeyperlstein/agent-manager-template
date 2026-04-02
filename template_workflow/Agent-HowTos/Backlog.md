# Backlog

The Backlog holds **feature stubs only** — raw intent captured before any design has started.

**No stories here.** Stories are written *after* HLD is complete. A backlog entry is a feature, not a story.

## What Belongs in Backlog

- A feature idea with enough context to design it
- Rough scope and out-of-scope boundaries
- No architecture, no Gherkin, no implementation details

## Feature Stub Format

```
---
id: "0001"
title: Feature title
type: feature
status: backlog
assignee: architect
depends_on: none
review_gate: yes
---

## Feature

**What is asked:** one paragraph — what this feature does
**Why it's needed:** the problem it solves
**Scope:** what is in
**Out of Scope:** what is explicitly not in
```

## What is NOT in a Backlog Entry

- Acceptance criteria (written at TaskReview after LLD)
- Gherkin scenarios (written at TaskReview after LLD)
- Architecture decisions (written at HLD)
- Stories / tasks (written as output of HLD)

## After Backlog

A feature exits Backlog when:
- Intent is clear enough to design
- Human moves it to `HLD` column

The HLD phase is where the feature gets designed and stories are first decomposed.
