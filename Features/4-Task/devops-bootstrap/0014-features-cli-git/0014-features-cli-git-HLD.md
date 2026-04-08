# HLD: Features CLI — Git (Features/-scoped Git Operations)

## 1. Problem Statement

Agents working in the Kanban workflow need to commit and push changes (column moves, task updates) without requiring broad git permissions. Standard git operations would allow agents to accidentally commit files outside the `Features/` scope, potentially affecting production code or other sensitive areas.

We need scoped git operations that:
- Only touch files inside `Features/`
- Autonomously handle staging, committing, and pushing
- Have a safe rollback mechanism for mistakes

## 2. Goals

- Provide `features git stage` — stage only Features/ files
- Provide `features git commit -m "<msg>"` — commit only if all staged files are within Features/
- Provide `features git push` — push only if last commit is Features/-scoped
- Provide `features git undo` — revert last Features/-scoped commit
- Handle out-of-bounds files with log-and-recover pattern
- Document in KANBAN.md

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
              │  (extends core CLI) │
              └──────────┬──────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐     ┌──────────┐     ┌──────────┐
   │  stage  │     │  commit  │     │   push   │
   │ command │     │ command  │     │ command  │
   └────┬────┘     └────┬─────┘     └────┬─────┘
        │               │                │
        ▼               ▼                ▼
   ┌─────────┐     ┌──────────┐     ┌──────────┐
   │ git add │     │ validate │     │ validate │
   │ Features│     │ Features │     │ last commit
   │ /       │     │ scope    │     │ scope    │
   └─────────┘     └────┬─────┘     └────┬─────┘
                        │                │
                        ▼                ▼
                   ┌─────────┐      ┌─────────┐
                   │ git     │      │ git     │
                   │ commit  │      │ push    │
                   └─────────┘      └─────────┘
```

### C4 L2 — Containers

Extends the core CLI package with git subcommands:

```
template_workflow/features/
├── __main__.py          # Entry point (extends core)
├── cli.py               # Click group with git subcommand
├── commands/
│   ├── __init__.py
│   ├── move.py          # (from core)
│   ├── new_id.py        # (from core)
│   ├── clean.py         # (from core)
│   └── git/             # NEW: git subcommands
│       ├── __init__.py
│       ├── stage.py
│       ├── commit.py
│       ├── push.py
│       └── undo.py
├── utils/
│   ├── __init__.py
│   ├── paths.py         # (from core)
│   └── git.py           # NEW: git operation wrappers
└── tests/
    ├── __init__.py
    └── test_git/        # NEW: git command tests
        ├── test_stage.py
        ├── test_commit.py
        ├── test_push.py
        └── test_undo.py
```

### Components & Data Model

**Git Operations Component (`utils/git.py`):**
- `git_stage_features() -> List[Path]`: Stage all files under Features/, return list of staged paths
- `git_get_staged_files() -> List[Path]`: Return list of currently staged files
- `git_commit(message: str, files: List[Path]) -> bool`: Commit with message, return success
- `git_push() -> bool`: Push current branch, return success
- `git_get_last_commit_files() -> List[Path]`: Return files touched by last commit
- `git_revert_last_commit() -> bool`: Revert last commit (creates new revert commit)
- `git_unstage_files(files: List[Path]) -> None`: Unstage specific files

**Stage Command (`commands/git/stage.py`):**
- Execute `git add Features/`
- Return list of staged files
- Print summary

**Commit Command (`commands/git/commit.py`):**
1. Get list of staged files
2. Validate all files are within `Features/` directory
3. If out-of-bounds files found:
   - Log the files to stderr
   - Unstage those files
   - Proceed with commit of Features/-only files
   - Re-stage the out-of-bounds files after commit
4. Execute `git commit -m "<message>"`
5. Print commit hash and summary

**Push Command (`commands/git/push.py`):**
1. Get files from last commit
2. Validate all files are within `Features/`
3. If not, reject push with error
4. Execute `git push`
5. Print push summary

**Undo Command (`commands/git/undo.py`):**
1. Get files from last commit
2. Verify all files are within `Features/`
3. If not, reject undo with error (safety guard)
4. Execute `git revert HEAD` (creates revert commit)
5. Print revert commit hash

### Flow

**Stage Flow:**
```
1. Execute: git add Features/
2. Get staged files: git diff --cached --name-only
3. Print: "Staged N files under Features/"
4. Return list of staged paths
```

**Commit Flow:**
```
1. Get staged files
2. Separate into: features_files, out_of_bounds_files
3. If out_of_bounds_files:
   - Log: "Out-of-bounds files detected: [list]"
   - Unstage out_of_bounds_files
4. Execute: git commit -m "<message>"
5. If out_of_bounds_files were unstaged:
   - Re-stage them: git add [files]
   - Log: "Re-staged out-of-bounds files"
6. Print commit result
```

**Push Flow:**
```
1. Get last commit files: git log -1 --name-only
2. Validate all within Features/
3. If any outside: reject with error
4. Execute: git push
5. Print push result
```

**Undo Flow:**
```
1. Get last commit files: git log -1 --name-only
2. Validate all within Features/
3. If any outside: reject with error
4. Execute: git revert HEAD --no-edit
5. Print revert commit hash
```

## 4. Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Shell git commands | Direct, familiar | Per-command permission prompts; no scope guard | Rejected — too much friction |
| Pre-commit hooks | Automatic enforcement | Not agent-friendly; blocks on violations | Rejected — agent needs control |
| MCP server for git | Standardized interface | Adds complexity; overkill for local operations | Rejected — simpler as CLI extension |
| CLI extension (selected) | Single allow; scope guard; intuitive | Requires building | **Selected** — best balance |

## 5. Logging, Monitoring & Metrics

All logs output to stderr.

**Log Entries:**

| Event | Level | Fields | Audience |
|-------|-------|--------|----------|
| Git stage completed | info | file_count, paths | DevOps |
| Git commit completed | info | commit_hash, message, file_count | DevOps |
| Out-of-bounds files detected | warn | file_paths, action_taken | DevOps |
| Git push completed | info | branch, remote | DevOps |
| Git revert completed | info | revert_commit_hash, original_commit | DevOps |
| Scope violation rejected | error | operation, violating_files | DevOps + Alerting |
| Git operation failed | error | command, exit_code, stderr | DevOps + Alerting |

**E2E Observability Contract:**
- Passing stage test observes: `"Staged N files"` log
- Passing commit test observes: `"Git commit completed"` with valid hash
- Passing push test observes: `"Git push completed"` log
- Passing undo test observes: `"Git revert completed"` with revert hash

## 6. Open Questions

**Q1: Entry point extension**
Should `features git` be a Click group with subcommands (`features git stage`) or flat commands (`features git-stage`)?
- **Decision:** Click group pattern — consistent with git CLI mental model.

**Q2: Undo behavior**
Should `undo` revert (safe, creates new commit) or reset (dangerous, rewrites history)?
- **Decision:** Revert only — never rewrite published history.

**Q3: Skill vs MCP**
Should this be implemented as Windsurf skill or MCP server instead of CLI?
- **Decision:** CLI extension — simpler, no external dependencies, works across all agent types.

## 7. Task Decomposition

Generate hex ids:
```bash
python3 -c "import secrets; print(secrets.token_hex(3))"
```

Feature ID: `95d961` (same epic as 0013: `23a043`)

### Task Stubs:

- [ ] `git-utils-c1d2e3-95d961-23a043.md`: Create `utils/git.py` with git operation wrappers
- [ ] `git-stage-command-f4a5b6-95d961-23a043.md`: Implement `features git stage`
- [ ] `git-commit-command-g7h8i9-95d961-23a043.md`: Implement `features git commit` with out-of-bounds handling
- [ ] `git-push-command-j0k1l2-95d961-23a043.md`: Implement `features git push` with scope validation
- [ ] `git-undo-command-m3n4o5-95d961-23a043.md`: Implement `features git undo` (revert)
- [ ] `cli-extension-p6q7r8-95d961-23a043.md`: Extend CLI with `features git` subcommand group
- [ ] `kanban-doc-update-s9t0u1-95d961-23a043.md`: Update KANBAN.md with git operations protocol

## Comments
**2026-04-03 — Architect:** HLD written, task stubs to be created, then move to HLD-Review.
