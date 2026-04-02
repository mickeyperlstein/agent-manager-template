# Meeting: Agent work-status visibility within a Kanban column
Date: 2026-04-02 Time: (now)

## Participants
- MOD + ARCH: Claude — playing Architect + facilitator — `~/.claude/agents/architect.md`
- PM: — cutthroat PM, product decisions and prioritization — `~/.claude/agents/pm.md`

## Goal
Decide: how should agents signal sub-column work status, and validate the overall workflow column structure.

## Relevant Info
- Current Kanban: column = folder location. Column moves = human commits only.
- Problem: tasks in `Features/4-Task/{feature}/` had no sub-state.
- CSV schema: `id,state,epic,name,assignee,type,review_required,approved,depends_on`

## Agenda
1. Status visibility mechanism
2. Workflow column structure — over/under-populated?
3. Filename convention
4. Configurable gates

## Notes
- status-in-frontmatter rejected in favour of individual file moves through columns
- `depends_on` handles ordering between tasks — no locks needed
- Folder-as-unit model dissolves at Task column; individual task files move independently
- HLD agent creates task stubs (what, scope, AC, test conditions, DoD) — not just the HLD doc
- Task column: agent adds LLD + Gherkin + TestPlan per stub, then moves to TaskReview
- PM flagged: HLD-Review + TaskReview = two human gates close together, risk of rubber-stamping
- ARCH counter: LLD doesn't exist at HLD-Review, so can't fold
- PM flagged: gap between Test and Review — no gate checking agent tests covered the AC
- Filename: `{name}-{taskid}-{featureid}-{epicid}.md` — name first for readability, all ids are hex
- Epic and feature need hex ids (slugs break path parsing with slashes)
- Configurable gates rejected — gate removal is liability; presentation varies, process doesn't
- TaskReview artifact must include human-readable summary alongside LLD for non-technical users
- Test coverage gap (PM): resolved — ACs defined at HLD, Gherkin covers ACs at Task, TaskReview verifies the mapping. Passing tests = coverage guaranteed by the chain.

## Rolling Summary
- Status visibility: solved by individual file moves through columns, not a status field
- Workflow: 9 columns confirmed, TaskReview stays as hard gate
- Task column produces: LLD + Gherkin + TestPlan (no code)
- Filename: `{name}-{taskid}-{featureid}-{epicid}.md`, all hex ids
- Gates: always present, presentation layer abstracts for non-technical users
- Test coverage: guaranteed by chain (HLD→Task→TaskReview), no extra gate needed
- Human review compression: HLD-Review = 60s async yes/no; TaskReview auto-advances on green
- Column moves: `features` CLI (sandboxed to Features/, single `allow`), replaces mark-for-deletion workaround
- Two new Backlog stories: 0013 (features CLI core), 0014 (features CLI git, separate risk surface)

## Decisions
1. **Status visibility**: no `status` field. Column location IS the status. Task files move individually through columns.
2. **Folder-as-unit dissolves at Task**: individual task files move from Task → TaskReview → Implementation independently.
3. **`depends_on` handles ordering**: no locks, no coordination file needed.
4. **HLD produces task stubs**: HLD agent creates stub files (what, scope, AC, test conditions, DoD) alongside the HLD doc. Task column adds LLD + Gherkin + TestPlan only.
5. **Filename convention**: `{name}-{taskid}-{featureid}-{epicid}.md`. All three ids are short hex. Name first for readability.
6. **Hex ids for epics and features**: slugs rejected — slash-unsafe for path parsing. Hex ids in frontmatter, human-readable title as separate field.
7. **TaskReview stays as hard gate**: PM's suggestion to fold into HLD-Review rejected — LLD doesn't exist at HLD-Review.
8. **No configurable gates**: presentation varies by user profile (plain-English summary for non-technical users), but the gate and artifact are always produced.
9. **Test coverage gap**: not a gap — guaranteed by HLD→Task→TaskReview chain. No additional gate needed.
10. **Column move mechanism**: `features` CLI (`python -m features`), sandboxed to `Features/` tree, single `allow` grant covers all workflow ops. Replaces write+mark-for-deletion workaround.
11. **`features` CLI split into two stories**: 0013 (core: column moves + ID generation + clean) ships first; 0014 (git: stage/commit/push scoped to Features/) is a separate story with its own risk/test surface.
12. **Human review compression**: HLD-Review = 60-second async, agent provides diff summary + single yes/no question. TaskReview auto-advances on green (all tests pass + artifact checklist complete); human signature only on red flag.

## Open Questions
- None.

## Action Items
- Update HLD data model: add `epic` (hex) and `feature` (hex) fields to CSV schema and frontmatter spec
- Update HLD: task stubs created by HLD agent, not Task agent — revise §12 Task Decomposition
- Update KANBAN.md: reflect individual file moves, folder lifecycle change, filename convention, Column Move Protocol section
- Update Agent HowTos: Backlog, HLD, Task, TaskReview to reflect new artifact map and filename convention
- Existing task files in `Features/4-Task/csv-two-way-sync/` need renaming to new convention and epic/feature ids added to frontmatter
- Story 0013: features CLI core — added to Backlog
- Story 0014: features CLI git — added to Backlog
