---
description: "Merge changes from a worktree branch into current branch"
argument-hint: Worktree branch name to merge (e.g., "feature/login")
allowed-tools: Bash, Read, Grep, TodoWrite, AskUserQuestion
---

# Git Worktree Merge

Merge changes from a worktree branch into the current branch.

## Phase 1: Analyze Current State

**Actions**:
1. `git branch --show-current` - get current branch
2. `git worktree list` - show all worktrees
3. `git status` - check for uncommitted changes

**If uncommitted changes**:
- Warn user
- Ask: stash, commit, or abort?

## Phase 2: Select Source Branch

**If `$ARGUMENTS` provided**:
- Use as source branch name
- Validate branch exists

**If empty**:
- List available worktree branches
- Ask user to select one

## Phase 3: Preview Changes

**Show merge preview**:
```bash
git log --oneline <current>..<source>
git diff --stat <current>..<source>
```

**Ask user**:
- Confirm merge?
- Merge strategy: merge commit or squash?

## Phase 4: Execute Merge

**Standard merge**:
```bash
git merge <source-branch> --no-ff -m "Merge branch '<source>' into <current>"
```

**Squash merge**:
```bash
git merge --squash <source-branch>
git commit -m "<generated-message>"
```

## Phase 5: Handle Conflicts

**If conflicts occur**:
1. List conflicting files
2. Ask user to resolve manually or abort
3. After resolution: `git add . && git commit`

## Phase 6: Post-Merge

**Ask user**:
- Delete source worktree? (use `/git:worktree-remove`)
- Push merged changes?
- Create PR?

**Show summary**:
- Commits merged
- Files changed
- Current branch status

## Merge Strategies

| Strategy | Use Case |
|----------|----------|
| merge --no-ff | Preserve full history |
| merge --squash | Clean single commit |
| rebase | Linear history (advanced) |

## Output Language

- All messages: Chinese
- Git commands: As-is
