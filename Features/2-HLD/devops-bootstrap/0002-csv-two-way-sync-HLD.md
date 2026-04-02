# High Level Design: CSV Two-Way Sync with Folder Structure

**Epic:** devops-bootstrap  
**Feature:** csv-two-way-sync  
*

**Status:** HLD  
**Author:** Agent  
**Date:** 2026-04-02  

---

## 1. Problem Statement

The team needs a single source of truth for Kanban state that:
- Lives at repo root as `tasks.csv` for easy import to Google Sheets/GitHub Projects
- Stays in sync with `Features/` folder structure (files drive CSV, CSV drives file moves)
- Supports bidirectional editing: edit CSV → folders update, move files → CSV updates

---

## 2. Goals

1. **Authoritative Source**: Folder structure is canonical; CSV is derived view
2. **Bidirectional Sync**: Changes in either direction propagate correctly
3. **Idempotent**: Running sync twice produces no changes on second run
4. **Atomic Commits**: CSV changes and folder moves happen in single commit
5. **Auto-Progression**: Stories can advance columns automatically when approved

---

## 3. Proposed Architecture

### 3.1 Data Model

**CSV Schema:**
```
id,epic,story,state,assignee,column,type,review_gate,approved
```

| Field | Source | Description |
|-------|--------|-------------|
| `id` | frontmatter | Unique story identifier (0001, 0002, etc.) |
| `epic` | folder path | Epic name from `{epic}/{type}/` structure |
| `story` | filename | Human-readable name from `0001-story-name.md` |
| `state` | frontmatter | Story state (backlog, in-progress, done) |
| `assignee` | frontmatter | Who owns the story |
| `column` | folder name | Kanban column (Backlog, HLD, Implementation, etc.) |
| `type` | folder path | Story type from `{epic}/{type}/` (stories, bugs, tasks) |
| `review_gate` | frontmatter | yes/no - requires human review |
| `approved` | frontmatter | yes/no - triggers auto-progression |

**Folder Structure:**
```
Features/
  1-Backlog/
    {epic}/
      {type}/
        {id}-{story-name}.md
  2-HLD/
    {epic}/
       {Feature-name}/
        {id}-{story-name}-HLD.md
  3-TaskReview/
  4-Implementation/
  5-Testing-Agent/
  6-Testing-Manual/
  7-Verified/
  8-Review/
  9-Done/
```

Example: `Features/1-Backlog/devops-bootstrap/stories/0003-github-repo.md`

### 3.2 Components

#### Component A: Folders → CSV (`folders_to_csv.py`)

**WHAT:** Scans Features/ tree, extracts metadata, generates tasks.csv  
**WHY:** CSV is derived view; must reflect actual folder state  
**HOW:**
1. Walk each column folder (1-Backlog, 2-HLD, etc.)
2. For each .md file:
   - Parse frontmatter (id, state, assignee, approved, etc.)
   - Extract epic/type from relative path
   - Extract story name from filename
   - Map folder name to column name
3. Write CSV sorted by id

**Key Design Decisions:**
- Derived values (epic, type, column) override frontmatter values
- Support both `state` and legacy `status` in frontmatter
- Default type to "stories" if not specified

#### Component B: CSV → Folders (`csv_to_folders.py`)

**WHAT:** Reads tasks.csv, moves files to correct column folders  
**WHY:** Editing CSV should drive folder reorganization  
**HOW:**
1. Read CSV rows
2. For each story:
   - **Assume synced:** Build expected path from `{column_folder}/{epic}/{type}/{id}-*.md`
   - **Verify:** Check if file exists at expected location (fast)
   - **Fallback:** If not found, search with rglob (slow, handles drift)
   - Determine target column (with auto-progression if approved=yes)
   - Move file if needed

**Path Lookup Strategy:**
```python
# Fast path: assume CSV is synced, build direct path
expected_path = f"{column_folder}/{epic}/{type}/{id}-*.md"
if exists(expected_path):
    current_file = expected_path
else:
    # Fallback: search everywhere (handles desync)
    current_file = rglob_search(features_dir, id)
```

**Auto-Progression Logic:**
```python
NEXT_COLUMN = {
    "Backlog": "HLD",
    "HLD": "TaskReview",
    "TaskReview": "Implementation",
    "Implementation": "Testing-Agent",
    "Testing-Agent": "Verified",
    "Testing-Manual": "Verified",
    "Verified": "Review",
    "Review": "Done",
    "Done": "Done",
}
```
If `approved=yes`, story advances to next column automatically.

### 3.3 Workflow

**Scenario 1: Move file in terminal**
```bash
mv Features/1-Backlog/story.md Features/4-Implementation/
git add .
git commit -m "Move story to Implementation"
# User runs: python3 scripts/folders_to_csv.py
# CSV regenerated to reflect new column
```

**Scenario 2: Edit CSV in Sheets**
```bash
# User edits tasks.csv, changes column from "Backlog" to "HLD"
# User runs: python3 scripts/csv_to_folders.py --dry-run
# Preview shows: Would move: Features/1-Backlog/... -> Features/2-HLD/...
# User runs: python3 scripts/csv_to_folders.py
# Files moved to match CSV
```

**Scenario 3: Auto-progression**
```bash
# User edits story frontmatter: approved: yes
# User runs: python3 scripts/folders_to_csv.py && python3 scripts/csv_to_folders.py
# Story automatically moves to next column
```

---

## 4. Pre-Commit Hook (Future)

**Trigger:** `git commit`  
**Action:**
1. Run `folders_to_csv.py` to capture any manual folder moves
2. Run `csv_to_folders.py` to apply any CSV edits
3. Stage both `tasks.csv` and moved files
4. Commit includes both changes atomically

**Implementation:**
```bash
#!/bin/sh
# .git/hooks/pre-commit
python3 scripts/folders_to_csv.py
python3 scripts/csv_to_folders.py
git add tasks.csv Features/
```

---

## 5. Configuration (Future)

**`template_workflow/kanban-sync.config.json`:**
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

Scripts read config to determine sync targets.

---

## 6. Idempotency Guarantee

**Definition:** Running sync twice produces no changes on second run.

**How:**
- `folders_to_csv.py`: Always regenerates CSV from scratch (no incremental state)
- `csv_to_folders.py`: Only moves files if `current_column != target_column`
- No timestamps or sequence numbers needed

**Verification:**
```bash
python3 scripts/folders_to_csv.py
python3 scripts/csv_to_folders.py
# Should produce: "Done: 0 files moved"
```

---

## 7. Error Handling

| Error | Handling |
|-------|----------|
| Story in CSV but no file | Log warning, skip (create case for future) |
| File exists at target | Log error, skip (collision) |
| Unknown column in CSV | Log error, skip |
| Missing frontmatter id | Skip file (not a story) |
| Invalid approved value | Treat as "no" |

---

## 8. Security & Permissions

- Scripts run with user's git permissions
- No external API calls in core sync
- Sheets/GitHub integration requires auth (future scope)

---

## 9. Testing Strategy

1. **Unit Tests**: Mock filesystem, verify path parsing
2. **Integration Tests**: Temp directory with sample stories
3. **Round-trip Test**: Folders→CSV→Folders should be no-op
4. **Auto-progression Test**: approved=yes triggers move

---

## 10. Open Questions

1. Should auto-progression require `review_gate=yes` also be satisfied?
2. Should there be a `--force` flag to override idempotency?
3. How to handle story deletion? (Remove from CSV? Move to archive?)
4. Should pre-commit hook be optional or mandatory?

---

## 11. Acceptance Criteria (HLD → Implementation)

- [x] Schema defined: `id, epic, story, state, assignee, column, type, review_gate, approved`
- [x] Bidirectional sync design documented
- [x] Auto-progression logic defined
- [x] Idempotency strategy documented
- [ ] Implementation: Python scripts (Phase 2)
- [ ] Pre-commit hook (Phase 2)
- [ ] Config file support (Phase 2)
- [ ] Documentation: CONTRIBUTING.md (Phase 2)

---

**Next Step:** Move to Implementation column and build the scripts per this design.
