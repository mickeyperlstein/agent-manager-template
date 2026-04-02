# High Level Design (HLD)

## What is an HLD?

A feature-level design specification covering all domains (frontend, backend, database, infra, etc.).

- **WHAT** are we building?
- **WHY** this approach? (trade-offs, alternatives)
- **HOW** will it work? (C4 L1/L2 — no implementation code)

## When to Work Here

**Column:** `2-HLD` — agent acts when a feature file is here.

When done, **the agent moves the file to `3-HLD-Review`**. This is the one column move agents are permitted to make.

## HLD Document Structure

```markdown
# HLD: [Feature Name]

## 1. Problem Statement

## 2. Goals

## 3. Architecture
### C4 L1 — Context
### C4 L2 — Containers
### Components & Data Model
### Flow

## 4. Alternatives Considered

## 5. Logging, Monitoring & Metrics
First-class design concerns — not added after the fact.

**Logs are the trace mechanism.** Every log entry must be meaningful — it must answer a question a human would ask during an incident. Noise logs (e.g. "entered function X", "processing...") are banned. If you can't explain why someone would need to read this log line, don't write it.

For each log entry, define:
- **What happened** (the event, not the code path)
- **Context fields** (trace/correlation id, user id, entity id, relevant state)
- **Level** — use the project log level convention:
  - `debug` — function entry/exit via wrappers only (never manual); developer use, may ofcourse be used for debugging in development
  - `info` — operational events for DevOps and IT techs
  - `warn` — recoverable issues surfaced to non-dev users
  - `error` — non-recoverable failures + exceptions; non-dev audience + alerting

Also define:
- **Metrics:** counters, gauges, histograms to emit — what do they measure and why
- **Dashboards / alerts:** Grafana panels or alerts affected
- **E2E observability contract:** what a passing test will observe (specific log entries, metric values, DB artifacts)

## 6. Open Questions

## 7. Task Decomposition
Tasks to be created in the Task column:
- [ ] 0001-{task-name}: one-line description
- [ ] 0002-{task-name}: one-line description
```

## Example

```
Features/
  1-Backlog/
    csv-two-way-sync.md              ← feature stub

  2-HLD/
    csv-two-way-sync-HLD.md          ← HLD written here

  3-HLD-Review/
    csv-two-way-sync-HLD.md          ← same file, moved by agent

  4-Task/
    csv-two-way-sync/
      csv-two-way-sync-HLD.md        ← HLD becomes sibling
      0001-folders-to-csv.md
      0002-csv-to-folders.md
      0003-pre-commit-hook.md
```

## File Path

```
Features/2-HLD/{feature}-HLD.md
```

## After HLD

1. Agent moves file to `Features/3-HLD-Review/`
2. Human reviews and approves
3. Human moves to `4-Task` — agent creates task files here
4. The HLD becomes a sibling inside `{feature}/` folder from Task onwards
