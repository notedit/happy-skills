# Happy Coding Agent

**中文** | [English](./README.md)

**用自然语言描述需求，自动生成设计文档并逐步实现代码。** 把"想法→设计→代码→提交"的完整开发流程自动化。

## Installation

```bash
# 在 Claude Code 中直接安装
/plugin install https://github.com/notedit/happy-coding-agent
```

### Alternative: CLI Tool

```bash
pip install git+https://github.com/notedit/happy-coding-agent.git
cd your-project && hca init
```

## Usage

### 1. Feature Development (Design → Execute)

```bash
# Step 1: 设计 - Q&A 对话生成设计文档
/feature-analyzer 用户登录功能，支持 OAuth2

# Step 2: 执行 - 按文档逐项实现
/feature-pipeline docs/features/user-login.md
```

### 2. Quick Development

```bash
/feature-dev 添加深色模式切换
```

### 3. Git Operations

```bash
/git:branch 用户登录      # 创建分支（支持中文）
/git:changes             # 查看更改（中文描述）
/git:commit              # 自动生成 commit message
/git:pr                  # 一键创建 PR
```

### 4. Worktree Parallel Development

```bash
/git:worktree-add feature/api   # 创建 worktree + 复制 .env
/git:worktree-merge             # 合并回当前分支
/git:worktree-remove            # 清理 worktree
```

### 5. Screenshot Analysis

```bash
/screenshot-analyzer ./app.png  # 从截图提取功能生成任务
```

## Commands Reference

### Feature Commands

| Command | Description |
|---------|-------------|
| `/feature-analyzer` | Turn ideas into designs through Q&A dialogue |
| `/feature-pipeline` | Execute tasks from design documents (checkboxes) |
| `/feature-dev` | Quick feature development |
| `/screenshot-analyzer` | Extract features from UI screenshots |

### Git Commands

| Command | Description |
|---------|-------------|
| `/git:commit` | Auto-generate semantic commit message |
| `/git:pr` | Complete workflow: commit, push, create PR |
| `/git:branch` | Create branch with conventional naming |
| `/git:changes` | Describe uncommitted changes |
| `/git:worktree-add` | Create worktree with .env files copied |
| `/git:worktree-merge` | Merge worktree branch into current |
| `/git:worktree-remove` | Remove worktree and cleanup |

## Components

### Skills

| Skill | Description |
|-------|-------------|
| `feature-design-assistant` | Feature design through Q&A |
| `task-execution-engine` | Execute tasks from design docs |
| `screenshot-feature-extractor` | Extract features from screenshots |
| `skill-creation-guide` | Guide for creating new skills |

### Agents

| Agent | Description |
|-------|-------------|
| `code-explorer` | Analyze codebase architecture |
| `code-architect` | Design feature implementations |
| `code-reviewer` | Review code for issues |
| `test-generator` | Generate test cases |
| `test-runner` | Execute and fix tests |

## Project Structure

```
happy-coding-agent/
├── .claude-plugin/plugin.json   # Plugin manifest
├── commands/                    # Slash commands
│   ├── feature-*.md
│   └── git/                     # Git commands
├── skills/                      # Skills
├── agents/                      # Sub-agents
├── cli/                         # CLI tool (hca)
└── docs/                        # Documentation
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `hca init` | Deploy plugin to current project |
| `hca init --select` | Interactively select components |
| `hca update` | Update from source repository |
| `hca status` | Show deployment status |

## License

MIT
