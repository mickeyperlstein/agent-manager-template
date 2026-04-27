---
id: bash1
epic: 6099
feature: a4c1
title: Bash Wrapper - Cache Initialization
type: task
layer: BASH
assignee: architect
review_gate: no
depends_on: ""
---

## Task: Cache Initialization in Bash Wrapper

**What:** Extend `push_template.sh` to set up and maintain a clean main checkout in a cache folder.

**Layer:** BASH (per HLD Architecture section)

**File to modify:** `push_template.sh`

## LLD (Low-Level Design)

### Interface

```bash
#!/bin/bash
# push_template.sh

# Usage: ./push_template.sh
# Environment variables:
#   PUSH_REPO_URL (required): URL of origin (template) repo
#   PUSH_CACHE_FOLDER (optional): path to cache, default ~/Documents/agent-manager-template-release
# Exit: 0 on success, 1 on error
```

### Algorithm

```bash
set -e

# 1. Read env vars
CACHE_DIR="${PUSH_CACHE_FOLDER:-$HOME/Documents/agent-manager-template-release}"
REPO_URL="${PUSH_REPO_URL}"

# 2. Validate
if [ -z "$REPO_URL" ]; then
  echo "error: PUSH_REPO_URL not set" >&2
  exit 1
fi

# 3. Create or reset cache
if [ ! -d "$CACHE_DIR" ]; then
  git clone "$REPO_URL" "$CACHE_DIR"
else
  cd "$CACHE_DIR"
  git fetch origin
fi

# 4. Ensure clean main checkout
cd "$CACHE_DIR"
git checkout main
git pull origin main

# 5. Hand off to Python for business logic
python3 push_template.py
```

### Responsibilities

- ✅ Create cache folder if missing
- ✅ Clone origin repo (first run)
- ✅ Checkout main branch
- ✅ Fetch latest from origin
- ✅ Pull main to latest state
- ✅ Exit with 1 if PUSH_REPO_URL missing
- ✅ Exit with error code from Python script
- ❌ DO NOT handle git merge (Python's job)
- ❌ DO NOT filter artifacts (Python's job)
- ❌ DO NOT commit or push (Python's job)

### Test Plan

**Unit test 1: Creates cache from scratch**
- Given: PUSH_REPO_URL set, cache folder missing
- When: ./push_template.sh (will call Python, mock Python to just exit 0)
- Then: Cache folder created, origin set, main checked out

**Unit test 2: Resets existing cache**
- Given: Cache exists with stale commits
- When: ./push_template.sh
- Then: Fetch + pull updated main to latest

**Unit test 3: Validates PUSH_REPO_URL**
- Given: PUSH_REPO_URL not set
- When: ./push_template.sh
- Then: Error message to stderr, exit 1

**Integration test: Hands off to Python**
- Given: Cache initialized
- When: ./push_template.sh with Python script in place
- Then: Python script receives clean main checkout

---

## Definition of Done

- [x] File: `push_template.sh` extended (not rewritten)
- [x] Handles first-run clone case
- [x] Handles subsequent-run fetch/pull case
- [x] Validates PUSH_REPO_URL environment variable
- [x] Ensures clean main checkout before calling Python
- [x] All tests passing (bash integration with mock Python)
- [x] No Python code in this script (respect the layer boundary)
