---
name: feature-analyzer
description: "Turn ideas into fully formed designs and specs through natural collaborative dialogue. Use when planning new features, designing architecture, or making significant changes to the codebase."
---

# Feature Analyzer

Help turn ideas into fully formed designs and specs through natural collaborative dialogue. Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

**Announce at start:** "I'm using the feature-analyzer skill to design this feature." 

## The Process

### Understanding the idea

- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

### Exploring approaches

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

### Presenting the design

- Once you believe you understand what you're building, present the design
- Break it into sections of 300-500 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

### Documentation

- Write the validated design to `docs/designs/YYYY-MM-DD-<topic>-design.md`
- Commit the design document to git

### Implementation Tasks

After presenting the design, generate an implementation task list using markdown checkboxes:

```markdown
## Implementation Tasks

- [ ] **Task Title** `priority:1` `phase:model` `time:15min`
  - files: src/file1.py, tests/test_file1.py
  - [ ] Step 1: Write failing test for X
  - [ ] Step 2: Run test, verify it fails
  - [ ] Step 3: Implement minimal code
  - [ ] Step 4: Run test, verify it passes
  - [ ] Step 5: Commit

- [ ] **Another Task** `priority:2` `phase:api` `deps:Task Title` `time:10min`
  - files: src/api.py
  - [ ] Step 1: Write failing test
  - [ ] Step 2: Implement and verify
  - [ ] Step 3: Commit
```

**Task Format:**
- `- [ ]` checkbox with **bold title**
- Inline attributes: `priority:N` `phase:X` `deps:A,B` `time:Nmin`
- Indented `- files:` line with exact paths (include test files)
- Indented `- [ ]` checkboxes for TDD steps (2-5 min each)

**Task Granularity (TDD Steps):**
- Each step should take 2-5 minutes
- "Write the failing test" - one step
- "Run it to verify it fails" - one step
- "Implement minimal code" - one step
- "Run test to verify it passes" - one step
- "Commit" - one step

**Task Generation Guidelines:**
- Break the design into atomic, implementable tasks
- Order tasks by dependency (foundations first)
- Use clear, action-oriented titles ("Create X", "Implement Y", "Add Z")
- Each task should be completable independently
- Include test tasks for each major component
- Phases: `model` → `api` → `ui` → `test` → `docs`

### Execution Handoff

After saving the design, offer execution choice:

**"设计完成并保存到 `docs/designs/<filename>.md`。两种执行方式：**

**1. 当前会话执行** - 使用 /feature-pipeline 逐任务执行，每个任务后review

**2. 新会话执行** - 在新会话中批量执行，适合大型功能

**选择哪种？"**

**If 当前会话执行 chosen:**
- Invoke `/feature-pipeline <design-file-path>`
- Stay in this session, execute task by task

**If 新会话执行 chosen:**
- Guide user to open new session
- Provide the design file path for reference

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
