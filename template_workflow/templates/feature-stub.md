# Feature Creation Template

Use this template to create features, epics, and tasks in the Kanban workflow.

> **Note:** This project uses **task**, not "story". If you're tempted to create a "story", create a **task** instead.

---

## 🎯 EPIC Template

**File location:** `{epic_id}.md` in `/epics` folder

```markdown
# Epic: <epic_name>

**ID:** <epic_id>  
**Status:** Backlog | HLD | Task | TaskReview | Implementation | Test | Done  
**Assignee:** architect | agent | human  
**Type:** epic  
**Review Gate:** yes | no  

## Summary
<one paragraph describing the epic goal and scope>

## Context
<why is this epic needed, what problem does it solve>

## Deliverables
- <deliverable 1>
- <deliverable 2>
- <deliverable 3>

## Features (Child Items)
- [Feature #0001](0001.md) — <one line>
- [Feature #0002](0002.md) — <one line>

## Success Criteria
- [ ] All features completed
- [ ] All gates passed
- [ ] Documentation updated

## Comments
**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

---

## 📋 FEATURE Template

**File location:** `{feature_id}.md` in `/features` folder or epic subfolder

```markdown
# Feature: <feature_name>

**ID:** <feature_id>  
**Epic:** <epic_id>  
**Status:** Backlog | HLD | Task | TaskReview | Implementation | Test | Done  
**Assignee:** architect | agent | human  
**Type:** feature  
**Review Gate:** yes | no  

## Summary
<one sentence describing what this feature does>

## Goals
- <goal 1>
- <goal 2>

## Scope
<what is included / what is NOT included>

## Requirements
- <requirement 1>
- <requirement 2>

## Tasks (Child Items)
- [Task #0001](0001.md) — <one line>
- [Task #0002](0002.md) — <one line>

## Acceptance Criteria
- [ ] All tasks completed
- [ ] Code reviewed
- [ ] Tests passing

## Comments
**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

---

## ✅ TASK Template

**File location:** `{task_id}.md` in task folder (e.g., `devops-bootstrap/{feature_id}-{task_id}/task.md`)

```markdown
# Task: <task_name>

**ID:** <task_id>  
**Feature:** <feature_id>  
**Epic:** <epic_id>  
**Status:** Backlog | Task | TaskReview | Implementation | Test | Done  
**Assignee:** architect | agent | human  
**Type:** task  
**Review Gate:** yes | no  

## Summary
<one line describing what needs to be done>

## Description
<detailed explanation of the work>

## Implementation Details
- <detail 1>
- <detail 2>

## Testing
<how will this be tested>

## Definition of Done
- [ ] Code written
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Review completed

## Comments
**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

---

## 🔄 CSV Entry Format

Add corresponding entries to `tasks.csv`:

```csv
id,epic,feature,task,status,assignee,column,type,review_gate,path
{id},{epic_id},{feature_id},{task_id},backlog,architect,Backlog,{type},yes,{path}
```

**Columns explained:**
- `id` — Unique identifier (alphanumeric, kebab-case)
- `epic` — Parent epic ID (or epic name if root epic)
- `feature` — Parent feature ID (optional)
- `task` — Task ID
- `status` — Current workflow status
- `assignee` — `architect`, `agent`, or `human`
- `column` — Kanban column (Backlog, HLD, Task, TaskReview, Implementation, Test, Done, Review)
- `type` — `epic`, `feature`, or `task`
- `review_gate` — `yes` or `no` (if gate required)
- `path` — File path to the artifact

---

## 📝 Artifact Protocol Rules

**MANDATORY:** Every session that modifies an epic, feature, or task MUST append a dated comment:

```markdown
## Comments
**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

No file may be modified without this entry dated **today**.

---

## ✨ Quick Checklist

When creating new work items:

- [ ] Choose unique ID (check `tasks.csv` for conflicts)
- [ ] Use correct template (epic → feature → task)
- [ ] Create markdown file in appropriate folder
- [ ] Add entry to `tasks.csv`
- [ ] Set initial status to `Backlog`
- [ ] Fill in all required fields
- [ ] Add dated comment if modifying existing item
- [ ] Link parent items in "child items" sections
- [ ] **If you're thinking "story" — use TASK instead**
