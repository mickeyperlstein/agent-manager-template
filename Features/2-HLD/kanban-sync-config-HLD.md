# Feature: CSV/Folder Sync Authority Config

**ID:** 0018  
**Status:** HLD  
**Assignee:** architect  
**Type:** feature  
**Review Gate:** yes  

## Summary
Define a config setting that specifies whether CSV or Folders is the source of truth for Kanban state, and enforce sync direction accordingly.

## Problem
Currently, bidirectional sync between CSV and folders causes data loss:
- Edit CSV → run `folders_to_csv` → lose CSV changes
- Edit folders → run `csv_to_folders` → lose folder changes

There is no defined authority or config to control which direction the sync should flow.

## Goals
- Single source of truth (SOT) is configurable per environment
- Agents and humans know which direction is authoritative
- Sync scripts validate authority before destructive operations
- Config is documented and accessible to all workflow participants

## Scope

**In:**
- Add config option to define SOT (CSV or Folders)
- Update sync scripts (`csv_to_folders.py`, `folders_to_csv.py`) to check authority
- Document authority setting in Agent-HowTos and start protocol
- Default authority setting (recommend CSV as SOT based on "Source of Truth: tasks.csv" in Kanban docs)

**Out:**
- Actual config file infrastructure (separate feature)
- Interactive prompts to switch authority

## Definition of Done
- [ ] Config option exists and is documented
- [ ] Sync scripts validate and respect authority before running
- [ ] Agent-HowTos/Kanban.md documents which is SOT
- [ ] Start protocol reminds agents of authority
- [ ] Config default is set

## Comments
**2026-04-09 — architect (feature creation):** Created to resolve bidirectional sync ambiguity and prevent data loss during workflow operations.
