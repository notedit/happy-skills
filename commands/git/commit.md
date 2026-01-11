---
description: "Commit changes with auto-generated semantic commit message (Conventional Commits format)"
argument-hint: Optional commit message
allowed-tools: Bash, Read, Grep, Glob, TodoWrite, AskUserQuestion
---

# Git Commit

Create a well-structured git commit with semantic commit message.

## Phase 1: Analyze Changes

**Actions**:
1. Run `git status` to check working tree state
2. Run `git diff` for unstaged changes
3. Run `git diff --cached` for staged changes
4. If no changes detected, inform user and exit

## Phase 2: Stage Files

**If unstaged changes exist**, ask user:
- Stage all changes? (`git add .`)
- Stage specific files?
- Only commit already staged changes?

Execute staging based on user choice.

## Phase 3: Generate Commit Message

**Analyze diff to determine**:
- Type: feat/fix/refactor/docs/test/chore/style/perf
- Scope: affected component/module (optional)
- Description: concise summary of changes

**Format** (Conventional Commits):
```
<type>(<scope>): <description>

[optional body]
```

**If `$ARGUMENTS` provided**, use it as commit message directly.

Present message to user, ask for confirmation or modification.

## Phase 4: Execute Commit

1. Run `git commit -m "<message>"`
2. Show commit result (hash, summary)
3. Ask if user wants to push

## Commit Types

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| refactor | Code refactoring |
| docs | Documentation |
| test | Tests |
| chore | Maintenance |
| style | Formatting |
| perf | Performance |

## Output Language

- Status messages: Chinese
- Commit message: English
