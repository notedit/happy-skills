---
description: "Describe uncommitted code changes in human-readable Chinese format"
argument-hint: Optional file path to focus on
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
---

# Git Changes

Analyze and describe current uncommitted changes in detail.

## Phase 1: Gather Changes

**Actions**:
1. `git status --porcelain` - file list
2. `git diff` - unstaged changes
3. `git diff --cached` - staged changes
4. If `$ARGUMENTS` has file path, focus on that file

## Phase 2: Categorize

**Categories**:
- New files (untracked)
- Modified files
- Deleted files
- Renamed files

## Phase 3: Analyze Each File

**For each changed file**:
1. Identify file type (code, config, docs, test)
2. Summarize key changes:
   - Functions added/modified/removed
   - Imports changed
   - Config values modified
   - Logic changes
3. Assess impact:
   - Breaking changes?
   - Affects other modules?
   - Needs tests?

## Phase 4: Generate Report

**Output format**:

```markdown
# 未提交变更报告

## 概览
- 修改: X files
- 新增: Y files
- 删除: Z files
- 行数: +A / -B

## 变更详情

### src/auth/login.ts (修改)
**类型**: 功能增强
**修改**:
- 新增 `validateEmail()` 函数
- 修改 `login()` 添加验证逻辑

**影响**:
- 需要更新单元测试

### tests/auth.test.ts (新增)
**类型**: 测试
**内容**: login 模块测试用例

## 建议
- 提交信息: `feat(auth): add email validation`
```

## Output Language

- All output: Chinese
- Technical terms (paths, functions): Original
- Suggested commit message: English
