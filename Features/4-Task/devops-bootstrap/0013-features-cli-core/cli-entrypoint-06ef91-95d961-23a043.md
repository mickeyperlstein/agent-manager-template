---
id: "06ef91"
epic: "23a043"
feature: "95d961"
title: CLI entrypoint and Click skeleton
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Create the Python package structure and Click-based CLI entrypoint for the features CLI tool.

## Scope
- Create `template_workflow/features/__init__.py`
- Create `template_workflow/features/__main__.py` with `cli()` entrypoint
- Create `template_workflow/features/cli.py` with Click group and stub commands (move, new-id, clean)
- Create `template_workflow/features/commands/__init__.py`
- Create `template_workflow/features/utils/__init__.py`

## Acceptance Criteria
- [ ] `python -m features --help` shows available commands
- [ ] Commands listed: move, new-id, clean
- [ ] Each command has --help that shows expected arguments

## Test Conditions
- Run `python -m features --help` and verify output
- Run `python -m features move --help` and verify output
- Run `python -m features new-id --help` and verify output
- Run `python -m features clean --help` and verify output

## Definition of Done
- All files created with proper structure
- Help output is informative and accurate
- No implementation yet (stubs only)
