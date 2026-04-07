# HLD: Multi-Agent Meeting Workflow (Agent-Agnostic)

## 1. Problem Statement

Users need to run structured multi-agent meetings (e.g., PM + Architect + CTO brainstorming a feature). The workflow was previously hardcoded in Windsurf's `.windsurf/workflows/meeting.md`. It needs to work across all supported AI tools (Claude, Windsurf, Cline, Cursor) using the template's canonical SOT + thin wrapper pattern — the same pattern already used by `/start`.

## 2. Goals

- Provide `template_workflow/commands/meeting-protocol.md` as the canonical, agent-agnostic meeting workflow
- Provide thin wrapper stubs for each AI tool (`.claude/commands/meeting.md`, `.windsurf/workflows/meeting.md`, etc.)
- Support full meeting lifecycle: validate → setup → run → close
- Support **working meeting** mode (`--working`) — convert an ongoing conversation into a meeting, capturing prior discussion as context
- Support resume from previous meetings (`--resume`)
- Produce durable meeting artifacts in `meetings/` folder
- Route messages to the right sub-agents (directed, broadcast, facilitator)
- On close, generate backlog items and action items with bidirectional references

## 3. Architecture

### C4 L1 — Context

```
┌──────────────────────────────────────────────────────┐
│                    User                               │
│  types: /meeting PM Architect CTO                    │
└──────────────────┬───────────────────────────────────┘
                   │
        ┌──────────▼──────────────┐
        │   AI Tool (any)         │
        │  Claude / Windsurf /    │
        │  Cline / Cursor         │
        └──────────┬──────────────┘
                   │ reads wrapper stub
                   ▼
        ┌──────────────────────────┐
        │  Wrapper Stub            │
        │  e.g. .claude/commands/  │
        │       meeting.md         │
        │  "read the protocol"     │
        └──────────┬───────────────┘
                   │ points to
                   ▼
        ┌──────────────────────────┐
        │  Canonical Protocol      │
        │  template_workflow/      │
        │  commands/               │
        │  meeting-protocol.md     │
        └──────────┬───────────────┘
                   │ orchestrates
          ┌────────┼────────┐
          ▼        ▼        ▼
     ┌────────┐ ┌────────┐ ┌────────┐
     │Agent 1 │ │Agent 2 │ │Agent N │
     │(MOD +  │ │(sub-   │ │(sub-   │
     │ role)  │ │ agent) │ │ agent) │
     └────────┘ └────────┘ └────────┘
          │        │        │
          ▼        ▼        ▼
     ┌─────────────────────────────┐
     │  meetings/                  │
     │  YYYY-MM-DD_<slug>.md      │
     │  (durable artifact)        │
     └─────────────────────────────┘
```

### C4 L2 — File Layout

```
template_workflow/
└── commands/
    └── meeting-protocol.md       ← canonical SOT (full workflow)

.claude/commands/
└── meeting.md                    ← Claude wrapper stub

.windsurf/workflows/
└── meeting.md                    ← Windsurf wrapper stub

meetings/                         ← created on first use
├── temp_meeting_<token>.md       ← ephemeral, deleted after save
└── YYYY-MM-DD_<slug>.md          ← durable meeting artifact
```

### Components

**1. Wrapper Stubs (one per AI tool)**

Thin files that follow the established pattern (same as `/start`):

```markdown
# /meeting

**BEFORE ANYTHING ELSE: read `template_workflow/commands/meeting-protocol.md` in full.**

That file is the protocol. This file is only the trigger.

Arguments: $ARGUMENTS
```

Each AI's native command format is used (`.claude/commands/` for Claude, `.windsurf/workflows/` for Windsurf, etc.) but all point to the same canonical protocol.

**2. Canonical Protocol (`template_workflow/commands/meeting-protocol.md`)**

Contains the full workflow, organized into steps:

| Step | Name | Description |
|------|------|-------------|
| 0a | Resume (optional) | If `--resume`: list recent meetings, let user pick, confirm/modify participant roster (add/remove), then jump to Step 3.5 |
| 0b | Working meeting (optional) | If `--working`: summarize current conversation, prefill meeting file with prior context, skip to Step 1 with context pre-loaded (see Working Meeting Mode below) |
| 1 | Validate participants | Resolve each name to an agent `.md` file (project-local first, then `~/ai/agents/`) |
| 2 | Create temp meeting file | Generate hex token, create `meetings/temp_meeting_<token>.md` with prefilled template |
| 3 | Save and clean up | User confirms → rename to `meetings/YYYY-MM-DD_<slug>.md`, delete temp file |
| 3.5 | Upload to participants | Include full meeting file content in each sub-agent's spawning prompt |
| 4 | Assign and spawn | Host plays first participant (MOD + role). Remaining participants spawned as sub-agents with identity + meeting protocol |
| 5 | Open the meeting | Introduce participants, show user commands |
| 6 | During meeting | MOD routes, updates Notes + Rolling Summary every ~5 exchanges |
| 7 | Close | Write Decisions, create backlog/action items with bidirectional references |

**3. Agent Lookup Order**

1. `<project-root>/ai/agents/<name>.md` (project-level overrides — highest priority)
2. `<project-root>/template_workflow/agents/<name>.md` (template defaults)
3. `~/ai/agents/<name>.md` (user-global agents)
4. Speculate common AI tool folders (`~/.claude/`, `~/.windsurf/`, `~/.cursor/`, etc.)
5. If not found: stop, report, offer solutions

If multiple matches: present options with key differences for user to choose.

**4. Meeting File Format**

```markdown
# Meeting: <topic>
Date: YYYY-MM-DD  Time: HH:MM

## Participants
- MOD + <LABEL>: <Model> — <role description>
- <LABEL>: <Model> <agent name> — <description> — `<path>`

## Topic
<one sentence>

## Goal
<what decision or output do we leave with>

## Relevant Info
<context, links, code snippets>

## Agenda
<numbered items>

## Notes
(live notes — updated during the meeting)

## Rolling Summary
(updated every ~5 exchanges)

## Decisions
(populated at end of meeting)
```

**5. Meeting Protocol (injected into every sub-agent)**

```
You are in a meeting. Regardless of how you normally work, the rules here are different.

Keep your expertise and personality — but answers are 1-3 sentences maximum. No bullet lists unless explicitly asked. No preamble, no summary, no sign-off.

Before speaking: ask yourself silently — do I have something worth adding? If yes, say it short. If no, stay quiet. Silence is valid.

You may address other participants by name or speak to the room. Push back, disagree, ask a direct question. The human runs the pace.

Tokens cost real money. Earn every word.
```

**6. Routing**

| Pattern | Behavior |
|---------|----------|
| `LABEL: <message>` | Route to that sub-agent only |
| No prefix | Broadcast to all sub-agents; MOD weighs in if useful |
| `MOD: <message>` | MOD responds directly, no sub-agent cost |

**7. User Commands During Meeting**

| Command | Action |
|---------|--------|
| `LABEL: <msg>` | Address one participant |
| (no prefix) | Speak to the room |
| `/notes` | Output current Notes + Rolling Summary |
| `/end-meeting` | Close the meeting |
| `/pause` | Pause the meeting |
| `/resume` | Resume the meeting |

**8. Closing Protocol**

On `/end-meeting`:
1. Write final Decisions, open questions, and action items to the meeting file
2. Update Rolling Summary one final time
3. Output tight bullet list: decisions, open questions, follow-ups
4. For each feature/action item: create backlog file with bidirectional meeting reference

**9. Working Meeting Mode (`--working`)**

A working meeting converts the current conversation into a structured meeting. Instead of starting from scratch, it captures what has already been discussed and brings participants up to speed.

**Invocation:**
```
/meeting --working PM Architect CTO
```

**Step 0b — Capture prior context:**

1. **Summarize the current conversation** — the host agent produces a structured summary of the ongoing discussion:
   - **What was discussed** — key topics, questions raised, options explored
   - **Current state** — where things stand right now (decisions made, blockers hit, open threads)
   - **Why a meeting is needed** — what triggered escalation from solo work to multi-agent discussion
2. **Prefill the meeting file** — the summary goes into two places:
   - `## Relevant Info` — the full prior-context summary so participants arrive informed
   - `## Notes` — seeded with a `### Prior Discussion (pre-meeting)` section containing the key points, so the running notes have continuity
3. **Infer Topic and Goal** — auto-fill from conversation context (user can override)
4. Proceed to Step 1 (validate participants) as normal

**Meeting file additions for working meetings:**

```markdown
## Relevant Info
### Prior Discussion (pre-meeting)
**Context:** <what was being worked on before the meeting was called>
**Key points discussed:**
- <point 1>
- <point 2>
**Current state:** <where things stand>
**Why this meeting:** <what needs multi-agent input>

## Notes
### Prior Discussion (pre-meeting)
- <key point 1 from conversation>
- <key point 2 from conversation>
- <decision or blocker that triggered the meeting>

### Meeting Notes
(live notes continue here)
```

**Why this matters:** Working meetings preserve conversational continuity. Without this, spawned sub-agents arrive with zero context and the user has to re-explain everything. The prior-context summary acts as a briefing document — participants can reference it, challenge it, or build on it immediately.

### Flow

```
User invokes /meeting [--working|--resume] PM Architect CTO
  │
  ├─ --resume? → Step 0a: list recent meetings (each with 1-paragraph summary
  │              from Rolling Summary so user can distinguish similar names)
  │              → user picks one
  │              → show previous participant roster
  │              → ask: "Same participants? Add/remove anyone?"
  │              → validate any new participants (Step 1)
  │              → jump to Step 3.5
  ├─ --working? → Step 0b: summarize current conversation
  │                         prefill Relevant Info + Notes with prior context
  │                         infer Topic + Goal
  │                         ▼ (fall through to Step 1)
  │
  ▼
Wrapper stub → loads canonical protocol
  │
  ▼
Step 1: Resolve "PM", "Architect", "CTO" to agent .md files
  │ (not found? stop and report)
  ▼
Step 2: Create temp_meeting_<hex>.md with prefilled template
  │ (if --working: template already has prior-context sections filled)
  ▼
Show user → ask to confirm/complete Topic, Goal, Agenda
  │
  ▼
Step 3: Save as meetings/YYYY-MM-DD_<slug>.md, delete temp
  │
  ▼
Step 3.5: Upload meeting file to all participants
  │
  ▼
Step 4: Host adopts first agent (MOD + PM)
         Spawn remaining as sub-agents with identity + protocol + context
  │
  ▼
Step 5: Open meeting, show commands
  │
  ▼
Step 6: Meeting loop
  │  ├─ Route messages per routing table
  │  ├─ Update Notes on key points
  │  └─ Update Rolling Summary every ~5 exchanges
  │
  ▼
Step 7: /end-meeting → Decisions → backlog items → done
```

## 4. Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Windsurf-only workflow (status quo) | Already works | Locked to one AI tool | Rejected — need agent-agnostic |
| MCP server for meeting orchestration | Standardized | Overkill for a prompt-based workflow | Rejected — no code needed |
| Single monolithic command file per AI | No indirection | Duplicated logic, drift risk | Rejected — violates SOT principle |
| Canonical protocol + thin wrappers | Single SOT, works everywhere | One level of indirection | **Selected** — matches `/start` pattern |

## 5. Logging, Monitoring & Metrics

This is a prompt-based workflow, not a CLI tool — there is no programmatic logging. Observability comes from the meeting artifact itself:

| Observable | Location | Audience |
|------------|----------|----------|
| Meeting happened | `meetings/YYYY-MM-DD_<slug>.md` exists | Human |
| Participants present | `## Participants` section | Human |
| Decisions made | `## Decisions` section | Human |
| Action items created | Backlog files with bidirectional refs | Human + Agents |
| Meeting quality | `## Rolling Summary` completeness | Human |

## 6. Documentation

Updates already made as part of this HLD:

| Doc | What changed |
|-----|-------------|
| `README.md` | Added Agent Lookup Order table (4 priority levels), Commands table (`/meeting`, `--working`, `--resume`), updated Repository Structure to show `template_workflow/`, `ai/agents/`, `meetings/` |
| `template_workflow/Agent-HowTos/HLD.md` | Added section 6 (Documentation) — HLDs must now update affected docs before moving to HLD-Review |

No changes needed to:
- `KANBAN.md` — no workflow/column changes
- Other Agent-HowTos — no column behavior changes

## 7. Open Questions

**Q1: Should 0012 (meeting stub template) be merged into this story?**
0012 focused on the file template only. This story covers the full workflow including the template. Recommend closing 0012 as superseded.

**Q2: Agent spawning mechanism differs per AI tool — does the protocol need to abstract this?**
No. The protocol describes *what* to do ("spawn as sub-agent with this context"). Each AI tool's native sub-agent mechanism handles *how*. The protocol stays tool-agnostic by describing intent, not implementation.

## 8. Task Decomposition

Feature ID: `0015`, Epic: `devops-bootstrap` (`23a043`)

### Task Stubs:

- [ ] `meeting-protocol-{tid}-0015-23a043.md`: Write canonical `template_workflow/commands/meeting-protocol.md` with all 8 steps
- [ ] `meeting-wrapper-claude-{tid}-0015-23a043.md`: Create `.claude/commands/meeting.md` wrapper stub
- [ ] `meeting-wrapper-windsurf-{tid}-0015-23a043.md`: Create `.windsurf/workflows/meeting.md` wrapper stub
- [ ] `meeting-template-{tid}-0015-23a043.md`: Create `template_workflow/templates/meeting-stub.md` — the prefilled meeting file template (absorbs scope of 0012)
- [ ] `meeting-e2e-test-{tid}-0015-23a043.md`: Manual E2E test — invoke `/meeting`, run full lifecycle, verify artifacts

## Comments
**2026-04-07 — Architect (HLD):** HLD written. Canonical protocol + wrapper pattern mirrors `/start`. Recommends closing 0012 as superseded. Ready for HLD-Review.
**2026-04-07 — Architect (HLD update):** Added working meeting mode (`--working`). Captures current conversation as prior-context summary, prefills Relevant Info + Notes so spawned participants arrive briefed. Preserves conversational continuity when escalating from solo work to multi-agent discussion.
**2026-04-07 — Architect (HLD docs):** Added section 6 (Documentation) listing all doc updates made: README.md (agent lookup, commands, repo structure), Agent-HowTos/HLD.md (new documentation requirement for HLDs).
