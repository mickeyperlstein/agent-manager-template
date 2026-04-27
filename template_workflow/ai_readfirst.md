# AI Agent: Read This First

**Before you do anything in this repository, read this entire file.**

This is the authoritative guide for AI agents working in this project. All `.CLAUDE.md`, `cline.md`, and similar ai agent files are hardlinks to this document.

---

## 1. Startup Protocol (MANDATORY)

Before taking any action:

1. **Understand the Kanban workflow** — Read [template_workflow/Agent-HowTos/Kanban.md](../Agent-HowTos/Kanban.md) in full
2. **Run housekeeping** — Execute `/housekeeping` to prune stragglers and reset state
3. **Read tasks.csv** — Understand which tasks are in which columns
4. **Confirm your column** — You can only work on tasks in these columns:
   - `1-Backlog` (create features/epics)
   - `2-HLD` (design multi domain architecture)
   - `3-HLD-Review` (present HLD for review)
   - `4-Task` (create task LLDs)
   - `5-TaskReview` (present tasks for review)
   - `6-Implementation` (write code)
   - `7-Test` (verify quality)
   - `8-Review` (conduct reviews)

If your assigned work is in any other column, stop and report to the human.

---

## 2. Gate Rules (NO EXCEPTIONS)

1. **Never skip a gate.** Not for urgency, simplicity, or pressure.
2. **Never move tasks between columns.** Only humans commit column movements.
3. **Never suggest fast-tracking.** If you're tempted, it's a process violation.
4. **Never implement work from a future column.** Stay in your lane.
5. **SRP Pragmatically** — Always CBA clustering vs splitting code.
6. **Think Big, Act Small + OCP** — Design for extension, implement for scope.
7. **Low code, DRY, clean flows** — One flowing test > fifty fragmented tests.
8. **No NIH** — Search standards → libraries → docker → custom (strict order).
9. use clear code clear naming conventions for everything, sections, filenames, item names, everything - if it requires a mandatory doc read - its not well named.

---

## 3. Your Column: What to Do

Navigate to your column's command:

- **Backlog:** [column-backlog.md](../commands/column-backlog.md)
- **HLD:** [column-hld.md](../commands/column-hld.md)
- **HLD-Review:** [column-hld-review.md](../commands/column-hld-review.md)
- **Task:** [column-task.md](../commands/column-task.md)
- **TaskReview:** [column-task-review.md](../commands/column-task-review.md)
- **Implementation:** [column-implementation.md](../commands/column-implementation.md)
- **Test:** [column-test.md](../commands/column-test.md)
- **Review:** [column-review.md](../commands/column-review.md)

Each command explains:
- What artifacts belong in this column
- Gate requirements to enter/exit
- Your responsibilities
- Success criteria
- Definition of done

---

## 4. Key Files (Know These)

| File | Purpose | Read When |
|------|---------|-----------|
| [agent-manager-claude.md](../../agent-manager-claude.md) | Authoritative rules + gate rules | Before any work |
| [column-*.md](../commands/column-backlog.md) | Column-specific protocols | Before working in a column |
| [feature-hld-template.md](../templates/feature-hld-template.md) | HLD template | Creating features |
| [task-lld-template.md](../templates/task-lld-template.md) | Task LLD template | Creating tasks |
| [tasks.csv](../../tasks.csv) | Kanban board state | Finding what to work on |

---

## 5. Artifact Protocol

Every session that modifies a file MUST add a dated comment:

```markdown
## Comments

**YYYY-MM-DD — [your role] ([context]):** What you did and why
```

No file modified without this entry. No exceptions.

---

## 6. If Blocked or Unsure: PAUSE and Escalate

**Don't guess. Don't continue with assumptions. Escalate.**

### When to Escalate
- When multiple options exist and your decision may break other rules its an open question
- Open question blocks progress (can't move forward without clarity)
- Architectural decision has multiple valid paths (ambiguous HLD)
- Gate rule seems to conflict with your current task
- Anything that would waste time if you guessed wrong

### How to Escalate

1. **PAUSE your current task**
2. **State the blocker clearly:**
   - What decision/question is blocking you?
   - What options exist?
   - ref the sources that are creating the question?
   - What information would unblock you?
3. **Escalate to senior** — whoever can respond and defend the decision
   - **Architecture decision** → escalate to senior-architect (agent or human who owns architecture)
   - **Implementation decision** → escalate to senior-implementer (agent or human who reviews code)
   - **Business/scope decision** → escalate to **HUMAN via meeting** (project owner, PM, stakeholder)
   - **Process decision** → escalate to whoever enforces the process (lead agent or human)

4. **If escalating to HUMAN:** Follow the meeting protocol
   - Read: [template_workflow/commands/meeting-protocol.md](../commands/meeting-protocol.md)
   - Use the `/meeting` command with your blocker as agenda and reference meterials in the correct sections
   - Present issue, options, and what you need decided
   - Wait for human decision
   - Exit meeting and RESUME your task

5. **If escalating to agent:** Post your blocker clearly and wait for response

6. **When response given (human or agent), ask to RESUME your task**

**Example:**
```
BLOCKED: HLD specifies "support multiple auth methods (OAuth2/SAML/LDAP)"
but Task only implements OAuth2. Should I:
  A) Design interface for all three, implement one?
  B) OAuth is a standard protocol with multiple multi star libs. Should I use libraryX, or libraryY - CBA is indecisive.
  B) Design/implement OAuth2 only, leave extensibility for future?
  C) Something else?

Pausing implementation until clarity. Ready to start Blocker Meeting - recommending to ad Senior Architect and PM. I will resume when meeting ends and I am unblocked Unless otherwise commanded.
```

### Quick Reference

- **Question about your column?** Read the [column command](#3-your-column-what-to-do)
- **Question about code style?** See [Gate Rules](#2-gate-rules-no-exceptions) above
- **Question about architecture?** Read the HLD file in Features/3-HLD-Review/
- **Still unsure after reading?** PAUSE and escalate (don't let it sit and don't just solve by throwing more code at it)

---

## 7. Remember

- **Think big, act small** — design for the future, implement for now
- **DRY obsessively** 
  - one long test is better than fifty short tests
  - one source of truth is better than multiple scattered docs
- **NIH** — use standards, multistar libraries, known dockers before custom code
- **Respect gates** — they exist to keep work clean and reviewable

---

**This file is your north star. Everything else links back to it.**

Questions? Read the relevant command file. Still stuck? Escalate.
