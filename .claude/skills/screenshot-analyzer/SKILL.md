---
name: screenshot-analyzer
description: "Analyze product screenshots to extract feature lists and generate development task checklists. Use when: (1) Analyzing competitor product screenshots for feature extraction, (2) Generating PRD/task lists from UI designs, (3) Batch analyzing multiple app screens, (4) Conducting competitive analysis from visual references."
---

# Screenshot Analyzer

Extract product features from UI screenshots and generate structured development task lists.

**Core principle**: Describe WHAT to build (features/interactions), NOT HOW (no tech stack).

## Process

1. **Analyze screenshots** - Identify UI components, interaction patterns, navigation structure
2. **Extract features** - Map UI elements to functional capabilities, categorize by module
3. **Generate tasks** - Output checkbox-format task list organized by functional modules

## Output

Write results to `docs/plans/YYYY-MM-DD-<product>-features.md` using the format in [references/output-format.md](references/output-format.md).

## Key Guidelines

- Use `- [ ]` checkbox format for all tasks
- Break features into small, executable subtasks
- Focus on user interactions, not implementation details
- For multiple screenshots: deduplicate features, map navigation flows
- For competitive analysis: highlight unique features and gaps
