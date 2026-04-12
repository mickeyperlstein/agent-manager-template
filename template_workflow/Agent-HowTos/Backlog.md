# Backlog

The Backlog holds **feature stubs only** — one file per feature, no tasks yet.

## Kanban Item Hierarchy

All are **items** with 4-char hex IDs. Visual structure:

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
      ├─ build-tool-choice-a3f9-ccfb-49b5.md       (task 1, child)
      ├─ reference-syntax-d7e2-ccfb-49b5.md        (task 2, child)
      └─ vscode-extension-f1c4-ccfb-49b5.md        (task 3, child)
```

**Item Types:**
- **Epic:** Large initiative/theme (e.g., "AI Agnostic Prompting"). 4-char hex ID. Folder contains feature files + optional epic definition.
- **Feature:** User-facing capability. In Backlog as `{feature}-{id}.md`. HLD is a sibling `{feature}-HLD.md` (moves through columns). Feature folder created at Task column (children = tasks).
- **Task:** Implementation unit. Created at Task column as children of feature folder. File format: `{name}-{taskid}-{featureid}-{epicid}.md` with all 4-char hex IDs.

## File Path

```
Features/1-Backlog/{feature}.md
```

## Feature Stub Format

```markdown
---
id: a3f9                ← 4-char hex, generated at creation
epic: 49b5              ← 4-char hex id of the epic this feature belongs to
feature: a3f9           ← 4-char hex id of this feature (same as id for feature-level stubs)
title: Feature title
type: feature
assignee: architect
review_gate: yes
approved: no
depends_on:             ← comma-separated 4-char hex ids this feature depends on; leave empty if none
---

## Feature

**What:** one paragraph
**Why:** the problem it solves
**Scope:** what is in
**Out of Scope:** what is not
```

## ID Generation

**All Kanban items (epics, features, tasks) must have 4-character hex IDs.** No sequential counter, no coordination needed. Generate with:
```bash
python3 -c "import secrets; print(secrets.token_hex(2))"
```

This produces IDs like `a3f9`, `ccfb`, `49b5` — always exactly 4 characters.

Every item uses the same format: `id` field in frontmatter and `{name}-{id}.md` in filename.

## What Does NOT Belong Here

- Tasks (created in the Task column after HLD)
- Gherkin (written at TaskReview)
- Architecture (written at HLD)
- LLD (written at TaskReview)

## After Backlog

Human moves the file to `2-HLD` when intent is clear enough to design.
