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

## 6. Documentation
Update any affected documentation as part of the HLD:
- **README.md** — if the feature adds new commands, folders, conventions, or lookup paths, update the relevant README sections (Commands, Repository Structure, Agent Lookup Order, etc.)
- **KANBAN.md** — if the feature changes workflow rules or column behavior
- **Agent-HowTos** — if the feature changes how a column works or adds new agent responsibilities

Documentation is a first-class deliverable, not an afterthought. If the HLD introduces something a user or agent needs to know about, it must be documented before moving to HLD-Review.

## 7. Open Questions

## 8. Task Decomposition
HLD agent creates task stub files alongside the HLD doc. Each stub file uses the filename convention:
`{name}-{taskid}-{featureid}-{epicid}.md`

**All IDs must be 4-char hex.** Generate one for each task:
```bash
python3 -c "import secrets; print(secrets.token_hex(2))"
```

Each stub must contain: What, Scope, Acceptance Criteria, Test Conditions, Definition of Done.
The Task column agent will add LLD + Gherkin + TestPlan to each stub.

- [ ] {name}-{taskid}-{featureid}-{epicid}.md: one-line description
- [ ] {name}-{taskid}-{featureid}-{epicid}.md: one-line description
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
    devops-bootstrap/
      csv-two-way-sync/
        csv-two-way-sync-HLD.md                          ← HLD reference (stays here)
        folders-to-csv-385474-e9245d-23a043.md           ← task stub created by HLD agent
        csv-to-folders-0640af-e9245d-23a043.md
        pre-commit-hook-3cda27-e9245d-23a043.md
```

## File Path

```
Features/2-HLD/{feature}-HLD.md
```

## After HLD

1. Agent creates task stub files in `Features/4-Task/{epic}/{feature}/` alongside a copy of the HLD
2. Agent moves the HLD file to `Features/3-HLD-Review/`
3. Human reviews HLD + task stubs and approves
4. Task column agent picks up each stub and adds LLD + Gherkin + TestPlan
