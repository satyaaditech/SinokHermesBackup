---
name: hermes-administration
description: Administer Hermes Agent — backup configuration, manage memory/profiles, and maintain the agent environment.
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos]
---

# Hermes Administration

Class-level skill for operating and maintaining a Hermes Agent instance.

## When to Use

- User wants to back up Hermes config, skills, memory, or cron jobs
- User wants to restore Hermes on a new machine
- User wants to update their profile or persistent memory
- User needs to fix stuck cron jobs or delivery issues

---

## 1. Backup & Disaster Recovery (from hermes-backup)

Backup Hermes data to a private git repository for disaster recovery and cross-machine sync.

### What Gets Backed Up

| Path | Why |
|------|-----|
| `~/.hermes/config.yaml` | Main configuration (model, tools, display, etc.) |
| `~/.hermes/SOUL.md` | Personality / system prompt |
| `~/.hermes/memories/` | Persistent memory (USER.md, MEMORY.md) |
| `~/.hermes/skills/` | All installed and agent-created skills |
| `~/.hermes/cron/` | Cron job definitions and output history |

### What Is EXCLUDED (secrets)

| Path | Reason |
|------|--------|
| `~/.hermes/.env` | API keys and tokens |
| `~/.hermes/auth.json` | OAuth tokens and credential pools |
| `~/.hermes/auth.lock` | Lock file |

### Quick Setup

**SSH authentication (recommended):**

```bash
ssh-keygen -t ed25519 -C "hermes-backup" -f ~/.ssh/hermes_backup -N ""
cat ~/.ssh/hermes_backup.pub
# Add public key to GitHub: Settings → SSH and GPG keys → New SSH key

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

**HTTPS + `.netrc`:**

Create a GitHub PAT with `repo` scope, then store it:
```python
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

### Backup Script

Copy `references/backup-hermes.sh` to `~/scripts/backup-hermes.sh`, make it executable, and run once to initialize the local git repo in `~/hermes-backup`.

### Add Remote & Push

SSH:
```bash
cd ~/hermes-backup
git remote add origin git@github-hermes:<username>/hermes-backup.git
git branch -M main
git push -u origin main
```

HTTPS:
```bash
cd ~/hermes-backup
git remote add origin https://github.com/<username>/hermes-backup.git
git branch -M main
git push -u origin main
```

### Schedule Daily Backup

**Option A: Linux cron**
```bash
crontab -l 2>/dev/null | { cat; echo "0 3 * * * /home/$(whoami)/scripts/backup-hermes.sh >> /home/$(whoami)/hermes-backup/backup.log 2>&1"; } | crontab -
```

**Option B: Hermes built-in cron** (v0.14.0+)
Set the script path to `~/scripts/backup-hermes.sh` in a Hermes cron job. Pre-v0.14.0 had a silent-delivery bug; use Linux cron on older versions.

### Restoring on a New Machine

1. Clone the repo: `git clone git@github.com:<user>/hermes-backup.git`
2. Copy contents into `~/.hermes/` (do **not** overwrite `.env` or `auth.json` if they exist)
3. Re-enter API keys in `~/.hermes/.env`
4. Restart Hermes gateway / CLI

### Pitfalls

- **Do NOT backup `.env` or `auth.json`.** If they leak, all API keys and OAuth tokens are compromised.
- **Large session stores.** `~/.hermes/sessions/` and `~/.hermes/state.db` are excluded by default (hundreds of MB).
- **Git branch name.** Old git versions default to `master`. The script forces `main`.

---

## 2. Memory & Profile Management (from hermes-memory-profile-update)

Update user profile and persistent memory correctly.

### Files

- **USER.md** → Profil user (siapa kamu, preferensi, persona)
- **MEMORY.md** → Fakta environment, project details, lessons learned

### Steps

**1. Baca Memory Saat Ini**
```python
read_file(path="~/.hermes/memories/USER.md")
read_file(path="~/.hermes/memories/MEMORY.md")
```

**2. Identifikasi Yang Perlu Diubah**
- Cari entry yang outdated atau salah
- Note exact text (harus persis untuk replace)

**3. Update Menggunakan Memory Tool**

**Replace Entry:**
```python
memory(
    action="replace",
    target="user",  # atau "memory"
    old_text="- Entry lama yang mau diganti",
    content="- Entry baru"
)
```

**Add Entry Baru:**
```python
memory(
    action="add",
    target="user",
    content="""New Entry Title:
- Detail 1
- Detail 2
- Detail 3"""
)
```

**4. Verifikasi Perubahan**
```python
read_file(path="~/.hermes/memories/USER.md")
```

### Common Pitfalls

1. **Multi-line replace sering gagal** → Gunakan single line atau pecah jadi beberapa replace
2. **Exact match required** → Copy-paste exact text dari file
3. **User vs Memory target** → Jangan sampai salah target file
4. **Character limits** → USER.md max 1,375 chars, MEMORY.md max 2,200 chars

### Best Practices

1. **Selalu baca dulu** sebelum edit → hindari replace yang gagal
2. **USER.md = preferences** (bisa berubah sesuai keinginan user)
3. **MEMORY.md = facts** (project details, environment, lessons learned)
4. **Gunakan "add" untuk baru**, "replace" untuk update, "remove" untuk hapus
5. **Verifikasi setelah edit** → pastikan changes tersimpan dengan benar

## References

- `references/backup-hermes.sh` — complete backup script (copy-and-run)
- `references/gitignore.txt` — `.gitignore` template for the backup repo
- `references/ssh-config.txt` — SSH host alias template
