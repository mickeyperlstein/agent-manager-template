---
id: "0005"
title: Sync stories to GitHub Projects via CSV + CI
status: backlog
assignee: architect
depends_on: s01, s02, s03
review_gate: yes
---

## Story
As the team, I want a CI workflow that reads `tasks.csv` on push and syncs cards to the GitHub Projects board so the board stays current without manual updates.

## Acceptance Criteria
- [ ] `.github/workflows/kanban-sync.yml` created
- [ ] Trigger: push to main
- [ ] Reads `tasks.csv`, creates/moves GitHub Projects cards to correct column
- [ ] Also triggered when a story file moves between column folders (gate-check)
- [ ] `.github/workflows/gate-check.yml` validates required files per column on push

## Dependencies
- s01 (CSV schema must exist)
- s02 (repo must exist)
- s03 (GitHub Projects board must exist)
