# Happy Coding Agent

**中文** | [English](./README.md)

**用自然语言描述需求，自动生成设计文档并逐步实现代码。** 把"想法→设计→代码→提交"的完整开发流程自动化。

## Installation

```bash
# 在 Claude Code 中直接安装
/plugin install https://github.com/belkov0912/happy-coding-agent.git
```

### Alternative: CLI Tool

```bash
pip install git+https://github.com/belkov0912/happy-coding-agent.git
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

#### 代码分析
| Agent | 描述 |
|-------|------|
| `code-explorer` | 通过追踪执行路径和映射架构来分析代码库 |
| `code-architect` | 基于现有模式设计功能架构 |
| `code-reviewer` | 审查代码中的 bug、安全漏洞和质量问题 |

#### 截图分析（多 Agent 流水线）
| Agent | 描述 |
|-------|------|
| `screenshot-ui-analyzer` | 分析视觉组件、布局结构和设计模式 |
| `screenshot-interaction-analyzer` | 分析用户交互流程和状态转换 |
| `screenshot-business-analyzer` | 提取业务逻辑和数据实体 |
| `screenshot-synthesizer` | 将分析结果综合为统一的功能列表 |
| `screenshot-reviewer` | 审查任务列表的完整性和质量 |

#### 测试
| Agent | 描述 |
|-------|------|
| `test-generator` | 基于现有模式生成全面的测试用例 |
| `test-runner` | 执行测试、诊断失败并提供修复方案 |

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
