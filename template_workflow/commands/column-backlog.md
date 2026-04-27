# Column: Backlog

**What:** Create new features, epics, and tasks. Get initial approval before moving to HLD.

**When to use this:** You are creating new work items that need to enter the Kanban workflow.

---

## Kanban Item Hierarchy

All items use **4-char hex IDs**. Structure:

```
Epic folder: ai-agnostic-prompting/
  ├─ ai-agnostic-prompting-49b5.md          (optional: epic definition)
  │
  ├─ modular-ai-toc-pipelines-ccfb.md       (feature stub in Backlog)
  │
  ├─ modular-ai-toc-pipelines-HLD.md        (HLD, moves through columns)
  │                                           Backlog → HLD → HLD-Review → Task → ...
  │
  └─ modular-ai-toc-pipelines/              (feature folder, created at Task column)
      ├─ build-tool-choice-a3f9-ccfb-49b5.md       (task 1)
      ├─ reference-syntax-d7e2-ccfb-49b5.md        (task 2)
      └─ vscode-extension-f1c4-ccfb-49b5.md        (task 3)
```

**Item Types:**
- **Epic:** Large initiative (e.g., "AI Agnostic Prompting"). Folder contains feature files + optional epic definition.
- **Feature:** User-facing capability. In Backlog as `{name}-{id}.md`. HLD is sibling `{name}-HLD.md` (moves through columns). Feature folder created at Task column.
- **Task:** Implementation unit. Created at Task column as children of feature. Format: `{name}-{taskid}-{featureid}-{epicid}.md`.

---

## ID Generation

**All items must have 4-character hex IDs.** Generate with:

```bash
python3 -c "import secrets; print(secrets.token_hex(2))"
```

Produces: `a3f9`, `ccfb`, `49b5` — always exactly 4 characters. Used in frontmatter `id:` field and filenames.

---

## Creating a Feature

Use the feature template:

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

## Feature Stub Format

```markdown
---
id: a3f9                ← 4-char hex, generated at creation
epic: 49b5              ← parent epic ID
feature: a3f9           ← same as id for feature-level stubs
title: Feature title
type: feature
assignee: architect
review_gate: yes
approved: no
depends_on:             ← comma-separated 4-char hex ids; leave empty if none
---

## Feature

**What:** one paragraph
**Why:** the problem it solves
**Scope:** what is in
**Out of Scope:** what is not
```

---

## Creating an Epic

Epics group related features.

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

## What Does NOT Belong Here

- Tasks (created in Task column after HLD)
- Gherkin (written at TaskReview)
- Architecture (written at HLD)
- LLD (written at TaskReview)

---

## Definition of Done

- [ ] Feature file created with all sections
- [ ] CSV entry added
- [ ] Dated comment added (who created, when, why)
- [ ] Human approval obtained
- [ ] Ready to move to HLD column
