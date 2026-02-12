# Happy Skills

**用自然语言描述需求，自动生成设计文档并逐步实现代码。** 把"想法→设计→代码→提交"的完整开发流程自动化。

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
/git:branch 用户登录      # 创建分支
/git:changes             # 查看更改
/git:commit              # 自动 commit
/git:pr                  # 一键 PR
```

### 4. Worktree Parallel Development

```bash
/git:worktree-add feature/api   # 创建 + 复制 .env
/git:worktree-merge             # 合并
/git:worktree-remove            # 清理
```

### 5. Screenshot Analysis

```bash
/screenshot-analyzer ./app.png
```

## Project Structure

```
happy-skills/
├── package.json                 # NPM package manifest & skills configuration
├── commands/                    # Slash commands
│   └── git/                     # Git commands (8)
├── skills/                      # Skills (direct invocation)
│   ├── feature-dev/             # Guided feature development
│   ├── feature-analyzer/        # Design doc generation
│   ├── feature-pipeline/        # Task execution engine
│   ├── screenshot-analyzer/     # Screenshot analysis
│   ├── skill-creation-guide/    # Skill creation guide
│   ├── tts-skill/               # MiniMax TTS API
│   ├── react-animation/         # ReactBits animations for Remotion
│   ├── gsap-animation/          # GSAP + Remotion motion graphics
│   └── video-producer/          # End-to-end video production
├── agents/                      # Sub-agents
└── docs/                        # Documentation
```

## Rules

- When updating commands, agents, or skills, sync to both `README.md` and `README_CN.md`
- Always update both README files together to keep them in sync
- Use AskUserQuestion for structured information gathering in skills
- Skills can be called directly: `/feature-dev`, `/feature-analyzer`, `/feature-pipeline`, `/screenshot-analyzer`, `/tts-skill`, `/video-producer`
