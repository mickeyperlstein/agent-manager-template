---
id: "0015"
title: Multi-agent meeting workflow (agent-agnostic)
status: backlog
assignee: architect
depends_on: "0008, 0009, 0010"
review_gate: yes — Mickey manually runs a meeting end-to-end
---

## Story
As a user of any AI coding assistant (Claude, Windsurf, Cline, Cursor), I want a `/meeting` command that spawns a multi-agent meeting so that I can run structured discussions between agent personas regardless of which AI tool I'm using.

## Background
Ported from `perli_old/.windsurf/workflows/meeting.md`. The original was Windsurf-specific. This version must be agent-agnostic by living in `template_workflow/` (the canonical SOT) with thin wrapper stubs for each supported AI.

## Scope

### Canonical workflow (`template_workflow/commands/meeting.md`)
- Full meeting lifecycle: validate participants, create temp file, save final file, spawn sub-agents, run meeting, close with decisions
- Resume support (`--resume`) — list recent meetings, reload context
- Participant lookup: search project-local agents first, then `~/ai/agents/`
- Meeting file format: participants, topic, goal, relevant info, agenda, notes, rolling summary, decisions
- MOD protocol: first participant played by host agent, remaining spawned as sub-agents
- Routing: `LABEL:` prefix for directed messages, no prefix for broadcast, `MOD:` for facilitator
- Closing: final decisions, open questions, action items written to meeting file; backlog items created with bidirectional references
- Meeting protocol injected into every sub-agent (1-3 sentence answers, no fluff, silence is valid)

### Wrapper stubs (one per supported AI)
- `.claude/commands/meeting.md` — Claude Code wrapper pointing to canonical SOT
- Equivalent stubs for Windsurf, Cline, Cursor once their wrapper stories (0009, 0010) establish the pattern

### `meetings/` folder convention
- Meeting files saved as `meetings/YYYY-MM-DD_<slug>.md`
- Temp files use hex-truncated timestamp token
- Folder auto-created on first meeting

## Acceptance Criteria
- [ ] `template_workflow/commands/meeting.md` contains the full agent-agnostic meeting workflow
- [ ] At least one wrapper stub exists (Claude Code) that loads the canonical workflow
- [ ] `/meeting <participant1> <participant2>` starts a meeting with validated participants
- [ ] `/meeting --resume` lists recent meetings and resumes selected one
- [ ] Meeting file is created with correct format (participants, topic, goal, agenda, notes, rolling summary, decisions)
- [ ] MOD plays first participant + facilitator; remaining participants spawned as sub-agents
- [ ] Routing works: directed (`LABEL:`), broadcast (no prefix), facilitator (`MOD:`)
- [ ] `/end-meeting` writes decisions, action items, and creates backlog items with bidirectional references
- [ ] No AI-specific logic in the canonical workflow — wrapper stubs handle AI-specific invocation
- [ ] Mickey manually runs a full meeting end-to-end

## Dependencies
- 0008 (Claude agent wrappers — establishes stub pattern)
- 0009 (Windsurf wrappers)
- 0010 (Cline wrappers)

## Notes
Original source: `perli_old/.windsurf/workflows/meeting.md`. Adapted to be agent-agnostic via the template's wrapper pattern.

## Comments
**2026-04-07 — architect (backlog creation):** Created backlog story from Windsurf-specific meeting workflow. Scoped as agent-agnostic feature using template_workflow SOT with thin wrapper stubs per AI tool.
