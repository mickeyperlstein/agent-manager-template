---
id: "3075d4"
title: Write canonical meeting protocol
type: task
epic: devops-bootstrap
feature: "0015"
feature_name: meeting-workflow
status: TaskReview
assignee: agent
depends_on: []
review_gate: yes
---

## Scope

Write `template_workflow/commands/meeting-protocol.md` — the canonical, agent-agnostic meeting workflow.

Must include all steps from the HLD:
- Step 0a: Resume mode (list recent meetings with 1-paragraph summary, confirm/modify participant roster)
- Step 0b: Working meeting mode (summarize current conversation, prefill Relevant Info + Notes)
- Step 1: Validate participants (agent lookup order per HLD)
- Step 2: Create temp meeting file with hex token
- Step 3: Save and clean up (rename to final path, delete temp)
- Step 3.5: Upload meeting file to participants
- Step 4: Assign and spawn (MOD + first role, remaining as sub-agents)
- Step 5: Open meeting (introductions, show user commands)
- Step 6: During meeting (routing, Notes updates, Rolling Summary every ~5 exchanges)
- Step 7: Close (Decisions, backlog items with bidirectional refs)

Include the meeting protocol injection text for sub-agents.
Include routing table and user commands.

## Acceptance Criteria

- [ ] File exists at `template_workflow/commands/meeting-protocol.md`
- [ ] All steps from HLD are present and complete
- [ ] No AI-tool-specific logic — protocol describes intent, not implementation
- [ ] Resume mode includes meeting summary preview and participant roster confirmation
- [ ] Working meeting mode includes prior-context capture and prefill

## Comments
**2026-04-07 — Architect (Task creation):** Task stub created from approved HLD.
**2026-04-07 — Agent (Task implementation):** Wrote `template_workflow/commands/meeting-protocol.md` with all steps (0a resume with summary + roster check, 0b working meeting, 1-7 full lifecycle). Includes routing table, user commands, sub-agent protocol injection, closing with backlog item creation. Ready for TaskReview.
