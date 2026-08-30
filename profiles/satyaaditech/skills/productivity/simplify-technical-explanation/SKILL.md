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

## Verification Checklist

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

1. **Starting too technical** — Always begin at Level 1
2. **Assuming knowledge** — Don't assume user knows basics
3. **No analogies** — Abstract concepts need concrete comparisons
4. **Jargon without explanation** — Define every technical term
5. **Wall of text** — Break into scannable sections
6. **Not checking understanding** — Ask "ada yang bingung?" after explaining

## Related Skills

- `gsd-installation-guide` — For GSD-specific documentation
- `youtube-content` — For summarizing video content simply
- `writing-plans` — For structuring multi-step explanations
