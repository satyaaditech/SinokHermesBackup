# Pembuatan Audio Renungan & Integrasi WhatsApp

Panduan ini mendokumentasikan setup Text-to-Speech (TTS) Bahasa Indonesia sarta integrasi pengiriman audio renungan ke WhatsApp agar saged dipun-putar langsung di chat (real-time).

## 1. Setup Voice TTS Bahasa Indonesia (Edge)

Secara default, agen ngginakaken swanten `en-US-AriaNeural` ingkang mboten pas kagem maos teks Indonesia/Jawa (aksen Inggris ketawis aneh). Supados pelafalan cetha lan alus, gantos konfigurasi TTS dhumateng swanten Basa Indonesia:

*   **Penyedia**: Microsoft Edge TTS (`edge`).
*   **Voice Model**: `id-ID-GadisNeural` (swara estri, alus sarta anteng, cocog kagem renungan) utawi `id-ID-ArdiNeural` (swara jaler, wibawa lan tenang).

### Cara Gantos Konfigurasi:
Jalankan perintah menika wonten ing terminal kagem ngubah sacara permanen ten profil Hermes:
```bash
hermes config set tts.edge.voice id-ID-GadisNeural
```

Verifikasi hasilipun kanthi perintah:\n```bash\nhermes config get tts.edge.voice\n# Output kudu: id-ID-GadisNeural\n```

## 2. Pengiriman Audio dhumateng WhatsApp (Real-time Playback)

Supados berkas audio renungan (`.ogg` utawi `.mp3`) saged dipun-putar kanthi langsung minangka **Pesen Swara (Voice Note)** wonten ing obrolan WhatsApp tanpa kedah dipun-download dhumateng galeri:

1.  **Format Berkas**: Gunakan format `.ogg`. Output rekaman saking `text_to_speech_ide` sacara otomatis gadhah codec Opus ingkang kompatibel kaliyan format WhatsApp Voice Note.
2.  **Message Type di API Gateway**:
    *   Nalika ngirim audio liwat gateway/n8n/script otomatisasi, **Message Type** kudu diset minangka **`audio`**, mboten dipun-set minangka `document`.
    *   WhatsApp badhe nampilaken berkas audio kanyatan menika awujud gelombang swanten (*waveform*) mawi tombol *Play* langsung wonten ing obrolan. Menawi diset minangka `document`, berkas kasebut namung badhe ngambang lan pating mecungul dados file biyasa.

## 3. Workaround Aksen Inggris Nyangkut (Cache Runtime)

Nalika konfigurasi sampun dipun-set dhumateng `id-ID-GadisNeural` nanging asil output saking tool `text_to_speech_ide` taksih medal mawi aksen Inggris (amargi cache runtime asisten ingkang saweg mlampah), gunakaken script Python mandiri kagem ngundhuh sarta ngompilasi ulang audio sacara manual ngginakaken `edge-tts` lan `ffmpeg`.

### Langkah Eksekusi Workaround:
Jalankan script python kados ing ngandhap punika kagem macak teks renungan dhumateng MP3 sarta ngubah dhumateng format OGG/Opus mawi `ffmpeg`:

```python
import asyncio
import edge_tts
import re
import subprocess

async def generate_tts(text_path, mp3_output, ogg_output):
    # 1. Bersihkan teks saking tag markdown (* dan _)
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    clean_text = re.sub(r'[*_]', '', text)
    
    # 2. Kontak server Edge TTS
    communicate = edge_tts.Communicate(clean_text, "id-ID-GadisNeural")
    await communicate.save(mp3_output)
    
    # 3. Konversi dhateng OGG/Opus kagem Voice Note
    cmd = ["ffmpeg", "-y", "-i", mp3_output, "-c:a", "libopus", "-b:a", "64k", ogg_output]
    subprocess.run(cmd)

asyncio.run(generate_tts("renungan.md", "output.mp3", "output.ogg"))
```

Script menika badhe meksa panggunaan swanten `id-ID-GadisNeural` sacara langsung tanpa dipun-pengaruhi dening pembacaan config saking runtime Hermes ingkang nyangkut.
