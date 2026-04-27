---
id: py01
epic: 6099
feature: a4c1
title: Python Filter - Artifacts & File Staging
type: task
layer: PYTHON
assignee: architect
review_gate: no
depends_on: ""
---

## Task: Filter & Stage Allowed Files

**What:** Parse `git status`, filter out dev-only artifacts, stage only allowed files.

**Layer:** PYTHON (per HLD Architecture section)

**File to modify:** `push_template.py`

**Assumption:** Bash wrapper (push_template.sh) has already ensured we're on a clean main checkout in the cache folder. This task runs after `git merge --ff-only dev/dev` succeeds.

## LLD (Low-Level Design)

### Interface

```python
def filter_artifacts(git_status: str) -> list:
    """
    Parse git status --porcelain output and return allowed file paths.
    
    Args:
        git_status (str): Output from `git status --porcelain`
        
    Returns:
        list: Filepaths that are allowed to be staged (artifacts excluded)
    """

def stage_allowed_files(repo_path: str) -> None:
    """
    Get git status, filter artifacts, stage only allowed files.
    
    Args:
        repo_path (str): Path to repo root
        
    Raises:
        subprocess.CalledProcessError: If git operations fail
    """
```

### Algorithm

**filter_artifacts(git_status: str) -> list:**

```python
# Excluded at root level (exact match only)
excluded_files = {
    'tasks.csv',
    'push_to_template.py',
    'push_template.sh',
}

# Excluded folders (prefix match with /)
excluded_folders = (
    'Features/',
    'meetings/',
)

allowed = []
for line in git_status.strip().split('\n'):
    if not line:
        continue
    
    # Parse: "M  README.md" → filepath = "README.md"
    parts = line.split(None, 1)
    if len(parts) < 2:
        continue
    
    filepath = parts[1]
    
    # Exclude exact matches at root
    if filepath in excluded_files:
        continue
    
    # Exclude folder prefixes
    if any(filepath.startswith(f) for f in excluded_folders):
        continue
    
    allowed.append(filepath)

return allowed
```

**stage_allowed_files(repo_path: str) -> None:**

```python
# 1. Get current git status
status_output = subprocess.run(
    ['git', 'status', '--porcelain'],
    cwd=repo_path,
    capture_output=True,
    text=True,
    check=True
).stdout

# 2. Filter to allowed files only
allowed_files = filter_artifacts(status_output)

# 3. Stage only allowed files (artifacts implicit excluded)
if allowed_files:
    subprocess.run(['git', 'add'] + allowed_files, cwd=repo_path, check=True)
```

### Invariants

- Artifacts are **never** staged (implicit exclusion, not explicit deletion)
- Whitelist approach: only stage what's allowed, don't try to remove what's not
- If all changes are artifacts (Features/*, meetings/*, etc.), nothing is staged — that's OK
- Folder prefix matching is exact: `Features/` stops `Features/item.md` but not `FeaturesThing/`
- Root-level exact match: `tasks.csv` but not `features/tasks.csv`

### Test Plan

**Unit test 1: Empty status**
- Given: `git status --porcelain` is empty
- When: `filter_artifacts("")`
- Then: Returns `[]`

**Unit test 2: Single allowed file**
- Given: `"M  README.md"`
- When: `filter_artifacts("M  README.md")`
- Then: Returns `["README.md"]`

**Unit test 3: Excludes Features/ folder**
- Given: `"?? Features/new-item.md"`
- When: `filter_artifacts(...)`
- Then: Returns `[]`

**Unit test 4: Excludes meetings/ folder**
- Given: `"M  meetings/2026-04-15.md\nM  README.md"`
- When: `filter_artifacts(...)`
- Then: Returns `["README.md"]`

**Unit test 5: Excludes root-level tasks.csv**
- Given: `"M  tasks.csv\nM  docs/guide.md"`
- When: `filter_artifacts(...)`
- Then: Returns `["docs/guide.md"]`

**Unit test 6: Mixed allowed and excluded**
- Given: `"M  README.md\n?? Features/item.md\nM  tasks.csv\nA  docs/api.md"`
- When: `filter_artifacts(...)`
- Then: Returns `["README.md", "docs/api.md"]` (in order)

**Integration test: Stage only allowed**
- Given: Repo with mixed allowed/excluded changes
- When: `stage_allowed_files(repo_path)`
- Then: `git status --short` shows only allowed files staged

---

## Definition of Done

- [ ] Function: `filter_artifacts()` implemented
- [ ] Function: `stage_allowed_files()` implemented
- [ ] All unit tests passing (6 tests)
- [ ] Integration test passing
- [ ] No subprocess calls in filter_artifacts (pure function, testable)
- [ ] Layer boundary: Python-only, no bash here
- [ ] Respect excluded items list: can be extended in central location
