---
description: "Analyze product screenshots to extract features and generate development task lists."
argument-hint: Screenshot path or description
allowed-tools: Read, Write, Grep, Glob, TodoWrite, AskUserQuestion, Skill
---

## Phase 1: Discovery

**Goal**: Understand what screenshots to analyze

Initial request: $ARGUMENTS

**Actions**:
1. If no screenshot path provided, ask user:
   - What screenshots do you want me to analyze?
   - What product/app are these from?
   - Is this for competitive analysis or internal product planning?
2. Read and verify the screenshot files exist
3. Confirm scope with user (single screen, full app, specific feature)

---

## Phase 2: Run with Screenshot Analyzer Skill

Use the Skill tool to invoke the "screenshot-analyzer" skill and follow its complete process.
