---
id: 5829
epic: 6099
feature: a4c1
title: Merge & Commit (Artifact Removal)
type: task
assignee: architect
review_gate: no
depends_on: "6eb3,e329"
---

## Task: Merge & Commit (Artifact Removal)

**What:** Implement git merge --ff-only, staging, and removal commit.

**Acceptance Criteria:**
- [ ] `git merge --ff-only dev` executes
- [ ] Fails gracefully if not fast-forward (exits with error)
- [ ] Stages only allowed files: `git add <allowed_files>`
- [ ] Creates commit: "chore: merge dev changes to template"
- [ ] Error handling: clear message if merge fails

**Definition of Done:**
- [ ] Functions: merge_dev(), stage_allowed_files(), commit_removal() implemented
- [ ] Unit tests pass
