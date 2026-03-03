# Happy Skills

**中文** | [English](./README_EN.md)

一组为 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 打造的 Skills，覆盖从需求分析到代码交付的完整研发流程。用一句自然语言启动，AI 自动完成探索、设计、实现、测试和提交。

## 安装

```bash
# 一键安装所有 Skills
npx skills add notedit/happy-skills

# 只装你需要的
npx skills add notedit/happy-skills --skills feature-dev,issue-flow

# 全局安装（所有项目可用）
npx skills add notedit/happy-skills -g
```

> 需要先安装 [skills CLI](https://www.npmjs.com/package/skills)：`npm install -g skills`

## 快速上手

### 从 Issue 到 PR —— 一条命令搞定

```bash
/issue-flow #123                                      # 自动：读 Issue → 探索代码 → 设计方案 → 组建团队 → 实现 → 提 PR
/issue-flow https://github.com/org/repo/issues/123    # 也支持 URL
/issue-flow                                           # 无参数则列出 open Issues 供选择
```

### 先设计，再实现

```bash
# 第一步：通过对话生成设计文档
/feature-analyzer 用户登录功能，支持 OAuth2 和微信扫码

# 第二步：按文档逐项实现
/feature-pipeline docs/features/user-login.md
```

### 快速开发

```bash
/feature-dev 给设置页添加深色模式切换
```

### 从截图生成任务

```bash
/screenshot-analyzer ./competitor-app.png    # 分析截图，提取功能清单和开发任务
```

## Skills 一览

### 研发类 (`skills/dev/`)

| Skill | 说明 |
|-------|------|
| `issue-flow` | Issue 驱动开发 —— 从 GitHub Issue 出发，自动完成方案设计、团队协作、PR 创建到合并的完整流程 |
| `feature-dev` | 引导式功能开发 —— 深度理解代码库，经过探索→设计→实现→测试→评审的完整周期 |
| `feature-analyzer` | 需求分析 —— 通过交互式对话，将模糊想法转化为结构化的设计文档 |
| `feature-pipeline` | 任务执行引擎 —— 读取设计文档，逐项实现，支持断点续做 |
| `screenshot-analyzer` | 截图分析 —— 从 UI 截图中识别功能特性，生成开发任务清单 |

### 视频动画类 (`skills/video/`)

| Skill | 说明 |
|-------|------|
| `video-producer` | 视频制作 —— 从自然语言描述到完整 Remotion 视频，包含叙事、编排和渲染 |
| `gsap-animation` | GSAP 动效 —— 时间线编排、文字拆分、SVG 形变等高级动画 |
| `spring-animation` | 弹簧动画 —— 基于物理的弹性入场、轨迹、编排序列 |
| `react-animation` | React 动效 —— ReactBits 精选视觉效果，适配 Remotion 视频制作 |

### 工具类 (`skills/utils/`)

| Skill | 说明 |
|-------|------|
| `tts-skill` | 语音合成 —— MiniMax TTS API，支持文本转语音、声音克隆、声音设计 |
| `cover-image` | 封面生成 —— 根据内容自动生成文章封面图 |
| `skill-creation-guide` | Skill 开发指南 —— 创建自定义 Skill 的完整教程 |

## 项目结构

```
happy-skills/
├── package.json          # 包配置 & Skills 注册
├── skills/
│   ├── dev/              # 研发类
│   ├── video/            # 视频动画类
│   └── utils/            # 工具类
└── docs/                 # 文档
```

## License

MIT
