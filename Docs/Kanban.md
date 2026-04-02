# Kanban — Column Reference

## Column Types

**Manual** (human moves the story) vs **Agent** (agent acts on it automatically)

| Column | Who Acts | Purpose |
|---|---|---|
| `Backlog` | Human | Raw ideas — no spec yet |
| `HLD` | Human | Spec + architecture written, ready to be reviewed |
| `TaskReview` | Human | Architect has signed off, CTO decides if it enters work |
| `InProgress` | Agent | Agent is actively building this |
| `Testing-Agent` | Agent | Agent runs automated tests |
| `Testing-Manual` | Human | Human QA — agent can't automate it |
| `Verified` | Human | Tests passed, human approved |
| `Review` | Human | PR is open, awaiting code review |
| `Done` | Human | PR merged, feature complete |

## Gate Owners

Each column transition has a distinct owner:

- `Backlog → HLD` — the *spec writer* gate (do we have enough info?)
- `HLD → TaskReview` — the *architect* gate (is the design sound?)
- `TaskReview → InProgress` — the *CTO* gate (is this prioritized?)
- `InProgress → Testing-*` — the *agent* routes this (auto vs manual test)
- `Testing-* → Verified` — the *QA* gate (does it actually work?)
- `Verified → Review` — the *PR* gate (is the code reviewable?)
- `Review → Done` — the *merge* gate

## Why Testing-Agent vs Testing-Manual?

The split ensures agents never halt. If tests can't be automated, the agent routes to `Testing-Manual` and keeps moving rather than blocking on automation it can't do.

## Folder Structure

```
Features/
  1-Backlog/
  2-HLD/
  3-TaskReview/
  4-InProgress/
  5-Testing-Agent/
  6-Testing-Manual/
  7-Verified/
  8-Review/
  9-Done/
```

Each story lives as a file (or subfolder) in its current column's folder. Moving a story = moving the file. Column moves are human commits only — agents never move stories.
