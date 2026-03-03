# PR Template

## Title Format

```
<type>: <concise description> (#<issue-number>)
```

**Type prefixes** (Conventional Commits):
- `feat` — new feature
- `fix` — bug fix
- `refactor` — code restructuring without behavior change
- `docs` — documentation only
- `test` — adding or updating tests
- `chore` — maintenance, dependencies, CI

Examples:
- `feat: add OAuth2 login support (#42)`
- `fix: resolve race condition in data sync (#87)`
- `refactor: extract validation logic to shared module (#15)`

## Body Template

```markdown
## Summary

<2-3 sentences describing what this PR does and why>

Closes #<ISSUE_NUMBER>

## Changes

- <bullet point for each logical change>
- <include file paths for clarity>

## Test Plan

- [ ] <specific test or verification step>
- [ ] <another test step>
- [ ] Existing tests pass

## Notes

<optional: migration steps, deployment considerations, breaking changes>
```

## Issue Linking

Always include `Closes #<N>` in the PR body to auto-close the Issue on merge. Use the exact keyword `Closes` (not `Fixes` or `Resolves`) for consistency.

## PR Creation Command

```bash
gh pr create \
  --title "<type>: <description> (#<N>)" \
  --body "$(cat <<'EOF'
## Summary

<summary>

Closes #<N>

## Changes

- <changes>

## Test Plan

- [ ] <test steps>
- [ ] Existing tests pass
EOF
)"
```
