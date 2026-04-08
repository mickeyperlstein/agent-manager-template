# Kanban Housekeeping Protocol

When you read the Kanban board, **always run housekeeping first**. This ensures the board state is clean before you plan your work.

---

## Step 1 — Rebuild task state from folder structure

Scan Features/ and regenerate tasks.csv from current state:

```bash
./template_workflow/scripts/folders_to_csv.py
```

This reads all `.md` files, extracts frontmatter, and rebuilds the authoritative task inventory.

---

## Step 2 — Detect stragglers via dry-run

See what file moves would happen if the CSV and folders diverged:

```bash
./template_workflow/scripts/csv_to_folders.py --dry-run
```

If the output is empty, the board is clean. If files are listed as "Would move", you have stragglers.

---

## Step 3 — Prune empty epic folders

An epic folder is empty if it contains no `.md` files. Remove them:

```bash
for col in Features/*/; do
  for epic in "$col"*/; do
    rmdir "$epic" 2>/dev/null
  done
done
```

**How it works:**
- `rmdir` succeeds → folder was empty, it's removed ✓
- `rmdir` fails → folder has files, it's left alone ✓

---

## Step 4 — Fix stragglers (if any)

If Step 2 showed moves:

1. **Edit tasks.csv** — change the `column` value for stragglers to their correct stage
2. **Apply the fixes:**
   ```bash
   ./template_workflow/scripts/csv_to_folders.py
   ```
   This reads the corrected CSV and moves files via `git mv` to match.

3. **Verify** — check `git status` to see the moves, then ask the human to confirm before committing.

---

## Step 5 — Report

Print a summary:

```
✓ Kanban Housekeeping Complete

Task inventory rebuilt from Features/
[N] empty folders pruned
[N] stragglers fixed via git mv

Board is clean. Proceeding to read Kanban state.
```

Or if clean:
```
✓ Kanban Housekeeping Complete
(Board already clean — no stragglers, no empty folders)

Proceeding to read Kanban state.
```

---

## Important Notes

- **Scripts are authoritative:** folders_to_csv.py and csv_to_folders.py use shared column map from `kanban.py`
- **Dry-run first:** Always check what would move with `--dry-run` before applying changes
- **Don't commit:** Report the moves and let the human confirm before you commit
- **Idempotent:** Running housekeeping twice in a row should find a clean board the second time

---

## When to Run

Run this protocol:
- **Every startup** as part of the startup protocol (Step 1a)
- **Manually** via `/housekeeping` command when the human asks for a board cleanup
- **Before reading the task board** to ensure you're seeing clean, accurate state
