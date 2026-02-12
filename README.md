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

### 3. Git Operations

```bash
/git:branch user-login       # Create branch (supports Chinese input)
/git:changes                 # View changes
/git:commit                  # Auto-generate commit message
/git:pr                      # One-click PR creation
```

### 4. Worktree Parallel Development

```bash
/git:worktree-add feature/api   # Create worktree + copy .env
/git:worktree-list              # List all worktrees with status
/git:worktree-merge             # Merge back to current branch
/git:worktree-remove            # Cleanup worktree
/git:worktree-remove --merged   # Batch remove merged worktrees
/git:worktree-remove --prune    # Clean stale worktrees
```

### 5. Screenshot Analysis

```bash
/screenshot-analyzer ./app.png  # Extract features from screenshot
```

## Commands Reference

### Git Commands

| Command | Description |
|---------|-------------|
| `/git:commit` | Auto-generate semantic commit message |
| `/git:pr` | Complete workflow: commit, push, create PR |
| `/git:branch` | Create branch with conventional naming |
| `/git:changes` | Describe uncommitted changes |
| `/git:worktree-add` | Create worktree with .env files copied |
| `/git:worktree-list` | List all worktrees with detailed status |
| `/git:worktree-merge` | Merge worktree branch into current |
| `/git:worktree-remove` | Remove worktree (supports --merged, --prune) |

## Components

### Skills

| Skill | Description |
|-------|-------------|
| `feature-dev` | Guided feature development with codebase understanding and architecture focus |
| `feature-analyzer` | Turn ideas into designs through Q&A dialogue |
| `feature-pipeline` | Execute tasks from design documents |
| `screenshot-analyzer` | Extract features from UI screenshots |
| `skill-creation-guide` | Guide for creating new skills |
| `tts-skill` | MiniMax TTS API - text-to-speech, voice clone, voice design |
| `react-animation` | ReactBits animations for Remotion - curated visual effects for video production |
| `gsap-animation` | GSAP + Remotion motion graphics - timeline orchestration, text splitting, SVG morphing |

### Agents

#### Code Analysis
| Agent | Description |
|-------|-------------|
| `code-explorer` | Analyze codebase by tracing execution paths and mapping architecture |
| `code-architect` | Design feature architectures based on existing patterns |
| `code-reviewer` | Review code for bugs, security vulnerabilities, and quality issues |

#### Screenshot Analysis (Multi-Agent Pipeline)
| Agent | Description |
|-------|-------------|
| `screenshot-ui-analyzer` | Analyze visual components, layout structure, and design patterns |
| `screenshot-interaction-analyzer` | Analyze user interaction flows and state transitions |
| `screenshot-business-analyzer` | Extract business logic and data entities |
| `screenshot-synthesizer` | Synthesize analysis results into unified feature list |
| `screenshot-reviewer` | Review task lists for completeness and quality |

#### Testing
| Agent | Description |
|-------|-------------|
| `test-generator` | Generate comprehensive test cases based on existing patterns |
| `test-runner` | Execute tests, diagnose failures, and provide fixes |

## Project Structure

```
happy-skills/
├── package.json                 # NPM package manifest & skills configuration
├── commands/                    # Slash commands
│   └── git/                     # Git commands
├── skills/                      # Skills
├── agents/                      # Sub-agents
└── docs/                        # Documentation
```

## License

MIT
