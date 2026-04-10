# Start Task

Usage: `/start` or `/start <task-id>`

---

## Protocol

### Step 0 — Housekeeping

Before reading the Kanban board, run `/housekeeping` to ensure the board is clean:
- Prune empty epic folders
- Move any stragglers to their correct stages
- Report what was cleaned

This ensures you're reading accurate board state.

### Step 1 — Orient

Read in this order (stop and report if any file is missing):
1. `template_workflow/Agent-HowTos/Kanban.md` — columns, gates, rules
2. `tasks.csv` — find your work

### Step 2 — Find the task

**If `<task-id>` was given:**
- Find the row in `tasks.csv` where `id = <task-id>`
- Locate the task file in `Features/` — filename format is `{name}-{taskid}-{featureid}-{epicid}.md`

**If no id given:**
- Filter `tasks.csv` for rows where `column` matches your role's active column (Task, Implementation, Test)
- Among those, find rows where all `depends_on` ids have `column = Done`
- Pick the first unblocked task

If no unblocked task is found: stop and tell the human exactly why (what is blocking).

### Step 3 — Read the task file

Read the full task file. Note:
- `title` and `type`
- `epic` and `feature` (for context)
- `depends_on` (verify all are done)
- `review_gate` (if `yes`, human must approve before you move forward)
- Acceptance criteria, scope, definition of done

Also read the feature HLD if present in the same folder.

### Step 4 — Confirm before acting

Output a confirmation block — do NOT begin work yet:

```
Task: <title> (<id>)
Column: <column>
Epic: <epic> / Feature: <feature>
Depends on: <ids or "none">

I will:
<1-3 sentence plain-English description of what you are about to do>

Scope:
- In: <what you will touch>
- Out: <what you will not touch>

Shall I proceed?
```

Wait for the human to say yes before doing anything.

### Step 5 — Work

On confirmation, follow the HowTo for your column:
- `Task` column → `template_workflow/Agent-HowTos/Task.md`
- `TaskReview` column → `template_workflow/Agent-HowTos/TaskReview.md`
- `Implementation` column → `template_workflow/Agent-HowTos/Implement.md`
- `Test` column → `template_workflow/Agent-HowTos/Test.md`

Update the frontmatter of the file you are working on with the current column status.

### Step 6 — Done

When finished:
- Append a dated comment to every file you modified
- Note where the file should move to next
- Do not move files or folders — that is a human commit
- Report what you did and what the human needs to do next
- Update the frontmatter status: if you did not move the file, set state to `{state}-verify`
