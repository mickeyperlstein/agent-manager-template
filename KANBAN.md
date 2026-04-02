# Kanban

**SOT:** `tasks.csv` — run `scripts/kanban-csv-sync.sh` to sync folders ↔ CSV ↔ Sheets.
**Agents:** read CSV on startup, act on stories where `column = InProgress` or `column = Testing-Agent`.
**Test routing:** after InProgress → `Testing-Agent` if tests can be automated, else `Testing-Manual` (default — never halt).
**CTO gate:** only CTO may commit a story from TaskReview → InProgress.

## HARD RULES — no exceptions, no shortcuts, not even for this repo

1. **Gates are not optional.** Every feature passes through every column in order. No skipping.
2. **No agent may suggest bypassing a gate** — not for urgency, not for simplicity, not because the CTO is present in the conversation.
3. **No agent may move a feature forward** — column moves are human commits only (CTO for TaskReview→InProgress, any human for others).
4. **"Fast-tracking" is a red flag.** If an agent suggests it, the CTO should treat it as a process violation.

## Columns

| Column | Type | Folder |
|---|---|---|
| Backlog | manual | `Features/1-Backlog/` |
| HLD | manual | `Features/2-HLD/` |
| TaskReview | manual | `Features/3-TaskReview/` |
| InProgress | agent | `Features/4-InProgress/` |
| Testing-Agent | agent | `Features/5-Testing-Agent/` |
| Testing-Manual | manual | `Features/6-Testing-Manual/` |
| Verified | manual | `Features/7-Verified/` |
| Review | manual | `Features/8-Review/` |
| Done | manual | `Features/9-Done/` |
