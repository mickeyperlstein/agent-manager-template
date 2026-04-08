# Kanban Housekeeping Protocol

When you read the Kanban board, **always run housekeeping first**. This ensures the board state is clean before you plan your work.

---

## Step 1 — Prune Empty Epic Folders

An epic folder is empty if it contains no `.md` files.

For every column `{column}` in `Features/1-Backlog` through `Features/9-Done`:
```bash
for epic in Features/{column}/*/ ; do
  rmdir "$epic" 2>/dev/null
done
```

**How it works:**
- `rmdir` succeeds (silently, `-2>/dev/null`) → folder was empty, it's removed ✓
- `rmdir` fails (output suppressed) → folder has files, it's left alone ✓

**Why:** Empty epic folders are cruft left behind when the last feature in an epic moved to a later stage.

---

## Step 2 — Detect and Fix Stragglers

A **straggler** is a feature stub or HLD file in an earlier stage, when evidence of later-stage work already exists (e.g., tasks have been broken down and moved to 4-Task).

### 2A — Find stragglers in 2-HLD and 3-HLD-Review

For each feature ID found in `Features/2-HLD/devops-bootstrap` or `Features/3-HLD-Review/devops-bootstrap`:
1. Extract the ID (e.g., `0013` from `0013-features-cli-core.md`)
2. Check if a folder exists: `Features/4-Task/devops-bootstrap/{id}-*/`
3. If yes → the feature has passed HLD-Review and moved to tasks. Move the feature files forward:

```bash
# Example: 0013-features-cli-core is in 2-HLD or 3-HLD-Review
# but 0013-features-cli-core/ folder exists in 4-Task
git mv Features/2-HLD/devops-bootstrap/0013-* Features/4-Task/devops-bootstrap/0013-*/
```

### 2B — Find completed HLDs (need to move to HLD-Review)

For each feature stub in `Features/2-HLD/devops-bootstrap`:
1. Extract the ID
2. Check if `{id}-HLD.md` exists in the same folder
3. If yes (completed HLD, not yet reviewed) → move both to `3-HLD-Review`:

```bash
# Example: 0012-meeting-stub-template.md + 0012-meeting-stub-template-HLD.md
# both exist in 2-HLD
git mv Features/2-HLD/devops-bootstrap/0012-* Features/3-HLD-Review/devops-bootstrap/
```

### 2C — Remove duplicate files

Check all columns for the same filename appearing in multiple stages:
```bash
# Example: 0015-meeting-workflow.md in both 2-HLD and 3-HLD-Review
git rm Features/2-HLD/devops-bootstrap/0015-meeting-workflow.md  # keep the later stage copy
```

---

## Step 3 — Report Summary

After running Steps 1–2, print a brief report:

```
✓ Kanban Housekeeping Complete

Pruned: [N] empty epic folders
Moved: [N] stragglers forward
  - {id} from {from-stage} → {to-stage}
Removed: [N] duplicate files

Board is clean. Proceeding to read Kanban state.
```

If no housekeeping was needed:
```
✓ Kanban Housekeeping Complete
(Board already clean — no stragglers, no empty folders)

Proceeding to read Kanban state.
```

---

## Important Notes

- **Git moves, not manual copies:** Always use `git mv` for file reorganization, never copy-paste
- **Idempotent:** If you run housekeeping twice in a row, the second run should find a clean board
- **Commits:** Do NOT commit housekeeping changes as you go. Report what would be moved, let the human confirm before committing (they may have intentional stragglers)
- **Test with `git status`** before committing to see all staged changes

---

## When to Run

Run this protocol:
- **Every startup** as part of the startup protocol (Step 1a)
- **Manually** via `/housekeeping` command when the human asks for a board cleanup
- **Before reading the task board** to ensure you're seeing clean state
