---
id: "0011"
title: MCP servers sync script (canonical → all tools)
status: backlog
assignee: architect
depends_on: "0006"
review_gate: yes
---

## Story
As the team, I want a single `template_workflow/mcp-servers.json` as the canonical MCP server registry, with a sync script that writes the correct config to each tool's expected location — so adding an MCP server once propagates everywhere.

## Acceptance Criteria
- [ ] `template_workflow/mcp-servers.json` schema defined (server name, command, args, env, tools enabled per agent)
- [ ] `scripts/sync-mcp.sh` reads canonical JSON and writes to:
  - Claude Code: `~/.claude/claude_desktop_config.json` (or `.claude/mcp.json` in project)
  - Windsurf: wherever research (0006) confirms Windsurf reads MCP config
  - Cline: wherever research (0006) confirms Cline reads MCP config
- [ ] Script is idempotent
- [ ] Script handles missing tool gracefully (skip, warn — don't fail)
- [ ] Lives in `agent-manager` repo (0001), consumed by perli via subtree

## Dependencies
- 0006 (research must confirm each tool's MCP config path)

## Notes
MCP config locations vary by OS and tool version. Research (0006) is the source of truth.
