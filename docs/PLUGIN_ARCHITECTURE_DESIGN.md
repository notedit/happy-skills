# Claude Code Plugin 标准架构设计方案

## 一、概述

本文档为 `happy-skills` 项目提供一个标准化的 Claude Code 插件组织方案。该方案**严格遵循 Claude Code 官方插件规范**，支持官方安装命令和 Marketplace 分发。

## 二、官方安装方式

### 2.1 安装命令

```bash
# 方式1: 从 GitHub 直接安装
/plugin install https://github.com/notedit/happy-skills

# 方式2: 从 Marketplace 安装 (需先注册)
/plugin install happy-skills@claude-plugin-directory

# 方式3: 从自定义 Marketplace 安装
/plugin marketplace add notedit/plugins
/plugin install happy-skills@notedit

# 方式4: 本地路径安装
/plugin install ./path/to/happy-skills

# 方式5: 可视化安装
/plugin  → 选择 "Discover" 浏览和安装
```

### 2.2 安装位置

| 位置 | 路径 | 作用域 |
|------|------|--------|
| 全局 | `~/.claude/skills/` | 所有项目可用 |
| 项目级 | `./.claude/skills/` | 仅当前项目，可提交到 Git |
| 插件包 | `.claude-plugin/` | 完整插件分发 |

## 三、官方插件目录结构

### 3.1 完整目录结构

```
happy-skills/
│
├── 📄 README.md                      # 项目说明 (Marketplace 展示)
├── 📄 LICENSE                        # 开源许可证
│
├── 📁 .claude-plugin/                # [核心] 插件元数据目录
│   ├── 📄 plugin.json                # [必需] 插件清单
│   └── 📄 marketplace.json           # [可选] Marketplace 发布配置
│
├── 📁 skills/                        # [核心] 技能目录
│   ├── 📁 feature-analyzer/
│   │   ├── 📄 SKILL.md               # 技能主文件 (必需)
│   │   ├── 📁 references/            # 参考文档
│   │   ├── 📁 scripts/               # 可执行脚本
│   │   └── 📁 assets/                # 资产文件
│   │
│   ├── 📁 feature-pipeline/
│   │   └── ...
│   │
│   ├── 📁 screenshot-analyzer/
│   │   └── ...
│   │
│   └── 📁 skill-creation-guide/
│       └── ...
│
├── 📁 commands/                      # [核心] 斜杠命令目录
│   ├── 📄 feature-analyzer.md
│   ├── 📄 feature-pipeline.md
│   ├── 📄 feature-dev.md
│   └── 📄 screenshot-analyzer.md
│
├── 📁 agents/                        # [核心] 子代理目录
│   ├── 📄 code-architect.md
│   ├── 📄 code-explorer.md
│   ├── 📄 code-reviewer.md
│   ├── 📄 screenshot-ui-analyzer.md
│   ├── 📄 screenshot-interaction-analyzer.md
│   ├── 📄 screenshot-business-analyzer.md
│   ├── 📄 screenshot-synthesizer.md
│   ├── 📄 screenshot-reviewer.md
│   ├── 📄 test-generator.md
│   └── 📄 test-runner.md
│
├── 📁 hooks/                         # [可选] 事件钩子
│   └── 📄 post-install.sh
│
├── 📄 .mcp.json                      # [可选] MCP 服务器配置
│
├── 📄 CLAUDE.md                      # 项目级 Claude 指令 (用于开发)
├── 📄 pyproject.toml                 # Python 包配置 (CLI 工具)
│
├── 📁 cli/                           # [辅助] CLI 工具 (可选分发方式)
│   └── ...
│
└── 📁 docs/                          # 文档目录
    └── ...
```

### 3.2 与当前结构对比

| 当前结构 | 官方结构 | 变更说明 |
|----------|----------|----------|
| `.claude/agents/` | `agents/` | 移到根目录 |
| `.claude/commands/` | `commands/` | 移到根目录 |
| `.claude/skills/` | `skills/` | 移到根目录 |
| `manifest.json` | `.claude-plugin/plugin.json` | 使用官方格式 |
| - | `.claude-plugin/marketplace.json` | 新增 Marketplace 配置 |

## 四、核心配置文件

### 4.1 plugin.json - 插件清单 (必需)

```json
{
  "name": "happy-skills",
  "version": "1.0.0",
  "description": "A collection of Claude Code skills, commands, and agents for rapid product development",
  "author": {
    "name": "notedit",
    "url": "https://github.com/notedit"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/notedit/happy-skills"
  },
  "homepage": "https://github.com/notedit/happy-skills",

  "claude_code": {
    "min_version": "1.0.0"
  },

  "components": {
    "skills": [
      "feature-analyzer",
      "feature-pipeline",
      "screenshot-analyzer",
      "skill-creation-guide"
    ],
    "commands": [
      "feature-analyzer",
      "feature-pipeline",
      "feature-dev",
      "screenshot-analyzer"
    ],
    "agents": [
      "code-architect",
      "code-explorer",
      "code-reviewer",
      "screenshot-ui-analyzer",
      "screenshot-interaction-analyzer",
      "screenshot-business-analyzer",
      "screenshot-synthesizer",
      "screenshot-reviewer",
      "test-generator",
      "test-runner"
    ]
  },

  "keywords": [
    "development",
    "productivity",
    "code-review",
    "architecture",
    "feature-design",
    "testing"
  ],

  "categories": [
    "Development Tools",
    "Productivity",
    "Code Quality"
  ]
}
```

### 4.2 marketplace.json - Marketplace 发布配置 (可选)

```json
{
  "listing": {
    "title": "Happy Skills",
    "tagline": "Rapid product development with AI-powered workflows",
    "description": "A comprehensive collection of skills, commands, and agents that accelerate software development through intelligent automation.",
    "icon": "assets/icon.png",
    "screenshots": [
      "assets/screenshots/feature-analyzer.png",
      "assets/screenshots/code-review.png"
    ]
  },

  "pricing": {
    "type": "free"
  },

  "support": {
    "documentation": "https://github.com/notedit/happy-skills#readme",
    "issues": "https://github.com/notedit/happy-skills/issues",
    "email": "support@example.com"
  },

  "verification": {
    "verified": false,
    "trust_level": "community"
  }
}
```

### 4.3 团队分发配置 (.claude/settings.json)

项目中添加此文件，团队成员克隆后自动安装插件：

```json
{
  "plugins": {
    "sources": [
      {
        "type": "github",
        "url": "https://github.com/notedit/happy-skills"
      }
    ],
    "auto_install": true
  },

  "marketplaces": [
    {
      "name": "notedit",
      "url": "https://github.com/notedit/plugins"
    }
  ]
}
```

## 五、组件文件规范

### 5.1 Skill 文件规范 (SKILL.md)

```yaml
---
name: feature-analyzer
description: |
  Feature design through incremental Q&A and validation.
  Use when: (1) Planning new features, (2) Designing architecture,
  (3) Creating implementation specs, (4) Breaking down complex requirements.
license: MIT
---

# Feature Design Assistant

## Overview
Brief description of the skill...

## Workflow
1. Discovery - Understand requirements
2. Analysis - Explore codebase
3. Design - Create architecture
4. Validation - Review with user

## Bundled Resources

### References
- `references/design-patterns.md` - Common design patterns

### Scripts
- `scripts/generate-spec.py` - Generate specification document

## Usage Examples
Example usage scenarios...
```

### 5.2 Command 文件规范

```yaml
---
description: "Turn ideas into fully formed designs and specs through collaborative dialogue"
argument-hint: "Optional feature description"
allowed-tools: Read, Write, Glob, Grep, Bash, TodoWrite, Task, Skill
---

## Phase 1: Discovery
Understand user requirements...

## Phase 2: Analysis
Explore codebase...

## Phase 3: Design
Create implementation plan...

## Variables
- $ARGUMENTS - User-provided arguments
```

### 5.3 Agent 文件规范

```yaml
---
name: code-architect
description: |
  Designs feature architectures by analyzing existing codebase patterns
  and conventions, then providing comprehensive implementation blueprints.
tools: Glob, Grep, Read, WebFetch, TodoWrite
model: opus
color: green
---

# Code Architect Agent

## Core Responsibilities
- Analyze codebase patterns
- Design feature architecture
- Create implementation blueprints

## Process
1. Pattern analysis
2. Architecture design
3. Blueprint generation

## Output Format
Structured architecture document...
```

## 六、安装流程详解

### 6.1 用户安装流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    Plugin Installation Flow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User runs: /plugin install <source>                         │
│                     │                                            │
│                     ▼                                            │
│  2. Claude Code fetches plugin from source                      │
│     - GitHub URL → Clone repository                             │
│     - Marketplace → Download package                            │
│     - Local path → Read directory                               │
│                     │                                            │
│                     ▼                                            │
│  3. Validate .claude-plugin/plugin.json                         │
│     - Check required fields                                     │
│     - Verify component paths                                    │
│                     │                                            │
│                     ▼                                            │
│  4. User reviews source code (security check)                   │
│     - MCP servers may have file system access                   │
│     - User must approve installation                            │
│                     │                                            │
│                     ▼                                            │
│  5. Copy components to target location                          │
│     - skills/ → ~/.claude/skills/ or ./.claude/skills/          │
│     - commands/ → ~/.claude/commands/                           │
│     - agents/ → ~/.claude/agents/                               │
│                     │                                            │
│                     ▼                                            │
│  6. Run post-install hooks (if any)                             │
│                     │                                            │
│                     ▼                                            │
│  7. Plugin ready to use                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 团队自动安装流程

```
┌─────────────────────────────────────────────────────────────────┐
│                  Team Auto-Install Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Developer clones project with .claude/settings.json         │
│                     │                                            │
│                     ▼                                            │
│  2. Claude Code detects plugin configuration                    │
│                     │                                            │
│                     ▼                                            │
│  3. Prompt: "This project requires plugins. Install?"           │
│                     │                                            │
│                     ▼                                            │
│  4. Auto-install plugins from configured sources                │
│                     │                                            │
│                     ▼                                            │
│  5. Team has consistent tooling                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 七、迁移计划

### 7.1 从当前结构迁移

```bash
# Step 1: 创建官方插件结构
mkdir -p .claude-plugin

# Step 2: 移动组件目录到根目录
mv .claude/agents ./agents
mv .claude/commands ./commands
mv .claude/skills ./skills

# Step 3: 创建 plugin.json
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "happy-skills",
  "version": "1.0.0",
  "description": "A collection of Claude Code skills, commands, and agents for rapid product development",
  "author": { "name": "notedit" },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/notedit/happy-skills"
  },
  "claude_code": { "min_version": "1.0.0" },
  "components": {
    "skills": ["feature-analyzer", "feature-pipeline", "screenshot-analyzer", "skill-creation-guide"],
    "commands": ["feature-analyzer", "feature-pipeline", "feature-dev", "screenshot-analyzer"],
    "agents": ["code-architect", "code-explorer", "code-reviewer", "screenshot-ui-analyzer", "screenshot-interaction-analyzer", "screenshot-business-analyzer", "screenshot-synthesizer", "screenshot-reviewer", "test-generator", "test-runner"]
  },
  "keywords": ["development", "productivity"]
}
EOF

# Step 4: 保留 .claude 目录用于项目自用
# .claude/CLAUDE.md 等文件保持不变

# Step 5: 更新 README.md 添加安装说明
```

### 7.2 保持向后兼容

为了同时支持官方安装和 `hca` CLI 安装：

```
happy-skills/
│
├── .claude-plugin/          # 官方插件格式
│   └── plugin.json
│
├── skills/                  # 官方位置 (主)
├── commands/                # 官方位置 (主)
├── agents/                  # 官方位置 (主)
│
├── .claude/                 # 项目开发配置
│   ├── CLAUDE.md
│   └── .hca/                # hca CLI 元数据
│
└── cli/                     # hca CLI 工具 (可选安装方式)
```

## 八、发布到 Marketplace

### 8.1 发布流程

```bash
# 1. 确保 plugin.json 完整
# 2. 添加 marketplace.json (可选，用于更好的展示)
# 3. 创建 GitHub Release

# 4. 提交到官方目录 (需审核)
# 访问: https://github.com/anthropics/claude-plugins-directory
# 提交 PR 添加你的插件

# 5. 或创建自己的 Marketplace
# 创建一个 GitHub 仓库作为 Marketplace
# 结构:
# my-marketplace/
# ├── index.json
# └── plugins/
#     └── happy-skills/
#         └── plugin.json
```

### 8.2 Marketplace 索引文件

```json
{
  "name": "notedit-plugins",
  "description": "Notedit's Claude Code Plugin Collection",
  "plugins": [
    {
      "name": "happy-skills",
      "version": "1.0.0",
      "source": "https://github.com/notedit/happy-skills",
      "description": "Rapid product development workflows"
    }
  ]
}
```

## 九、CLI 工具定位调整

### 9.1 hca CLI 的新定位

由于 Claude Code 有官方安装机制，`hca` CLI 工具调整为：

| 功能 | 官方方式 | hca CLI |
|------|----------|---------|
| 安装插件 | `/plugin install` | 备用方式 |
| 更新插件 | `/plugin update` | 备用方式 |
| 验证插件 | - | `hca validate` (开发工具) |
| 打包插件 | - | `hca package` (开发工具) |
| 查看状态 | `/plugin list` | `hca status` |

### 9.2 hca CLI 专注开发者工具

```bash
# 插件开发命令
hca init           # 创建新插件项目
hca validate       # 验证插件结构
hca package        # 打包发布
hca test           # 测试插件

# 辅助安装 (当 /plugin 不可用时)
hca install        # 手动部署到项目
```

## 十、使用指南

### 10.1 用户安装和使用

```bash
# 1. 安装插件
/plugin install https://github.com/notedit/happy-skills

# 2. 使用斜杠命令
/feature-analyzer 实现用户登录功能
/feature-pipeline docs/login-design.md
/screenshot-analyzer ./screenshots/app.png

# 3. Skills 自动触发
# 对话中请求功能设计时，Claude 会自动调用相关 Skill

# 4. Agents 自动调度
# Task 工具会根据任务类型自动选择合适的 Agent
```

### 10.2 团队项目配置

```bash
# 1. 项目根目录添加 .claude/settings.json
{
  "plugins": {
    "sources": [
      { "type": "github", "url": "https://github.com/notedit/happy-skills" }
    ]
  }
}

# 2. 提交到版本控制
git add .claude/settings.json
git commit -m "Add Claude Code plugin configuration"

# 3. 团队成员克隆后自动安装
```

## 十一、总结

### 关键变更

1. **目录结构**: 组件目录从 `.claude/` 移到根目录
2. **元数据**: 使用 `.claude-plugin/plugin.json` 替代自定义格式
3. **安装方式**: 使用官方 `/plugin install` 命令
4. **分发渠道**: 支持 GitHub、Marketplace、本地路径
5. **CLI 定位**: `hca` 专注开发者工具，非必需

### 优势

- 符合 Claude Code 官方规范
- 支持官方安装命令
- 可发布到 Marketplace
- 团队可通过 settings.json 自动分发
- 保持与 hca CLI 的兼容性
