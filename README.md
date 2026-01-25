# Happy Skills

[中文](./README_CN.md) | **English**

**Describe requirements in natural language, auto-generate design docs and implement code step by step.** Automate the complete development flow: Idea → Design → Code → Commit.

## Installation

### Option 1: Using npx skills add (Recommended)

```bash
# Install to current project
npx skills add notedit/happy-skills

# Or install globally
npx skills add notedit/happy-skills -g
```

### Option 2: Using Claude Code Plugin System

```bash
# Step 1: Add the marketplace
/plugin marketplace add notedit/happy-skills

# Step 2: Install the plugin
/plugin install ha@happy-skills
```

### Verify Installation

```bash
# Test a skill
/feature-dev add a simple feature
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
├── .claude-plugin/plugin.json   # Plugin manifest
├── commands/                    # Slash commands
│   └── git/                     # Git commands
├── skills/                      # Skills
├── agents/                      # Sub-agents
└── docs/                        # Documentation
```

## License

MIT
