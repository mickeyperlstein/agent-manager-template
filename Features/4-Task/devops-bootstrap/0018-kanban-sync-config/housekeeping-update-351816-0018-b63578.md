---
id: 351816
feature: 0018
epic: b63578
status: Task
type: task
review_gate: yes
---

# Task: Update housekeeping protocol for SOT authority

## What
Update `template_workflow/commands/housekeeping-protocol.md` to respect SOT configuration. Step 1 (Rebuild task state from folders) should only run if SOT is "folders", not "csv".

## Scope
- Modify Step 1 in housekeeping protocol
- Add SOT check: if SOT is CSV, skip folder-to-CSV rebuild
- If SOT is Folders, run rebuild as currently documented
- Document the reason for the conditional step

## Acceptance Criteria
- [ ] Protocol checks SOT before running Step 1
- [ ] CSV is safe (won't be overwritten if it's SOT)
- [ ] Folders SOT case still works
- [ ] Documentation is clear about why step is conditional

## Test Conditions
- With `sot: csv`, Step 1 is skipped with explanation
- With `sot: folders`, Step 1 runs as before
- Protocol explains the safety logic
- No other steps are affected

## Definition of Done
- [ ] Housekeeping protocol updated
- [ ] Documentation reviewed and approved
- [ ] Manual test confirms behavior with both SOT values

## Comments

**2026-04-10 — architect (task creation):** Created task stub as part of HLD decomposition for feature 0018.
