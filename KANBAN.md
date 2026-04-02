# Kanban

**SOT:** `tasks.csv` — run `scripts/folders_to_csv.py` to sync folders → CSV.
**Agents:** read CSV on startup, act on stories where `column = HLD`, `column = Implementation`, or `column = Testing-Agent`.
**Test routing:** after Implementation → `Testing-Agent` if tests can be automated, else `Testing-Manual` (default — never halt).
**CTO gate:** only CTO may commit a story from TaskReview → Implementation.

## HARD RULES — no exceptions, no shortcuts, not even for this repo

1. **Gates are not optional.** Every feature passes through every column in order. No skipping.
2. **No agent may suggest bypassing a gate** — not for urgency, not for simplicity, not because the CTO is present.
3. **No agent may move a feature forward** — with one exception: the HLD agent moves a completed HLD to `HLD-Review`. All other column moves are human commits only.
4. **"Fast-tracking" is a red flag.** If an agent suggests it, treat it as a process violation.

## Columns

| Column | Type | Who Acts | Folder |
|---|---|---|---|
| Backlog | manual | Human | `Features/1-Backlog/` |
| HLD | agent | Architect agent | `Features/2-HLD/` |
| HLD-Review | manual | Human | `Features/3-HLD-Review/` |
| TaskReview | agent + human | Architect agent + CTO | `Features/4-TaskReview/` |
| Implementation | agent | Implementation agent | `Features/5-Implementation/` |
| Testing-Agent | agent | Testing agent | `Features/6-Testing-Agent/` |
| Testing-Manual | manual | Human | `Features/7-Testing-Manual/` |
| Verified | manual | Human | `Features/8-Verified/` |
| Review | manual | Human | `Features/9-Review/` |
| Done | manual | Human | `Features/10-Done/` |
