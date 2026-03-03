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

### 3. Screenshot Analysis

```bash
/screenshot-analyzer ./app.png
```

## Project Structure

```
happy-skills/
├── package.json                 # NPM package manifest & skills configuration
├── skills/                      # Skills (direct invocation)
│   ├── dev/                     # Development skills
│   │   ├── feature-dev/         # Guided feature development
│   │   ├── feature-analyzer/    # Design doc generation
│   │   ├── feature-pipeline/    # Task execution engine
│   │   ├── screenshot-analyzer/ # Screenshot analysis
│   │   └── issue-flow/          # Issue-driven development workflow
│   ├── video/                   # Video & animation skills
│   │   ├── video-producer/      # End-to-end video production
│   │   ├── gsap-animation/      # GSAP + Remotion motion graphics
│   │   ├── spring-animation/    # Remotion spring physics animations
│   │   └── react-animation/     # ReactBits animations for Remotion
│   └── utils/                   # Utility skills
│       ├── tts-skill/           # MiniMax TTS API
│       ├── cover-image/         # Cover image generation
│       └── skill-creation-guide/# Skill creation guide
└── docs/                        # Documentation
```

## Rules

- When updating skills, sync to both `README.md`(中文) and `README_EN.md`(English)
- Always update both README files together to keep them in sync
- Use AskUserQuestion for structured information gathering in skills
- Skills can be called directly: `/feature-dev`, `/feature-analyzer`, `/feature-pipeline`, `/screenshot-analyzer`, `/tts-skill`, `/video-producer`, `/issue-flow`
