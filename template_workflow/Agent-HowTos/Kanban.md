# Kanban Workflow for Agents

**Source of Truth:** `tasks.csv` — run `template_workflow/scripts/folders_to_csv.py` to sync folders → CSV.

**Your Role:** Act on stories where `column = HLD`, `column = Task`, `column = TaskReview`, or `column = Test`.

**Gate:** Only a human may commit a task from TaskReview → Implementation.

---

## ⛔ HARD RULES — No Exceptions

1. **Gates are not optional.** Every feature passes through every column in order. No skipping.
2. **No agent may suggest bypassing a gate.**
3. **No agent may move a feature forward** — with one exception: the HLD agent moves a completed HLD to `HLD-Review`. All other column moves are human commits only.
4. **"Fast-tracking" is a red flag.** Treat it as a process violation.

---

## Summary

| Column | Who Acts | Folder | File Structure |
|---|---|---|---|
| Backlog | Human | `Features/1-Backlog/` | `{feature}.md` |
| HLD | Agent (Architect) | `Features/2-HLD/` | `{feature}-HLD.md` |
| HLD-Review | Human | `Features/3-HLD-Review/` | `{feature}-HLD.md` |
| Task | Agent | `Features/4-Task/{epic}/{feature}/` | `{feature}-HLD.md` + `{name}-{taskid}-{featureid}-{epicid}.md` files |
| TaskReview | Agent (Architect) + Human | `Features/5-TaskReview/{epic}/{feature}/` | individual task files move here as completed |
| Implementation | Agent | `Features/6-Implementation/{epic}/{feature}/` | individual task files move here after review |
| Test | Agent → Human if needed | `Features/7-Test/{epic}/{feature}/` | individual task files move here |
| Review | Human | `Features/8-Review/{epic}/{feature}/` | individual task files move here |
| Done | Human | `Features/9-Done/{epic}/{feature}/` | individual task files move here |

## Gates (Column Transitions)

| Gate | Owner | Required to Advance |
|------|-------|---------------------|
| `Backlog → HLD` | Human | Feature stub with clear scope |
| `HLD → HLD-Review` | **HLD agent** | HLD doc complete |
| `HLD-Review → Task` | Human | Human approves HLD |
| `Task → TaskReview` | Agent | Per task file: agent adds LLD + Gherkin + TestPlan, moves file to TaskReview |
| `TaskReview → Implementation` | **Human** | Per task file: human reviews LLD + Gherkin + TestPlan, commits move |
| `Implementation → Test` | Agent | Agent routes automatically |
| `Test → Review` | Human | Tests pass, human approves |
| `Review → Done` | Human | PR merged |

## Filename Convention

Task files (and all items from Task column onwards) use:
```
{name}-{taskid}-{featureid}-{epicid}.md
```
- `name` — human-readable slug (shown first for readability in file explorer)
- `taskid`, `featureid`, `epicid` — 3-byte hex, generated at creation, collision-free across agents and branches

Example: `folders-to-csv-385474-e9245d-23a043.md`

## Folder Lifecycle

Files move individually from Task onwards. `depends_on` controls ordering between tasks.

```
1-Backlog/   {feature}.md
2-HLD/       {feature}-HLD.md
3-HLD-Review/{feature}-HLD.md
4-Task/      {epic}/{feature}/
               {feature}-HLD.md          ← reference, stays here
               {name}-{tid}-{fid}-{eid}.md
               {name}-{tid}-{fid}-{eid}.md

5-TaskReview/{epic}/{feature}/           ← individual files move here as agent completes them
6-Implementation/{epic}/{feature}/       ← individual files move here after human review
7-Test/{epic}/{feature}/
8-Review/{epic}/{feature}/
9-Done/{epic}/{feature}/
```

## V-Model Alignment

### Test Philosophy

A lean E2E suite (~30 well-chosen scenarios) beats a test pyramid. Tests exist to catch regressions — not to satisfy coverage metrics. Unit tests only where logic is genuinely complex and isolated.

### V-Model Documents → Kanban Artifacts

| V-Model Document | Kanban Equivalent | Where |
|---|---|---|
| Test Plan | Quality policy + workflow rules | `template_workflow/Agent-HowTos/Kanban.md`, `CLAUDE.md` |
| Test Design Spec | Acceptance criteria + test conditions | Task column (task files) |
| Test Case Spec | Gherkin scenarios + LLD test plan | TaskReview (task files) |
| Test Procedure | Board workflow + quality gates | `template_workflow/Agent-HowTos/Kanban.md` gates |
| Test Suite | Automated test suites | Test column |
| RTM | Task id → feature HLD link | task file `feature` field |
| Test Execution Report | Kanban metrics (cycle time, CFD) | tasks.csv |
| Test Summary Report | Retrospectives / flow reviews | meetings/ |
