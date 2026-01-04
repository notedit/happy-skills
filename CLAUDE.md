# Happy Coding Agent

A Claude Code plugin for rapid product development.

## Project Structure

```
happy-coding-agent/
├── .claude-plugin/plugin.json   # Plugin manifest (official format)
├── skills/                      # Skills (root - for plugin distribution)
├── commands/                    # Commands (root - for plugin distribution)
├── agents/                      # Agents (root - for plugin distribution)
├── .claude/                     # Project-level configs (for development)
└── cli/                         # CLI tool (hca command)
```

## Rules

- When updating commands, agents, or skills, sync to both root and .claude directories
- Always update README.md when adding/modifying components
- Use AskUserQuestion for structured information gathering in skills

## Installation

```bash
# Official way (in Claude Code)
/plugin install https://github.com/notedit/happy-coding-agent

# Alternative (CLI)
pip install git+https://github.com/notedit/happy-coding-agent.git
hca init
```

## Commands

| Command | Description |
|---------|-------------|
| `/feature-analyzer` | Design features through structured Q&A dialogue |
| `/feature-pipeline` | Execute tasks from design documents |
| `/screenshot-analyzer` | Extract features from UI screenshots |
| `/feature-dev` | Guided feature development |

## Skills

### feature-design-assistant
Turn ideas into fully formed designs using structured AskUserQuestion flows.

See: `skills/feature-design-assistant/SKILL.md`

### task-execution-engine
Execute implementation tasks from design documents using markdown checkboxes.

See: `skills/task-execution-engine/SKILL.md`

### screenshot-feature-extractor
Multi-agent pipeline for extracting features from UI screenshots.

See: `skills/screenshot-feature-extractor/SKILL.md`

### skill-creation-guide
Guide for creating new skills with proper structure and best practices.

See: `skills/skill-creation-guide/SKILL.md`
