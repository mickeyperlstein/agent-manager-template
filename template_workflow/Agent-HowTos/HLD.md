# High Level Design (HLD)

## What is an HLD?

An **HLD (High Level Design)** document is a feature-level design specification covering all domains (frontend, backend, database, infra, test data, etc.).

HLD answers:
- **WHAT** are we building? (Components, interfaces, data models)
- **WHY** this approach? (CBA, trade-offs, alternatives considered)
- **HOW** will it work? (Architecture and flow — no implementation code)

HLD operates at **C4 Level 1 (Context) and Level 2 (Container)**. Component-level detail (C4 L3) belongs in the LLD, written at TaskReview.

## When to Work on HLD

**Column:** `HLD` (Features/2-HLD/{Feature-Name}/)

The agent acts when a feature is in the `HLD` column. When done, **the agent moves the feature to `HLD-Review`** — this is the one column move agents are permitted to make.

## Stories Are Written HERE — Not in Backlog

The Backlog holds feature stubs. The HLD produces stories.

Once the HLD design is settled, decompose the feature into implementable stories. List them in the HLD under `## Story Decomposition`. Stories move to TaskReview for LLD and Gherkin.

## HLD Document Structure

```markdown
# High Level Design: [Feature Name]

## 1. Problem Statement

## 2. Goals

## 3. Proposed Architecture
### 3.1 C4 Context Diagram (L1)
### 3.2 C4 Container Diagram (L2)
### 3.3 Components
### 3.4 Data Model
### 3.5 Flow

## 4. Alternatives Considered

## 5. Open Questions

## 6. Story Decomposition
Stories produced by this HLD (move to TaskReview for LLD + Gherkin):
- [ ] {id}-{story-name}: one-line description
```

## After HLD

1. Agent moves feature to `HLD-Review` (Features/3-HLD-Review/)
2. Human reviews and approves
3. Human moves to `TaskReview`
4. Architect agent writes LLD + Gherkin per story

## See Also

- `Kanban.md` — Full column workflow
- `TaskReview.md` — LLD and Gherkin gate
