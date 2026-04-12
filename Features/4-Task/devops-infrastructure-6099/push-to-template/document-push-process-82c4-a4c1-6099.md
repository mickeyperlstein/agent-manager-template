---
id: 82c4
epic: 6099
feature: a4c1
title: Document Push-to-Template Process
type: task
assignee: agent
review_gate: yes
approved: no
depends_on: bb31, 369f
---

## What
Write comprehensive documentation for the push-to-template workflow: how to manually run it, how it's integrated into CI/CD, what the cache folder does, what to do if something breaks.

## Scope
- README section: "Pushing Template Updates to Main"
- Step-by-step for manual run
- Environment variables and CLI args
- CI/CD integration (GitHub Actions example)
- Troubleshooting: merge fails, push fails, cache corrupted
- Architecture overview: bash wrapper, push_template.py, cache lifecycle
- Examples: what gets pushed, what gets excluded

## Out of Scope
- General git workflow documentation
- Contributing guidelines
- Template feature documentation

## Acceptance Criteria
- [ ] README updated with "Push Process" section
- [ ] Manual invocation documented: `bash push_wrapper.sh`
- [ ] All CLI args and env vars documented
- [ ] GitHub Actions workflow example provided
- [ ] Error scenarios documented with solutions
- [ ] Architecture diagram or text explanation of cache flow
- [ ] Examples show before/after (dev vs clean main)
- [ ] Troubleshooting guide covers common failures

## Test Conditions
**Happy path:** Follow documentation, push succeeds
- Given: documentation is clear and complete
- When: user follows steps to manually push
- Then: push completes successfully

**Error scenario:** Documentation helps user recover
- Given: merge failed during push
- When: user consults troubleshooting section
- Then: user understands why and how to fix it

## Definition of Done
- [ ] README updated with push process section
- [ ] All code examples tested and working
- [ ] Architecture flow is clear (text or diagram)
- [ ] Troubleshooting covers at least 3 error scenarios
- [ ] Examples use actual file names and commands
- [ ] Documentation is readable by non-experts
- [ ] CI/CD integration example is production-ready
- [ ] Links to relevant files (push_wrapper.sh, push_template.py, version.json)
