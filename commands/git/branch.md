---
description: "Create a new git branch with conventional naming (supports Chinese input)"
argument-hint: Branch name or description (e.g., "user login" or "feature/user-login")
allowed-tools: Bash, Read, TodoWrite, AskUserQuestion
---

# Git Branch

Create a new branch following naming conventions.

## Phase 1: Parse Input

**Parse `$ARGUMENTS`**:
- If formatted (feature/xxx, fix/xxx): use as-is
- If description: generate branch name
- If empty: ask user for branch purpose

## Phase 2: Generate Branch Name

**Format**: `<type>/<description>`

**Types**:
| Type | Use Case |
|------|----------|
| feature/ | New features |
| fix/ | Bug fixes |
| hotfix/ | Urgent fixes |
| refactor/ | Refactoring |
| docs/ | Documentation |
| test/ | Testing |
| chore/ | Maintenance |

**Rules**:
- Lowercase
- Hyphens for spaces
- Under 50 characters
- Descriptive but concise

**Examples**:
- "user login" → `feature/user-login`
- "fix crash" → `fix/crash`
- "update docs" → `docs/update`

**Chinese input**: Translate to English
- "用户登录" → `feature/user-login`
- "修复首页崩溃" → `fix/homepage-crash`

## Phase 3: Handle Uncommitted Changes

**If uncommitted changes exist**, ask:
- Stash changes?
- Commit first?
- Carry to new branch? (default)

## Phase 4: Create Branch

**Actions**:
1. `git checkout -b <branch-name>`
2. Ask: push to remote? (`git push -u origin <branch>`)
3. Show success message

## Output Language

- All messages: Chinese
- Branch names: English
