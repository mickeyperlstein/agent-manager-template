# Agent Manager Template

[![Template Version](https://img.shields.io/github/v/release/mickeyperlstein/agent-manager-template?label=template)](https://github.com/mickeyperlstein/agent-manager-template/releases)

A GitHub template repository for teams using AI coding assistants (Claude, Windsurf, Cline, etc.) with structured Kanban workflow governance.

## What This Is

This repository provides:

1. **Kanban-as-Code** — Your project board lives in `Features/` folder structure, version-controlled with git
2. **Agent Governance** — Clear rules for when AI agents write design docs vs code vs tests
3. **CSV Sync** — Bidirectional sync between folder structure and `tasks.csv` for Google Sheets/GitHub Projects import
4. **Automatic Housekeeping** — Prunes empty folders and fixes stragglers at every startup

## Who This Is For

If you want to use AI coding assistants (Claude, Windsurf, Cline, etc.) with structured workflow governance, this template is for you.

You build a team in your IDE with each agent having specific roles and responsibilities. Agents and humans work together on tasks in a structured Kanban workflow where **you** (the human) gatekeep all column transitions.

---

## Quick Start

**New project:**
```bash
git clone https://github.com/mickeyperlstein/agent-manager-template.git my-project
cd my-project && bash setup.sh
```

**Existing project:**
See [agent-manager-template.INSTALL.md](agent-manager-template.INSTALL.md) for adding this template to your repo.

---

## How It Works

### Kanban Board as Folders

```
Features/
├── 1-Backlog/          # Raw intent — feature stubs
├── 2-HLD/              # High-level design (agent writes)
├── 3-HLD-Review/       # Human approves design
├── 4-Task/             # Task decomposition (agent creates subtasks)
├── 5-TaskReview/       # Low-level design + test spec (agent adds, human approves)
├── 6-Implementation/   # Code & tests (agent writes)
├── 7-Test/             # Test results (agent verifies)
├── 8-Review/           # PR review (human approves)
└── 9-Done/             # Merged & complete
```

**Stories are markdown files** — they move between folders as they progress. A feature stays in one folder until the human commits it forward to the next.

### The Workflow

1. **Human** creates a feature stub in `1-Backlog` with intent and scope
2. **Architect agent** writes high-level design (HLD) → moves to `2-HLD`
3. **Human** reviews HLD → commits to `3-HLD-Review` if approved
4. **Architect agent** decomposes feature into tasks → commits to `4-Task`
5. **Task agent** adds low-level design (LLD) per task → commits to `5-TaskReview`
6. **Human** reviews tasks → commits to `6-Implementation` if approved
7. **Implementation agent** writes code & tests → commits to `7-Test`
8. **Test agent** runs tests → commits to `8-Review` if passing
9. **Human** reviews PR → merges to `9-Done`

**Agents never move files between columns** — only humans commit column transitions.

---

## Installation & Maintenance

📖 **See [agent-manager-template.INSTALL.md](agent-manager-template.INSTALL.md)** for:
- Installing into a **new project**
- Adding to an **existing project**
- **Updating** an existing install
- Handling file conflicts
- Troubleshooting

---

## Commands

| Command | Description |
|---------|-------------|
| `/start [task-id]` | Start working on a task — reads Kanban, confirms scope, begins work |
| `/housekeeping` | Prune empty folders and move stragglers to correct stages |
| `/meeting <participants...>` | Start a multi-agent meeting with named participants |
| `/meeting --working <participants...>` | Convert current chat into a meeting with prior context |
| `/meeting --resume` | Resume a recent meeting |

---

## Agent Lookup Order

When commands like `/meeting` need to find an agent, the lookup order is:

| Priority | Path |
|----------|------|
| 1 | `<project-root>/ai/agents/<name>.md` — project-level overrides |
| 2 | `<project-root>/template_workflow/agents/<name>.md` — template defaults |
| 3 | `~/ai/agents/<name>.md` — user-global agents |
| 4 | `~/.claude/`, `~/.windsurf/`, etc. — AI tool config folders |

---

## Documentation

- **[agent-manager-template.INSTALL.md](agent-manager-template.INSTALL.md)** — Installation & maintenance guide
- **[agent-manager-template.KANBAN.md](agent-manager-template.KANBAN.md)** — Full Kanban workflow rules
- **CLAUDE.md** / **.clinerules** / **.windsurfrules** — Agent-specific rules
- **template_workflow/commands/** — Command protocols (canonical documentation)
- **Features/** — Your Kanban board (version-controlled folder structure)

---

## Repository Structure

```
├── Features/                    # Kanban board (authoritative source)
├── template_workflow/
│   ├── commands/                # Canonical command protocols
│   ├── agents/                  # Template agent definitions
│   ├── scripts/                 # CSV sync, onboarding
│   └── Agent-HowTos/            # Detailed role guides
├── ai/agents/                   # Project-level agent overrides
├── meetings/                    # Meeting artifacts (auto-created)
├── CLAUDE.md                    # Claude Code rules
├── .clinerules                  # Cline rules
├── .windsurfrules               # Windsurf rules
├── setup.sh                     # Initialize folder structure
└── tasks.csv                    # Auto-generated task inventory
```

---

## License

MIT — Use this template for your own projects.
