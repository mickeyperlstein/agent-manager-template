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

### Full Workflow Diagram

```mermaid
flowchart TD
    subgraph BACKLOG["1 · Backlog  👤 Human"]
        B_in["{feature}.md\n─────────────\n· title · scope\n· out-of-scope"]
    end

    subgraph HLD["2 · HLD  🤖 Architect Agent"]
        H_in["{feature}-HLD.md\n─────────────\n· C4 L1/L2 diagrams\n· Components & data model\n· Task decomposition list"]
    end

    subgraph HLDREVIEW["3 · HLD-Review  👤 Human"]
        HR_in["Human reviews HLD\n─────────────\n· Design sound?\n· Tasks complete?\n· Approve to proceed"]
    end

    subgraph TASK["4 · Task  🤖 Agent"]
        T_in["{feature}/\n─────────────\n· {feature}-HLD.md\n· 0001-{task}.md\n· 0002-{task}.md"]
    end

    subgraph TASKREVIEW["5 · TaskReview  🤖 Architect Agent  →  👤 Human"]
        TR_in["LLD added per task\n─────────────\n· C4 L3 · interfaces\n· sequences · data shapes\n· Gherkin scenarios"]
    end

    subgraph IMPL["6 · Implementation  🤖 Agent"]
        I_in["Code\n─────────────\n· Tests first (TDD)\n· Implements LLD contracts\n· Updates Gherkin checklist"]
    end

    subgraph TEST["7 · Test  🤖 Agent"]
        T2_in["Verify\n─────────────\n· Unit · Integration\n· Acceptance (Gherkin)\n· Routes back if fail"]
    end

    subgraph REVIEW["8 · Review  👤 Human"]
        R_in["PR open\n─────────────\n· Code review\n· Feedback addressed"]
    end

    subgraph DONE["9 · Done  👤 Human"]
        D_in["PR merged\n─────────────\nFeature complete"]
    end

    BACKLOG -->|"Human moves"| HLD
    HLD -->|"Agent moves\nwhen done"| HLDREVIEW
    HLDREVIEW -->|"Human approves"| TASK
    TASK -->|"Human moves"| TASKREVIEW
    TASKREVIEW -->|"Human approves"| IMPL
    IMPL -->|"Agent routes"| TEST
    TEST -->|"Pass"| REVIEW
    TEST -->|"Fail"| IMPL
    TEST -->|"Needs human"| REVIEW
    REVIEW -->|"PR merged"| DONE

    style BACKLOG fill:#f5f5f5,stroke:#999
    style HLD fill:#dbeafe,stroke:#3b82f6
    style HLDREVIEW fill:#e0f2fe,stroke:#0284c7
    style TASK fill:#dbeafe,stroke:#3b82f6
    style TASKREVIEW fill:#dbeafe,stroke:#3b82f6
    style IMPL fill:#dcfce7,stroke:#16a34a
    style TEST fill:#fef9c3,stroke:#ca8a04
    style REVIEW fill:#f3e8ff,stroke:#9333ea
    style DONE fill:#d1fae5,stroke:#059669
```

### V-Model Alignment

The Kanban left leg (design) maps to the V-Model and its right leg (testing):

```
DESIGN ──────────────────────────────────────────── TESTING
                                                            
Backlog    Requirements / feature intent    ←→  E2E / Gherkin acceptance tests
HLD        Architecture (C4 L1/L2)         ←→  Container smoke tests
TaskReview Design (C4 L3 / LLD)            ←→  Integration tests
Implement  Code                            ←→  Unit tests
```

### Human vs Agent Responsibilities

| Who | Does |
|-----|------|
| **Human** | Creates feature stubs, moves stories between columns, approves gates, merges PRs |
| **Architect agent** | Writes HLD, decomposes stories, writes LLD + Gherkin per story |
| **Implementation agent** | Writes tests and code from LLD contracts |
| **Testing agent** | Runs all test levels, verifies Gherkin, routes to Verified or Testing-Manual |

Agents never move stories. Humans commit all column transitions.

### Getting Started

#### New Projects (Use This Template)

1. **Use this template** to create your project repo on GitHub
2. **Clone your new repo** and run onboarding to install Kanban rules:
   ```bash
   ./scripts/windsurf_onboarding.sh
   ```
3. **Create feature stubs** in `Features/1-Backlog/{epic}/0001-feature-name.md` (stories are written later, as output of HLD)
4. **Move stories** through columns via git mv and commit

#### Existing Projects (Add to Repo)

If you already have a project and want to add the agent-manager workflow:

1. **Download the template files** into your project root:

   **Option A: Git pull from remote (recommended)**
   ```bash
   # Add the template repo as a remote
   git remote add template https://github.com/mickeyperlstein/agent-manager-template.git
   
   # Fetch the template (don't merge — your histories are unrelated)
   git fetch template main
   
   # Checkout template files into your project
   git checkout template/main -- template_workflow
   
   # Optional: copy other files if needed
   git checkout template/main -- agent-manager-template.KANBAN.md
   git checkout template/main -- agent-manager-template.README.md
   
   # Commit the imported files
   git add template_workflow agent-manager-template.KANBAN.md agent-manager-template.README.md
   git commit -m "Add agent-manager-template workflow from upstream"
   ```

   **Option B: Curl download**
   ```bash
   curl -L https://github.com/mickeyperlstein/agent-manager-template/raw/main/template_workflow.zip | unzip -d your-project/
   ```

   **Option C: Manual copy**
   Copy the required structure from the template repo manually.
   ```
   your-existing-project/
   ├── template_workflow/        # Copy from template
   │   ├── commands/
   │   ├── agents/
   │   └── templates/
   ├── Features/                   # Create or adapt existing
   ├── ai/agents/                  # Optional: project-level agent overrides
   └── agent-manager-template.KANBAN.md  # Rename if conflicts with your KANBAN.md
   ```

3. **Initialize the workflow**:
   ```bash
   # Create Features/ structure if it doesn't exist
   mkdir -p Features/{1-Backlog,2-HLD,3-HLD-Review,4-Task,5-TaskReview,6-Implementation,7-Test,8-Review,9-Done}
   
   # Run onboarding for your AI tool
   ./template_workflow/scripts/windsurf_onboarding.sh
   # or for Claude: ./template_workflow/scripts/claude_onboarding.sh
   ```

4. **Adapt your existing work**: Move any existing tasks/stories into `Features/1-Backlog/` following the story format.

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
