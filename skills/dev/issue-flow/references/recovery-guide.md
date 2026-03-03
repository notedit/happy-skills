# Recovery Guide — Resuming Interrupted Workflows

## How Recovery Works

When `/issue-flow #<N>` is re-run for an Issue that was previously started, the skill detects existing artifacts and offers to resume.

## Detection Signals

| Signal | Check | Meaning |
|--------|-------|---------|
| Existing branch | `git branch -a --list '*issue/<N>*'` | Work was started |
| Plan comment on Issue | `gh issue view <N> --json comments` + search for `<!-- issue-flow-plan -->` | Plan was published |
| Open PR | `gh pr list --head 'issue/<N>*' --state open` | PR was created |
| Merged PR | `gh pr list --head 'issue/<N>*' --state merged` | Work is complete |

## Recovery Scenarios

### Scenario 1: Branch exists, no plan comment

**What happened**: Interrupted during Phase 2 (exploration/planning).

**Recovery**:
1. Switch to existing branch
2. Skip Phase 0-1
3. Resume at Phase 2 (re-explore if needed, or ask user if they have a plan)

### Scenario 2: Branch exists, plan comment exists, no PR

**What happened**: Interrupted during Phase 3 (implementation).

**Recovery**:
1. Switch to existing branch
2. Read the plan from the Issue comment
3. Check `git log` to see which steps were already completed
4. AskUserQuestion: resume from where it stopped / restart implementation / re-plan
5. Resume Phase 3 from the first incomplete step

### Scenario 3: PR exists and is open, CI failing

**What happened**: Interrupted during Phase 4 (CI fix attempts).

**Recovery**:
1. Switch to existing branch
2. Check CI failure details: `gh pr checks <PR> --json`
3. AskUserQuestion: attempt auto-fix / manual fix / close PR
4. Resume Phase 4d

### Scenario 4: PR exists and is open, CI passing

**What happened**: Interrupted before merge decision.

**Recovery**:
1. AskUserQuestion: merge now / keep open / request review

### Scenario 5: PR is already merged

**What happened**: Merge succeeded but cleanup may be incomplete.

**Recovery**:
1. Check if Issue is closed
2. Perform Phase 5 cleanup if needed
3. Report completion

## User Decision Point

When existing work is detected, always use AskUserQuestion with these options:

- **Resume** — continue from where it left off
- **Start fresh** — delete existing branch and start over
- **Cancel** — do nothing

Never silently overwrite existing work.
