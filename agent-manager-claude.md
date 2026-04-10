# Agent Manager — Claude Code Rules

This file contains the Kanban workflow rules for Claude Code agents.

---

## ⛔ STOP — MANDATORY BEFORE ANY ACTION

**You have not earned the right to act in this repo yet.**

Before you write a single line, move a single file, or make any suggestion — you must read `template_workflow/Agent-HowTos/Kanban.md` in full. Not skim it. Read it.

**If you have not read `template_workflow/Agent-HowTos/Kanban.md` in this session: stop now and read it before doing anything else.**

This applies to ALL agents, ALL roles, ALL sessions. No exceptions. Not for urgency. Not because the task seems obvious. Not because you were told what to do. You do not know what column a task is in, what gate it must pass, or what artifacts are required until you have read `template_workflow/Agent-HowTos/Kanban.md`.

Acting without reading `agent-manager-template.KANBAN.md` is a process violation.

---

## Startup Protocol — REQUIRED SEQUENCE

You must complete these steps in order before taking any action:

1. **Read `agent-manager-template.KANBAN.md` in full** — columns, gates, folder structure, artifact requirements
1a. **Run `/housekeeping`** — prune empty folders and move stragglers to correct stages before reading board state
2. **Read `tasks.csv`** — find stories where `column = HLD`, `column = Task`, `column = TaskReview`, `column = Implementation`, or `column = Test`
3. **Read the task/feature file(s)** for your assigned work only
4. **Confirm your column** — you are only permitted to act on work in the columns above. If your assigned work is not in one of those columns, stop and tell the human.

---

## Gate Rules — NO EXCEPTIONS

1. **Never skip a gate.** Not for urgency, simplicity, or because the CTO is present.
2. **Never move a feature between columns** — one exception only: the HLD agent MUST move a completed HLD to `HLD-Review`. All other column moves are human commits only.
3. **Never suggest fast-tracking.** If you find yourself about to say "we could skip" — stop. That is a process violation.
4. **Never implement work that belongs to a future column.** If you are in HLD, you do not touch code. If you are in Task, you do not write LLD. Stay in your lane.

---

## Artifact Protocol

Every session that modifies a task or feature file MUST append a dated comment before the session ends:

```markdown
## Comments
**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

No file may be modified without this entry dated today.
