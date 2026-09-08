# Spesifikasi Subtitle Video (.ass), Tata Letak YouTube & Format WhatsApp Renungan

Dokumen ini menjadi standar baku tata letak visual video renungan dan format penyajian teks multi-bahasa.

---

## 1. Spesifikasi Subtitle Video (.ass) — Bebas Tabrakan & Ramah Lansia

### Masalah yang Dihindari:
1. **Tabrakan Vertikal**: Subtitle di tengah layar (`Alignment: 5`) menimpa header, judul video, dan badge pembicara.
2. **Karakter Kotak Rusak (`⧠`)**: Emoji Unicode di dalam teks acara `.ass` gagal dirender oleh font sistem Linux/FFmpeg.

### Standar Baku Style .ass:
```ini
[Script Info]
Title: Renungan Penyiswaan
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,46,&H00FFFFFF,&H000000FF,&H00000000,&HB00A1520,-1,0,0,0,100,100,0,0,3,12,0,2,140,140,90,1
Style: SabdaJawa,DejaVu Sans,46,&H00E8FFFF,&H000000FF,&H00000000,&HB00A1828,-1,-1,0,0,100,100,0,0,3,12,0,2,140,140,90,1
Style: SpeakerBadge,DejaVu Sans,26,&H0099DDFF,&H000000FF,&H00000000,&H90002040,-1,0,0,0,100,100,0,0,3,8,0,2,200,200,240,1
```

### Aturan Event Subtitle:
* `Alignment: 2` (Bottom-Center).
* Margin vertikal untuk teks utama: `MarginV: 90`.
* Margin vertikal untuk badge pembicara: `MarginV: 240` (berada tepat di atas teks narasi).
* Gunakan teks label ASCII murni tanpa emoji di file `.ass`:
  - `[SABDA SUCI - BASA JAWI]`
  - `[URAIAN & REFLEKSI]`
  - `[PRAKTIK HARIAN]`
  - `[RENUNGAN & PANUTUP]`

---

## 2. Struktur Code Block WhatsApp per Bahasa

Setiap naskah (Basa Jawa, Bahasa Indonesia, English) wajib disajikan dalam ` ```text ` terpisah:

```text
*HARI, TANGGAL BULAN TAHUN*

*RENUNGAN PENYISWAAN*

🛡️ *JUDUL TEMATIK RENUNGAN* 🌊🕊️✨

📺 *Video YouTube :* https://youtu.be/...

_Salam Bahagia Bp/Ibu/Sdr semuanya,_

*📖 SABDA HARI INI :*
[Kutipan Sabda Verbatim Murni 100%]

Terjemahan : [...]

💭 *URAIAN :*
[...]

🧘 *PRAKTIK :*
1. [...]
2. [...]
3. [...]
✅ Dapat dipraktikkan di mana saja dan kapan saja.

🎯 *RENUNGAN :*
[...]

📝 *APLIKASI :*
1. [...]
2. [...]
3. [...]

🙏 Semoga kita semua senantiasa dalam Lindungan dan Bimbingan Kasih Sang Guru Sejati. Satuhu. 🙏

---
Tautan Pustaka Digital & Dokumen:
• 📺 Video YouTube: https://youtu.be/...
• 📄 Google Doc: https://docs.google.com/document/d/...
• 🌐 Pustaka Web Kontemplasi: https://kontemplasi.satyaaditech.web.id/

📖 Waos naskah jangkep wonten ing Pustaka Kontemplasi: https://kontemplasi.satyaaditech.web.id/#<slug>
```

---

## 3. Pantangan Produksi
1. **NO E-CARD**: Dilarang membuat berkas e-card PNG (Pak Satya menyiapkan poster infografis sendiri).
2. **NO ROBOTIC TTS**: Wajib menggunakan Gemini 2.5 Audio Engine (Charon/Aoede). Dilarang fallback ke Edge-TTS/suara sintetis tanpa persetujuan.
