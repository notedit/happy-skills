---
description: "Complete workflow: commit, push, and create Pull Request"
argument-hint: Optional PR title or target branch
allowed-tools: Bash, Read, Grep, Glob, TodoWrite, AskUserQuestion
---

# Git PR

Complete git workflow from local changes to Pull Request.

## Phase 1: Pre-flight Check

**Actions**:
1. `git status` - check for changes
2. `git branch --show-current` - get current branch
3. Warn if on main/master branch
4. Check remote tracking: `git rev-parse --abbrev-ref @{u}`

## Phase 2: Commit Changes

**If uncommitted changes exist**:
- Follow `/git:commit` workflow
- Skip if no changes

## Phase 3: Push to Remote

**Actions**:
1. Check remote branch: `git ls-remote --heads origin <branch>`
2. If not exists: `git push -u origin <branch>`
3. If exists: `git push`
4. Handle push conflicts (suggest `git pull --rebase`)

## Phase 4: Create Pull Request

**Actions**:
1. Determine target branch (default: main, or from `$ARGUMENTS`)
2. Get commits: `git log main..<branch> --oneline`
3. Generate PR content:
   ```markdown
   ## Summary
   - Key changes description

   ## Changes
   - List based on commits

   ## Testing
   - How to verify
   ```
4. Create PR:
   ```bash
   gh pr create --title "<title>" --body "<body>" --base <target>
   ```
5. Return PR URL

## Error Handling

| Situation | Action |
|-----------|--------|
| No `gh` CLI | Provide manual instructions |
| Push rejected | Suggest `git pull --rebase` |
| On main branch | Ask to create feature branch first |

## Output Language

- Status messages: Chinese
- PR title/body: English
