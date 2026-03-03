# Team Roles — Candidate Pool & Selection Logic

## Role Candidate Pool

These roles are NOT all used every time. Select roles based on the Issue characteristics and technical plan.

### Engineer (Implementation)

- **Agent type**: `general-purpose`
- **When to use**: Always needed for team execution (at least one)
- **Prompt template**: Provide the technical plan, assigned implementation steps, and key codebase patterns. Ask the engineer to implement following existing conventions.
- **Multiple engineers**: For large changes spanning distinct modules, spawn 2 engineers each owning a separate module to parallelize work.

### Code Reviewer

- **Agent type**: `code-reviewer`
- **When to use**: Changes involving complex logic, security-sensitive code, or public APIs
- **Prompt template**: After implementation is complete, provide the diff and ask for review focusing on bugs, security, and code quality.
- **Timing**: Spawned AFTER implementation tasks are complete

### Test Writer / Runner

- **Agent type**: `test-writer-fixer` or `test-runner`
- **When to use**:
  - `test-writer-fixer`: When new tests need to be written or existing tests updated
  - `test-runner`: When only existing tests need to be verified
- **Skip when**: Project has no test framework and Issue doesn't require adding one
- **Prompt template**: Provide the implementation diff and ask to write/run tests following project conventions.

### Frontend Developer

- **Agent type**: `frontend-developer`
- **When to use**: Issue involves UI components, CSS, React/Vue/Angular work
- **Signals**: Issue labels contain `frontend`, `ui`, `css`; plan modifies `.tsx`, `.vue`, `.svelte`, `.css` files
- **Prompt template**: Provide component requirements, existing UI patterns, and design specs if available.

### Backend Architect

- **Agent type**: `backend-architect`
- **When to use**: Issue involves API design, database schema changes, server-side architecture
- **Signals**: Issue labels contain `backend`, `api`, `database`; plan modifies route handlers, models, migrations
- **Prompt template**: Provide API requirements, existing patterns, and data model context.

### Security Auditor

- **Agent type**: `security-auditor`
- **When to use**: Changes to authentication, authorization, input validation, data handling, or cryptography
- **Signals**: Issue labels contain `security`; plan touches auth middleware, user input handling, or data storage
- **Prompt template**: After implementation, provide the full diff for security review.
- **Timing**: Spawned AFTER implementation tasks are complete

### Technical Writer

- **Agent type**: `technical-writer`
- **When to use**: Issue explicitly requires documentation updates, or changes affect public APIs/configurations
- **Signals**: Issue labels contain `docs`, `documentation`; plan includes README or doc file changes
- **Prompt template**: Provide the implementation summary, API changes, and target doc files.

## Selection Decision Tree

```
Start
  |
  v
Is it a simple change (1-2 files, no tests)? ──Yes──> Direct implementation (no team)
  |
  No
  |
  v
Always include: 1x Engineer (general-purpose)
  |
  v
Does the plan touch .tsx/.vue/.css/UI files? ──Yes──> Add: Frontend Developer
  |
  No
  |
  v
Does the plan touch API routes/DB/server? ──Yes──> Add: Backend Architect
  |
  v
Does the project have a test framework? ──Yes──> Add: Test Writer/Runner
  |
  v
Is the change security-sensitive? ──Yes──> Add: Security Auditor (post-impl)
  |
  v
Does the Issue require doc updates? ──Yes──> Add: Technical Writer
  |
  v
Is the change complex or risky? ──Yes──> Add: Code Reviewer (post-impl)
```

## Team Communication Protocol

1. **Leader** (you, the orchestrator) creates all tasks and assigns them
2. **Engineers** implement and mark tasks complete via `TaskUpdate`
3. **Post-implementation roles** (reviewer, security auditor) are spawned only after implementation tasks are marked complete
4. **Conflicts**: If two teammates modify the same file, the leader resolves conflicts
5. **Blocking issues**: Teammates send messages to the leader when blocked; leader decides resolution
6. **Max team size**: Cap at 4 concurrent agents to manage complexity
