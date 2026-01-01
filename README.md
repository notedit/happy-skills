# Happy Coding Agent

A collection of Claude Code skills, commands, and agents for rapid product development.

## Commands

| Command | Description |
|---------|-------------|
| `/analyze-feature` | Turn ideas into fully formed designs and specs through collaborative dialogue |
| `/analyze-screenshot` | Analyze product screenshots to extract features and generate task lists |
| `/feature-dev` | Guided feature development with codebase understanding and architecture focus |

## Agents

| Agent | Description |
|-------|-------------|
| `code-explorer` | Deeply analyzes codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies |
| `code-architect` | Designs feature architectures by analyzing existing patterns and providing comprehensive implementation blueprints |
| `code-reviewer` | Reviews code for bugs, security vulnerabilities, and quality issues with confidence-based filtering |

## Skills

| Skill | Description |
|-------|-------------|
| `analyze-feature` | Feature design through incremental Q&A and validation |
| `screenshot-analyzer` | Extract features from UI screenshots, generate development checklists |
| `skill-creator` | Guide for creating new skills |

## Project Structure

```
.claude/
├── agents/             # Custom agents
│   ├── code-architect.md
│   ├── code-explorer.md
│   └── code-reviewer.md
├── commands/           # Slash commands
│   ├── analyze-feature.md
│   ├── analyze-screenshot.md
│   └── feature-dev.md
└── skills/             # Reusable skills
    ├── analyze-feature/
    ├── screenshot-analyzer/
    └── skill-creator/
```
