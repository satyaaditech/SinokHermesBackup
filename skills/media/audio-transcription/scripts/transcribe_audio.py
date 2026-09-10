#!/usr/bin/env python3
"""
Audio transcription script using faster-whisper on CPU/GPU.
"""
import sys
import os
import argparse
import time
from faster_whisper import WhisperModel

def transcribe_audio(audio_path, output_dir="/tmp", model_size="base", language="id", cpu_threads=4):
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    out_full = os.path.join(output_dir, f"{base_name}_transcript.txt")
    out_plain = os.path.join(output_dir, f"{base_name}_plain.txt")

    print(f"Loading faster-whisper ({model_size}) model...")
    t0 = time.time()
    model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=cpu_threads)

    print(f"Transcribing {audio_path}...")
    segments, info = model.transcribe(
        audio_path,
        beam_size=1,
        language=language if language != "auto" else None,
        vad_filter=True
    )

    print(f"Detected language: {info.language} (prob: {info.language_probability:.2f})")

    lines = []
    plain_text = []
    with open(out_full, "w", encoding="utf-8") as f_full, \
         open(out_plain, "w", encoding="utf-8") as f_plain:
        for s in segments:
            line = f"[{s.start:.1f}s - {s.end:.1f}s] {s.text.strip()}"
            f_full.write(line + "\n")
            f_full.flush()
            plain_text.append(s.text.strip())

        f_plain.write(" ".join(plain_text))

    print(f"Transcription complete in {time.time()-t0:.1f}s!")
    print(f"Full transcript: {out_full}")
    print(f"Plain text: {out_plain}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio file")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--output_dir", default="/tmp", help="Output directory")
    parser.add_argument("--model", default="base", help="Model size: base, small, medium")
    parser.add_argument("--lang", default="id", help="Language code (id, en, jw, auto)")
    parser.add_argument("--threads", type=int, default=4, help="CPU threads")
    args = parser.parse_args()

    transcribe_audio(args.audio_path, args.output_dir, args.model, args.lang, args.threads)
