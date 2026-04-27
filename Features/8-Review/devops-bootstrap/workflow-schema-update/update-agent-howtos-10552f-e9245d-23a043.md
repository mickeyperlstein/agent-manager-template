---
id: 10552f
epic: 23a043
feature: e9245d
title: Update Agent HowTos for new artifact map and filename convention
type: task
assignee: agent
review_gate: no
approved: yes
depends_on: 6764ce
fast_tracked: yes
source: meetings/2026-04-02_agent-work-status-visibility.md
---


## What
Update all Agent HowTo files to reflect the new workflow artifact map, filename convention, and frontmatter schema.

## Why fast-tracked
Pure doc update. Decisions made in meeting 2026-04-02.

## LLD

### `template_workflow/Agent-HowTos/Backlog.md`
- Frontmatter template: add `epic` (hex) and `feature` (hex) fields — note these are set when a feature is created

### `template_workflow/Agent-HowTos/HLD.md`
- Add: HLD agent creates task stub files alongside the HLD doc
- Task stub format: `{name}-{taskid}-{featureid}-{epicid}.md` with what, scope, AC, test conditions, DoD
- Clarify: Task column adds LLD + Gherkin + TestPlan only — decomposition happens here at HLD

### `template_workflow/Agent-HowTos/Task.md`
- Update frontmatter template: add `epic`, `feature`, use new filename convention
- Update folder structure example to show new filename pattern
- Clarify: task files received from HLD already have what/scope/AC/test conditions/DoD
- Task agent job: add LLD + Gherkin + TestPlan, then move file to TaskReview

## Test Results — 2026-04-02

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Frontmatter updated | ✅ PASS | `Task.md` frontmatter includes `epic` and `feature` fields |
| Folder structure example updated | ✅ PASS | `Task.md` shows `{name}-{taskid}-{featureid}-{epicid}.md` pattern |
| Task agent job scope correct | ✅ PASS | `Task.md` states task agent job is to add LLD + Gherkin + TestPlan |

### `template_workflow/Agent-HowTos/TaskReview.md`
- Clarify: review is per task file (individual), not per feature folder
- Add: human-readable summary must accompany LLD for non-technical reviewers

## Test Results — 2026-04-02

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Review is per task file | ✅ PASS | `TaskReview.md` states review is per task file (individual) |
| Human-readable summary required | ✅ PASS | `TaskReview.md` states human-readable summary must accompany LLD |

### `template_workflow/Agent-HowTos/LLD.md`
- Update frontmatter template: add `epic`, `feature`, use new filename convention
- Update folder structure example to show new filename pattern
- Clarify: LLD files received from HLD already have what/scope/AC/test conditions/DoD
- LLD agent job: add Gherkin + TestPlan, then move file to TaskReview

## Test Results — 2026-04-02

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Frontmatter updated | ✅ PASS | `LLD.md` frontmatter includes `epic` and `feature` fields |
| Folder structure example updated | ✅ PASS | `LLD.md` shows `{name}-{taskid}-{featureid}-{epicid}.md` pattern |
| LLD agent job scope correct | ✅ PASS | `LLD.md` states LLD agent job is to add Gherkin + TestPlan |

### `template_workflow/commands/start-protocol.md`
- Update filename lookup to use new `{name}-{taskid}-{featureid}-{epicid}.md` convention

## Test Results — 2026-04-02

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Filename lookup updated | ✅ PASS | `start-protocol.md` uses `{name}-{taskid}-{featureid}-{epicid}.md` pattern |

## Acceptance Criteria
- [x] All HowTo frontmatter templates include `epic` and `feature` hex fields
- [x] HLD HowTo states task stubs are created here
- [x] Task HowTo shows new filename convention and correct job scope (LLD + Gherkin + TestPlan)
- [x] TaskReview HowTo states per-task (not per-folder) review
- [x] start-protocol.md reflects new filename convention

## Test Results — 2026-04-02

| Criterion | Status | Evidence |
|-----------|--------|----------|
| `epic` and `feature` in HowTo frontmatter | ✅ PASS | `template_workflow/Agent-HowTos/HLD.md` and `Task.md` updated with hex id fields |
| HLD HowTo states task stubs created here | ✅ PASS | `HLD.md` §7: "HLD agent creates task stub files alongside the HLD doc" |
| Task HowTo shows new filename convention | ✅ PASS | `Task.md` shows `{name}-{taskid}-{featureid}-{epicid}.md` pattern |
| TaskReview per-task review | ✅ PASS | `TaskReview.md`: "review is per task file (individual), not per feature folder" |
| start-protocol.md filename convention | ✅ PASS | `commands/start-protocol.md` updated to reference new filename pattern |

**Route:** All criteria pass. Move to Review.
