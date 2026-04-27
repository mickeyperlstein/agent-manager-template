# Column: Backlog

**What:** Create new features, epics, and tasks. Get initial approval before moving to HLD.

**When to use this:** You are creating new work items that need to enter the Kanban workflow.

---

## Creating a Feature

Use the feature template as your starting point:

See: [feature-hld-template.md](../templates/feature-hld-template.md)

**Checklist:**

- [ ] Feature has unique 4-char hex ID (e.g., `a4c1`)
- [ ] Epic ID is correct (links to parent epic)
- [ ] Title is clear and specific
- [ ] Scope section: what IS included, what IS NOT
- [ ] Why: explain the problem this solves
- [ ] Acceptance criteria are measurable and testable
- [ ] Definition of Done is explicit
- [ ] Add dated comment with your name and context

**Before moving to HLD:**
- [ ] Feature is approved by human
- [ ] No dependencies blocked
- [ ] Ready for architectural design

---

## Creating an Epic

Epics group related features. Use feature-stub.md as reference for structure.

**Checklist:**
- [ ] Epic has unique 4-char hex ID
- [ ] Summary is one paragraph
- [ ] Deliverables are listed
- [ ] Success criteria are defined
- [ ] Child features are linked

---

## Adding to tasks.csv

Every feature/epic must have a CSV entry:

```csv
id,epic,feature,task,status,assignee,column,type,review_gate,path
```

- `id` — 4-char hex, unique
- `status` — backlog
- `column` — Backlog
- `type` — epic or feature
- `review_gate` — yes or no (require gate before HLD?)
- `path` — file path to the artifact

---

## Definition of Done (Backlog)

- [ ] Feature file created with all sections
- [ ] CSV entry added
- [ ] Dated comment added (who created, when, why)
- [ ] Human approval obtained
- [ ] Ready to move to HLD column
