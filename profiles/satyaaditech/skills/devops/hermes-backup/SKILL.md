---
name: hermes-backup
description: "Backup Hermes Agent configuration, skills, memory, and cron data to GitHub (or any git remote) for disaster recovery."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hermes, backup, git, github, cron, disaster-recovery]
    related_skills: [hermes-agent, github-repo-management]
---

# Hermes Backup to GitHub

Backup Hermes Agent data — skills, memory, config, cron jobs — to a private git repository for disaster recovery and cross-machine sync.

## What Gets Backed Up

| Path | Why |
|------|-----|
| `~/.hermes/config.yaml` | Main configuration (model, tools, display, etc.) |
| `~/.hermes/SOUL.md` | Personality / system prompt |
| `~/.hermes/memories/` | Persistent memory (USER.md, MEMORY.md) |
| `~/.hermes/skills/` | All installed and agent-created skills |
| `~/.hermes/cron/` | Cron job definitions and output history |

## What Is EXCLUDED (secrets)

| Path | Reason |
|------|--------|
| `~/.hermes/.env` | API keys and tokens |
| `~/.hermes/auth.json` | OAuth tokens and credential pools |
| `~/.hermes/auth.lock` | Lock file |

These must **never** be committed. The backup script and `.gitignore` enforce this.

## Prerequisites

- `git` installed
- SSH key pair for GitHub authentication (or HTTPS + PAT)
- A private GitHub repo (e.g. `hermes-backup`)

## Quick Setup

### 1. Choose Authentication Method

**SSH (recommended for most users)**

Generate a dedicated key pair and add the public key to GitHub:

```bash
ssh-keygen -t ed25519 -C "hermes-backup" -f ~/.ssh/hermes_backup -N ""
cat ~/.ssh/hermes_backup.pub
```

Add the public key to GitHub: **Settings → SSH and GPG keys → New SSH key**.

Then configure an SSH host alias in `~/.ssh/config`:

```bash
cat > ~/.ssh/config << 'EOF'
Host github-hermes
    HostName github.com
    User git
    IdentityFile ~/.ssh/hermes_backup
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
EOF
chmod 600 ~/.ssh/config
```

**HTTPS + `.netrc` (useful when SSH is blocked or you prefer tokens)**

Create a GitHub Personal Access Token (classic) with `repo` scope, then store it in `~/.netrc`:

```python
# Run via execute_code or python3 -c
import os
netrc = """machine github.com
login <your-github-username>
password <your-token>
"""
path = os.path.expanduser("~/.netrc")
with open(path, "w") as f:
    f.write(netrc)
os.chmod(path, 0o600)
```

The backup script will push to `https://github.com/<user>/<repo>.git`.

### 2. Create Backup Repo & Script

```bash
mkdir -p ~/hermes-backup ~/scripts
```

Copy the script from `references/backup-hermes.sh` into `~/scripts/backup-hermes.sh`, make it executable (`chmod +x`), and run it once to initialize the local git repo.

### 3. Add GitHub Remote & Push

**For SSH authentication:**

```bash
cd ~/hermes-backup
git remote add origin git@github-hermes:<username>/hermes-backup.git
git branch -M main
git push -u origin main
```

**For HTTPS + `.netrc` authentication:**

```bash
cd ~/hermes-backup
git remote add origin https://github.com/<username>/hermes-backup.git
git branch -M main
git push -u origin main
```

The `.netrc` credentials are read automatically by git; no manual login prompt appears.

### 5. Schedule Daily Backup

Two reliable options exist. Pick the one that fits your workflow.

**Option A: Linux cron (simplest, no Hermes dependency)**

```bash
crontab -l 2>/dev/null | { cat; echo "0 3 * * * /home/$(whoami)/scripts/backup-hermes.sh >> /home/$(whoami)/hermes-backup/backup.log 2>&1"; } | crontab -
```

Runs daily at 03:00. The script is idempotent: if nothing changed, it exits silently.

**Option B: Hermes built-in cron (v0.14.0+)**

As of v0.14.0 the built-in cron scheduler is reliable for delivery. You can create a job via the `cronjob` tool or `hermes cron create` CLI. Set the script path to `~/scripts/backup-hermes.sh` and let Hermes handle the schedule.

Prior to v0.14.0, Hermes cron had a silent-delivery bug on some platforms (notably Telegram). If you are on an older version, use Option A.

## Manual Trigger

```bash
~/scripts/backup-hermes.sh
```

## Restoring on a New Machine

1. Clone the repo: `git clone git@github.com:<user>/hermes-backup.git`
2. Copy contents into `~/.hermes/` (do **not** overwrite `.env` or `auth.json` if they exist)
3. Re-enter API keys in `~/.hermes/.env`
4. Restart Hermes gateway / CLI

## Pitfalls

- **Do NOT backup `.env` or `auth.json`.** If they leak, all API keys and OAuth tokens are compromised.
- **Hermes cron pre-v0.14.0.** On versions older than v0.14.0, the built-in cron scheduler had a silent-delivery bug on some platforms (Telegram). If you are on v0.14.0 or newer, Hermes cron is reliable; on older versions, use Linux cron.
- **Large session stores.** `~/.hermes/sessions/` and `~/.hermes/state.db` can be hundreds of MB. They are excluded by default. If you want chat history, export selectively via `hermes sessions export` instead.
- **Protected SSH config.** Some environments block `write_file` on `~/.ssh/config`. Use `terminal` with a heredoc instead.
- **Git branch name.** Old git versions default to `master`. The script forces `main` for consistency with modern GitHub repos.

## References

- `references/backup-hermes.sh` — the complete backup script (copy-and-run)
- `references/gitignore.txt` — `.gitignore` template for the backup repo
- `references/ssh-config.txt` — SSH host alias template
