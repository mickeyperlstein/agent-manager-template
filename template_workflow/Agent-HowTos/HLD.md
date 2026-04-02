# High Level Design (HLD)

## What is an HLD?

An **HLD (High Level Design)** document is a feature-level design specification. It covers the full feature — potentially spanning multiple domains (frontend, backend, database, infra, test data, etc.).

HLD answers:
- **WHAT** are we building? (Components, interfaces, data models)
- **WHY** this approach? (CBA, trade-offs, alternatives considered)
- **HOW** will it work? (Architecture and flow — no implementation code)

HLD operates at **C4 Level 1 (Context) and Level 2 (Container)**. Component-level detail (C4 L3) belongs in the LLD, written at TaskReview.

## Stories Are Written HERE — Not in Backlog

**The Backlog holds feature stubs. The HLD produces stories.**

Once the HLD design is settled, the architect decomposes the feature into implementable stories. These stories live as child files under the HLD folder and move to TaskReview for LLD and Gherkin.

```
Features/2-HLD/{epic}/{feature-name}/
  {id}-{feature-name}-HLD.md       ← feature-level HLD
  stories/
    {id}-{story-name}.md           ← stories written as HLD output
```

## When to Write an HLD

**Column:** `HLD` (Features/2-HLD/{Feature-Name}/)

Write an HLD when a feature is in the HLD column. This happens after:
- Backlog: Raw feature stub captured
- HLD: Design the solution (current step) → stories decomposed here
- Before: TaskReview (architect sign-off + LLD per story)

## HLD Document Structure

```markdown
# High Level Design: [Feature Name]

## 1. Problem Statement
What problem are we solving?

## 2. Goals
1. Goal one
2. Goal two

## 3. Proposed Architecture
### 3.1 C4 Context Diagram (L1)
System boundary — who uses it, what external systems interact

### 3.2 C4 Container Diagram (L2)
Major containers (services, datastores, scripts) and their interactions

### 3.3 Components
- Component A does X
- Component B does Y

### 3.4 Data Model
Key entities and relationships

### 3.5 Flow
Step-by-step how it works

## 4. Alternatives Considered
- Option A: rejected because...
- Option B: chosen because...

## 5. Open Questions
- Question 1

## 6. Story Decomposition
Stories produced by this HLD (to be moved to TaskReview for LLD + Gherkin):
- [ ] {id}-{story-name}: one-line description
- [ ] {id}-{story-name}: one-line description
```

## HLD vs LLD

| HLD | LLD (written at TaskReview) |
|-----|-----------------------------|
| Feature level | Story level |
| C4 L1/L2 | C4 L3 (Component) |
| What/why/how (no code) | Interface contracts, sequences, data shapes |
| Architect writes | Architect writes per story |
| Produces stories | Produces Gherkin + implementable spec |

## After HLD

Once HLD is complete and stories are decomposed:
1. Feature + stories move to `TaskReview`
2. Architect writes LLD per story and adds Gherkin
3. CTO signs off and moves to `Implementation`

## See Also

- `Kanban.md` — Full column workflow
- `TaskReview.md` — LLD and Gherkin gate
