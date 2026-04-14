---
id: 2970
epic: 6099
feature: a4c1
title: CI/GitHub Actions Integration
type: task
assignee: architect
review_gate: no
depends_on: "6eb3,e329,5829,c773"
---

## Task: CI/GitHub Actions Integration

**What:** Wire up script for GitHub Actions, document env vars, make callable from CI.

**Acceptance Criteria:**
- [ ] Script callable from GitHub Actions workflow
- [ ] Env vars: BRANCH (default dev), VERSION (optional)
- [ ] Exit codes clear: 0=success, 1=failure
- [ ] No interactive prompts (CI-friendly)
- [ ] Logging to stdout/stderr

**Definition of Done:**
- [ ] GitHub Actions example workflow provided
- [ ] Env vars documented
- [ ] CI integration tested
