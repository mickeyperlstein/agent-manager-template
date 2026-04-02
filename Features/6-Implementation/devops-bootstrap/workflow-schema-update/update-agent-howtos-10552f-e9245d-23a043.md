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

### `template_workflow/Agent-HowTos/TaskReview.md`
- Clarify: review is per task file (individual), not per feature folder
- Add: human-readable summary must accompany LLD for non-technical reviewers

### `template_workflow/commands/start-protocol.md`
- Update filename lookup to use new `{name}-{taskid}-{featureid}-{epicid}.md` convention

## Acceptance Criteria
- [ ] All HowTo frontmatter templates include `epic` and `feature` hex fields
- [ ] HLD HowTo states task stubs are created here
- [ ] Task HowTo shows new filename convention and correct job scope (LLD + Gherkin + TestPlan)
- [ ] TaskReview HowTo states per-task (not per-folder) review
- [ ] start-protocol.md reflects new filename convention
