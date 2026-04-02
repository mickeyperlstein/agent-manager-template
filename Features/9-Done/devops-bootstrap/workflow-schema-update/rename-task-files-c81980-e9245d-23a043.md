---
id: c81980
epic: 23a043
feature: e9245d
title: Rename existing task files to new filename convention
type: task
assignee: agent
review_gate: no
approved: yes
depends_on: 10552f
fast_tracked: yes
source: meetings/2026-04-02_agent-work-status-visibility.md
---

## What
Rename all task files in `Features/4-Task/csv-two-way-sync/` to the new `{name}-{taskid}-{featureid}-{epicid}.md` convention and add `epic` and `feature` hex id fields to their frontmatter.

## Why fast-tracked
Pure mechanical rename + frontmatter update. Convention decided in meeting 2026-04-02.

## LLD

Existing files and their new names (featureid for csv-two-way-sync, epicid for devops-bootstrap):

| Current filename | New filename |
|---|---|
| `folders-to-csv-task.md` | `folders-to-csv-385474-{featureid}-{epicid}.md` |
| `csv-to-folders-task.md` | `csv-to-folders-0640af-{featureid}-{epicid}.md` |
| `pre-commit-hook-task.md` | `pre-commit-hook-3cda27-{featureid}-{epicid}.md` |
| `e2e-tests-task.md` | `e2e-tests-8bed76-{featureid}-{epicid}.md` |
| `migrate-ids-task.md` | `migrate-ids-fd2dbd-{featureid}-{epicid}.md` |
| `update-howtos-task.md` | `update-howtos-73df4b-{featureid}-{epicid}.md` |

Steps:
1. Generate hex ids for the csv-two-way-sync feature and devops-bootstrap epic (if not already assigned)
2. `git mv` each file to new name
3. Add `epic: {epicid}` and `feature: {featureid}` to each file's frontmatter

## Acceptance Criteria
- [ ] All 6 task files renamed to new convention
- [ ] All 6 task files have `epic` and `feature` in frontmatter
- [ ] `git mv` used (preserves history)
- [ ] tasks.csv regenerated after rename

## Test Results — 2026-04-02

### Evidence from git log (commit 049e37e)

| Original Filename | Git Status | Renamed Filename |
|---|---|---|
| `csv-to-folders-task.md` | R097 | `csv-to-folders-0640af-bd72df-23a043.md` |
| `e2e-tests-task.md` | R097 | `e2e-tests-8bed76-bd72df-23a043.md` |
| `folders-to-csv-task.md` | R097 | `folders-to-csv-385474-bd72df-23a043.md` |
| `migrate-ids-task.md` | R097 | `migrate-ids-fd2dbd-bd72df-23a043.md` |
| `pre-commit-hook-task.md` | R097 | `pre-commit-hook-3cda27-bd72df-23a043.md` |
| `update-howtos-task.md` | R100 | `update-howtos-73df4b-bd72df-23a043.md` |

**R097/R100**: Git rename detection with 97%/100% similarity — confirms `git mv` was used, history preserved.

### Frontmatter Verification (sample: folders-to-csv-385474-bd72df-23a043.md)
```yaml
---
epic: 23a043
feature: bd72df
id: 385474
---
```

✅ `epic` and `feature` hex ids present in frontmatter.

### Current Location
All 6 files found at: `Features/4-Task/devops-bootstrap/csv-two-way-sync/`

### tasks.csv Check
❌ **FAIL**: `tasks.csv` does not contain updated paths for csv-two-way-sync feature. File shows stale data (path column still shows `devops-bootstrap/stories` for 0002 feature).

**Route**: Move back to Implementation for CSV regeneration.
