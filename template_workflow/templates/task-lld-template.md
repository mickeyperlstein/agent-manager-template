# Task LLD Template

Use this template when creating a **Task** with a Low-Level Design (LLD) for implementation.

The LLD (Low-Level Design) is the detailed blueprint before coding. It specifies: **Layer**, **File Target**, **Assumptions**, **Interface**, **Algorithm**, **Invariants**, **Tests**, and **Definition of Done**.

---

```markdown
---
id: xxxx
epic: yyyy
feature: zzzz
title: <Task Name>
type: task
layer: BASH|PYTHON|JS|[OTHER]
file_to_modify: <filename or path>
assignee: architect
review_gate: no
depends_on: ""
---

## Task: <Task Name>

**What:** <One sentence: what does this task accomplish?>

**Layer:** `[BASH|PYTHON|JS|OTHER]` — Which execution layer is this in?

**File to modify:** `<path/to/file>` — What existing file does this task edit? (Not create new)

## LLD (Low-Level Design)

### Assumptions

What state are we in before this task runs? What preconditions must be true?

- <Assumption 1>
- <Assumption 2>

### Responsibilities

**This layer/task owns:**
- ✅ <Responsibility 1>
- ✅ <Responsibility 2>

**This layer/task does NOT own:**
- ❌ <Explicitly what it doesn't do — respect layer boundaries>
- ❌ <Another thing it doesn't do>

### Interface

Function signatures, CLI parameters, or contract specification.

```python
def function_name(arg1: Type, arg2: Type) -> ReturnType:
    """Docstring explaining contract."""
```

Or for Bash:

```bash
# Usage: ./script.sh [options]
# Environment: VAR_NAME=value
# Exit: 0 on success, 1 on error
```

### Algorithm

Pseudocode or step-by-step algorithm description.

```
Step 1: <What happens>
Step 2: <What happens>
Step 3: <What happens>
```

Or provide actual pseudocode.

### Invariants

What must always be true after this task completes?

- <Invariant 1>
- <Invariant 2>

### Test Plan

**Unit tests (implementation-level):**

Test 1: <Test name>
- Given: <preconditions>
- When: <action>
- Then: <assertion>

Test 2: <Test name>
- Given: <preconditions>
- When: <action>
- Then: <assertion>

**Integration tests (interaction-level):**

Integration Test 1: <Test name>
- Given: <preconditions and prior task state>
- When: <action>
- Then: <assertion, verified via logs/artifacts/harness>

---

## Acceptance Criteria

- [ ] Function/script matches interface contract exactly
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Layer boundaries respected (no mixing concerns)
- [ ] Code is observable (logs, artifacts, or harness output)
- [ ] Definition of Done checklist completed

## Definition of Done

- [ ] Code written (file_to_modify edited, not created)
- [ ] Matches LLD interface and algorithm exactly
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Layer boundary respected (doesn't violate HLD architecture)
- [ ] Observable via logs, DB artifacts, or harness
- [ ] No shortcuts from LLD without documented reason
- [ ] Task file updated with acceptance criteria marked done

---

## Comments

**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

---

## Template Notes

- **`layer:` field is MANDATORY** — explicitly state BASH, PYTHON, JS, or other
- **`file_to_modify:` field is MANDATORY** — what file does this task edit? Prevents "new file" scope creep
- **Assumptions section prevents surprises** — what state must be true for this task to work?
- **Responsibilities section enforces boundaries** — explicitly say what this layer does NOT do
- **Invariants section clarifies side effects** — what must be true after this task?
- If reviewing an LLD, ask:
  - Is `layer:` clear? Would I implement it the same way?
  - Is `file_to_modify:` explicit? Am I editing existing code, not writing new?
  - Do the Responsibilities respect the HLD Architecture section?
  - Are the Invariants testable?

---

## Layer Responsibility Reference

**Use this to fill in Responsibilities section:**

| Layer | Typically owns | Typically does NOT own |
|-------|---|---|
| **BASH** | Infrastructure, setup, env vars, shell operations, git clone/checkout/pull, orchestration | Business logic, filtering, commits, pushing |
| **PYTHON** | Business logic, filtering, transformations, commits, pushes, error handling | Infrastructure setup, git clone, checkout, orchestration |
| **JS** | Client logic, DOM manipulation, user interaction | Server operations, system calls, infrastructure |

Adapt to your system. The key: **be explicit, respect the split, don't mix concerns.**


#### Documentation Section

When this task is implemented, update `Architecture/hld_perli_system.md` with:

| Section | What | Lines |
|---------|------|-------|
| C4 Context Diagram | Add Guardian User, Child Device User, Guardian App, Bracelet App actors; show relationships to Traccar and Backend API | TBD |
| C4 Container Diagram | Add Guardian & Bracelet containers; show UI layers (MainScreen, ConfigScreen), Service layers (GeolocationService, ConfigurationService, PushService, Preferences), OS Integration | TBD |
| Path Dependency Legend | Explain path dependency strategy, benefits (zero drift, automatic updates, no version coordination), minimal IoC patterns | TBD |
| Location Sync Flow | Document Guardian/Bracelet → BackgroundGeolocation → ConfigurationService → Traccar Server flow | TBD |
| Cross-references | Add [links](path) to HLD, README docs, E2E test docs | TBD |

**No speculation, no bloat** — only what this task implements is documented.
