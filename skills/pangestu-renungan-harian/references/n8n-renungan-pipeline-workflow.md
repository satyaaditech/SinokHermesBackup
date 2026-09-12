# n8n Workflow: Pipeline Renungan Pangestu (100% Native Built-in Nodes & Official YouTube)

- **Workflow ID**: `UBMaa9yeTpO28E9z`
- **Status**: `ACTIVE`
- **Trigger Webhook**: `POST https://n8n.satyaaditech.web.id/webhook/renungan-pangestu-nocode` (Internal: `http://127.0.0.1:5678/webhook/renungan-pangestu-nocode`)
- **Automation Runner Port**: `http://172.17.0.1:8089` (Internal service for FFmpeg render, GDoc formatting, Web sync)

## Alur Pembagian Peran
1. **Sinox**: Riset naskah Pangestu verbatim 100% -> Draft teks polos Basa Indonesia -> Nyuwun ACC Pak Satya.
2. **Pak Satya**:
   - Maringi ACC & milih versi basa.
   - Ndamel Poster Infografis (ChatGPT / Canva).
   - Ndamel Audio Rekaman (Gemini Canvas Dual-Voice: Charon kagem Sabda Jawi, Aoede kagem Uraian/Refleksi).
   - Ngintun file Poster & Audio dhateng Telegram.
3. **Sinox -> n8n Workflow (`UBMaa9yeTpO28E9z`)**:
   - Mengirim payload data lengkap ke Webhook `renungan-pangestu-nocode`.
   - Node 3 (Quality Gate): Validasi kelengkapan teks, tanggal, judul, file path.
   - Node 4 & 5a-5b: Render FFmpeg portrait HD (1080x1920) -> Baca binary -> Upload resmi YouTube `@siswatalkstv` (OAuth2 `bRNGQ7vD6HinIyDT`, privacy *Unlisted*).
   - Node 6: Format Google Doc (H1 Judul + Poster Center 320pt + Page Break + H2 Indent 24pt + Footer UTF-16).
   - Node 7: Deploy Pustaka Web `kontemplasi.satyaaditech.web.id` + Git sync.
   - Node 8: Arsip Markdown ke Obsidian NVMe `/mnt/usb-nvme/obsidian/`.
   - Node 9: Logging Master Google Sheets `1QuTSjBV-iOckaIoSu07wQa0LcnbgdR97mxAqOloIEb0`.
   - Node 10: Validasi 3 link & notifikasi siaran Telegram.
