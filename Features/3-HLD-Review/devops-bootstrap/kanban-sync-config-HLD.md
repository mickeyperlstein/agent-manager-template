---
id: 0018
type: feature
status: HLD-Review
review_gate: yes
---

# HLD: CSV/Folder Sync Authority Config

## 1. Problem Statement

The Kanban board has a critical data loss hazard:
- Source of Truth (SOT) is ambiguous: both `tasks.csv` and `Features/` folder structure exist
- Sync scripts run bidirectionally without authority validation
- Operators don't know which direction is safe to sync
- Common failure mode: edit CSV → run `folders_to_csv.py` → lose CSV changes (overwritten by folder state)

**Impact:** Data loss, confusion about board state, accidental destruction of work-in-progress.

---

## 2. Goals

- Single, explicit, configurable source of truth (CSV or Folders)
- Sync scripts validate authority before running destructive operations
- Agents and humans see which direction is authoritative in every interaction
- Default to CSV as SOT (matches "Source of Truth: tasks.csv" documented in Kanban.md)
- Prevent bidirectional sync operations that can cause data loss

---

## 3. Architecture

### Authority Model

**Authority** is a single source of truth, configurable per environment:
- `SOT=csv` — CSV is authoritative, folders are derived. `folders_to_csv.py` is forbidden; only `csv_to_folders.py` is safe.
- `SOT=folders` — Folders are authoritative, CSV is derived. `csv_to_folders.py` is forbidden; only `folders_to_csv.py` is safe.

Default: `SOT=csv` (matches existing Kanban.md statement "Source of Truth: tasks.csv")

### Config Location

**In `template_workflow/config.json`** (or environment):
```json
{
  "kanban": {
    "source_of_truth": "folders"  // or "csv"
  }
}
```

Rationale: `template_workflow/` is already the location for template settings/hooks; keeps all harness config in one place.

### Sync Script Validation

Both sync scripts check authority before running:

**`folders_to_csv.py`:**
- Reads `SOT` from config
- If `SOT=csv`, exits with error: "Authority is CSV. Rebuild from folders is forbidden. Use `csv_to_folders.py` instead."
- If `SOT=folders`, proceeds (allowed)

**`csv_to_folders.py`:**
- Reads `SOT` from config
- If `SOT=folders`, exits with error: "Authority is Folders. Sync from CSV is forbidden. Use `folders_to_csv.py` instead."
- If `SOT=csv`, proceeds (allowed)

### Data Flow

```
CSV (SOT=csv)
  ↓ (csv_to_folders.py allowed)
  Features/ folders (derived, read-only)

Features/ (SOT=folders)
  ↓ (folders_to_csv.py allowed)
  CSV (derived, read-only)
```

### Housekeeping Protocol Update

The housekeeping protocol currently runs `folders_to_csv.py` in Step 1. With authority config:
- If `SOT=csv`: skip Step 1 (CSV is authoritative, don't overwrite it)
- If `SOT=folders`: run Step 1 as before

This prevents accidental data loss during routine maintenance.

---

## 4. Alternatives Considered

**A. No config, always default to folders as SOT**
- ✓ Simpler (no moving parts)
- ✗ Inflexible; teams working in folders will make that the source
- ✗ Config exists in code comments, easy to forget

**B. Detect SOT automatically (check which is newer)**
- ✗ Fragile; doesn't survive across machines/branches
- ✗ Ambiguous after a merge
- ✗ Doesn't prevent mistakes, only detects them

**C. Interactive prompts ("Which is your SOT?") at runtime**
- ✗ Adds friction to every sync operation
- ✗ Risk of typos causing data loss
- ✗ Out of scope for this feature

**Chosen: A + config option** — Explicit, configurable, defaults to CSV (current documented practice).

---

## 5. Logging, Monitoring & Metrics

### Logs

When sync scripts run:
- ✓ Log which SOT is active: `Kanban SOT is 'csv' — csv_to_folders.py allowed`
- ✓ Log when a script is forbidden: `ERROR: Kanban SOT is 'folders', folders_to_csv.py forbidden`
- ✓ Log number of files synced: `Synced 12 files from CSV to Features/ (csv → folders)`

### Metrics

- Counter: `kanban.sync.attempts` (tagged by direction: csv→folders, folders→csv, forbidden)
- Counter: `kanban.sync.errors` (tagged by error reason: wrong_authority, missing_file, etc.)

### E2E Observability Contract

In tests:
- Verify SOT config is respected (forbidden direction fails, allowed direction succeeds)
- Verify log entries match expected format
- Verify no data loss after sync operations

---

## 6. Documentation

### Updates to template_workflow/Agent-HowTos/Kanban.md

Add to top of document:
```markdown
**Authority:** `tasks.csv` is the default source of truth (SOT). 
Configure in `.claude/config.json` with `"sot": "csv"` or `"sot": "folders"`.
Sync scripts will reject operations that violate this authority.
```

### Updates to template_workflow/commands/housekeeping-protocol.md

Step 1 (Rebuild task state):
```markdown
If SOT is CSV (default), skip this step — CSV is authoritative.
If SOT is Folders, run folders_to_csv.py to rebuild CSV from current state.
```

### Updates to CLAUDE.md / agent-manager-claude.md

Add:
```markdown
**Kanban Authority:** Source of truth is configured in `.claude/config.json` → `kanban.sot`.
Default is `csv`. If you're confused about sync direction, check this config.
```

---

## 7. Open Questions

- Should we add a `/sot` command to switch authority? (Deferred to follow-up feature)
- Should we log to a specific Kanban event log vs. stdout? (Use project log convention)
- Should Authority be per-project or global? (Per-project in `.claude/config.json`)

---

## 8. Task Decomposition

| Task | What | Assignee |
|------|------|----------|
| config-setup | Create `.claude/config.json` with default `sot: csv` | agent |
| folders-to-csv-validation | Add SOT check to `folders_to_csv.py`; reject if `sot=csv` | agent |
| csv-to-folders-validation | Add SOT check to `csv_to_folders.py`; reject if `sot=folders` | agent |
| housekeeping-update | Update housekeeping protocol to check SOT in Step 1 | agent |
| docs-update | Update Kanban.md, housekeeping protocol, CLAUDE.md | agent |

---

## Task Stubs

The following tasks will be created in `Features/4-Task/devops-bootstrap/0018-kanban-sync-config/`:

- [ ] config-setup-{taskid}-0018-devops-bootstrap.md
- [ ] folders-to-csv-validation-{taskid}-0018-devops-bootstrap.md
- [ ] csv-to-folders-validation-{taskid}-0018-devops-bootstrap.md
- [ ] housekeeping-update-{taskid}-0018-devops-bootstrap.md
- [ ] docs-update-{taskid}-0018-devops-bootstrap.md

---

# Review 2026-04-11

## Participants
- Presenter: Architect
- Reviewers: architect-reviewer, PM, Mickey (human)

## Questions & Answers
- Q (Mickey): Why not run both scripts non-destructively and keep dual states in sync?
- A (Presenter): Authority model is simpler and provides operational clarity. Avoids merge/reconcile complexity.
- Q (ARCH-R): What happens to the Features/ folder state during reconciliation if CSV is SOT?
- A (Presenter): Folders get overwritten, not deleted. Should clarify operator expectations in task docs.
- Q (PM): Are operators actively losing data today, or is this a theoretical hazard?
- A (Presenter): HLD identifies risk but doesn't cite real incidents; actual observed issue is orphan folders.

## Rolling Summary
- Problem framed as "critical data loss hazard," but actual observed issue is orphan folders, not data loss
- Full authority-config solution may be over-scoped for the current pain point
- Architecture is sound, but scope should be reconsidered to match real problem

## Decisions
- Outcome: Deferred — Not Accepted as-is
- Actual pain point is orphan folders; revise HLD to scope for that rather than general authority model
- Kanban movement: 3-HLD-Review → 2-HLD
- Rescope when orphan cleanup requirements are clearer

---

## Comments

**2026-04-09 — architect (HLD):** Designed authority-based sync system to prevent data loss. Default SOT is CSV (matches existing Kanban.md doctrine). Sync scripts will validate and reject operations that violate authority. Documentation updates ensure agents know the policy.

**2026-04-11 — review (deferral):** Reviewed against observed problem (orphan folders vs. theoretical data loss). Full authority config may over-scope. Defer to 2-HLD for rescoping focused on orphan cleanup.
