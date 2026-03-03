# Happy Skills

[中文](./README_CN.md) | **English**

**Describe requirements in natural language, auto-generate design docs and implement code step by step.** Automate the complete development flow: Idea → Design → Code → Commit.

## Installation

### Using npx skills (Recommended)

```bash
# Install all skills from this package
npx skills add notedit/happy-skills

# Install specific skills only
npx skills add notedit/happy-skills --skills feature-dev,feature-analyzer

# Install globally (available in all projects)
npx skills add notedit/happy-skills -g
```

> **Note**: `npx skills` requires the [skills CLI](https://www.npmjs.com/package/skills). Install it with `npm install -g skills` if not already available.

### Verify Installation

```bash
# Test a skill
/feature-dev add a simple feature

# Or test another skill
/feature-analyzer design a user authentication system
```

## Usage

### 1. Feature Development (Design → Execute)

```bash
# Step 1: Design - Generate design doc through Q&A dialogue
/feature-analyzer user login with OAuth2 support

# Step 2: Execute - Implement tasks from design doc
/feature-pipeline docs/features/user-login.md
```

### 2. Quick Development

```bash
/feature-dev add dark mode toggle
```

### 3. Issue-Driven Development

```bash
/issue-flow #123                              # Implement a GitHub Issue end-to-end
/issue-flow https://github.com/org/repo/issues/123  # URL format
/issue-flow                                   # Pick from open issues
```

### 4. Screenshot Analysis

```bash
/screenshot-analyzer ./app.png  # Extract features from screenshot
```

## Components

### Development Skills (`skills/dev/`)

| Skill | Description |
|-------|-------------|
| `feature-dev` | Guided feature development with codebase understanding and architecture focus |
| `feature-analyzer` | Turn ideas into designs through Q&A dialogue |
| `feature-pipeline` | Execute tasks from design documents |
| `screenshot-analyzer` | Extract features from UI screenshots |
| `issue-flow` | AI-native Issue-driven development: Issue → Plan → Team Execute → PR → Merge |

### Video & Animation Skills (`skills/video/`)

| Skill | Description |
|-------|-------------|
| `video-producer` | End-to-end Remotion video production from natural language briefs - narrative structure, scene orchestration, rendering |
| `gsap-animation` | GSAP + Remotion motion graphics - timeline orchestration, text splitting, SVG morphing |
| `spring-animation` | Remotion spring physics for motion graphics - bouncy entrances, elastic trails, orchestrated sequences |
| `react-animation` | ReactBits animations for Remotion - curated visual effects for video production |

### Utility Skills (`skills/utils/`)

| Skill | Description |
|-------|-------------|
| `tts-skill` | MiniMax TTS API - text-to-speech, voice clone, voice design |
| `cover-image` | Cover image generation |
| `skill-creation-guide` | Guide for creating new skills |

## Project Structure

```
happy-skills/
├── package.json                 # NPM package manifest & skills configuration
├── skills/                      # Skills
│   ├── dev/                     # Development skills
│   ├── video/                   # Video & animation skills
│   └── utils/                   # Utility skills
└── docs/                        # Documentation
```

## License

MIT
