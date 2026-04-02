# Kanban — Column Reference

## Column Types

**Manual** (human moves the story) vs **Agent** (agent acts on it automatically)

| Column | Who Acts | Artifact Level | Purpose |
|---|---|---|---|
| `Backlog` | Human | Feature stub | Raw intent — no design yet |
| `HLD` | Agent (Architect) | Feature design (C4 L1/L2) | Architect agent designs feature; decomposes into stories |
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
| `HLD → TaskReview` | Architect agent | HLD doc (C4 L1/L2) + story list decomposed |
| `TaskReview → Implementation` | Architect agent + CTO | LLD per story (C4 L3) + Gherkin written by agent; CTO commits move |
| `Implementation → Testing-*` | Agent | Agent routes — never halts |
| `Testing-* → Verified` | QA / Human | All tests pass or human approves |
| `Verified → Review` | PR author | PR open |
| `Review → Done` | Reviewer | PR merged |

## V-Model Alignment

The left leg (design) and right leg (testing) of the V-Model map to Kanban columns:

| V-Model Level | Left Leg (Kanban) | Right Leg (Tests) |
|---|---|---|
| Requirements | Backlog (feature intent) | E2E / acceptance tests (Gherkin) |
| Architecture | HLD (C4 L1/L2) | Container-level smoke tests |
| Design | TaskReview (LLD, C4 L3) | Component / integration tests |
| Implementation | Implementation | Unit tests |

Test coverage at each level should be defined in the LLD before implementation starts.

## Story Lifecycle

Stories do not exist in Backlog. They are created as output of HLD:

```
Backlog         → HLD             → TaskReview      → Implementation → ...
[feature stub]    [feature design]  [story + LLD]     [story code]
                  [stories born]    [Gherkin added]
```

## Why Testing-Agent vs Testing-Manual?

The split ensures agents never halt. If tests can't be automated, the agent routes to `Testing-Manual` and keeps moving rather than blocking on automation it can't do.

## Folder Structure

```
Features/
  1-Backlog/         ← feature stubs only
  2-HLD/             ← feature HLD + stories/ subfolder
  3-TaskReview/      ← stories with LLD + Gherkin
  4-Implementation/  ← stories being coded
  5-Testing-Agent/   ← automated testing
  6-Testing-Manual/  ← human QA
  7-Verified/        ← approved
  8-Review/          ← PR open
  9-Done/            ← merged
```

Moving a story = moving the file. **Column moves are human commits only — agents never move stories.**
