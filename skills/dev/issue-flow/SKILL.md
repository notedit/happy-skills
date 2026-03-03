---
name: issue-flow
description: >
  AI-Native Issue-Driven development workflow. From GitHub Issue to merged PR:
  parse issue, explore codebase, design technical plan, execute with agent team,
  create PR, and cleanup. Use when a user wants to implement a GitHub Issue
  end-to-end: `/issue-flow #123` or `/issue-flow` to pick from open issues.
metadata:
  tags:
    - development
    - github
    - workflow
    - issue
    - team
---

# Issue Flow — AI-Native Issue-Driven Development

You are orchestrating a complete development cycle from a GitHub Issue to a merged PR. Follow the phases below strictly. Every major decision requires human confirmation.

**Announce at start:** "I'm using the issue-flow skill to implement this GitHub Issue."

Initial request: $ARGUMENTS

---

## Phase 0: Preflight

**Goal**: Validate environment and resolve the target Issue.

**Actions**:

1. **Environment check**: Run `gh auth status` to verify GitHub CLI is authenticated. If it fails, tell the user to run `gh auth login` and stop.

2. **Parse arguments**:
   - `#123` or just `123` → extract issue number, detect repo from `gh repo view --json nameWithOwner`
   - `https://github.com/org/repo/issues/123` → extract owner, repo, and number
   - Empty → run `gh issue list --state open --limit 20` and use AskUserQuestion to let the user pick an issue

3. **Fetch Issue details**:
   ```bash
   gh issue view <N> --json number,title,body,labels,comments,assignees,state
   ```
   Store: `ISSUE_NUMBER`, `ISSUE_TITLE`, `ISSUE_BODY`, `ISSUE_LABELS`.

4. **Check for existing work**:
   - Search for branch `issue/<N>-*` via `git branch -a --list '*issue/<N>*'`
   - If found, AskUserQuestion: resume existing branch / start fresh / cancel

5. **Detect project features** (used later for team composition):
   - Has test framework? (check for `jest.config*`, `vitest.config*`, `pytest.ini`, `*test*` dirs)
   - Has CI? (check `.github/workflows/`, `.gitlab-ci.yml`, etc.)
   - Has linter? (check `.eslintrc*`, `biome.json`, `.prettierrc*`)
   - Primary language(s) from file extensions

---

## Phase 1: Worktree Setup

**Goal**: Create an isolated workspace.

**Actions**:

1. Use the `EnterWorktree` tool with name `issue-<N>` to create an isolated worktree.
2. Create and switch to branch `issue/<N>-<slugified-title>`:
   - Slugify: lowercase, replace spaces/special chars with `-`, truncate to 50 chars
   - Example: Issue #42 "Add OAuth2 Login Support" → `issue/42-add-oauth2-login-support`
   - Run: `git checkout -b issue/<N>-<slug>`

---

## Phase 2: Technical Planning

**Goal**: Deep codebase exploration → technical plan → user approval.

### Step 2a: Codebase Exploration

Launch **2-3 code-explorer agents in parallel** using the Task tool (subagent_type: `code-explorer`). Tailor each agent's focus to the Issue:

- **Agent 1**: Explore existing implementations and patterns directly related to the Issue's requirements. Return a list of 5-10 key files.
- **Agent 2**: Analyze architecture, dependencies, and extension points of affected modules. Return a list of 5-10 key files.
- **Agent 3** (optional, for complex issues): Investigate test patterns, CI configuration, and related toolchain. Return a list of 5-10 key files.

After agents return, **read all key files** they identified to build deep understanding.

### Step 2b: Design Technical Plan

Based on the exploration, design a technical plan with:

1. **Summary**: 2-3 sentence overview of the approach
2. **Files to modify/create**: List with brief description of changes
3. **Implementation steps**: Ordered, concrete steps (each step = one logical unit of work)
4. **Test strategy**: What to test, how to test
5. **Risk assessment**: Potential issues and mitigations

Format the plan according to `rules/plan-format.md`.

### Step 2c: Publish Plan to Issue

Post the plan as a comment on the Issue using `gh issue comment`:

```bash
gh issue comment <N> --body "$(cat <<'EOF'
<plan content formatted per rules/plan-format.md>
EOF
)"
```

Use the HTML comment marker `<!-- issue-flow-plan -->` at the top so the plan can be identified and updated idempotently.

### Step 2d: User Confirmation

Use AskUserQuestion with options:
- **Approve** — proceed with implementation
- **Modify** — user provides feedback, return to Step 2b
- **Cancel** — abort the workflow

Do NOT proceed without explicit approval.

---

## Phase 3: Team Execution

**Goal**: Implement the plan — either directly or with an agent team.

### Decision: Direct vs Team

**Direct implementation** (no team) when ALL of these are true:
- Plan involves 1-2 files
- No complex cross-module changes
- No separate test/review/docs work needed

**Team execution** when ANY of these are true:
- Plan involves 3+ files across multiple modules
- Tests need to be written or updated
- Security-sensitive changes
- Documentation updates required
- Frontend + backend changes together

### Path A: Direct Implementation

1. Implement changes following the plan step by step
2. Run existing tests if available
3. Skip to Phase 4

### Path B: Team Execution

1. **Create team**: Use `TeamCreate` with name `issue-<N>`.

2. **Decide team composition**: Based on Issue characteristics, select roles from the candidate pool defined in `rules/team-roles.md`. Consider:
   - Issue labels (e.g., `frontend`, `security`, `docs`)
   - File types in the plan (`.tsx` → frontend, `.sql` → backend, etc.)
   - Whether tests exist and need updating
   - Risk level of the changes

3. **Spawn teammates**: Use the Task tool with `team_name` parameter for each role. Give each teammate:
   - The technical plan
   - Their specific tasks
   - Context about the codebase patterns discovered in Phase 2

4. **Create tasks**: Use `TaskCreate` for each implementation step from the plan. Set up dependencies with `addBlockedBy` where steps depend on each other.

5. **Assign and coordinate**: Assign tasks to teammates via `TaskUpdate`. Monitor progress, resolve blockers, and coordinate between teammates.

6. **Iteration limit**: Each task gets at most **2 fix iterations**. If a task still fails after 2 rounds:
   - Log the issue
   - AskUserQuestion: fix manually / skip / abort

7. **Shutdown team**: After all tasks complete, send `shutdown_request` to each teammate, then `TeamDelete`.

---

## Phase 4: PR & CI

**Goal**: Commit, push, create PR, handle CI.

### Step 4a: Commit & Push

1. Stage all changes: review with `git status` and `git diff`
2. Commit with a descriptive message referencing the Issue:
   ```
   feat: <summary from plan> (#<N>)
   ```
3. Push the branch:
   ```bash
   git push -u origin issue/<N>-<slug>
   ```

### Step 4b: Create PR

Create PR using `gh pr create` with the template from `rules/pr-template.md`:

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
<PR body per rules/pr-template.md, includes Closes #N>
EOF
)"
```

### Step 4c: Post Implementation Summary to Issue

Add a comment to the Issue summarizing what was implemented:

```bash
gh issue comment <N> --body "$(cat <<'EOF'
<!-- issue-flow-impl -->
## Implementation Complete

- PR: #<PR_NUMBER>
- <brief summary of changes>
EOF
)"
```

### Step 4d: CI Check

1. Wait briefly, then check CI status:
   ```bash
   gh pr checks <PR_NUMBER> --watch --fail-fast
   ```

2. If CI **fails**: AskUserQuestion with options:
   - **Auto-fix** — attempt to diagnose and fix CI failures (max 2 iterations)
   - **Manual** — user will fix manually
   - **Abort** — close the PR

3. If CI **passes** (or no CI configured): AskUserQuestion with options:
   - **Merge** — merge the PR now
   - **Keep open** — leave PR open for human review
   - **Request review** — assign reviewer via `gh pr edit --add-reviewer`

---

## Phase 5: Cleanup

**Goal**: Clean up resources after merge.

**Actions** (only if PR was merged):

1. **Check Issue status**: Verify if `Closes #N` auto-closed the Issue. If not:
   ```bash
   gh issue close <N> --comment "Closed via PR #<PR_NUMBER>"
   ```

2. **Report**: Output a completion summary:
   ```
   ## Issue Flow Complete

   - Issue: #<N> <title>
   - Branch: issue/<N>-<slug>
   - PR: #<PR_NUMBER> (merged)
   - Files changed: <count>
   - Implementation: <1-2 sentence summary>
   ```

---

## Error Recovery

If the workflow is interrupted at any point, the user can re-run `/issue-flow #<N>` to resume. See `references/recovery-guide.md` for detailed recovery scenarios.

## Key Principles

- **Human-in-the-loop**: Every major decision (plan approval, merge, CI failure handling) requires explicit user confirmation
- **Idempotent comments**: Issue comments use HTML markers (`<!-- issue-flow-plan -->`, `<!-- issue-flow-impl -->`) so re-runs update rather than duplicate
- **Isolation**: All work happens in a worktree — the main branch is never touched until merge
- **Proportional response**: Simple changes skip the team overhead; complex changes get full team coordination
