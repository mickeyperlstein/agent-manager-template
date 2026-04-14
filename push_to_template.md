# Push to Template Script

## What

Automated script that maintains a clean checkout of the `main` branch by:
- Creating a transitory cache folder
- Fast-forward merging dev commits
- Removing dev-only artifacts (Features/, meetings/, tasks.csv, push scripts)
- Pushing clean template to origin/main

**Result**: origin/main contains only template code, no dev metadata or feature tracking.

## Why

Replaces manual git filtering and complex `.gitignore` strategies. The script uses a whitelist approach: only stage allowed files, implicitly excluding artifacts. This is safer and more maintainable than explicit removal.

## Installation

```bash
# Copy script to project root
cp push_to_template.py /path/to/repo/

# Ensure it's executable
chmod +x push_to_template.py
```

## Usage

### Manual Run

```bash
# Basic usage (uses defaults)
python3 push_to_template.py

# With environment variables
BRANCH=dev PUSH_DEV_REPO=/path/to/dev/repo python3 push_to_template.py
```

**Output**:
- Exit code 0: success
- Exit code 1: failure (see stderr for details)
- stdout: progress messages
- stderr: errors

### GitHub Actions

```yaml
# .github/workflows/push-template.yml
name: Push Clean Template

on:
  push:
    branches: [main]

jobs:
  push-template:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Checkout both main and dev
        run: |
          git fetch origin main:main
          git fetch origin dev:dev
      
      - name: Run push-to-template
        env:
          PUSH_DEV_REPO: ${{ github.workspace }}
          BRANCH: main
        run: python3 push_to_template.py
      
      - name: Report result
        if: always()
        run: |
          echo "Script exit code: ${{ job.status }}"
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `PUSH_DEV_REPO` | (required) | Path to dev repository to merge from |
| `PUSH_CACHE_FOLDER` | `~/Documents/agent-manager-template-release/` | Cache folder location |
| `BRANCH` | `dev` | Branch name to merge from dev |
| `VERSION` | (optional) | Version string for logging |

**Example:**
```bash
PUSH_DEV_REPO=/home/user/projects/repo \
PUSH_CACHE_FOLDER=/tmp/cache \
BRANCH=dev \
VERSION=1.0.0 \
python3 push_to_template.py
```

## Process Flow

```
Input: PUSH_DEV_REPO, BRANCH
  ↓
[1] Initialize Cache
    - Create cache folder at PUSH_CACHE_FOLDER
    - Stash any existing work (preserve if interrupted)
    - Fetch latest from origin
    - Pull main to latest state
    ↓
[2] Setup Remotes
    - Add dev repo as 'dev' remote
    - Ensure 'origin' points to shared remote
    ↓
[3] Merge Dev Branch
    - Fetch from dev remote
    - Merge BRANCH with --ff-only (fast-forward only)
    - Fail gracefully if not fast-forward
    ↓
[4] Filter Artifacts
    - Get git status of merged changes
    - Filter artifacts:
      * Features/ folder
      * meetings/ folder
      * tasks.csv
      * push_to_template.py
      * push_template.sh
    - Stage only allowed files
    ↓
[5] Commit & Push
    - Commit with message: "chore: merge dev changes to template"
    - Push to origin/main
    ↓
Output: Exit code 0 (success) or 1 (failure)
```

## Artifact Removal Strategy

The script uses a **whitelist approach**:
1. Get git status of all changed files
2. Filter OUT excluded items (Features/, meetings/, etc.)
3. Stage ONLY allowed files with `git add`
4. Commit and push

**Result**: Excluded files are never staged, so they're implicitly removed from main.

### Excluded Items

- `Features/` - Feature tracking folder and all contents
- `meetings/` - Meeting notes folder and all contents
- `tasks.csv` - Task list (root level only)
- `push_to_template.py` - Script itself
- `push_template.sh` - Shell wrapper

To add items to exclusion list, edit the `filter_artifacts()` function in `push_to_template.py`.

## Error Handling

### Merge Fails (Not Fast-Forward)

**Cause**: Someone manually edited origin/main (not pushed via script)

**Error**: `error: merge --ff-only dev/main failed (not fast-forward)`

**Fix**:
```bash
# Inspect origin/main to see what diverged
git log origin/main

# Option 1: Reset origin/main to expected state (careful!)
# Option 2: Resolve divergence in dev repo, then retry script
```

### Push Fails (Permission/Network)

**Cause**: origin/main is unreachable or permission denied

**Error**: `error: push to origin/main failed`

**Fix**:
```bash
# Check origin is reachable
git ls-remote origin

# Check credentials (SSH key, PAT, etc.)
# Retry script (idempotent - safe to retry)
python3 push_to_template.py
```

### Cache Corruption

**Cause**: Interrupted run or stale cache

**Error**: Merge or push failures with confusing git errors

**Fix**:
```bash
# Delete cache folder (transitory by design)
rm -rf ~/Documents/agent-manager-template-release/

# Retry script (will reinitialize cache)
python3 push_to_template.py
```

## Idempotency & Safety

The script is **idempotent**: safe to retry on any failure.

**Why**:
- Cache is reset fresh each run (stash→fetch→pull)
- If merge fails → exit(1), nothing persisted to main
- If push fails → exit(1), cache unchanged
- Next run starts clean and retries safely

**No cleanup needed**: Just fix the underlying issue and run again.

## Testing

```bash
# Run unit tests
python3 -m pytest tests/test_push_to_template.py -v

# Run with dry-run (manual verification)
# Edit main() to add dry-run support or inspect cache manually
ls -la ~/Documents/agent-manager-template-release/
git -C ~/Documents/agent-manager-template-release/ log --oneline
```

## Files

- `push_to_template.py` - Main script with all functions
- `tests/test_push_to_template.py` - Unit tests (21 tests, all passing)

## Workflow Integration

The script is designed to be called from:
- Manual CLI: `python3 push_to_template.py`
- GitHub Actions: see example above
- Other CI systems: set env vars and run

All integration points should:
- Set `PUSH_DEV_REPO` to the dev repository path
- Capture exit code (0 = success, 1 = failure)
- Log stdout/stderr for debugging
- Retry on failure (script is idempotent)
