# Kanban — Column Reference

## Column Types

| Column | Who Acts | Artifact Level | Purpose |
|---|---|---|---|
| `Backlog` | Human | Feature stub | Raw intent — no design yet |
| `HLD` | Agent (Architect) | Feature design (C4 L1/L2) | Architect agent designs feature, decomposes stories; **agent moves to HLD-Review when done** |
| `HLD-Review` | Human | — | Human reviews and approves the HLD |
| `TaskReview` | Agent (Architect) + Human (CTO) | Story LLD (C4 L3) + Gherkin | Architect agent writes LLD + Gherkin per story; CTO commits approval |
| `Implementation` | Agent | Code | Agent builds from LLD ([see Implement.md](Implement.md)) |
| `Testing-Agent` | Agent | Test results | Agent runs automated tests ([see Testing-Agent.md](Testing-Agent.md)) |
| `Testing-Manual` | Human | QA sign-off | Human QA — cannot be automated |
| `Verified` | Human | Approval | Tests passed, human approved |
| `Review` | Human | PR | PR open, awaiting code review |
| `Done` | Human | Merged | PR merged, feature complete |

## Gate Owners and Required Artifacts

| Gate | Owner | Required to Advance |
|------|-------|---------------------|
| `Backlog → HLD` | Human | Feature stub with clear scope |
| `HLD → HLD-Review` | **Architect agent** | HLD doc (C4 L1/L2) + story list |
| `HLD-Review → TaskReview` | Human | Human approves HLD |
| `TaskReview → Implementation` | Architect agent + CTO | LLD per story (C4 L3) + Gherkin; CTO commits move |
| `Implementation → Testing-*` | Agent | Agent routes — never halts |
| `Testing-* → Verified` | Human | All tests pass, human approves |
| `Verified → Review` | PR author | PR open |
| `Review → Done` | Reviewer | PR merged |

## V-Model Alignment

| V-Model Level | Left Leg (Kanban) | Right Leg (Tests) |
|---|---|---|
| Requirements | Backlog | E2E / Gherkin acceptance tests |
| Architecture | HLD (C4 L1/L2) | Container smoke tests |
| Design | TaskReview (LLD, C4 L3) | Integration tests |
| Implementation | Implementation | Unit tests |

## Story Lifecycle

```
Backlog         → HLD              → HLD-Review    → TaskReview      → Implementation
[feature stub]    [feature design]   [human review]  [story + LLD]     [story code]
                  [stories born]                     [Gherkin added]
                  [agent moves ↑]
```

## Folder Structure

```
Features/
  1-Backlog/         ← feature stubs only
  2-HLD/             ← agent writes HLD here
  3-HLD-Review/      ← awaiting human HLD approval
  4-TaskReview/      ← stories with LLD + Gherkin
  5-Implementation/  ← stories being coded
  6-Testing-Agent/   ← automated testing
  7-Testing-Manual/  ← human QA
  8-Verified/        ← approved
  9-Review/          ← PR open
  10-Done/           ← merged
```

**Only the HLD agent may move a story (HLD → HLD-Review). All other column moves are human commits only.**
