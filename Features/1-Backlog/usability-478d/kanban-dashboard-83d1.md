---
id: 83d1
epic: 478d
feature: 83d1
title: Kanban Dashboard
type: feature
assignee: architect
review_gate: yes
approved: no
depends_on:
---

## Feature

**What:** A simple web dashboard to visualize Kanban board state across all 9 columns, query items by epic/status/metadata, and identify bottlenecks at a glance.

**Why:** Currently tasks.csv is static and queryable only with grep/awk. A dashboard makes it easy to see real-time Kanban state, spot stuck work (e.g., 37 items in Column 4), and validate metadata compliance across 60+ items.

**Scope:**
- Read-only dashboard (no mutations via UI)
- Column view showing item counts and summary
- Filter by epic, column, ID format
- Search by item name/ID
- Highlight metadata gaps (missing implementation_artifacts, unresolved depends_on, etc.)
- Export current state as JSON

**Out of Scope:**
- Moving items between columns via UI (keep that as git operations)
- Real-time sync or webhooks
- Authentication/multi-user
- Analytics or velocity tracking (v2)
