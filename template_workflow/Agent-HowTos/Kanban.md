# Kanban — Column Reference

See `KANBAN.md` at the repo root for the authoritative column list, gate owners, and folder structure rules.

## Summary

| Column | Who Acts | Purpose |
|---|---|---|
| `Backlog` | Human | Feature stub — raw intent |
| `HLD` | Agent (Architect) | Writes HLD; **agent moves to HLD-Review when done** |
| `HLD-Review` | Human | Reviews and approves HLD |
| `Task` | Agent | Creates task files from HLD decomposition |
| `TaskReview` | Agent (Architect) + Human | Writes LLD + Gherkin per task; human approves |
| `Implementation` | Agent | Builds from LLD |
| `Test` | Agent → Human if needed | Runs tests; routes to Review or back |
| `Review` | Human | PR open, code review, merge |
| `Done` | Human | Complete |

## Folder Convention

```
1-Backlog/   {feature}.md
2-HLD/       {feature}-HLD.md
3-HLD-Review/{feature}-HLD.md
4-Task/      {feature}/
               {feature}-HLD.md    ← HLD travels with tasks
               0001-{task}.md
               0002-{task}.md
5-TaskReview/{feature}/            ← whole folder moves from here
6-Implementation/{feature}/
7-Test/{feature}/
8-Review/{feature}/
9-Done/{feature}/
```

## V-Model Alignment

### Test Philosophy

A lean E2E suite (~30 well-chosen scenarios) beats a test pyramid. Tests exist to catch regressions — not to satisfy coverage metrics. Unit tests only where logic is genuinely complex and isolated.

### V-Model Documents → Kanban Artifacts

| V-Model Document | Kanban Equivalent | Where |
|---|---|---|
| Test Plan | Quality policy + workflow rules | `KANBAN.md`, `CLAUDE.md` |
| Test Design Spec | Acceptance criteria + test conditions | Task column (task files) |
| Test Case Spec | Gherkin scenarios + LLD test plan | TaskReview (task files) |
| Test Procedure | Board workflow + quality gates | `KANBAN.md` gates |
| Test Suite | Automated test suites | Test column |
| RTM | Task id → feature HLD link | task file `feature` field |
| Test Execution Report | Kanban metrics (cycle time, CFD) | tasks.csv |
| Test Summary Report | Retrospectives / flow reviews | meetings/ |

**Only the HLD agent may move a story. All other column moves are human commits only.**
