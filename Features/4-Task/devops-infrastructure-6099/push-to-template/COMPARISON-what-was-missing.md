# Comparison: What Was Missing

## Original HLD (insufficient)

✅ **Had:**
- Clear "What" and "Why"
- Acceptance criteria
- Test conditions (Gherkin)
- Out of scope items


❌ **Missing:**
- **Architecture/Layer Diagram** — didn't explicitly say "bash does X, Python does Y"
- **Layer boundary rules** — didn't say "no git init in Python, no filtering in Bash"
- **File mappings** — didn't say which task modifies which file
- **Layer context in acceptance criteria** — acceptance criteria didn't mention layer split

**Result:** Implementer could infer anything. I inferred "do everything in Python" (wrong).

---

## Original LLDs (insufficient)

Example: task 6eb3 (Cache Initialization)

✅ **Had:**
- Function signatures
- Algorithm pseudocode
- Test plan

❌ **Missing:**
- **Layer designation** (`layer: BASH` or `layer: PYTHON`)
- **File to modify** (which file? new or existing?)
- **Assumptions** (what state are we in before this task?)
- **Responsibilities** (what is this layer responsible for, and what it's NOT)
- **Invariants** (what must always be true after this task)
- **Boundary rules** (what you don't do, respect the layer split)

**Result:** Task 6eb3 showed `subprocess.run(['git', 'init'])` but never said whether that was bash or Python. I assumed Python and built a 364-line monolith.

---

## What Proper LLDs Need (New Template)

Every LLD must have:

```markdown
---
layer: [BASH|PYTHON|JS|OTHER]  ← CRITICAL
file_to_modify: [filename]     ← CRITICAL
depends_on: [task ids]         ← Shows sequence
---

## Assumptions
What state are we in before this task runs?

## Responsibilities
- ✅ What this layer DOES
- ❌ What this layer DOESN'T (respect boundaries)

## Interface
Function signatures and contract

## Algorithm
Pseudocode or description

## Invariants
What must always be true

## Test Plan
Unit + integration tests

## Definition of Done
- Marked against this task, not guess
```

---

## How This Prevents Scope Creep

**Scenario: If proper LLDs existed**

Task 6eb3 (Cache Init) would have said:
```
layer: BASH
file_to_modify: push_template.sh
```

Implementer reads: "This is bash, I'm editing the wrapper script."

Implementer sees: `git clone`, `git checkout`, `git pull` — all shell operations.

Implementer does NOT see: `subprocess.run()`, exception handling, git config setup.

**Result:** Correct 15-line bash script, not 364-line Python monolith.

---

## Action Items

To prevent this in the future:

1. **Update the HLD template** to require Architecture/Layer section
2. **Update the LLD template** to require `layer:` and `file_to_modify:` fields
3. **Create layer boundary rules** (in CLAUDE.md or Implement.md):
   - Bash handles infrastructure (clone, checkout, fetch, pull, shell operations)
   - Python handles business logic (filtering, merging, committing, pushing)
   - Never reinvent git in subprocess — use it natively
4. **In task review**, check:
   - Does task's `layer:` match the actual implementation?
   - Does `file_to_modify:` match what was edited?
   - Did the implementer respect the layer boundary?

This moves the responsibility from "gates catch mistakes" to "clear specs prevent mistakes."
