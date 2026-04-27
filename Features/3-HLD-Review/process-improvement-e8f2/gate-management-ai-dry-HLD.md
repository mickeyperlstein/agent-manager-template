---
id: e8f2
epic: process-improvement
feature: e8f2
title: Gate Management & AI DRY Principle - Template Clarity & Enforcement
type: feature
assignee: architect
review_gate: yes
approved: no
priority: high
depends_on: ""
---

## Feature

**What:** Eliminate HLD/LLD ambiguity by making layer boundaries explicit in templates. Enforce DRY by consolidating duplicate documentation (HowTos vs Protocols).

**Why:** Current state: agents over-engineer (364-line monoliths instead of 90-line correct implementation) because HLD/LLD don't specify which layer owns what. Root cause: layer boundaries are implicit, not explicit. Secondary issue: HowTos exist but agents don't read them—drift between "how to" guidance and actual protocols.

**Scope:**
- Update HLD template to require `## Architecture & Layer Responsibilities` section
- Add design principles: **Think Big/Act Small**, **Open-Closed Principle**, **SRP with Pragmatism (CBA)**
- Update Task LLD template to require `layer:`, `file_to_modify:`, Responsibilities, Assumptions, Invariants
- Update agent-manager-claude.md with explicit Layer Boundary Rules
- Add gate rule 5: **SRP Pragmatically** — always CBA clustering vs. splitting
- Add gate rule 6: **Think Big, Act Small + OCP** — design for extension, implement for now
- Add gate rule 7: **Low code, DRY, Parameterized tests** — minimize LOC, one test > many tests
- Add gate rule 8: **No NIH** — search standards → libraries → docker → custom (in order)
- Update Implement.md HowTo with pre-code clarity checks
- Consolidate HowTos and Protocols (eliminate drift)
- Document which are authoritative (protocols vs guidance)

**Out of Scope:**
- Rewriting existing HLDs/LLDs (backlog item)
- Changing gate sequence or Kanban columns
- Modifying review-protocol.md (separate effort)

## NIH vs existing Library/Docker Decision Matrices

Use these CBA matrices to decide: use existing or write custom code?

### Scenario 1: Git Operations

**Problem:** Need to merge branches, stage files, commit, push.

| Factor | Library (GitPython) | Custom (subprocess) |
|--------|---|---|
| **Cost: Learning curve** | 2 hrs (API) | 1 hr (git commands) |
| **Cost: Maintenance** | 0 (community) | High (subprocess boilerplate) |
| **Cost: LOC** | ~40 lines | ~200+ lines |
| **Cost: Risk** | Low (mature, widely used) | High (edge cases, shell injection) |
| **Benefit: Simplicity** | High (Pythonic API) | Low (commands, parsing) |

**Decision:** ✅ **Use GitPython**  
Rationale: Maintenance cost and risk far exceed learning curve. 160+ LOC savings worth the library dependency.

---

### Scenario 2: JSON Parsing

| Factor | Library (json + jsonschema) | Custom (regex) |
|--------|---|---|
| **Cost: Learning curve** | 30 min | 1 hr |
| **Cost: Maintenance** | 0 (stdlib) | High (escaping, nesting) |
| **Cost: LOC** | ~15 lines | ~80+ lines |
| **Cost: Risk** | None (stdlib) | High (malformed JSON, edge cases) |

**Decision:** ✅ **Use json + jsonschema**  
Rationale: Stdlib cost is zero. Custom regex is fragile. Library wins decisively.

---

### Scenario 3: Filtering Git Status

| Factor | Library (None exists) | Custom (string split + loop) |
|--------|---|---|
| **Cost: Learning curve** | N/A | 30 min |
| **Cost: Maintenance** | N/A | Low (simple logic) |
| **Cost: LOC** | N/A | ~30 lines |
| **Cost: Risk** | N/A | Low (testable, no deps) |

**Decision:** ✅ **Use Custom Code**  
Rationale: No library exists. Code is small, maintainable, domain-specific. Forcing a library here is worse than custom.

---

### Scenario 4: Argument Parsing

| Factor | Library (argparse) | Custom (manual parsing) |
|--------|---|---|
| **Cost: Learning curve** | 1 hr | 2 hrs |
| **Cost: Maintenance** | 0 (stdlib) | Medium (parsing, help text) |
| **Cost: LOC** | ~20 lines | ~60+ lines |
| **Cost: Risk** | None (stdlib) | High (--help, validation edge cases) |

**Decision:** ✅ **Use argparse**  
Rationale: Stdlib cost is zero. Custom parsing error-prone. Library is the obvious choice.

---

### Decision Rule (Simplified)

```
1. Does a mature library exist?
   → YES: Go to 3
   → NO: Go to 2

2. Can I write custom code <50 lines AND testable in <1 hour?
   → YES: Write custom
   → NO: Find library or redesign

3. Is it used by 1000+ projects (GitHub stars, npm downloads)?
   → YES: Use library
   → NO: Evaluate maturity

4. Will custom be <30% the size of library + dependencies?
   → YES: Consider custom
   → NO: Use library
```

---

## Architecture & Flow

**What changes in this feature?**

```
Existing:
  - agent-manager-claude.md (CHANGED: add layer rules + NIH gate)
  - template_workflow/Agent-HowTos/Implement.md (CHANGED: add clarity)

New:
  - template_workflow/templates/feature-hld-template.md (NEW)
  - template_workflow/templates/task-lld-template.md (NEW)

Decision Points:
  - HowTos consolidation: Move to Commands/ or remove? (OPEN)
  - Authoritative vs Guidance: Which docs do agents read? (OPEN)
```

---

## Components: Existing, New, Changed

| Component | Status | File | Library vs Custom | Decision |
|-----------|--------|------|---|---|
| Layer boundary rules | NEW | agent-manager-claude.md | Custom (no lib) | **DECIDED:** Custom rules |
| HLD template | NEW | feature-hld-template.md | Custom vs tool | **DECIDED:** Custom template |
| Task LLD template | NEW | task-lld-template.md | Custom vs tool | **DECIDED:** Custom template |
| HowTos consolidation | CHANGED | template_workflow/ | Move vs remove | **OPEN:** Decide at review |

---

## Library vs Custom Decisions (CBA Matrices)

### Decision 1: Templates — Custom Markdown vs Jinja2

| Factor | Custom Markdown | Jinja2 Template Engine |
|--------|---|---|
| **Standard** | Markdown (universal) | Jinja2 (template-specific) |
| **Popularity** | Universal (every project) | Specific (template engines) |
| **Cost: Learning** | 0 (Markdown native) | 4 hrs (Jinja2) |
| **Cost: Maintenance** | Low (static examples) | Medium (engine state) |
| **Dependencies** | None | Jinja2 package |

**DECIDED:** ✅ Use Custom Markdown  
**Sources:**
- Markdown is industry standard for documentation (used by GitHub, GitLab, every project)
- Templates are *examples and guidance*, not code generation
- No generation needed — agents copy/paste and customize

**Rationale:** Templates are static examples. Markdown is standard. No benefit from Jinja2 complexity.

---

### Decision 2: HowTos Consolidation — Move vs Deprecate

| Factor | Move to Commands/ | Deprecate (remove) |
|--------|---|---|
| **Cost: Migration** | 2 hrs | 1 hr |
| **Cost: Maintenance** | Medium | None |
| **Benefit: Clarity** | Medium (new location) | High (less docs) |

**OPEN:** To be decided at review  
**Questions:**
- Do agents read HowTos if moved?
- Should we consolidate into agent-manager-claude.md instead?
- Is the guidance valuable or noise?

---

## Architecture & Layer Responsibilities

**Two-tier approach:**

```
Tier 1: Authoritative Rules (agent-manager-claude.md)
├─ Startup Protocol (REQUIRED, checked on session start)
├─ Gate Rules (NO EXCEPTIONS)
├─ Layer Boundary Rules (PREVENT SCOPE CREEP)
└─ Artifact Protocol (MANDATORY comments)

Tier 2: Operational Guidance (template_workflow/)
├─ Templates/ (feature-hld-template.md, task-lld-template.md)
├─ Commands/ (meeting-protocol.md, review-protocol.md, etc.)
└─ [DEPRECATED] Agent-HowTos/ (Kanban.md, Implement.md, etc.)
    ↳ Move to Commands/ or remove if replaced by Templates
```

**Layer Boundary Rules (what's explicit, what's implicit):**

- Explicit (in templates, in frontmatter): `layer:`, `file_to_modify:`, Responsibilities
- Explicit (in HLD): Architecture diagram, layer ownership
- Implicit (agents should infer): What layer does NOT own = everything in Responsibilities "❌" section

**Invariant:** If an agent is confused about which layer owns a responsibility, the LLD failed—it's not the agent's fault.

## Acceptance Criteria

- [ ] Feature-HLD template includes Design Principles: Think Big/Act Small, OCP, SRP Pragmatism
- [ ] Feature-HLD template includes examples of clustering vs splitting with CBA
- [ ] Feature-HLD template includes `## Architecture & Layer Responsibilities` section (mandatory)
- [ ] Task-LLD template includes `layer:` and `file_to_modify:` frontmatter fields (mandatory)
- [ ] Task-LLD template includes Responsibilities, Assumptions, Invariants sections
- [ ] agent-manager-claude.md Gate Rule 5: **SRP Pragmatically** (CBA, not dogma)
- [ ] agent-manager-claude.md Gate Rule 6: **Think Big, Act Small + OCP** (design extension, implement scope)
- [ ] agent-manager-claude.md Gate Rule 7: **Low Code, DRY, Parameterized Tests** (minimize LOC)
- [ ] agent-manager-claude.md Gate Rule 8: **No NIH** (standards → libraries → docker → custom)
- [ ] Implement.md includes DRY testing guidance (parameterized over repetitive)
- [ ] Implement.md includes pre-code LLD clarity checks
- [ ] Decision documented: Are HowTos moved to Commands/ or removed?
- [ ] agent-manager-claude.md references authoritative protocols (not HowTos)
- [ ] All templates in template_workflow/templates/ are indexed
- [ ] Clear statement: what agents MUST read vs. what is optional guidance

## Test Conditions

**Happy path: Agent uses new HLD + LLD, creates correct scope**
- Given: New HLD with explicit Architecture section, new Task LLD with layer/file/responsibilities
- When: Agent implements following new templates
- Then: Implementation matches layer boundaries, respects file targets, no scope creep

**Error path: Agent given old HLD without Architecture section**
- Given: Old ambiguous HLD (no layer diagram, implicit boundaries)
- When: Agent implements
- Then: Agent guesses about layer, creates monolith, scope creeps

**Error path: Drift detection (HowTos not read)**
- Given: Agent told to read Implement.md HowTo, but actually reads agent-manager-claude.md
- When: Agent implements
- Then: HowTo guidance not applied, only rules applied
- Conclusion: HowTos add no value if not read—consolidate into Protocols

## Gherkin

```gherkin
Feature: Gate management prevents scope creep via explicit layer boundaries

  Scenario: HLD with Architecture section prevents monolith
    Given an HLD with explicit "## Architecture & Layer Responsibilities"
    And task LLDs with layer: BASH and layer: PYTHON designations
    And Responsibilities sections that say "BASH does NOT: [merge, filter, commit]"
    When an agent implements the tasks
    Then agent creates 15-line bash + 70-line Python (correct split)
    And does not create 364-line monolith

  Scenario: Task LLD with file_to_modify prevents new-file scope creep
    Given a task with file_to_modify: push_template.sh
    And a Responsibilities section saying "edit existing file, do NOT create new"
    When an agent implements
    Then agent modifies push_template.sh only
    And does not create push_to_template.py (new file, wrong scope)

  Scenario: HowTos vs Protocols clarity
    Given agent-manager-claude.md as authoritative
    And Implement.md HowTo as optional guidance
    When documentation is clear about which is which
    Then agents prioritize Protocols over HowTos
    And HowTos can be pruned if not used
```

## Definition of Done

- [ ] HLD template created with Architecture & Layer Responsibilities section
- [ ] Task LLD template created with layer/file_to_modify/Responsibilities/Assumptions/Invariants
- [ ] agent-manager-claude.md updated with Layer Boundary Rules
- [ ] Implement.md updated with pre-code clarity checks
- [ ] Decision on HowTos: move to Commands/, remove, or keep with explicit "optional guidance" label
- [ ] All templates indexed and linked from template_workflow/README (if it exists)
- [ ] Clear statement in agent-manager-claude.md: "Read this, not HowTos"
- [ ] Tested on blind architect: fresh agent creates HLD following new protocol without prior context

---

## Comments

**2026-04-15 — Claude (HLD creation for gate management):**

Created HLD for explicit layer boundaries and DRY principle. Added:
- Gate Rule 5: **Think Big, Act Small** — design with future scope in mind, implement only what's needed
- Gate Rule 6: **No NIH** — strict priority order: standards → libraries → docker → custom

Per feedback: agents prefer writing custom code instead of using battle-tested libraries (GitPython vs subprocess, custom DB layers, etc.). Also: tendency to over-engineer (building plugin systems, generic frameworks) for single use case. "Think big, act small" prevents both extremes.

Immediate concerns:

1. **NIH Problem:** Added Gate Rule 5 to enforce library-first approach. Before implementing anything, search for existing libraries. Only custom code if: (a) no library, (b) library unmaintained, (c) custom significantly smaller/clearer.

2. **HowTos drift:** Implement.md is a HowTo, but agents don't read it (they read agent-manager-claude.md rules instead). Should we:
   - Move HowTos to `template_workflow/commands/` and rename to `implement-protocol.md`?
   - Or label HowTos as "optional guidance" and accept they won't be read?
   - Or remove them entirely if they're not consulted?

3. **Authoritative vs. Guidance:** agent-manager-claude.md is read (it's in startup protocol). But Implement.md HowTo is optional. Should we consolidate? Should gates only reference agent-manager-claude.md (rules) and deprecate HowTos (guidance)?

Ready for review.
