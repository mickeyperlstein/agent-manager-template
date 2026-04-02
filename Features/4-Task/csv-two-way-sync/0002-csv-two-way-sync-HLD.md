# High Level Design: CSV Two-Way Sync with Folder Structure

**Epic:** devops-bootstrap  
**Feature:** csv-two-way-sync

**Status:** HLD-Review  
**Author:** Agent  
**Date:** 2026-04-02  

---

## 1. Problem Statement

The team needs a single source of truth for Kanban state that:
- Lives at repo root as `tasks.csv` for easy import to Google Sheets/GitHub Projects
- Stays in sync with `Features/` folder structure (folders drive CSV, CSV drives file moves)
- Supports bidirectional editing: edit CSV → folders update, move files → CSV updates

---

## 2. Goals

1. **Authoritative Source**: Folder structure is canonical; CSV is a derived view
2. **Bidirectional Sync**: Changes in either direction propagate correctly
3. **Idempotent**: Running sync twice produces no changes on second run
4. **Atomic Commits**: CSV changes and folder moves happen in a single commit
5. **Auto-Progression**: Items advance columns automatically when `approved=yes` and `review_required=no`

---

## 3. Proposed Architecture

### 3.1 Data Model

**CSV Schema:**
```
id,state,epic,name,assignee,type,review_required,approved,depends_on
```

**Example Row:**
```
a3f9c1,2-HLD,devops-bootstrap,Implement CSV sync,Agent,feature,yes,no,
```
in the shared library of python, make sure the csv order is simple to change.

both scripts need to be based on a shared module that includes the schema so a change in the schema doesnt break anything

| Field | Source | Description |
|-------|--------|-------------|
| `id` | frontmatter | Short hex ID (e.g. `a3f9c1`) — generated at item creation, unique across agents and branches, no coordination required |
| `epic` | folder path | Epic name |
| `name` | filename | Item name — works for features and tasks alike |
| `assignee` | frontmatter | Owner |
| `state` | folder path | Kanban column — derived from `Features/{n}-{Kanban}/`. This IS the lifecycle state; no separate state field needed |
| `type` | frontmatter | `feature` / `bug` / `task` |
| `review_required` | frontmatter | `yes` / `no` — if `yes`, auto-progression is blocked until human clears it |
| `approved` | frontmatter | `yes` / `no` — `yes` triggers auto-progression to next column (only if `review_required=no`) |
| `depends_on` | frontmatter | comma-separated hex ids this item depends on; empty = no dependencies |

**Folder Structure:**
```
Features/
  1-Backlog/
    {feature}.md
  2-HLD/
    {feature}-HLD.md
  3-HLD-Review/
    {feature}-HLD.md
  4-Task/
    {feature}/
      {feature}-HLD.md
      {name}-task.md
      {name}-task.md
  5-TaskReview/
    {feature}/          ← whole folder moves from here
  6-Implementation/
    {feature}/
  7-Test/
    {feature}/
  8-Review/
    {feature}/
  9-Done/
    {feature}/
  10-Canceled/
    {feature}/          ← deleted/canceled items archived here
```

### 3.2 Components

#### Component A: Folders → CSV (`folders_to_csv.py`)

**WHAT:** Scans Features/ tree, extracts metadata, generates tasks.csv  
**WHY:** CSV is derived view; must reflect actual folder state  
**HOW:**
1. Walk each state folder (1-Backlog through 10-Canceled)
2. For each .md file: parse frontmatter, derive `name` and `state` from path, map to CSV row
3. Write CSV sorted by id -- add args to specify csv order

**Key Design Decisions:**
- `state` is always derived from the folder — never read from frontmatter
- Item name is derived from filename — frontmatter is informational only

#### Component B: CSV → Folders (`csv_to_folders.py`)

**WHAT:** Reads tasks.csv, moves files/folders to correct Kanban column  
**WHY:** Editing CSV should drive folder reorganization  
**HOW:**
1. Read CSV rows
2. For each item: fast-path lookup by expected path, fallback rglob
3. Determine target column (with auto-progression if `approved=yes` and `review_gate=no`)
4. Move file or folder if needed

**Path Lookup Strategy:**
```
# Fast path: item is where CSV says it is
expected = Features/{n}-{state}/{name}*

# Fallback: search all columns (handles desync)
rglob Features/ for id match
```
`{n}-{state}` = the state folder (e.g. `1-Backlog`, `4-Task`)

**Auto-Progression:**
```
Backlog → HLD → HLD-Review → Task → TaskReview → Implementation → Test → Review → Done
```
If `approved=yes` AND `review_gate=no`, item advances to next column automatically.

#### Component C: shared module

schema order

### 3.3 Workflow

```gherkin
Feature: Folder move updates CSV

  Scenario: Move file in terminal
    Given a feature file exists in Features/1-Backlog/
    When the user runs git mv to Features/2-HLD/ and commits
    And runs folders_to_csv.py
    Then tasks.csv reflects column = HLD for that item
    And the log contains info: "file moved" with from/to fields

  Scenario: Edit CSV column drives folder move
    Given tasks.csv has an item with column = Backlog
    When the user changes column to HLD in CSV
    And runs csv_to_folders.py
    Then the file is moved to Features/2-HLD/
    And the log contains info: "file moved" with from/to fields

  Scenario: Auto-progression
    Given an item has approved = yes and review_gate = no
    When the user runs folders_to_csv.py then csv_to_folders.py
    Then the item moves to the next column automatically
    And the log contains info: "auto-progression applied" with from_column and to_column
```

---

## 4. Setup Integration

`setup.sh` must call `folders_to_csv.py` as its final step to generate the initial `tasks.csv`:

```bash
python3 template_workflow/scripts/folders_to_csv.py
```

---

## 5. Pre-Commit Hook

Mandatory. Runs on every commit.

```bash
#!/bin/sh
# .git/hooks/pre-commit
python3 template_workflow/scripts/folders_to_csv.py
python3 template_workflow/scripts/csv_to_folders.py
git add tasks.csv Features/
```

---

## 6. Logging, Monitoring & Metrics

Logging is the trace mechanism. Every log entry must answer a question someone would ask during an incident. No noise logs.

**Log level convention:**
- `debug` — function entry/exit via wrappers only (never manual)
- `info` — operational events for DevOps/IT (sync started, N files moved, CSV written)
- `warn` — recoverable issues (file not found at expected path, fallback to rglob)
- `error` — failures + exceptions (collision at target, corrupt frontmatter, permission denied)

**Key log events:**

| Event | Level | Fields |
|-------|-------|--------|
| Sync started | info | script, direction, item_count |
| File moved | info | from, to, item_id |
| Fallback rglob triggered | warn | item_id, expected_path |
| Collision at target | error | item_id, target_path |
| Auto-progression applied | info | item_id, from_column, to_column |
| Sync complete | info | files_moved, duration_ms |

**E2E observability contract:** A passing test reads the log and confirms expected entries appear with correct fields. No assertion on internal state.

---

## 7. Configuration (Future)

Sheets and GitHub Projects integration requires auth. Auth mechanism (OAuth token / service account / PAT) is out of scope for this HLD — defined per target in a future auth spec.

```json
{
  "version": "1.0.0",
  "targets": {
    "folders": true,
    "sheets": { "enabled": true, "spreadsheet_id": "..." },
    "gh-projects": { "enabled": false, "project_number": 1 }
  }
}
```

---

## 8. Idempotency Guarantee

Running sync twice produces no changes on second run.

- `folders_to_csv.py`: Always regenerates CSV from scratch
- `csv_to_folders.py`: Only moves if `current_column != target_column`

---

## 9. Error Handling

| Error | Level | Handling |
|-------|-------|----------|
| Item in CSV but file not found | error | Log + skip |
| File exists at target (collision) | error | Log + skip |
| Unknown column in CSV | error | Log + skip |
| Missing id in file metadata | warn | Skip file silently |
| Invalid `approved` value (not yes/no) | warn | Treat as `no` |

---

## 10. Testing Strategy

Black-box E2E only. Tests verify behavior through observable outputs — log entries and filesystem state. No mocking of internals.

```gherkin
Feature: Sync idempotency

  Scenario: Running sync twice produces no changes
    Given the folder structure and CSV are in sync
    When folders_to_csv.py runs twice
    Then the log contains info: "0 files moved" on the second run

Feature: Auto-progression gate

  Scenario: Auto-progression blocked by review_gate
    Given an item has approved = yes and review_gate = yes
    When csv_to_folders.py runs
    Then the item does not move
    And no auto-progression log entry is written

  Scenario: Collision is logged and skipped
    Given a file already exists at the target column path
    When csv_to_folders.py attempts to move an item there
    Then the file is not moved
    And the log contains error: "collision at target" with item_id and target_path

  Scenario: Fallback rglob when file not at expected path
    Given an item's file is not at the expected path
    When csv_to_folders.py runs
    Then the log contains warn: "fallback rglob triggered"
    And the file is found and moved to the correct column
```

---

## 11. Decisions (from Open Questions)

1. **Auto-progression requires `review_gate=no`** — `approved=yes` alone is not sufficient
2. **No `--force` flag** — idempotency is not overridable
3. **Canceled items** — move to `Features/10-Canceled/`; not deleted, not in active columns
4. **Pre-commit hook is mandatory** — not optional

---

## 12. Task Decomposition

`folders_to_csv.py` and `csv_to_folders.py` already exist at `template_workflow/scripts/`. Tasks are reviews and updates against this HLD:

- [ ] 0013-folders-to-csv: review existing script — verify column derivation, `name` field, logging spec, 10-Canceled support
- [ ] 0014-csv-to-folders: review existing script — verify auto-progression gate (`review_gate=no` required), column names, logging spec
- [ ] 0015-pre-commit-hook: implement mandatory pre-commit hook
- [ ] 0016-e2e-tests: write E2E test suite per §10 Gherkin scenarios
- [ ] 0017-migrate-ids: update all existing files in `Features/` to replace sequential ids (0001, 0002, ...) with hex ids in frontmatter and filenames
- [ ] 0018-update-howtos: update all `template_workflow/Agent-HowTos/` files to reflect new frontmatter schema (hex id, depends_on, removed state, approved/review_gate values)

---

## Comments
**2026-04-02 — Architect (meeting):** Updated to reflect finalized column structure (9+1 columns including 10-Canceled), new folder convention, logging first-class, E2E Gherkin test scenarios, all open questions resolved, `state` field removed (column IS the state), `feature` renamed to `name`, `approved` valid values defined (yes/no), auth deferred to future spec, id changed from sequential to short hex (collision-free across agents/branches), migration task added for existing files.
