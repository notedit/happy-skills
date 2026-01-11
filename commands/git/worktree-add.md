---
description: "Create a new git worktree with environment files copied"
argument-hint: Branch name or new branch name (e.g., "feature/new-feature")
allowed-tools: Bash, Read, Glob, TodoWrite, AskUserQuestion
---

# Git Worktree Add

Create a new worktree and copy essential environment files.

## Phase 1: Parse Input

**Parse `$ARGUMENTS`**:
- If branch name provided: use it
- If empty: ask user for branch name or create new branch

**Check**:
1. `git worktree list` - show existing worktrees
2. Validate branch exists or will be created

## Phase 2: Determine Worktree Path

**Default path**: `../<repo-name>-<branch-name>`

**Example**:
- Repo: `my-project`, Branch: `feature/login`
- Path: `../my-project-feature-login`

Ask user to confirm or customize path.

## Phase 3: Create Worktree

**If branch exists**:
```bash
git worktree add <path> <branch>
```

**If new branch**:
```bash
git worktree add -b <branch> <path>
```

## Phase 4: Copy Environment Files

**Files to copy** (if they exist in main worktree):
| File | Description |
|------|-------------|
| .env | Environment variables |
| .env.local | Local environment |
| .env.development | Development config |
| .env.development.local | Local dev config |
| .env.test | Test config |
| .env.production.local | Local prod config |
| .envrc | direnv config |

**Copy command**:
```bash
for f in .env .env.local .env.development .env.development.local .env.test .env.production.local .envrc; do
  [ -f "$f" ] && cp "$f" "<worktree-path>/"
done
```

**Additional files** (ask user):
- `.npmrc` / `.yarnrc` - Package manager config
- `config/local.json` - Local config files
- Other project-specific files

## Phase 5: Post-Setup

**Actions**:
1. Show success message with worktree path
2. List copied environment files
3. Suggest next steps:
   - `cd <worktree-path>`
   - Install dependencies if needed
   - `git worktree list` to see all worktrees

## Error Handling

| Situation | Action |
|-----------|--------|
| Branch already checked out | Suggest using existing worktree |
| Path exists | Ask to remove or use different path |
| Uncommitted changes | Warn user, suggest stash |

## Output Language

- All messages: Chinese
- Commands and paths: As-is
