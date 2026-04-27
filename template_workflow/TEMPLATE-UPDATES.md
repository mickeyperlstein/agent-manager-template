# Template & Rule Updates: Scope Clarity & Layer Boundaries

**Date:** 2026-04-15  
**Purpose:** Prevent scope creep and implementation mistakes by making HLD/LLD layer boundaries explicit

---

## What Changed

### 1. New HLD Template: `feature-hld-template.md`

**Location:** `template_workflow/templates/feature-hld-template.md`

**New mandatory section:** `## Architecture & Layer Responsibilities`

This section requires:
- Clear diagram showing layers/components
- Explicit statement of what each layer owns
- Explicit statement of what each layer does NOT own
- Layer boundary rules (invariants)

**Why:** Prevents HLD ambiguity that leads to 364-line monoliths instead of 90-line correct implementations.

**Example from push-to-template HLD:**
```
┌─────────────────────────────────────────────────┐
│  push_template.sh (BASH wrapper)                │
│  ├─ Check/create cache folder                  │
│  ├─ git clone origin (if missing)              │
│  └─ Call: python3 push_template.py             │
└─────────────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────────────┐
│  push_template.py (PYTHON core logic)           │
│  ├─ git merge --ff-only dev/dev                │
│  ├─ Filter artifacts                           │
│  └─ Commit & push                              │
└─────────────────────────────────────────────────┘
```

---

### 2. New Task LLD Template: `task-lld-template.md`

**Location:** `template_workflow/templates/task-lld-template.md`

**New mandatory frontmatter fields:**
```yaml
layer: BASH|PYTHON|JS|[OTHER]      # CRITICAL
file_to_modify: <path/to/file>     # CRITICAL
```

**New mandatory sections:**
- `## Assumptions` — what state are we in before this task?
- `## Responsibilities` — what does this layer own, what does it NOT?
- `## Invariants` — what must be true after completion?

**Why:** Makes it impossible to write an LLD that's ambiguous about "which layer owns this?"

**Checked by:** Before implementation, verify layer designation matches file target.

---

### 3. Updated `agent-manager-claude.md`

**Added:** `## Layer Boundary Rules — PREVENT SCOPE CREEP`

New rules:
1. **Every HLD MUST define Architecture & Layer Responsibilities**
2. **Every Task LLD MUST specify `layer:` and `file_to_modify:`**
3. **Responsibilities section is required** (what this layer owns, what it doesn't)

**Added reference table:** When to use BASH vs Python vs JS (architecture guidance)

**During review:** Check that implementation respects declared layer and file target.

---

### 4. Updated `template_workflow/Agent-HowTos/Implement.md`

**Added:** Pre-implementation LLD clarity check

Before writing code, verify:
- [ ] `layer:` field matches HLD Architecture
- [ ] `file_to_modify:` is explicit (edit, don't create new)
- [ ] Responsibilities section is clear
- [ ] Assumptions section is present

**Added:** Routing rule — if LLD is unclear on layer/boundaries, route back to TaskReview.

---

## How This Prevents the push-to-template Mistake

**Before (what went wrong):**

HLD said: "Maintains local cache folder with clean main checkout"

Implementer thought: "I'll do this in Python with git operations"

Result: 364-line Python monolith, wrong layer, replaces existing code, scope creep.

---

**After (with updated templates):**

HLD now includes:
```markdown
## Architecture & Layer Responsibilities

┌─────────────────────┐
│ push_template.sh (BASH)
│ - Cache setup      │
│ - git clone, checkout, pull
│ - Orchestration    │
└─────────────────────┘
      ▼
┌─────────────────────┐
│ push_template.py (Python)
│ - Merge & filter   │
│ - Commit & push    │
└─────────────────────┘

Layer Boundary Rules:
- BASH handles: cache init, clone, checkout, pull
- Python handles: merge, filter, commit, push
- Invariant: Cache always starts clean before Python
```

Task LLD includes:
```yaml
layer: BASH
file_to_modify: push_template.sh

## Responsibilities
- ✅ Create cache if missing
- ✅ git clone origin
- ✅ git checkout main
- ✅ git fetch + pull
- ❌ Do NOT handle merge (Python's job)
- ❌ Do NOT filter artifacts (Python's job)
```

Implementer reads: "Oh, I'm editing push_template.sh in bash. I shouldn't write ~15 lines of bash for setup, then call Python."

Result: 15-line bash wrapper + 70-line Python core = correct architecture.

---

## Implementation Checklist

When creating a new Feature with multiple layers:

- [ ] Read `feature-hld-template.md`
- [ ] Include `## Architecture & Layer Responsibilities` section
- [ ] Draw a layer diagram (ASCII or description)
- [ ] Explicitly state layer boundaries
- [ ] For each Task, specify `layer:` and `file_to_modify:` in frontmatter
- [ ] For each Task, include Responsibilities and Invariants sections

When implementing a Task:

- [ ] Check LLD's `layer:` field
- [ ] Check LLD's `file_to_modify:` field
- [ ] Verify you're editing the declared file, not creating new
- [ ] Verify you're not crossing layer boundaries (per Responsibilities)
- [ ] Verify assumptions are met before starting

---

## Templates Location

- **HLD template:** `template_workflow/templates/feature-hld-template.md`
- **Task LLD template:** `template_workflow/templates/task-lld-template.md`
- **General feature template:** `template_workflow/templates/feature-stub.md` (for reference)

---

## Rules Updated

- **agent-manager-claude.md** — Added Layer Boundary Rules section
- **template_workflow/Agent-HowTos/Implement.md** — Added pre-implementation LLD clarity check
