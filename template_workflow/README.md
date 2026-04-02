# template_workflow

Shared agent tooling consumed by project repos as an upstream.

## Load Order

```
agent-manager-template/template_workflow/   ← upstream defaults
project-repo/template_workflow/             ← project overrides (takes precedence)
```

Project-level files shadow upstream files of the same name. Never edit upstream files directly in a consuming repo — override them in the project's own `template_workflow/` folder.

## Version Policy

- Version is stored in `version.json` at the root of this folder.
- Bump the version on every breaking change to template structure or config schema.
- Consuming repos check `template_workflow/version.json` to know which template version they're on.

| Change type | Version bump |
|---|---|
| Breaking structure or schema change | minor or major |
| Additive / backwards-compatible | patch |

## Checking Your Version

From a consuming repo:

```bash
cat template_workflow/version.json
```
