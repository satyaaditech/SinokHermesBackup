---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work

---

## Kanban Lane Integration (absorbed from kanban-codex-lane)

Use Codex as an isolated implementation lane inside a Hermes Kanban workflow. Hermes always owns the task lifecycle; Codex is an input-only lane.

### When to Use
Use when the Kanban task is a coding/refactor task with clear acceptance criteria, a bounded diff can be evaluated, and the repo can be checked out in an isolated worktree.

### Worktree Isolation
```bash
TASK_ID="${HERMES_KANBAN_TASK:-t_manual}"
REPO="/path/to/repo"
BASE="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
SAFE_TASK="$(printf '%s' "$TASK_ID" | tr -cd '[:alnum:]_-')"
BRANCH="codex/${SAFE_TASK}/$(date -u +%Y%m%d%H%M%S)"
WORKTREE="/tmp/${SAFE_TASK}-codex-lane"

git -C "$REPO" worktree add -b "$BRANCH" "$WORKTREE" "$BASE"
```

### Ownership Rules
- Hermes owns the Kanban lifecycle. Codex must never call `kanban_complete`, `kanban_block`, or gateway messaging.
- Hermes owns final acceptance. Treat Codex commits/diffs as untrusted patches until reviewed.
- Hermes owns test execution. Repeat required verification independently.
- Hermes owns cleanup. Kill stuck Codex processes and remove temporary worktrees.

### Reconciliation Checklist
- [ ] `git status --short` shows only expected files.
- [ ] `git diff` was reviewed by Hermes.
- [ ] No secrets, credentials, or unrelated data included.
- [ ] Hermes ran canonical tests independently.
- [ ] Accepted commits were applied to the Hermes-owned workspace.

### kanban_complete Metadata
```json
{
  "codex_lane": {
    "used": true,
    "mode": "exec | goal | skipped",
    "worktree": "/absolute/path/to/worktree",
    "branch": "codex/t_xxx/20260508100000",
    "result": "accepted | rejected | partial | timed_out",
    "tests_run": [{"command": "...", "exit_code": 0, "owner": "hermes | codex"}]
  }
}
```
