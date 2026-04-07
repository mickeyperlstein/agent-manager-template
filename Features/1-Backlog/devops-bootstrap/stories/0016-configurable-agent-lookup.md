---
id: "0016"
title: Configurable agent lookup order via CONFIG file
column: backlog
assignee: architect
review_gate: yes — HLD reviewed for config format and backward compatibility
---

## Story
As a project maintainer, I want the agent lookup priority order to be configurable via a CONFIG file instead of hardcoded in README/meeting-protocol, so that I can customize agent resolution without modifying template files.

## Background
Currently, the agent lookup order is hardcoded in `README.md` lines 135-146 and referenced in `meeting-protocol.md` Step 1:

1. `<project-root>/ai/agents/<name>.md` (project-level overrides)
2. `<project-root>/template_workflow/agents/<name>.md` (template defaults)
3. `~/ai/agents/<name>.md` (user-global agents)
4. `~/.claude/`, `~/.windsurf/`, etc. (AI tool folders — speculative fallback)

This is a "priority matrix" that users may want to customize per-project. Making it configurable increases flexibility without breaking the template.

## Scope

### CONFIG file design
- Location: `<project-root>/ai/config.yaml` (or `.json` — TBD in HLD)
- Schema: Ordered list of lookup sources with optional paths and conditions
- Default behavior: If no config file exists, use current hardcoded priority matrix
- Override capability: Allow projects to add, remove, or reorder lookup sources

### Example config (YAML sketch):
```yaml
agent_lookup_order:
  - source: project_override
    path: ai/agents
    priority: 1
  - source: template_default
    path: template_workflow/agents
    priority: 2
  - source: user_global
    path: ~/ai/agents
    priority: 3
  - source: ai_tool_folders
    paths: [~/.claude, ~/.windsurf, ~/.cursor, ~/.cline]
    pattern: agents/{name}.md
    priority: 4
```

### Meeting protocol update
- Step 1 in `meeting-protocol.md` checks for `ai/config.yaml` first
- If found: use configured lookup order
- If not found: use hardcoded fallback (current behavior)
- Document the config file option in README.md

### Backward compatibility
- No breaking changes — existing projects without `ai/config.yaml` continue to work
- Template `template_workflow/agents/` remains the SOT for defaults

## Acceptance Criteria
- [ ] HLD defines config file format (YAML vs JSON), schema, and error handling
- [ ] `ai/config.yaml` (or chosen format) is parsed and validated on `/meeting` invocation
- [ ] Custom lookup order is respected when resolving agent files
- [ ] Fallback to hardcoded order when config file is absent
- [ ] README.md updated to document the configuration option
- [ ] Meeting protocol updated to check config file before applying defaults
- [ ] Error messages clearly indicate when config parsing fails vs agent not found
- [ ] Unit tests for config parsing and lookup order resolution

## Dependencies
- 0015 (meeting workflow — baseline for agent lookup logic)

## Notes
Reference: README.md lines 135-146 (Agent Lookup Order), meeting-protocol.md Step 1

## Comments
**2026-04-07 — architect (backlog creation):** Created from user observation that the hardcoded priority matrix should be configurable. Scoped as a backlog feature pending HLD for config format decisions.
