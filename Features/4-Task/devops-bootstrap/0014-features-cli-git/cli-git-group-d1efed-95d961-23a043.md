---
id: "d1efed"
epic: "23a043"
feature: "95d961"
title: CLI git subcommand group
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Extend CLI with `features git` subcommand group.

## Scope
- Update `cli.py` to add `git` Click group
- Register stage, commit, push, undo as subcommands
- Create `commands/git/__init__.py`
- Ensure `features git --help` works

## Acceptance Criteria
- [ ] `features git` is a valid command group
- [ ] `features git stage`, `features git commit`, `features git push`, `features git undo` work
- [ ] `features git --help` shows subcommands
- [ ] Each subcommand has --help

## Test Conditions
- Run `features git --help` → verify subcommands listed
- Run each subcommand --help → verify args documented

## Definition of Done
- CLI extension complete
- All AC met
- Tests pass
