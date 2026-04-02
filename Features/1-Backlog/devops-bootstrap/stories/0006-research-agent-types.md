---
id: "0006"
title: Research agent types — folders, wrappers, MCP, and testing
status: backlog
assignee: architect
depends_on: "0001"
review_gate: yes — output is a written report for Mickey
---

## Story
As the team, we need to know exactly how every major AI coding assistant loads agents/rules, where their configs live, how to test each wrapper manually, and how their MCP server configs are structured — before writing a single stub or sync script.

## Scope — Tools to Research
| Tool | Known config file | Notes |
|---|---|---|
| Claude Code | `CLAUDE.md`, `.claude/agents/` | Confirmed |
| Windsurf | `.windsurfrules` | Confirm exact path |
| Cline | `.clinerules` | Confirm exact path |
| Gemini CLI | `gemini.md` | New — needs research |
| Cursor | `.cursorrules` | Confirm still current |
| Copilot / VS Code | `.github/copilot-instructions.md` | Confirm |

Goal: `template_workflow/rules/global.md` becomes the upstream SOT that compiles into each tool's format.

## Acceptance Criteria
- [ ] Research doc written at `template_workflow/research/agent-types.md`
- [ ] For each tool:
  - Exact folder(s) and filename where rules/agents are loaded from
  - File format and required frontmatter (if any)
  - How the tool discovers project-level vs global-level config
  - Manual test steps Mickey can follow to verify a wrapper loaded correctly
- [ ] MCP servers config location per tool documented
- [ ] Sync strategy documented: canonical `template_workflow/mcp-servers.json` → each tool's config path
- [ ] Mapping table: `rules.md section` → `tool config file` for the compiler script (0011)

## Output
`template_workflow/research/agent-types.md` — delivered to Mickey for review before any stubs are written.

## Notes
This unblocks 0008, 0009, 0010, and 0011. No code written here — research and documentation only.
Gemini CLI config convention (`gemini.md`) flagged 2026-04-02 — verify it's not `GEMINI.md` or something else.
