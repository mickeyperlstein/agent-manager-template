# Agent Manager Template

A GitHub template repository for teams using AI coding assistants (Claude, Windsurf, Cline, etc.) with structured Kanban workflow governance.

## What This Is

This repository provides:

1. **Kanban-as-Code** — Your project board lives in `Features/` folder structure, version-controlled with git
2. **Agent Governance** — Clear rules for when AI agents write design docs vs code vs tests
3. **CSV Sync** — Bidirectional sync between folder structure and `tasks.csv` for Google Sheets/GitHub Projects import
4. **Onboarding Scripts** — One-command setup to install Kanban rules into agent memory

## Who This Is For

If you want to use AI coding assistants (Claude, Windsurf, Cline, etc.) with structured workflow governance, this template is for you.

You will build a team in your IDE of choice with each agent having specific roles and responsibilities and work together to complete tasks in a structured Kanban workflow where you (the human) gatekeep task transitions.

## How It Works

### Kanban Board as Folders

```
Features/
├── 1-Backlog/          # {feature}.md — raw intent
├── 2-HLD/              # {feature}-HLD.md — agent writes design
├── 3-HLD-Review/       # human approves HLD
├── 4-Task/             # {feature}/ — agent creates task files
├── 5-TaskReview/       # agent adds LLD + Gherkin; human approves
├── 6-Implementation/   # agent writes code from LLD
├── 7-Test/             # agent runs tests; routes forward or back
├── 8-Review/           # PR open, human reviews
└── 9-Done/             # merged & complete
```

Stories are markdown files that move between folders as they progress.
### Getting Started

### How to install this template

to add the agent-manager workflow to your repo:

1. **Clone the template**:
  **Option A: Git pull from remote (recommended)**
   ```bash
   # Add the template repo as a remote
   git remote add template https://github.com/mickeyperlstein/agent-manager-template.git
   
   # Fetch the template (don't merge — your histories are unrelated)
   git fetch template main

   # clear you repo of any changes
   git stash 
   
   # Checkout template files into your project
   git checkout template/main 
   
   # Commit the imported files
   git add template_workflow agent-manager-template.KANBAN.md agent-manager-template.README.md
   
   # Install template workflow - empty folders and files
   bash ./setup.sh

   # Run onboarding for your AI tool
   ./template_workflow/scripts/windsurf_onboarding.sh
   # or for Claude: ./template_workflow/scripts/claude_onboarding.sh
  
   git commit -m "Add agent-manager-template workflow from upstream"
   
   # return to state before stash
   git stash pop
   ```

4. **Adapt your existing work**: Move any existing tasks/stories into `Features/1-Backlog/` following the story format.

### Handling File Conflicts

When adding the template to an existing project, you may have conflicting files:

agent uses ### AGENT_MANAGER_TEMPLATE_START and ### AGENT_MANAGER_TEMPLATE_END to mark the template sections for your conflict resolution convenience

| Your Project | Template File | Resolution |
|--------------|---------------|------------|
| `CLAUDE.md` | `CLAUDE.md` | **Merge or rename.** Template uses `agent-manager-template.CLAUDE.md`  and has tried to make global changes one liners or sungle paragraphs for easy maintenance
| `.windsurfrules` | `.windsurfrules` | **Merge.** Add the Kanban startup protocol to your existing rules, or rename to keep both. |


**Quick conflict resolution commands:**
```bash
# If you have an existing CLAUDE.md and want both
git checkout template/main -- CLAUDE.md
mv CLAUDE.md agent-manager-template.CLAUDE.md

# Merge .gitignore entries (add these if not present)
echo "meetings/" >> .gitignore
echo "tasks.csv" >> .gitignore
echo "Features/**/temp_*" >> .gitignore
```

## Agent Lookup Order

When commands like `/meeting` need to resolve a participant name to an agent file, the lookup order is:

| Priority | Path | Purpose |
|----------|------|---------|
| 1 | `<project-root>/ai/agents/<name>.md` | **Project-level overrides** — customize an agent for this repo only |
| 2 | `<project-root>/template_workflow/agents/<name>.md` | **Template defaults** — shipped with this template |
| 3 | `~/ai/agents/<name>.md` | **User-global agents** — your personal agents shared across all projects |
| 4 | `~/.claude/`, `~/.windsurf/`, `~/.cursor/`, `~/.cline/` | **AI tool folders** — speculative fallback |

Higher priority wins. To override a template agent for a specific project, create `ai/agents/<name>.md` in your repo — it takes precedence over `template_workflow/agents/<name>.md`.

## Commands

| Command | Description |
|---------|-------------|
| `/start [task-id]` | Start working on a task — reads Kanban state, confirms scope, begins work |
| `/meeting <participants...>` | Start a multi-agent meeting with named participants |
| `/meeting --working <participants...>` | Convert current conversation into a meeting, capturing prior discussion as context |
| `/meeting --resume` | Resume a recent meeting — shows summaries, confirms/modifies participant roster |

## Documentation

- `KANBAN.md` — Full column definitions and workflow rules
- `Features/` — Where you create and move story files organized by status
- `template_workflow/commands/` — Canonical command protocols (agent-agnostic)
- `.windsurfrules` — Windsurf agent behavior rules
- `CLAUDE.md` — Claude Code agent behavior rules
- `.clinerules` — Cline agent behavior rules

## Repository Structure

```
├── Features/              # Kanban board (authoritative source)
├── template_workflow/
│   ├── commands/          # Canonical command protocols (SOT)
│   ├── agents/            # Template-default agent definitions
│   └── templates/         # File templates (meeting stubs, etc.)
├── ai/agents/             # Project-level agent overrides
├── meetings/              # Meeting artifacts (created on first use)
├── scripts/               # Onboarding and sync utilities
├── Docs/                  # Additional documentation
├── KANBAN.md             # Main workflow rules for ai agents
└── tasks.csv             # Generated Kanban export
```

## License

MIT — Use this template for your own projects.
