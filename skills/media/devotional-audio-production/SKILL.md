---
name: devotional-audio-production
description: Use when generating spoken audio/TTS for devotionals.
---

# Devotional Audio & Spoken Text Production

SOP and technical guidelines for producing high-quality spoken audio (Text-to-Speech) for daily devotionals, sermons, and contemplative texts.

## 1. Text Sanitization & Pacing for Speech
Raw text formatted for messaging apps (WhatsApp/Telegram) contains visual markers that break or degrade spoken audio. Always sanitize before sending to TTS:

1. **Strip Emojis & Decorative Bullets**:
   - Remove decorative symbols like `🍃`, `📖`, `❤️1.`, `✝️`, `🧏♂️`, and directional arrows (`==>`).
   - Replace numbered emoji lists with standard spoken transitions: *"Poin pertama"*, *"Poin kedua"*, *"Satu"*, *"Dua"*.

2. **Expand Liturgical & Devotional Abbreviations**:
   - `IB MGU` / `IB MINGGU` → *"Ibadah Minggu"*
   - `TB` → *"Terjemahan Baru"*
   - `SSJ` → *"Serat Sasangka Jati"*
   - Expand book names and scripture citations: *"Mazmur 147:3"* → *"Mazmur pasal 147 ayat 3"*.

3. **Spoken Cadence & Pauses**:
   - Insert comma breaks after speaker addresses (*"Shalom, Bapak, Ibu."*).
   - Use sacred pauses (1.0s - 2.5s) between major sections (scripture reading, reflection, practical application) to allow the message to breathe.

## 2. Edge-TTS Chunking Pipeline (Anti-429 & Anti-Desync)
Sending large texts (>3,000 characters) in a single request to Microsoft Edge-TTS or chaining parallel requests frequently triggers WebSocket errors (`WSServerHandshakeError: 429` / rate-limit) or gateway timeouts.

### Sequential Chunking Pattern
1. **Divide into Thematic Blocks**:
   - Split the full devotional into 3–5 logical blocks of 800–1,200 characters each (e.g. Pembuka + Sabda, Uraian Batin, Langkah Praktis, Doa Penutup).
2. **Execute via Local CLI**:
   - Use the local CLI binary `/home/satyaaditech/.local/bin/edge-tts --file <chunk.txt> --voice <voice> --rate="<rate>" --write-media <chunk.mp3>`.
   - Recommended Indonesian devotional voices:
     - `id-ID-ArdiNeural` (rate -3% to -5%): warm, pastoral, solemn, grounded.
     - `id-ID-GadisNeural` (rate -2% to -4%): gentle, calm, contemplative.
3. **Sequential Processing with Delay**:
   - Process chunks in serial order with `time.sleep(1.5)` between calls to respect WebSocket handshake thresholds.
4. **Lossless Audio Concatenation via FFmpeg**:
   - Create a text manifest `concat.txt`:
     ```
     file '/tmp/chunk_0.mp3'
     file '/tmp/chunk_1.mp3'
     file '/tmp/chunk_2.mp3'
     ```
   - Concat without re-encoding:
     ```bash
     ffmpeg -y -f concat -safe 0 -i concat.txt -c copy master_output.mp3
     ```

## 3. Platform Distribution Constraints
- **Telegram Hard Limit (4096 Chars)**:
  - Rich devotionals with expanded reflections and practical application often exceed Telegram's 4096-character limit.
  - Split into 2 parts when sending to Telegram topics:
    - *Part 1*: Header, Sabda/Scripture, Translation, Pangilon Rasa (Reflection).
    - *Part 2*: Laku Panyiswan (Application), Jangkar Batin (Core Takeaway), Reflection Question, Closing Prayer.
  - Always use HTML `parse_mode="HTML"` with clean tags (`<b>`, `<i>`, `<blockquote>`) to avoid Markdown parse breakage on complex punctuation.
