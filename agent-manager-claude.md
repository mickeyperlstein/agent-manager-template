# Agent Manager — Claude Code Rules

This file contains the Kanban workflow rules for Claude Code agents.

---

## ⛔ STOP — MANDATORY BEFORE ANY ACTION

**You have not earned the right to act in this repo yet.**

Before you write a single line, move a single file, or make any suggestion — you must read `template_workflow/Agent-HowTos/Kanban.md` in full. Not skim it. Read it.

**If you have not read `template_workflow/Agent-HowTos/Kanban.md` in this session: stop now and read it before doing anything else.**

This applies to ALL agents, ALL roles, ALL sessions. No exceptions. Not for urgency. Not because the task seems obvious. Not because you were told what to do. You do not know what column a task is in, what gate it must pass, or what artifacts are required until you have read `template_workflow/Agent-HowTos/Kanban.md`.

Acting without reading `agent-manager-template.KANBAN.md` is a process violation.

---

## Startup Protocol — REQUIRED SEQUENCE

You must complete these steps in order before taking any action:

1. **Read `agent-manager-template.KANBAN.md` in full** — columns, gates, folder structure, artifact requirements
1a. **Run `/housekeeping`** — prune empty folders and move stragglers to correct stages before reading board state
2. **Read `tasks.csv`** — find stories where `column = HLD`, `column = Task`, `column = TaskReview`, `column = Implementation`, or `column = Test`
3. **Read the task/feature file(s)** for your assigned work only
4. **Confirm your column** — you are only permitted to act on work in the columns above. If your assigned work is not in one of those columns, stop and tell the human.

---

## Gate Rules — NO EXCEPTIONS

1. **Never skip a gate.** Not for urgency, simplicity, or because the CTO is present.
2. **Never move a feature between columns** — one exception only: the HLD agent MUST move a completed HLD to `HLD-Review`. All other column moves are human commits only.
3. **Never suggest fast-tracking.** If you find yourself about to say "we could skip" — stop. That is a process violation.
4. **Never implement work that belongs to a future column.** If you are in HLD, you do not touch code. If you are in Task, you do not write LLD. Stay in your lane.
5. **Think big, act small. Design for extension, implement for now.** Respect Open-Closed Principle:
   - **Think big:** Understand the full scope and future evolution (in HLD)
   - **Act small:** Implement only what's needed now (in tasks)
   - **Extensible, not abstract:** Build interfaces open for extension, closed for modification
   - **Open-Closed Principle (OCP):** New features added without modifying existing code
   - Example: Design auth to support OAuth2/SAML/LDAP via interface, implement OAuth2 only. SAML later uses same interface, no changes to OAuth2 code.
   - Anti-pattern: Building a plugin system, generic config framework, or "future-proof" abstraction for one use case today

6. **Respect SRP pragmatically — always CBA clustering vs splitting.** Don't over-fragment code:
   - **Cluster if:** Responsibilities change together, coupling reduces complexity, splitting requires orchestration
   - **Split if:** Different reasons to change, splitting reduces cognitive load, reusability matters
   - **Always justify:** CBA matrix showing cohesion vs. orchestration trade-off
   - Example: User validation + serialization cluster (same logic), but separate from Notifier (different reason)
   - Anti-pattern: Five tiny classes with an orchestrator that glues them together

7. **Low code amounts. DRY obsessively. One flowing test beats fifty fragmented tests.** Minimize LOC everywhere:
   - **Code:** Delete dead code, reuse logic, avoid duplication
   - **Tests:** One clean test with multiple assertions in logical flow > many tests with repeated setup/teardown bloat
   - **Test flow:** ASSERT dir exists → ASSERT can write → ASSERT can copy (clean, TDD style, fails on first problem)
   - **Anti-pattern:** `test_dir_exists()`, `test_can_write()`, `test_can_copy()` (each with setup/try/finally, massive overhead)
   - **Configuration:** DRY config, avoid repetition, use defaults
   - **Documentation:** Link, don't duplicate. One source of truth
   - Rule: One flowing test > fifty fragmented tests with setup hell

8. **Never build what already exists — prefer in strict order: standards → libraries → docker → custom.** Before implementing anything: search and prefer in this order:
   
   **Priority 1: Industry Standards** (RFC, specification, widely-adopted baseline)
   - Example: OAuth2 for auth (not custom), REST for APIs, OpenTelemetry for tracing
   
   **Priority 2: Multi-star libraries/frameworks** (1000+ GitHub stars, widely used, maintained)
   - Example: Django (Python web), FastAPI (Python API), GitPython (git operations)
   - Also: Open source over closed source, Free over paid (if equivalent)
   
   **Priority 3: Established Docker images** (well-maintained, official or verified sources)
   - Example: Official PostgreSQL image, Redis image, Nginx image
   - Use existing container over building custom service
   
   **Priority 4: Custom code** (last resort)
   - Only if: no standard exists, no library exists, no Docker image exists, OR custom is significantly cheaper/simpler/smaller
   - Burden of proof is on you to justify custom code
   
   For each choice in the HLD, create a **CBA matrix:**
   - Either: **DECIDED** with sources (links to GitHub, Docker Hub, docs proving your choice)
   - Or: **OPEN** with evaluation criteria (what would change your decision?)
   
   Search hierarchy: Standard → Library (pip, npm, gems) → Docker image → Custom code

---

## Layer Boundary Rules — PREVENT SCOPE CREEP

**Every HLD MUST define Architecture & Layer Responsibilities.** If the feature spans multiple execution layers (Bash, Python, JavaScript, etc.), explicitly state:
- What each layer owns
- What each layer does NOT own
- Where the boundary is (which file, which function, which interface)

**Every Task LLD MUST specify:**
- `layer:` field (BASH, PYTHON, JS, OTHER)
- `file_to_modify:` field (what existing file, not new file)
- Responsibilities section (what this layer does, what it does NOT)

**Layer Responsibility Examples:**

| When to use | BASH | Python | JS |
|---|---|---|---|
| Infrastructure setup | ✅ | ❌ | ❌ |
| Git clone/checkout/pull | ✅ | ❌ | ❌ |
| Orchestration/wrapper | ✅ | ❌ | ❌ |
| Business logic | ❌ | ✅ | ❌ |
| Data transformation/filtering | ❌ | ✅ | ❌ |
| Git merge/commit/push logic | ❌ | ✅ | ❌ |
| Client logic/UI | ❌ | ❌ | ✅ |
| DOM manipulation | ❌ | ❌ | ✅ |

**Why this matters:** 
- Scope creep happens when layer boundaries are unclear (e.g., "I'll do cache management in Python" instead of bash)
- Implementation mistakes cascade when the HLD doesn't state which layer owns what
- Tasks become ambiguous about what file to edit and what responsibility they own

**During Task Creation:**
If the task's `layer:` and `file_to_modify:` are unclear, route back to HLD review with: "Please clarify in the Architecture section: which layer owns X, and which file does this task modify?"

**During Task Review:**
Before approving a task, verify:
- Did the implementation respect the declared `layer:`?
- Did it modify only the declared `file_to_modify:` (not create new files)?
- Did it respect the Responsibilities section (not cross layer boundaries)?

---

## Artifact Protocol

Every session that modifies a task or feature file MUST append a dated comment before the session ends:

```markdown
## Comments
**YYYY-MM-DD — [role] ([context]):** <what was discussed or changed>
```

No file may be modified without this entry dated today.
