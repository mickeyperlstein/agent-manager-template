---
epic: 23a043
feature: bd72df
id: fd2dbd
title: Migrate existing feature files from sequential to hex ids
type: task
assignee: architect
review_gate: yes
approved: no
depends_on:
---

## What
Update all existing files in `Features/` to replace sequential numeric ids (0001, 0002, ...) with short hex ids — in both frontmatter and filenames.

## Scope
- In: all .md files under Features/ with sequential ids
- Out: HLD content, folder structure

## Acceptance Criteria
- [ ] All frontmatter `id:` fields replaced with unique hex ids
- [ ] Filenames updated to match (e.g. `0001-name.md` → `a3f9c1-name.md`)
- [ ] No duplicate hex ids across all files
- [ ] `depends_on` references updated to new hex ids where applicable
- [ ] tasks.csv regenerated after migration

## Test Conditions
- Run folders_to_csv.py after migration → all ids in CSV are hex format → no sequential ids remain
- No duplicate ids in CSV → log: sync complete with correct item_count

## Definition of Done
- [ ] All files migrated
- [ ] tasks.csv regenerated and validated
- [ ] No broken depends_on references
