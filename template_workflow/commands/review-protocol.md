# Review Protocol

Usage: `/review <id>`

---

A review is a **collaborative critique meeting** where a Presenter defends their work (HLD or Task implementation) and Reviewers ask questions to identify gaps, risks, or improvements. Reviews are iterative — items cycle back for refinement until accepted. See [meeting-protocol.md](template_workflow/commands/meeting-protocol.md) for the foundational structure; reviews adapt it for the presenter-vs-questioner dynamic.

---

## Step 0: Load Review Context

1. When `/review <id>` is called (or review is triggered):
   - If `<id>` is specified, resolve it:
     - Check `tasks.csv` for a row where `id = <id>` (e.g., `/review 0018` → `kanban sync config HLD`)
     - Or search for `<id>` as a filename pattern (e.g., `/review kanban-sync-config` → `kanban-sync-config-HLD.md`)
   - If no `<id>`, check the current context (user's open file) — if it's in `3-HLD-Review` or `3-TaskReview` folder, use that
   - Locate the file in `Features/3-HLD-Review/` or `Features/3-TaskReview/` (or `Features/4-Task/` for task reviews)
   - Determine the **review type**: `HLD-Review` (architectural) or `Task-Review` (implementation)
   - Read the file entirely to understand what is being reviewed

---

## Step 1: Identify Participants & Roles

**Presenter** (always the assignee of the item being reviewed, unless otherwise noted):
- The agent assigned to the specific HLD or Task file
- The Presenter defends the work from the file itself — they come prepared

**Reviewers** (questioners):
- All other participants explicitly named, or:
- Default: relevant domain experts (e.g., for an HLD review, include security, ops, product if interested parties)
- Reviewers come to ask questions and identify issues
- If Reviewer not specified, a Senior of the presenter agent will be spawned called Senior-{agent-name} like Senior-architect, Senior-Devops etc.
**MOD** (facilitator):
- You (AI) — routes questions, documents Rolling Summary + Decisions, manages kanban outcomes

For each participant, validate their agent file (search order: project-level → template defaults → user-global → common tool folders). Stop if any agent file is missing; ask the user to resolve before proceeding.

---

## Step 2: Spawn Review Meeting

1. Load each Reviewer's agent file (use their identity + review protocol rules).
2. Spawn sub-agents with:
   - Their identity + review protocol (below) + review background (file being reviewed + type)
   - Full text of the file being reviewed (so Presenter and Reviewers arrive informed)
3. You adopt the Presenter's identity directly (no spawn cost).

### Review Protocol — Injected Into Every Sub-Agent

> You are in a review. A Presenter (the Owner) is defending their work. Your role is to ask tough questions to identify gaps, risks, or improvements dont forget testplans and documentation.
>
> Keep your expertise — but stay concise: 1-3 sentences per question or comment. No preamble, no summary.
>
> Before speaking: Does this question or concern matter? If yes, ask it. If no, stay quiet. Silence is valid.
>
> You may ask the Presenter directly or raise concerns to the room. Listen to other Reviewers too — build on their questions.
>
> The Presenter will answer from the file. The MOD routes and documents.
>
> Tokens cost real money. Earn every word.

---

## Step 3: Open the Review

Introduce the review:

1. **File being reviewed:** []() Path, type (HLD-Review or Task-Review) file for user to cmd-click and open
2. **Participants:**
   - `MOD + PRESENTER: <Model> — [Presenter role] + facilitator`
   - `REVIEWER [LABEL]: <Model> — [role] — <agent file path>`
   - (one line per reviewer)

3. **Show commands:**
   ```
   Review commands:
   - REVIEWER: <question> — ask the Presenter a question
   - PRESENTER: <response> — answer from the file
   - MOD: <note> — document a key point (no sub-agent cost)
   - /notes — show current Questions/Answers + Rolling Summary
   - /pause — pause the review
   - /resume — resume the review
   - /end-review — close the review and produce decisions
   ```
4. **Auto-pitch opening context:** The Presenter automatically gives a 1-minute pitch on what this is and why it matters. and make sure to highlight what stays and what changes in flows.

---

## Step 4: During the Review — MOD Responsibilities

**Routing:**
- `REVIEWER: <question>` → route to Presenter, wait for answer
- All Reviewers can ask follow-up or side questions in parallel
- `PRESENTER: <response>` → MOD logs it, passes to room
- `/notes` → show current Q&A summary + Rolling Summary

**Documentation (breadcrumbs, not stenography):**
- Keep a running list of **Questions Asked** (by whom, brief version)
- Log **Presenter Answers** (one line each)
- Every ~5-7 questions, update **Rolling Summary**: what's been covered, any concerns emerging, consensus forming
- Flag **concerns/gaps** as they surface

**On conflict:** `MOD: [REVIEWER1] and [REVIEWER2] disagree on [X]. Presenter, how do you address both?`

**Tone:** You are the Presenter here too — if the file is solid, say so. If you spot an issue the Reviewers missed, raise it. Don't hide behind facilitation.

**continue asking questions** until you feel confident that the file is ready for the next step. and no participantr has any questions. last question needs to be "Any more questions"? when no more questions, summarize the review and move to the next step.
---

## Step 5: Close the Review

On `/end-review` or `accept` or when all questions are answered:

1. Tally **Decisions** — what needs to be fixed (if anything)?
2. Update **Rolling Summary** one final time.
3. **Determine outcome:**
   - ✅ **Accepted** — no changes needed, move to next column
   - ❌ **Not Accepted** — significant issues, return to source column (Task or HLD) for rework
   - ⚠️ **Accepted with Conditions** — move forward, but specific items must be addressed before merge/deployment

4. Output a summary to the user:
   ```
   Outcome: [Accepted / Not Accepted / Accepted with Conditions]
   Action Items:
   - [item 1]
   - [item 2]
   Kanban movement: [source column] → [destination column]
   ```

---

## Step 6: Kanban Movement & Iteration

**After review closes:**

1. Add a new `# Review [YYYY-MM-DD]` section at the bottom of the file (see template below).
2. Document the review outcome.
3. **If Accepted or Accepted with Conditions:**
   - File moves out of `3-HLD-Review` or `3-TaskReview` to the next column
   - If Accepted with Conditions, action items must be tracked (inline notes or backlog ticket)
4. **If Not Accepted:**
   - File returns to source column (e.g., `3-HLD-Review` → `2-HLD`)
   - Presenter addresses feedback
   - File re-enters review cycle (new `# Review [date]` section added on next review)

Multiple review cycles build a **history** at the bottom of the file — each review cycle gets its own dated section.

---

## Review Section Template

Add this to the **bottom of the file being reviewed** for each review cycle:

```markdown
# Review [YYYY-MM-DD]

## Participants
- Presenter: [agent name]
- Reviewers: [agent1], [agent2], [agent3]

## Questions & Answers
- Q (Reviewer name): [question]
- A (Presenter): [answer]
- Q (Reviewer name): [follow-up]
- A (Presenter): [answer]

## Rolling Summary
- [Key topic covered, direction]
- [Emerging concern or consensus]

## Decisions
- [What needs to be fixed / addressed]
- Outcome: Accepted | Not Accepted | Accepted with Conditions
- Kanban movement: [from] → [to]
```

Each review cycle appends a new section, so the file builds a review history over time.

---

---

## Current Items in Review

**HLD Reviews (3-HLD-Review):**
- `Features/3-HLD-Review/devops-bootstrap/kanban-sync-config-HLD.md`
- `Features/3-HLD-Review/devops-bootstrap/4char-hash-ids-HLD.md`

**Task Reviews (3-TaskReview):**
- None

---

## Comments

**2026-04-11 — Claude (review-protocol creation):** Structured review-protocol to mirror meeting-protocol's clarity while adapting for the Presenter-vs-Reviewer dynamic. Reviews are iterative, simpler than meetings (no backlog creation, no template file — just inline sections), and move items back for rework if not accepted.