---
id: 92bcfd
epic: 23a043
feature: e9245d
title: Create Windsurf /start workflow equivalent
type: task
assignee: agent
review_gate: no
approved: yes
depends_on: 10552f
fast_tracked: yes
source: meetings/2026-04-02_agent-work-status-visibility.md
---

## What
Create `.windsurf/workflows/start.md` as a Windsurf-native equivalent of `.claude/commands/start.md` — a thin wrapper that forces the agent to read `template_workflow/commands/start-protocol.md` before acting.

## Why fast-tracked
Mirror of the Claude command. Same protocol, different trigger mechanism. No design needed.

## LLD

Create `.windsurf/workflows/start.md`:
```markdown
---
description: Start working on a task. Reads the task file, confirms scope with the human, then begins.
---

**BEFORE ANYTHING ELSE: read `template_workflow/commands/start-protocol.md` in full.**

You have not earned the right to act until you have read it. That file is the protocol. This file is only the trigger.
```

Windsurf workflows support a `description` frontmatter field used in the UI. Keep the wrapper as thin as the Claude version — one directive, one pointer.

## Acceptance Criteria
- [ ] `.windsurf/workflows/start.md` exists
- [ ] File contains `description` frontmatter
- [ ] File points to `template_workflow/commands/start-protocol.md`
- [ ] Wording matches the Claude wrapper in tone and intent
