# Happy Coding Agent

[中文](./README_CN.md) | **English**

**Describe requirements in natural language, auto-generate design docs and implement code step by step.** Automate the complete development flow: Idea → Design → Code → Commit.

## Installation

```bash
# Step 1: Add the marketplace
/plugin marketplace add notedit/happy-coding-agent

# Step 2: Install the plugin
/plugin install hc@happy-coding-agent
```

### Alternative: CLI Tool

```bash
pip install git+https://github.com/notedit/happy-coding-agent.git
cd your-project && hca init
```

### Verify Installation

```bash
# Open plugin manager to confirm
/plugin

# Test a command
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
/git:worktree-merge             # Merge back to current branch
/git:worktree-remove            # Cleanup worktree
```

### 5. Screenshot Analysis

```bash
/screenshot-analyzer ./app.png  # Extract features from screenshot
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
