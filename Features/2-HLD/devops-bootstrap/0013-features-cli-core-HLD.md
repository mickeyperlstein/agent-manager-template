# HLD: Features CLI — Core (Column Moves + ID Generation)

## 1. Problem Statement

Agents working in the Kanban workflow need to move task files between column folders and generate unique hex IDs. Currently, this requires shell commands (`mv`, `mkdir`, `rm`) which trigger permission prompts on every operation. This creates friction and slows down agent work.

We need a sandboxed CLI tool that:
- Handles all permission-sensitive workflow operations inside `Features/`
- Provides a single `allow` grant point for agents
- Enforces safety constraints (never operates outside `Features/`)

## 2. Goals

- Provide `features move <filepath> <target-column>` for safe column moves
- Provide `features new-id [task|feature|epic]` for collision-free 3-byte hex ID generation
- Provide `features clean` for bulk deletion of marked-for-deletion files
- Enforce startup guard: all paths must be within `Features/`
- Enable single `allow` on `python -m features` covering all operations
- Document the protocol in KANBAN.md

## 3. Architecture

### C4 L1 — Context

```
┌─────────────────────────────────────────────────────────────┐
│                         Agent                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Claude/Windsurf Code with permission prompts       │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │ single 'allow' for python -m features│
└────────────────────────┼────────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   features CLI      │
              │  (sandboxed ops)    │
              └──────────┬──────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐     ┌──────────┐     ┌──────────┐
   │  move   │     │ new-id   │     │  clean   │
   │ command │     │ command  │     │ command  │
   └────┬────┘     └────┬─────┘     └────┬─────┘
        │               │                │
        ▼               ▼                ▼
   ┌─────────┐     ┌──────────┐     ┌──────────┐
   │ git mv  │     │ secrets  │     │  rm +    │
   │ mkdir   │     │ token_hex│     │  git rm  │
   │ -p      │     │          │     │          │
   └─────────┘     └──────────┘     └──────────┘
```

### C4 L2 — Containers

Single Python package with modular command structure:

```
template_workflow/features/
├── __init__.py          # Package init
├── __main__.py          # Entry point: cli()
├── cli.py               # Click-based CLI definition
├── commands/
│   ├── __init__.py
│   ├── move.py          # Move command implementation
│   ├── new_id.py        # ID generation implementation
│   └── clean.py         # Clean command implementation
├── utils/
│   ├── __init__.py
│   ├── paths.py         # Path validation (Features/ constraint)
│   └── git.py           # Git operation wrappers
└── tests/
    ├── __init__.py
    ├── test_move.py
    ├── test_new_id.py
    └── test_clean.py
```

### Components & Data Model

**Path Validation Component (`utils/paths.py`):**
- `validate_within_features(path: Path) -> Path`: Raises `ValueError` if path escapes `Features/`
- `get_features_root() -> Path`: Returns absolute path to `Features/` directory
- `resolve_column_path(column: str, epic: str, feature: str) -> Path`: Builds target path from components

**Git Operations Component (`utils/git.py`):**
- `git_mv(src: Path, dst: Path) -> bool`: Execute `git mv`, return success
- `git_rm(path: Path) -> bool`: Execute `git rm`, return success
- `ensure_dir(path: Path) -> None`: `mkdir -p` equivalent

**ID Generation Component (`commands/new_id.py`):**
- `generate_id() -> str`: `secrets.token_hex(3)` wrapper
- `check_collision(features_dir: Path, id: str) -> bool`: Scan all .md files for duplicate IDs in frontmatter

**Move Command (`commands/move.py`):**
- Parse source file frontmatter for epic/feature
- Validate target column (must be 1-9 with name)
- Build target path: `Features/{column}/{epic}/{feature}/{filename}`
- Execute `git mv` + `mkdir -p` as needed
- Update file frontmatter: `column: {target}`

**Clean Command (`commands/clean.py`):**
- Walk `Features/` for all `.md` files
- Parse frontmatter, collect files where `state: marked-for-deletion`
- Execute `git rm` for each (or `rm` if not tracked)
- Print summary of actions

### Flow

**Move Flow:**
```
1. Parse arguments: filepath, target-column
2. Resolve absolute paths, validate within Features/
3. Read source file, parse frontmatter for epic/feature
4. Build destination path
5. Ensure destination directory exists
6. Execute git mv
7. Update frontmatter column field
8. Print success message
```

**New-ID Flow:**
```
1. Parse optional type argument (task/feature/epic)
2. Generate 3-byte hex ID
3. Scan all Features/ .md files for collision
4. If collision, regenerate and retry (max 10 attempts)
5. Print ID to stdout (for capture by agent)
```

**Clean Flow:**
```
1. Walk Features/ directory tree
2. For each .md file: parse frontmatter
3. If state == "marked-for-deletion": collect path
4. For each collected path: git rm (or rm)
5. Print count of deleted files
```

## 4. Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Shell scripts (`mv`, `rm`) | Simple, no code | Per-command permission prompts | Rejected — too much friction |
| Direct Python file ops | Full control | Permission prompts for each script | Rejected — same problem |
| CLI with single entrypoint | One `allow` covers all | Requires building CLI | **Selected** — solves the core problem |
| `mark-for-deletion` only | No file deletion | Accumulates dead files | Rejected — need clean command |

## 5. Logging, Monitoring & Metrics

All logs output to stderr (stdout reserved for command output like ID generation).

**Log Entries:**

| Event | Level | Fields | Audience |
|-------|-------|--------|----------|
| CLI invoked | info | command, args | DevOps |
| Path validation failed | error | path, reason | DevOps + Alerting |
| Move completed | info | src, dst, duration_ms | DevOps |
| ID generated | info | id, type, collision_count | DevOps |
| ID collision detected | warn | attempted_id, retry | DevOps |
| Clean deleted N files | info | count, paths | DevOps |
| Git operation failed | error | command, exit_code, stderr | DevOps + Alerting |

**Metrics (future — CLI v2):**
- `features_moves_total` — counter by column
- `features_ids_generated_total` — counter
- `features_cleaned_total` — counter
- `features_operation_duration_ms` — histogram by command

**E2E Observability Contract:**
- Passing move test observes: `"Move completed"` log with correct src/dst
- Passing new-id test observes: stdout contains 6-char hex string, no collision warnings
- Passing clean test observes: `"Clean deleted"` log with count > 0

## 6. Open Questions

None. Design is complete for core scope.

## 7. Task Decomposition

HLD agent creates task stub files alongside the HLD doc.

Generate hex ids:
```bash
python3 -c "import secrets; print(secrets.token_hex(3))"
```

### Task Stubs:

- [ ] `cli-entrypoint-a1b2c3-bd72df-23a043.md`: Create `__main__.py` entrypoint and Click CLI skeleton
- [ ] `path-validation-d4e5f6-bd72df-23a043.md`: Implement `utils/paths.py` with Features/ constraint validation
- [ ] `move-command-g7h8i9-bd72df-23a043.md`: Implement `features move` with git mv and frontmatter update
- [ ] `new-id-command-j0k1l2-bd72df-23a043.md`: Implement `features new-id` with collision detection
- [ ] `clean-command-m3n4o5-bd72df-23a043.md`: Implement `features clean` for marked-for-deletion files
- [ ] `kanban-doc-update-p6q7r8-bd72df-23a043.md`: Add "Column Move Protocol" section to KANBAN.md

## Comments
**2026-04-03 — Architect:** HLD written, task stubs to be created, then move to HLD-Review.
