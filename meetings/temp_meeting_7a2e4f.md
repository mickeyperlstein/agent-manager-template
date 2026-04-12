# Meeting: Externalizing Reusable Documentation Concepts

Date: 2026-04-11

## Participants
- MOD + ARCH: Claude — playing architect + facilitator
- ARCH: architect — Senior software architect. Deep expertise in distributed systems, Node.js, TypeScript, VS Code extensions, event-driven architecture — `~/.claude/agents/architect.md`

## Goal
Decide: Should reusable documentation concepts (like "item formatting" used across kanban columns) be externalized to reference files (@item-format.md) or kept embedded in their primary file (kanban.md)?

## Relevant Info
- Current pattern: kanban.md explains item format, used throughout the template
- Question: Is this a good pattern, or should item-format be its own @-referenced file?
- Context: review-protocol.md shows referential pattern (references @meeting-protocol.md for foundational structure)
- Trade-off: embedded = discoverable but repetitive; externalized = DRY but requires more navigation

## Agenda
1. Examine current kanban.md structure — where is item format defined and reused?
2. Discuss: Does the review-protocol referential pattern apply here?
3. Recommend: Should we externalize item-format (and similar concepts) into reference files?

## Notes
(live notes — updated during the meeting)

## Rolling Summary
(updated every ~5 exchanges)

## Decisions
(populated at end of meeting)
