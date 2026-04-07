---
id: "8a9f1f"
epic: "23a043"
feature: "95d961"
title: Path validation with Features/ constraint
type: task
assignee: agent
review_gate: no
approved: yes
---

## What
Implement path validation utilities that enforce all operations stay within the `Features/` directory tree.

## Scope
- Create `template_workflow/features/utils/paths.py`
- Implement `get_features_root() -> Path` — returns absolute path to `Features/`
- Implement `validate_within_features(path: Path) -> Path` — raises ValueError if path escapes `Features/`
- Implement `resolve_column_path(column: str, epic: str, feature: str) -> Path` — builds target path

## Acceptance Criteria
- [ ] `validate_within_features` raises ValueError for paths outside Features/
- [ ] `validate_within_features` returns resolved Path for valid paths
- [ ] `resolve_column_path` builds correct path structure
- [ ] All functions have docstrings

## Test Conditions
- Test with path inside Features/ → should pass
- Test with path outside Features/ → should raise ValueError
- Test `resolve_column_path("6-Implementation", "23a043", "95d961")` returns correct path

## Definition of Done
- `paths.py` implemented with all functions
- Unit tests pass
- Path traversal attempts are blocked
