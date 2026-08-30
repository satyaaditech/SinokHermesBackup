---
name: gsd-installation-guide
description: >
  Create comprehensive installation guides for GSD (Get Shit Done) workflow
  system on macOS, including AI agent setup (Antigravity/OpenCode), prerequisites,
  troubleshooting, and Telegram delivery. Use when user requests GSD installation
  help or wants a reusable installation document.
---

# GSD Installation Guide Creation

This skill provides a template and workflow for creating comprehensive GSD installation documentation for macOS users.

## When to Use

- User asks for GSD installation help on MacBook/macOS
- User wants a reusable installation document
- User needs comparison between AI agents (Antigravity vs OpenCode)
- User prefers documentation delivered to Telegram

## Prerequisites Check

Before providing instructions, confirm:
1. **User's OS** — macOS (MacBook), Windows, or Linux
2. **Existing tools** — Homebrew, Node.js, npm already installed?
3. **AI Agent preference** — Free (Antigravity) or Production (OpenCode)?
4. **API Keys** — Does user have OpenRouter/Anthropic/Google accounts?

## Installation Guide Structure

```markdown
# 🚀 Panduan Lengkap: Install GSD di [OS]

## 📋 Daftar Isi
1. Pendahuluan
2. Pilihan AI Agent
3. Instalasi Prerequisites
4. Opsi A: [Agent 1] + GSD
5. Opsi B: [Agent 2] + GSD
6. Perbandingan
7. Troubleshooting
8. Mulai Project Pertama
9. Cheat Sheet Command
10. Checklist Instalasi
```

## Key Sections

### 1. Prerequisites (macOS)

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.js
brew install node

# Verify
node --version && npm --version
```

### 2. AI Agent Options

| Agent | Install Command | Price | Best For |
|-------|-----------------|-------|----------|
| Antigravity | `npm install -g @google/antigravity` | Free (quota) | Learning, small projects |
| OpenCode | `brew install opencode` | Pay-per-token | Production work |
| Claude Code | `npm install -g @anthropic-ai/claude-code` | $20/month | Professional use |

### 3. GSD Installation

```bash
# For Antigravity
npx get-shit-done-cc@latest --antigravity --global

# For OpenCode
npx get-shit-done-cc@latest --opencode --global

# For Claude Code
npx get-shit-done-cc@latest --claude --global
```

### 4. Test Installation

```bash
# Start AI agent
antigravity  # or opencode / claude

# Inside agent, test GSD
/gsd-help
```

### 5. Common Troubleshooting

| Error | Solution |
|-------|----------|
| `npm: command not found` | `brew install node` |
| `brew: command not found` | Install Homebrew first |
| GSD not detected | Re-run install with correct flag |
| API Key Invalid | Check env variable, restart terminal |

## Telegram Delivery

After creating the guide:

1. Save as `.md` file:
   ```bash
   write_file path="/home/satyaaditech/gsd-installation-guide.md"
   ```

2. Send summary to Telegram:
   ```
   send_message target="telegram" message="[Quick start summary]"
   ```

3. Send file to Telegram:
   ```
   send_message target="telegram" message="MEDIA:/path/to/file.md"
   ```

## User Preferences (Important)

- **Format**: Plain text with bullet points (• or ▸), NO markdown tables in Telegram messages
- **Language**: Indonesian (Bahasa Indonesia)
- **Tone**: Friendly, conversational, like explaining to a friend
- **Complexity**: Start simple (like explaining to 15-year-old), offer technical details optionally
- **Delivery**: ALWAYS send to Telegram — never silent, never empty

## Cross-Platform Awareness

**CRITICAL**: Always confirm user's OS before giving installation instructions.

| Platform | Package Manager | Notes |
|----------|-----------------|-------|
| macOS | Homebrew (`brew`) | Most common for developers |
| Linux | apt/dnf/pac | Varies by distro |
| Windows | Chocolatey/scoop | Or WSL for Linux tools |

**Common mistake**: Giving Linux instructions to macOS user (or vice versa). Always ask first!

## Explanation Levels

When explaining technical concepts:

### Level 1: Simple (15-year-old)
- Use analogies (pizza ordering, school projects)
- Avoid jargon (no "context engineering", "orchestration")
- Focus on what/why, not how

### Level 2: Intermediate
- Introduce technical terms with explanations
- Show command examples
- Explain trade-offs

### Level 3: Advanced
- Deep technical details
- Architecture diagrams
- Performance considerations

**Always start at Level 1**, then ask if user wants more detail.

## Checklist Template

```
[ ] Step 1: Install Homebrew
[ ] Step 2: Install Node.js
[ ] Step 3: Install AI Agent
[ ] Step 4: Setup (Login / API Key)
[ ] Step 5: Install GSD
[ ] Step 6: Test /gsd-help
```

## Pitfalls

1. **Assuming OS** — Don't assume Linux just because you're on Linux
2. **Skipping prerequisites** — Homebrew/Node.js must be installed first
3. **Not testing** — Always include `/gsd-help` test step
4. **Forgetting API keys** — OpenCode needs OPENROUTER_API_KEY env var
5. **Too technical** — Start simple, escalate complexity only if asked
6. **No Telegram delivery** — User expects docs sent to Telegram

## Resources

- GSD Repo: https://github.com/gsd-build/get-shit-done
- GSD User Guide: https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md
- Antigravity: https://github.com/google/antigravity
- OpenCode: https://github.com/opencode-ai/opencode
- OpenRouter: https://openrouter.ai/
