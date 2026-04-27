# template_workflow

Shared agent tooling consumed by project repos as an upstream.

## Load Order

```
agent-manager-template/template_workflow/   ← upstream defaults
project-repo/template_workflow/             ← project overrides (takes precedence)
```

Project-level files shadow upstream files of the same name. Never edit upstream files directly in a consuming repo — override them in the project's own `template_workflow/` folder.

## Version Policy

- Version is stored in `version.json` at the root of this folder.
- Bump the version on every breaking change to template structure or config schema.
- Consuming repos check `template_workflow/version.json` to know which template version they're on.

| Change type | Version bump |
|---|---|
| Breaking structure or schema change | minor or major |
| Additive / backwards-compatible | patch |

## Checking Your Version

From a consuming repo:

```bash
cat template_workflow/version.json
```

## Available Commands

The `commands/` folder contains workflow protocols for AI agents and column guides:

**Slash Commands (Claude Code / AI assistants):**
- **[meeting-protocol.md](commands/meeting-protocol.md)** — `/meeting` command for structured meetings
- **[start-protocol.md](commands/start-protocol.md)** — `/start` command to begin a task
- **[review-protocol.md](commands/review-protocol.md)** — `/review` command for code reviews
- **[housekeeping-protocol.md](commands/housekeeping-protocol.md)** — `/housekeeping` command for maintenance tasks

**Kanban Column Protocols:**
- **[column-backlog.md](commands/column-backlog.md)** — Backlog column (1-Backlog) — create features & epics
- **[column-task.md](commands/column-task.md)** — Task column (4-Task) — add LLD + Gherkin + TestPlan
- **[column-taskreview.md](commands/column-taskreview.md)** — TaskReview column (5-TaskReview) — human LLD gate
- **[column-implement.md](commands/column-implement.md)** — Implementation column (6-Implementation) — TDD code + tests
- **[column-test.md](commands/column-test.md)** — Test column (7-Test) — verify E2E scenarios
- **[column-testing-agent.md](commands/column-testing-agent.md)** — Testing-Agent — automated test verification

## Reference Documentation

The `Docs/` folder contains reference material:
- **[Docs/Kanban-Workflow.md](Docs/Kanban-Workflow.md)** — Overall Kanban structure, gates, and rules
