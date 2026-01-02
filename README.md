# Happy Coding Agent

A collection of Claude Code skills, commands, and agents for rapid product development.

## Commands

| Command | Description |
|---------|-------------|
| `/analyze-feature` | Turn ideas into fully formed designs and specs through collaborative dialogue |
| `/analyze-screenshot` | Analyze product screenshots to extract features and generate task lists |
| `/feature-dev` | Guided feature development with codebase understanding and architecture focus |

## Agents

### Code Analysis Agents

| Agent | Description |
|-------|-------------|
| `code-explorer` | Deeply analyzes codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies |
| `code-architect` | Designs feature architectures by analyzing existing patterns and providing comprehensive implementation blueprints |
| `code-reviewer` | Reviews code for bugs, security vulnerabilities, and quality issues with confidence-based filtering |

### Screenshot Analysis Agents (Multi-Agent Pipeline)

| Agent | Description |
|-------|-------------|
| `screenshot-ui-analyzer` | Analyzes visual components, layout structure, and design patterns |
| `screenshot-interaction-analyzer` | Analyzes user interaction flows, clickable elements, and state transitions |
| `screenshot-business-analyzer` | Extracts business logic, functional modules, and data entities |
| `screenshot-synthesizer` | Synthesizes analysis results into unified feature list and task breakdown |
| `screenshot-reviewer` | Reviews task lists for completeness, consistency, and quality |

## Skills

| Skill | Description |
|-------|-------------|
| `analyze-feature` | Feature design through incremental Q&A and validation |
| `screenshot-analyzer` | Multi-agent pipeline for extracting features from UI screenshots and generating task lists |
| `skill-creator` | Guide for creating new skills |

## Project Structure

```
.claude/
├── agents/                              # Custom agents
│   ├── code-architect.md
│   ├── code-explorer.md
│   ├── code-reviewer.md
│   ├── screenshot-ui-analyzer.md        # Multi-agent pipeline
│   ├── screenshot-interaction-analyzer.md
│   ├── screenshot-business-analyzer.md
│   ├── screenshot-synthesizer.md
│   └── screenshot-reviewer.md
├── commands/                            # Slash commands
│   ├── analyze-feature.md
│   ├── analyze-screenshot.md
│   └── feature-dev.md
└── skills/                              # Reusable skills
    ├── analyze-feature/
    ├── screenshot-analyzer/
    └── skill-creator/
```

## Screenshot Analysis Architecture

The `/analyze-screenshot` command uses a multi-agent pipeline for comprehensive analysis:

```
                    ┌─────────────────┐
                    │   Coordinator   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  UI Analyzer    │ │  Interaction    │ │   Business      │
│  (parallel)     │ │   Analyzer      │ │    Analyzer     │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Synthesizer   │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    Reviewer     │
                    └─────────────────┘
```

**Benefits:**
- **Thoroughness** - Three specialized perspectives catch more details
- **Speed** - Parallel analysis reduces total time
- **Quality** - Synthesis + Review ensures coherent output
- **Specialization** - Each agent focuses on its domain expertise
