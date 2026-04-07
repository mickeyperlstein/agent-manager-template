# Meeting Protocol

Usage: `/meeting [--working|--resume] <participant1> <participant2> [participant3...]`

---

## Step 0a: Resume (if `--resume`)

If the command includes `--resume`:

1. List files in the `meetings/` folder, sorted by date descending (most recent first), limit to 5.
2. For each meeting file, read the `## Rolling Summary` section and show a **1-paragraph summary** alongside the filename — so the user can distinguish meetings with similar names.
3. Present the list as numbered options. Wait for the user to select one.
4. Once selected, load the meeting file and show the **previous participant roster** from `## Participants`.
5. Ask: **"Same participants? Want to add or remove anyone?"**
   - If the user adds participants: validate them (Step 1) before proceeding.
   - If the user removes participants: note the change in `## Notes`.
   - If no changes: proceed as-is.
6. Jump to Step 3.5 (Upload meeting file to participants).

If no meetings exist or no valid selection is made: inform the user and abort.

---

## Step 0b: Working Meeting (if `--working`)

A working meeting converts the current conversation into a structured meeting. Instead of starting from scratch, it captures what has already been discussed.

1. **Summarize the current conversation** — produce a structured summary:
   - **What was discussed** — key topics, questions raised, options explored
   - **Current state** — where things stand right now (decisions made, blockers hit, open threads)
   - **Why a meeting is needed** — what triggered escalation from solo work to multi-agent discussion

2. **Prefill the meeting file** — the summary goes into two places:
   - `## Relevant Info` → full prior-context summary so participants arrive informed
   - `## Notes` → seeded with a `### Prior Discussion (pre-meeting)` section containing the key points, so running notes have continuity

3. **Infer Topic and Goal** — auto-fill from conversation context (user can override in Step 2).

4. Proceed to Step 1.

---

## Step 1: Validate Participants

For each participant name in the argument list, search for their agent file in this order:

1. `<project-root>/ai/agents/<name>.md` (project-level overrides — highest priority)
2. `<project-root>/template_workflow/agents/<name>.md` (template defaults)
3. `~/ai/agents/<name>.md` (user-global agents)
4. Speculate common AI tool folders: `~/.claude/`, `~/.windsurf/`, `~/.cursor/`, `~/.cline/` — look for `agents/<name>.md` or similar paths

Use whichever is found first. If multiple files match for the same participant, present numbered options with a brief diff of key differences (role, description, model). Wait for the user to choose.

If an agent file is not found: **stop immediately**. Tell the user exactly which agent was not found, show the paths you searched, and offer solutions (create the agent file, check the name, etc.). Do not proceed — a meeting does not happen without its participants.

---

## Step 2: Create Temp Meeting File

1. Get the current Unix timestamp in seconds, convert to hex, truncate to 6 characters. This is the `<token>`.
2. Create `<project-root>/meetings/temp_meeting_<token>.md`. If the `meetings/` folder doesn't exist, create it first.
3. Prefill the file from context:

```markdown
# Meeting: <prefill from command context or leave blank>
Date: <today YYYY-MM-DD>  Time: <current time HH:MM>

## Participants
- MOD + <first participant LABEL>: <Actual Model> — playing [first participant role] + facilitator (agent recommends: <Model from agent file>)
- <LABEL>: <Actual Model> <agent name> — <one line from agent description> — `<path where agent file was found>` (agent recommends: <Model from agent file>)
- (repeat for each remaining participant)

## Topic
<prefill if obvious from context, otherwise leave blank>

## Goal
<prefill if obvious, otherwise leave blank>

## Relevant Info
<prefill if there is prior conversation context (especially for --working mode), otherwise leave blank>

## Agenda
<prefill if obvious, otherwise leave blank>

## Notes
(live notes — updated during the meeting)

## Rolling Summary
(updated every ~5 exchanges)

## Decisions
(populated at end of meeting)
```

**For `--working` mode:** the `## Relevant Info` and `## Notes` sections are already prefilled from Step 0b with the prior-context summary. Merge rather than overwrite.

4. Show the prefilled file to the user and ask them to review/complete:
   - **Topic** — one sentence
   - **Goal** — what decision or output do we leave with?
   - **Relevant Info** — context participants need (notes, links, code snippets)
   - **Agenda** — items in order (say "help me" and the agent drafts it)

5. Wait for the user to confirm before proceeding.

---

## Step 3: Save and Clean Up

Once confirmed:

1. Save the final file to: `<project-root>/meetings/YYYY-MM-DD_<slug>.md`
   where `<slug>` is kebab-case derived from the topic.
2. When saving, format the user's written content for readability:
   - Use proper indentation and numbering for lists
   - Fix glaring typos without changing wording
   - If a word is ambiguous, add (possible alternatives) in parentheses based on context
3. Delete `<project-root>/meetings/temp_meeting_<token>.md`.

---

## Step 3.5: Upload Meeting File to Participants

Before spawning any agents, "upload" the finalized meeting file to each participant:

- **For yourself (MOD + first participant):** Read and assimilate the complete meeting file content.
- **For each sub-agent:** Include the full meeting file content in their spawning prompt so they arrive prepared with context, questions, and opinions.

---

## Step 4: Assign and Spawn

**You play the first participant directly** — load their agent file (from whichever path was found in Step 1) and adopt that identity. You speak as both MOD and that first role. No spawn, no cost.

All remaining participants are spawned as sub-agents:
- Load their identity from their agent file
- Spawn with: **their identity** + **meeting protocol** (below) + **meeting background** (Goal + Relevant Info + Agenda from the meeting file)

### Meeting Protocol — Injected Into Every Sub-Agent

> You are in a meeting. Regardless of how you normally work, the rules here are different.
>
> Keep your expertise and personality — but answers are 1-3 sentences maximum. No bullet lists unless explicitly asked. No preamble, no summary, no sign-off.
>
> Before speaking: ask yourself silently — do I have something worth adding? If yes, say it short. If no, stay quiet. Silence is valid.
>
> You may address other participants by name or speak to the room. Push back, disagree, ask a direct question. The human runs the pace — they may be slow, may just listen, may jump in mid-thought. Wait for them.
>
> Tokens cost real money. Earn every word.

---

## Step 5: Open the Meeting

Introduce the meeting:

1. List each participant with their label, one-line role, agent file path, and model information:
   - For yourself: `MOD + [LABEL]: <Actual Model> — playing [role] + facilitator (agent recommends: <Model>)`
   - For each sub-agent: `[LABEL]: <Actual Model> <agent name> — [role] — <path> (agent recommends: <Model>)`
   
   **Note:** The model field in the agent file is a *recommendation*. The actual model used may differ based on availability, cost, or user preference. Always document the actual model being used.

2. Show the user their commands:

> **Meeting commands:**
> - Address one participant: `LABEL: your message` (e.g., `PM: what's your take?`)
> - Speak to the room (no prefix): all participants respond
> - `MOD: <message>` — speak to the facilitator directly, no sub-agent cost
> - `/notes` — show current Notes + Rolling Summary
> - `/pause` — pause the meeting
> - `/resume` — resume the meeting
> - `/end-meeting` — close the meeting and produce decisions

---

## Step 6: During the Meeting — MOD Responsibilities

MOD is a participant, not an invisible layer:

- **Routes messages** to the correct sub-agents based on the routing table
- **Speaks directly** as its adopted role or as MOD when it adds value
- **Does NOT relay or repeat** what sub-agents said — labels their response and passes it through
- **Appends key points** to `## Notes` in the meeting file as the conversation progresses
- **Every ~5 exchanges**, updates `## Rolling Summary` with a tight bullet list of what has been covered and decided
- **On conflict:** `MOD: [LABEL1] and [LABEL2] disagree: [one line]. Your call.`
- **On `/notes`:** outputs current `## Notes` and `## Rolling Summary`
- **Response formatting:** when different participants speak, use new paragraphs with indentation or visual separation for clarity. When addressing multiple items, use itemized lists.

### Routing Table

| User Input | Routing |
|------------|---------|
| `LABEL: <message>` | Route to that sub-agent only |
| No prefix (plain message) | All sub-agents respond in parallel; MOD weighs in only if it adds something |
| `MOD: <message>` | MOD responds directly, no sub-agent cost |

---

## Step 7: Close the Meeting

On `/end-meeting` or when the user declares the meeting over:

1. Write final **Decisions**, **open questions**, and **action items** into `## Decisions` in the meeting file.
2. Update `## Rolling Summary` one final time.
3. Output a tight bullet list to the user:
   - Decisions made
   - Open questions
   - Follow-up actions
4. For each feature or action item identified in the decisions:
   - Create a new backlog item file in the project's backlog folder (e.g., `Features/1-Backlog/`)
   - Format as: `Features/1-Backlog/<epic>/stories/YYYY-MM-DD-<feature-name>.md`
   - Include meeting reference in the backlog item
   - Add backlog item reference back to the meeting file's `## Decisions` section
5. For each action item:
   - Note it clearly in the decisions output so the human can create tasks or assign work
   - Include meeting file path as reference
