
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

