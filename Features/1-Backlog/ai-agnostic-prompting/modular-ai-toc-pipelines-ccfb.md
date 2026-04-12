---
id: ccfb
epic: 49b5
feature: ccfb
title: Modular AI TOC Pipelines
type: feature
assignee: architect
review_gate: yes
approved: no
depends_on:
---

# Modular AI TOC Pipelines

## What

Build a system that enables modular source documentation with AI-optimized monolithic output. Developers edit small, focused protocol files; push-time build generates complete protocols with reference resolution, TOC with line numbers, and tamper detection.

## Why

AI agents reliably read linear files but skip or invent cross-file references. Current workaround is full duplication (DRY violation). Modular sources + automated build solves this by keeping source DRY while delivering monolithic, AI-friendly outputs.

## Scope

- Design concept hierarchy for shared definitions across protocols (columns, gates, formats)
- Design reference syntax and resolution system (cross-folder references)
- Integrate build phase into `push_template.py`
- Build AI-optimized output: TOC with line numbers, clear naming conventions
- Add tamper detection (checksums in `versions.json`)
- VSCode extension for reference navigation (cmd-click to source files)

## Out of Scope

- Refactoring existing protocol content (happens during implementation)
- Tool-specific wrapper customization (separate concern)
- Hardlink cross-platform sync (out of scope for this feature)

---

## Open Questions for HLD

**Architecture & Design:**
- [ ] Build tool: custom builder vs. Pandoc/LaTeX/simple includes? Trade-offs?
- [ ] Concept hierarchy: shared concepts across meeting, review, kanban? Dependency graph as DAG?
- [ ] Reference syntax: markdown `[ref]` style? Must support easy VSCode cmd-click navigation to sources.
- [ ] Modular structure: split by concept? by protocol layer? hybrid?

**AI Optimization:**
- [ ] Add AI TOC with line numbers to reduce grep/discovery tool usage?
- [ ] Use clear naming conventions on sub-refs for discoverability?

**Implementation Details:**
- [ ] Checksum persistence: commit to `versions.json` or calculate on-the-fly?
- [ ] Validation on edit: alert only, block push, or auto-restore?

---

## Context

**Source:** Meeting 2026-04-11 — Monolithic vs. Modular Documentation (`/meetings/2026-04-11_monolithic-vs-modular-docs.md`)

**Key constraint:** Protocols share concepts that appear in multiple output files. Naive split-by-protocol recreates cross-file ref problem. HLD must design concept hierarchy first.

---

## Acceptance Criteria

- [ ] HLD addresses all open questions with design rationale
- [ ] Build pipeline integrated into `push_template.py` and tested
- [ ] At least one protocol (meeting-protocol) split, rebuilt, and verified
- [ ] AI TOC with line numbers implemented and validated
- [ ] Tamper detection (checksums) working and integrated
- [ ] VSCode extension (or extension approach) documented
- [ ] Tested on Mac and Windows (separate file vs. hardlink behavior confirmed)

---

## Comments

**2026-04-11 — Architect (feature creation):** Created from meeting discussion. Belongs to epic "AI Agnostic Prompting" (to be formalized). Requires HLD to finalize architecture before Task decomposition.
