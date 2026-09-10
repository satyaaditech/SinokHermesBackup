---
name: audio-transcription
description: "Transcribe and summarize audio files or voice notes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Audio, Transcription, Whisper, Voice-Notes, Summarization, Media]
    related_skills: [youtube-operations, telegram-formatting]
---

# Audio Transcription & Summarization

This skill covers end-to-end processing for local audio files, Telegram voice notes, podcasts, meeting recordings, and voice memos: extracting audio metadata, transcribing speech to text using `faster-whisper`, and generating structured summaries.

## Trigger Conditions
- User sends an audio attachment (`.mp3`, `.m4a`, `.wav`, `.ogg`, `.aac`, Telegram voice bubble).
- User requests a transcript, summary, or analysis of an audio file stored locally or on server.
- Audio needs to be analyzed for fraud detection, meeting action items, lecture notes, or dialogue transcription.

---

## Step 1: Inspect Audio Duration & Properties

Always inspect the audio length first to plan the execution model and avoid timeouts:

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /path/to/audio.mp3
```

---

## Step 2: Choose Model & Compute Configuration

| Hardware / Resource | Recommended Model | Compute Type | Settings |
|---|---|---|---|
| **CPU (Quad-core / Laptop / Low-spec)** | `base` | `int8` | `cpu_threads=4`, `beam_size=1` (~20-25s per 1 min audio) |
| **CPU (High-spec / Multi-core Server)** | `small` or `base` | `int8` | `cpu_threads=8`, `beam_size=2` |
| **GPU (NVIDIA CUDA Available)** | `small`, `medium`, or `large-v3` | `float16` | `device="cuda"`, `beam_size=5` |

> ⚠️ **CPU Timeout Pitfall**: Running `small` or `medium` on a modest CPU for files longer than 3 minutes will easily exceed terminal timeouts (300s). Always default to `base` with `int8` on CPU unless GPU is available or time limit is high. `base` achieves high accuracy for Indonesian, Javanese, English, etc.

---

## Step 3: Transcription Script Template

Execute transcription via `faster-whisper` and stream segments to disk:

```python
import time
from faster_whisper import WhisperModel

audio_path = "/path/to/audio.mp3"
output_full = "/tmp/transcript_full.txt"
output_plain = "/tmp/transcript_plain.txt"

# Initialize faster-whisper
model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=4)

# Transcribe with language detection or hint
segments, info = model.transcribe(
    audio_path,
    beam_size=1,
    language="id", # Set language code if known (e.g. 'id', 'en', 'jw') or omit for auto-detect
    vad_filter=True
)

lines = []
plain_text = []

with open(output_full, "w", encoding="utf-8") as f_full, \
     open(output_plain, "w", encoding="utf-8") as f_plain:
    for s in segments:
        line = f"[{s.start:.1f}s - {s.end:.1f}s] {s.text.strip()}"
        f_full.write(line + "\n")
        f_full.flush()
        plain_text.append(s.text.strip())

    f_plain.write(" ".join(plain_text))

print(f"Transcription complete: {len(plain_text)} segments processed.")
```

---

## Step 4: Structuring the Summary

When presenting the summary to the user:
1. **Overview & Context**: Total duration, main participants/speakers, core topic.
2. **Key Discussion Points**: Grouped by logical themes or chronological flow.
3. **Critical Assessment / Red Flags** (if applicable): Financial claims, investment schemes, advance-fee requests, compliance/legal issues.
4. **Action Items / Next Steps**: Concrete deliverables, deadlines, or follow-up items.
5. **Language & Persona Adaptation**: Maintain the user's preferred communication language (e.g., Basa Jawi Krama Alus or Indonesian) while keeping technical/legal terms accurate.

---

## Pitfalls & Best Practices

1. **Audio Slicing / Sub-segmenting**:
   - If slicing audio with `ffmpeg`, never use `-c copy` on MP3 slices with sub-second accuracy as it corrupts frame headers for PyAV. Always re-encode:
     ```bash
     ffmpeg -y -ss <start> -to <end> -i input.mp3 /tmp/slice.wav
     ```
2. **Repetition / Hallucination Loops**:
   - In noisy or silent sections, Whisper may repeat words. Use `vad_filter=True` and `beam_size=1` or `temperature=0.0` to suppress hallucinations.
3. **Large Files (>15 Minutes)**:
   - Run in background or with generous timeout (`timeout=600`), writing increments to `/tmp/transcript_full.txt`.
