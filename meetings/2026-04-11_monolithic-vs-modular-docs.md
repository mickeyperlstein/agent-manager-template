# Meeting: Should documentation use monolithic files or modular files with cross-references?
Date: 2026-04-11  Time: 

## Participants
- MOD + ARCH: Claude Haiku 4.5 — playing Architect + facilitator


## Topic
Should documentation use monolithic files (like Kanban.md) or modular files with cross-references? especially in small sahared topics like formats, locations...

## Goal
Decide on a documentation file structure pattern: monolithic vs. modular with references. Apply pattern to project going forward.

## Relevant Info
Current examples in the project:
- `Kanban.md` — one comprehensive file covering workflow, columns, gates, filename conventions, folder lifecycle, V-model alignment
- `meeting-protocol.md` — detailed protocol steps, nested sections
- `review-protocol.md` — similar detailed protocol file
- Question: should these be split into smaller concept files (e.g., 'itemformats.md` '`) with a parent file referencing them?

## Agenda
1. Trade-offs: monolithic vs. modular (discoverability, maintenance, cognitive load, navigation)
2. Patterns: when does monolithic work? When does modular shine? (size, audience, change frequency)
3. Current structure audit: are Kanban.md, meeting-protocol.md, review-protocol.md in the right form?
4. Recommendation: a pattern for this project going forward (and any immediate restructuring needed)
5. how do i read the refs in vscode, jump to the ref files. 
## Notes
(live notes — updated during the meeting)

## Rolling Summary
- Identified core constraint: AIs skip cross-file refs but read linear files reliably
- Tested enforcement mechanisms for AI reliability: explicit gates, hardlinks, modular build approach
- Cross-platform analysis: hardlinks work on Mac (dev convenience), become copies on Windows (fine for read-only templates)
- Proposed solution: modular source files + build step in push_template.py to generate monolithic files marked "GENERATED"
- Decided: defer implementation, create backlog item for HLD phase

## Decisions
**Decision: Documentation structure will use monolithic files for AI consumption**

Rationale: AIs reliably read linear files top-to-bottom but skip/invent cross-file references. Hardlinks on Mac provide dev convenience; Windows users receive read-only compiled files.

**Backlog item created:** `Features/1-Backlog/template-infrastructure/protocol-build-pipeline-2026-04-11.md` — design and implement modular source files + automated build in push_template.py with version validation and tamper detection.

**Open questions for HLD:**
1. Build tool: Bash concatenation vs. Pandoc document processing? Trade-offs depend on link handling and formatting requirements.
2. Checksum strategy: commit checksums to git (.meeting-protocol.checksum) or calculate on-the-fly?
3. Per-protocol customization: should each *-protocol.sh handle tool-specific variations (Claude Code vs. Cursor wrappers)?
4. Validation: what happens if generated file is manually edited? Alert only, or block push?
5. Wrapper strategy: should wrappers be hardlinked (Mac) or separate copies (cross-platform)?

## Action Items
- [ ] Create HLD for protocol-build-pipeline backlog item
- [ ] Answer open questions in HLD before implementation

## Comments
**2026-04-11 — Architect (meeting):** Concluded meeting on documentation file structure. Core insight: AI reliability constraint (skip refs) drives monolithic requirement. Deferred implementation to backlog with HLD phase to resolve build tool choice and validation strategy.