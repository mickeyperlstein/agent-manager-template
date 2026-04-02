---
epic: 23a043
feature: bd72df
id: 385474
title: Review and update folders_to_csv.py
type: task
assignee: architect
review_gate: yes
approved: no
depends_on:
---

## What
Review the existing `template_workflow/scripts/folders_to_csv.py` against the HLD and update it to match: correct column names (1-Backlog through 10-Canceled), `name` field derived from filename, hex id from frontmatter, `depends_on` field, shared schema module.

## Scope
- In: folders_to_csv.py, shared schema module
- Out: csv_to_folders.py (separate task), pre-commit hook

## Acceptance Criteria
- [ ] Scans all columns including 10-Canceled
- [ ] Derives `name` from filename, `state` from folder path
- [ ] Reads hex `id` from frontmatter
- [ ] Reads `depends_on` from frontmatter
- [ ] Uses shared schema module for CSV field order
- [ ] Logs per spec (info/warn/error, structured fields)

## Test Conditions
- Happy path: scan Features/ → CSV reflects correct state, name, id → log: "sync complete" with item_count
- Missing id in frontmatter → log: warn, file skipped
- 10-Canceled folder → items appear in CSV with state = Canceled

## Definition of Done
- [ ] Script passes E2E scenarios from HLD §10
- [ ] All log events present per §6
- [ ] No regressions on existing behavior

## LLD

### Problem with current script
Current `folders_to_csv.py` has the wrong column map (9 old columns: `3-TaskReview`, `4-InProgress`, etc.), wrong field names (`story`, `status`, `path` instead of `name`, `state`, `approved`, `depends_on`), no shared schema module, and uses `print()` instead of structured logging.

### Changes required

#### 1. Create `template_workflow/scripts/schema.py` (new shared module)
```python
# schema.py — single source of truth for CSV field order and column names
CSV_FIELDS = [
    'id', 'epic', 'feature', 'state', 'name',
    'assignee', 'type', 'review_required', 'approved', 'depends_on'
]

COLUMN_MAP = {
    '1-Backlog':       'Backlog',
    '2-HLD':           'HLD',
    '3-HLD-Review':    'HLD-Review',
    '4-Task':          'Task',
    '5-TaskReview':    'TaskReview',
    '6-Implementation':'Implementation',
    '7-Test':          'Test',
    '8-Review':        'Review',
    '9-Done':          'Done',
    '10-Canceled':     'Canceled',
}

PROGRESSION = [
    'Backlog', 'HLD', 'HLD-Review', 'Task', 'TaskReview',
    'Implementation', 'Test', 'Review', 'Done'
]
```

#### 2. Update `folders_to_csv.py`

**Imports:** replace inline `COLUMN_MAP` and `fieldnames` with `from schema import CSV_FIELDS, COLUMN_MAP`.

**Name derivation (`extract_name_from_filename`):**
```python
HEX_SEGMENT = re.compile(r'^[0-9a-f]{6}$')

def extract_name_from_filename(filepath: Path) -> str:
    parts = filepath.stem.split('-')
    # Strip trailing 6-char hex segments (taskid, featureid, epicid)
    while parts and HEX_SEGMENT.match(parts[-1]):
        parts.pop()
    return '-'.join(parts) if parts else filepath.stem
```

**Field mapping in `scan_features()`:**
- `state`: `COLUMN_MAP[folder.name]` (derived from folder, never frontmatter)
- `name`: `extract_name_from_filename(md_file)`
- `review_required`: `fm.get('review_gate', 'no')`  ← note: frontmatter field is `review_gate`
- `approved`: `fm.get('approved', 'no')`
- `depends_on`: `fm.get('depends_on', '')`
- Remove: `story`, `status`, `path`

**Logging:** replace `print()` with Python `logging` module. Emit:
```
INFO  sync started  script=folders_to_csv direction=folders→csv item_count=N
WARN  missing id in frontmatter  file=<path>
INFO  sync complete  files_moved=0 item_count=N duration_ms=N
```
Use `logging.basicConfig(stream=sys.stderr)`. `item_count` = files written to CSV. `files_moved=0` always (this script reads only; no files are moved).

**CSV output:** use `schema.CSV_FIELDS` as `fieldnames` in `csv.DictWriter`. Sort output by `id`. Write to `tasks.csv` at repo root.

**Missing id handling:** if `'id' not in fm` → log warn, skip file (do not write row).

### No other files touched
`csv_to_folders.py` and the pre-commit hook are out of scope for this task.

---

## Gherkin

```gherkin
Feature: folders_to_csv.py scans Features/ and writes tasks.csv

  Background:
    Given a repo with Features/ containing files in various column folders

  Scenario: Happy path — file with complete frontmatter is written to CSV
    Given a file exists at Features/4-Task/devops-bootstrap/csv-two-way-sync/folders-to-csv-385474-bd72df-23a043.md
    And its frontmatter contains id=385474, epic=23a043, feature=bd72df, assignee=architect, type=task, review_gate=yes, approved=no, depends_on=
    When folders_to_csv.py runs
    Then tasks.csv contains a row with id=385474, state=Task, name=folders-to-csv, epic=23a043, feature=bd72df, review_required=yes, approved=no, depends_on=
    And the log contains info: "sync complete" with item_count > 0

  Scenario: Missing id in frontmatter — file is skipped
    Given a file exists in Features/4-Task/ with no id field in frontmatter
    When folders_to_csv.py runs
    Then tasks.csv does not contain a row for that file
    And the log contains warn: "missing id in frontmatter" with the file path

  Scenario: 10-Canceled folder — items appear with state=Canceled
    Given a file exists at Features/10-Canceled/devops-bootstrap/csv-two-way-sync/some-task-aabbcc-bd72df-23a043.md
    And its frontmatter contains id=aabbcc
    When folders_to_csv.py runs
    Then tasks.csv contains a row with id=aabbcc and state=Canceled

  Scenario: State is always derived from folder path, not frontmatter
    Given a file exists at Features/9-Done/devops-bootstrap/csv-two-way-sync/some-task-aabbcc-bd72df-23a043.md
    And its frontmatter contains a stale column field with value=Task
    When folders_to_csv.py runs
    Then tasks.csv contains a row with id=aabbcc and state=Done

  Scenario: Name is derived from filename slug (hex segments stripped)
    Given a file at Features/4-Task/.../my-feature-name-a1b2c3-d4e5f6-111222.md
    When folders_to_csv.py runs
    Then tasks.csv contains a row with name=my-feature-name

  Scenario: Sync started and sync complete log events present
    When folders_to_csv.py runs
    Then the log contains info: "sync started" with fields script, direction, item_count
    And the log contains info: "sync complete" with fields item_count, duration_ms
```

---

## TestPlan

**Approach:** Black-box E2E. Each test creates a controlled Features/ tree in a temp directory, runs `folders_to_csv.py`, then asserts on `tasks.csv` content and log output. No mocking of internals.

**Test harness:** pytest with `tmp_path` fixture. Capture stderr for log assertions.

| # | Scenario | Setup | Run | Assert CSV | Assert Log |
|---|----------|-------|-----|------------|------------|
| 1 | Happy path | File in 4-Task with full frontmatter | `python folders_to_csv.py` | Row present: state=Task, name=slug, review_required=yes | INFO sync complete, item_count=1 |
| 2 | Missing id | File in 4-Task with no id field | `python folders_to_csv.py` | Row absent | WARN missing id in frontmatter |
| 3 | 10-Canceled | File in 10-Canceled with id | `python folders_to_csv.py` | Row: state=Canceled | INFO sync complete |
| 4 | State from folder | File in 9-Done but frontmatter says Task | `python folders_to_csv.py` | state=Done | — |
| 5 | Name from filename | File named `my-feature-a1b2c3-d4e5f6-111222.md` | `python folders_to_csv.py` | name=my-feature | — |
| 6 | Sync log events | Any valid file | `python folders_to_csv.py` | — | INFO sync started, INFO sync complete with duration_ms |
| 7 | Idempotency | Run twice on same tree | Run twice | CSV identical both runs | Second run: item_count same, no errors |
| 8 | depends_on field | File with depends_on=385474 in frontmatter | `python folders_to_csv.py` | depends_on=385474 in row | — |

**Test file location:** `template_workflow/tests/test_folders_to_csv.py`

**CI:** Tests run via `pytest template_workflow/tests/` — no manual setup required.

## Comments
**2026-04-02 — Task agent:** Added LLD, Gherkin, and TestPlan. Identified 6 gaps between current script and HLD: wrong column map, wrong field names (story/status/path vs name/state/approved/depends_on), no shared schema module, no structured logging, missing 10-Canceled support, no depends_on/approved fields read from frontmatter.
