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

**What:** A simple web UI to visualize and manage Kanban board state across all 9 columns, query items by epic/status/metadata, and identify bottlenecks at a glance and help determine/define priority.

**Why:** Currently tasks.csv is static and queryable only with grep/awk. A dashboard makes it easy to see real-time Kanban state, spot stuck work (e.g., 37 items in Column 4), and validate metadata compliance across 60+ items.

** How:**:
Create Kanban UI with tasks moved from side to side, left to right. allow certain columns to have different colors. epics have a color and can be fltered out for clarity

**Scope:**
- Backend: Flask (Python), read/write tasks.csv directly
- Column view showing item counts and summary
- Filter by epic, column, ID format, status
- Search by item name/ID
- Highlight metadata gaps (missing implementation_artifacts, unresolved depends_on, etc.)
- Move items between columns via UI → updates tasks.csv → trigger sync script
- Export current state as JSON
- Frontend: simple HTML/JS (TBD in HLD)

**Out of Scope:**
- Real-time sync or webhooks
- Authentication/multi-user
- Analytics or velocity tracking (v2)
- Complex querying (DuckDB deferred)
