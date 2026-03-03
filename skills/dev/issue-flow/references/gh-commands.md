# gh CLI Quick Reference

## Issue Operations

```bash
# List open issues
gh issue list --state open --limit 20

# View issue details (JSON)
gh issue view <N> --json number,title,body,labels,comments,assignees,state

# View issue details (human-readable)
gh issue view <N>

# Add comment to issue
gh issue comment <N> --body "<markdown content>"

# Close issue with comment
gh issue close <N> --comment "Closed via PR #<PR>"

# Get repo info
gh repo view --json nameWithOwner -q .nameWithOwner
```

## PR Operations

```bash
# Create PR
gh pr create --title "<title>" --body "<body>"

# Create PR with specific base branch
gh pr create --title "<title>" --body "<body>" --base main

# Check CI status (blocking, with timeout)
gh pr checks <PR_NUMBER> --watch --fail-fast

# Check CI status (non-blocking)
gh pr checks <PR_NUMBER>

# Merge PR (squash)
gh pr merge <PR_NUMBER> --squash --delete-branch

# Merge PR (merge commit)
gh pr merge <PR_NUMBER> --merge --delete-branch

# Add reviewer
gh pr edit <PR_NUMBER> --add-reviewer <username>

# View PR
gh pr view <PR_NUMBER>
```

## API Operations (for comment editing)

```bash
# List issue comments (find by marker)
gh api repos/{owner}/{repo}/issues/<N>/comments \
  --jq '.[] | select(.body | contains("issue-flow-plan")) | .id'

# Update existing comment
gh api repos/{owner}/{repo}/issues/comments/<COMMENT_ID> \
  -X PATCH -f body="<new content>"
```

## Branch Operations

```bash
# Check for existing issue branches
git branch -a --list '*issue/<N>*'

# Push new branch
git push -u origin <branch-name>
```

## Tips

- Always use `--json` flag when you need to parse output programmatically
- Use `--jq` for inline JSON filtering
- `gh` respects the current repo context from the working directory
- For HEREDOC body content, use `"$(cat <<'EOF' ... EOF)"` pattern to preserve formatting
