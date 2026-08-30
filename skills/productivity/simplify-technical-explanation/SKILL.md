---
name: simplify-technical-explanation
description: >
  Explain complex technical concepts in simple, accessible language — like
  explaining to a 15-year-old. Use analogies, avoid jargon, and focus on
  what/why before how. Escalate complexity only when user requests more detail.
---

# Simplifying Technical Explanations

This skill provides a framework for breaking down complex technical topics into easy-to-understand explanations.

## When to Use

- User says "jelaskan dengan bahasa sederhana" or "seperti ke anak 15 tahun"
- User seems confused by technical jargon
- Introducing a new concept to a non-technical user
- User asks for "intinya apa?" or "maksudnya gimana?"

## Explanation Framework

### Level 1: Simple (Default Starting Point)

**Characteristics:**
- Use everyday analogies (pizza, school, games, shopping)
- No jargon or acronyms without explanation
- Short sentences, conversational tone
- Focus on **what** it does and **why** it matters
- Use emojis and visual formatting

**Example Structure:**
```
🎮 **Analogi Sederhana**

Bayangkan [konsep] itu seperti [sesuatu yang familiar]...

**Tanpa [konsep]:**
```
[scenario buruk]
```

**Dengan [konsep]:**
```
[scenario baik]
```

**Intinya:** [1 kalimat sederhana]
```

### Level 2: Intermediate (When Asked)

**Characteristics:**
- Introduce technical terms with plain-English explanations
- Show concrete examples/commands
- Explain trade-offs and when to use what
- Use tables for comparisons

### Level 3: Advanced (On Request)

**Characteristics:**
- Deep technical details
- Architecture diagrams
- Performance considerations
- Edge cases and pitfalls

## Analogy Bank

| Technical Concept | Simple Analogy |
|-------------------|----------------|
| API | Waiter at restaurant (takes order, brings food) |
| Database | Filing cabinet for information |
| Context Window | Short-term memory (forgets when full) |
| Git Commit | Save point in a video game |
| Deployment | Moving from practice to live game |
| Authentication | Showing ID at club entrance |
| Rate Limiting | Queue system at popular store |
| Caching | Keeping frequently-used items on desk |
| Load Balancing | Multiple checkout lanes at supermarket |
| Microservices | Restaurant with specialized chefs |
| CI/CD | Assembly line with quality checks |
| Container (Docker) | Lunchbox — keeps everything together |
| Cloud Computing | Renting electricity vs building power plant |
| AI Agent | Smart assistant who can use tools |
| Coding Harness | Seatbelt + steering wheel for the AI driver |
| Claude Code vs Pi | Aggressive driver (autopilot) vs careful driver (asks first) |
| Context Engineering | Giving assistant a good briefing before task |

## Language Patterns

### DO ✅

- "Bayangkan..." (Imagine...)
- "Kayak..." / "Seperti..." (Like...)
- "Gampangnya..." (Simply put...)
- "Intinya..." (The gist is...)
- "Masalahnya..." / "Solusinya..." (The problem is... / The solution is...)
- Use emojis for visual breaks 🎯📌✅❌

### DON'T ❌

- Start with technical definitions
- Use acronyms without explanation
- Say "obviously" or "clearly"
- Assume prior knowledge
- Wall of text without breaks

## Example: Explaining GSD

### Bad (Too Technical)
```
GSD is a meta-prompting and context engineering system that solves
context rot through spec-driven development workflows with multi-agent
orchestration and atomic git commits.
```

### Good (Simple)
```
🎮 **GSD itu Apa Sih?**

Bayangkan kamu punya teman super pinter (si AI) yang bisa ngerjain
tugas coding buat kamu.

**Masalahnya:**
- Kalau kamu cuma bilang "buatin aku game dong", hasilnya bakal acak-acakan
- Temen kamu ini gampang lupa kalau tugasnya kepanjangan
- Hasilnya sering nggak sesuai yang kamu mau

**GSD itu seperti...** 📋

> Buku panduan yang bikin temen super pinter kamu nggak lupa dan
> ngerjain tugas dengan bener dari awal sampai akhir!
```

## Summarizing Technical Articles / Reviews

When a user asks you to summarize a technical article, blog post, or product review, do NOT default to formal/journalistic language. The user likely wants to understand the *point*, not a play-by-play of the article.

### Default Approach

1. **Start with the core thesis** in 1 plain sentence.
2. **Use an analogy** the user can relate to (see Analogy Bank above).
3. **Highlight trade-offs** with simple good/bad framing.
4. **Offer to go deeper** only after confirming understanding.

### Structure

```
🎯 **Intinya:** [One sentence, what the author decided and why]

📌 **Analogi Sederhana:**
[Compare the technical choices to an everyday scenario]

**Kenapa pindah?**
• [Simple reason 1]
• [Simple reason 2]

**Trade-off-nya:**
✅ Bagusnya: [Benefit]
❌ Kurangnya: [Drawback]

**Kesimpulan:** [One sentence recommendation]
```

### What to AVOID in article summaries

- ❌ Formal journalist tone: "The author posits that..." / "It is noteworthy that..."
- ❌ Wall of feature lists without context
- ❌ Acronyms without explanation (LLM, CLI, TUI, RPC, etc.)
- ❌ Starting with the author's bio or background
- ❌ Too many quotes from the article without interpretation

### What to DO instead

- ✅ Speak like you're chatting with a friend: "Jadi si penulis tuh..."
- ✅ Lead with the decision/outcome, not the article structure
- ✅ Ask "Udah jelas? Mau aku jelasin lebih detail?" after the summary
- ✅ If the user says "kok belum ngerti?" — immediately switch to an analogy

Before sending explanation, check:

- [ ] Did I use an analogy or real-world comparison?
- [ ] Are there any unexplained technical terms?
- [ ] Is the formatting easy to scan (headers, bullets, emojis)?
- [ ] Did I focus on what/why before how?
- [ ] Is the tone conversational, not lecture-like?
- [ ] Would a 15-year-old understand this?

## Escalation Pattern

When user wants more detail:

```
User: "Oh gitu, terus cara kerjanya gimana?"

You: "Oke, gue jelasin lebih detail ya..."

[Move to Level 2 explanation]
```

When user is satisfied:

```
User: "Oh oke oke, sekarang aku ngerti"

You: "Mantap! Ada yang mau ditanyain lagi?"
```

## User Preferences (This User)

- **Language**: Indonesian (Bahasa Indonesia)
- **Tone**: Casual, friendly, like talking to a friend
- **Format**: Bullet points (• or ▸), NO markdown tables in Telegram
- **Delivery**: Always send to Telegram with clear formatting
- **Confirmation**: Check understanding before moving to technical details

## Pitfalls

1. **Summarizing in journalist language** — When summarizing a technical article/review, users often respond "Aku kok masih belum mengerti?" because the summary was written like a tech news article (formal, feature-list heavy, no analogy). Fix: immediately restart with a simple analogy the user can relate to. Do NOT re-summarize with more words — reframe with a comparison.
2. **Starting too technical** — Always begin at Level 1
3. **Assuming knowledge** — Don't assume user knows basics
4. **No analogies** — Abstract concepts need concrete comparisons
5. **Jargon without explanation** — Define every technical term
6. **Wall of text** — Break into scannable sections
7. **Not checking understanding** — Ask "ada yang bingung?" after explaining

## Related Skills

- `gsd-installation-guide` — For GSD-specific documentation
- `youtube-content` — For summarizing video content simply
- `writing-plans` — For structuring multi-step explanations
