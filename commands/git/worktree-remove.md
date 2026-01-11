---
description: "Remove a git worktree and optionally delete the branch"
argument-hint: Worktree path or branch name (e.g., "../my-project-feature" or "feature/login")
allowed-tools: Bash, Read, TodoWrite, AskUserQuestion
---

# Git Worktree Remove

Safely remove a worktree and clean up associated resources.

## Phase 1: List Worktrees

**Actions**:
```bash
git worktree list
```

**Show table**:
| Path | Branch | Status |
|------|--------|--------|
| /path/to/main | main | (bare) |
| /path/to/feature | feature/x | clean |

## Phase 2: Select Worktree

**If `$ARGUMENTS` provided**:
- Match by path or branch name
- Validate worktree exists

**If empty**:
- Show worktree list
- Ask user to select one

**Prevent removing main worktree**.

## Phase 3: Pre-Removal Checks

**Check for uncommitted changes**:
```bash
cd <worktree-path> && git status
```

**If changes exist**:
- Show changed files
- Ask user:
  - Stash changes?
  - Commit changes?
  - Discard changes?
  - Abort removal?

**Check for unpushed commits**:
```bash
git log origin/<branch>..<branch> --oneline
```

If unpushed: warn user and ask to push first.

## Phase 4: Remove Worktree

**Standard removal**:
```bash
git worktree remove <path>
```

**Force removal** (if dirty):
```bash
git worktree remove --force <path>
```

## Phase 5: Branch Cleanup

**Ask user**: Delete the branch too?

**If yes, check merge status**:
```bash
git branch --merged main | grep <branch>
```

**Delete branch**:
- If merged: `git branch -d <branch>`
- If not merged: warn, require `git branch -D <branch>`

**Delete remote branch** (optional):
```bash
git push origin --delete <branch>
```

## Phase 6: Prune Stale References

**Clean up**:
```bash
git worktree prune
```

**Show final worktree list**.

## Safety Checks

| Check | Action |
|-------|--------|
| Uncommitted changes | Require user decision |
| Unpushed commits | Warn and confirm |
| Unmerged branch | Require force confirm |
| Main worktree | Block removal |

## Output Language

- All messages: Chinese
- Paths and commands: As-is
