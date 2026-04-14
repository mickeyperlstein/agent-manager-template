---
id: a4c1
epic: 6099
feature: a4c1
title: Push-to-Template Automation Script
type: feature
assignee: architect
review_gate: yes
approved: no
priority: high
depends_on:
---

## Feature

**What:** Automated script that maintains a clean checkout of main branch, merges dev commits, removes dev-only artifacts, and pushes clean template to origin/main.

**Why:** Downstream users need a clean template without the template project's own Features/, meetings/, tasks.csv artifacts.

**Scope:**
- Bash wrapper: manages cache folder, checkout, merge
- Python script (existing push_template.py): filters and pushes
- Git merge --ff-only
- Remove: Features/, meetings/, tasks.csv, push_to_template.py, push_template.sh
- CI-friendly

**Out of Scope:**
- Complex error recovery
- Multi-branch support
