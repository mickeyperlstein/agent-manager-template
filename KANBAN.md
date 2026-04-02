# Kanban

**SOT:** `tasks.csv` — run `template_workflow/scripts/folders_to_csv.py` to sync folders → CSV.
**Agents:** read CSV on startup, act on stories where `column = HLD`, `column = Task`, `column = TaskReview`, or `column = Test`.
**CTO gate:** only a human may commit a story from TaskReview → Implementation.

## HARD RULES — no exceptions

1. **Gates are not optional.** Every feature passes through every column in order. No skipping.
2. **No agent may suggest bypassing a gate.**
3. **No agent may move a feature forward** — with one exception: the HLD agent moves a completed HLD to `HLD-Review`. All other column moves are human commits only.
4. **"Fast-tracking" is a red flag.** Treat it as a process violation.

## Columns

| Column | Who Acts | Folder | File Structure |
|---|---|---|---|
| Backlog | Human | `Features/1-Backlog/` | `{feature}.md` |
| HLD | Agent (Architect) | `Features/2-HLD/` | `{feature}-HLD.md` |
| HLD-Review | Human | `Features/3-HLD-Review/` | `{feature}-HLD.md` |
| Task | Agent | `Features/4-Task/{feature}/` | `{feature}-HLD.md` + `{id}-{task}.md` files |
| TaskReview | Agent (Architect) + Human | `Features/5-TaskReview/{feature}/` | same folder, LLD added per task |
| Implementation | Agent | `Features/6-Implementation/{feature}/` | same folder |
| Test | Agent → Human if needed | `Features/7-Test/{feature}/` | same folder |
| Review | Human | `Features/8-Review/{feature}/` | same folder |
| Done | Human | `Features/9-Done/{feature}/` | same folder |

## Gates

| Gate | Owner | Required to Advance |
|------|-------|---------------------|
| `Backlog → HLD` | Human | Feature stub with clear scope |
| `HLD → HLD-Review` | **HLD agent** | HLD doc complete |
| `HLD-Review → Task` | Human | Human approves HLD |
| `Task → TaskReview` | Human | Tasks decomposed, files created |
| `TaskReview → Implementation` | Architect agent + Human | LLD + Gherkin per task; human commits move |
| `Implementation → Test` | Agent | Agent routes automatically |
| `Test → Review` | Human | Tests pass, human approves |
| `Review → Done` | Human | PR merged |

## Folder Lifecycle

A feature starts as a single file and grows into a folder as tasks are added:

```
1-Backlog/   {feature}.md
2-HLD/       {feature}-HLD.md
3-HLD-Review/{feature}-HLD.md
4-Task/      {feature}/
               {feature}-HLD.md
               0001-{task}.md
               0002-{task}.md
5-TaskReview/{feature}/        ← whole folder moves
6-Implementation/{feature}/   ← whole folder moves
7-Test/{feature}/              ← whole folder moves
8-Review/{feature}/            ← whole folder moves
9-Done/{feature}/              ← whole folder moves
```
