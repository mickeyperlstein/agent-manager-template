# Backlog

The Backlog holds **feature stubs only** — one file per feature, no tasks yet.

## File Path

```
Features/1-Backlog/{feature}.md
```

## Feature Stub Format

```markdown
---
id: a3f9c1              ← short hex, generated at creation (e.g. python3 -c "import secrets; print(secrets.token_hex(3))")
title: Feature title
type: feature
assignee: architect
review_gate: yes
approved: no
depends_on:             ← comma-separated hex ids this feature depends on; leave empty if none
---

## Feature

**What:** one paragraph
**Why:** the problem it solves
**Scope:** what is in
**Out of Scope:** what is not
```

## ID Generation

IDs are short hex strings — no sequential counter, no coordination needed. Generate with:
```bash
python3 -c "import secrets; print(secrets.token_hex(3))"
```

## What Does NOT Belong Here

- Tasks (created in the Task column after HLD)
- Gherkin (written at TaskReview)
- Architecture (written at HLD)
- LLD (written at TaskReview)

## After Backlog

Human moves the file to `2-HLD` when intent is clear enough to design.
