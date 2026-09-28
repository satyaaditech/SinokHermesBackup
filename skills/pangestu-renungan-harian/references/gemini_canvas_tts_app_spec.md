# Gemini Canvas TTS Application Specification for Daily Reflections

Panduan dan template prompt untuk membuat aplikasi Text-to-Speech (TTS) interaktif satu file (Single-file HTML + Tailwind CSS + Vanilla JS) di Google Gemini Canvas. Dirancang khusus untuk memproduksi audio renungan harian (Bilingual: Indonesia & Jawa) yang khidmat, tenang, dan alami.

---

## 1. Arsitektur Teknis Aplikasi Canvas
* **Runtime**: Client-side murni di browser (Web Speech API + Web Audio API).
* **UI/UX**: Single file HTML, Tailwind CSS CDN, Dark Theme (Slate #0f172a / Amber #f59e0b), Font Serif (Georgia/Merriweather).
* **Audio Engine**:
  * Dual-Voice switching: Suara A (Kutipan Sabda, Deep/Male) dan Suara B (Narasi/Uraian, Warm/Female).
  * Smart Pacing: Kecepatan kontemplatif (0.88x–0.92x), jeda dinamis (1.5s antar paragraf, 2.0s setelah Sabda).
  * Javanese Phonetic Engine: Normalisasi pelafalan vokal dan konsonan Jawa.
  * Ambient BGM Auto-Ducking: Ducking musik pengiring saat narasi aktif (volume turun ke 15%).
  * MediaRecorder Exporter: Merekam output audio gabungan TTS + BGM langsung ke file `.wav` / `.webm`.

---

## 2. Master Prompt Siap Pakai untuk Gemini Canvas

```text
Buatkan sebuah aplikasi web Text-to-Speech (TTS) interaktif satu file mandiri (Single-file HTML + Tailwind CSS + Vanilla JavaScript) di dalam Canvas yang dirancang khusus untuk memproduksi audio "Renungan Spiritual & Olah Rasa" dalam Bahasa Indonesia dan Bahasa Jawa agar terdengar sangat natural, tenang, khidmat, dan indah didengarkan.

Aplikasi ini harus berjalan langsung di browser (client-side) menggunakan Web Speech API dan Web Audio API tanpa memerlukan backend eksternal.

FITUR UTAMA DAN SPESIFIKASI TEKNIS:

1. SMART SCRIPT EDITOR & JAVANESE PHONETIC PARSER:
   - Area Textarea besar untuk input naskah renungan (mendukung teks biasa atau Markdown).
   - Tombol "Auto-Detect & Bersihkan Teks":
     * Menghapus simbol markdown (**, ##, *, _) yang sering terbaca aneh oleh mesin TTS.
     * Membersihkan URL dan tag tanpa merusak tanda baca jeda (. , : ; ? !).
   - Javanese Phonetic Normalizer Engine (Fitur Khusus Basa Jawa):
     * Otomatis mengonversi ejaan kata-kata Jawa yang sering salah dilafalkan oleh TTS standar.
   - Segmentasi Otomatis Suara (Dual Role):
     * Deteksi tag [SABDA] ... [/SABDA] (suara berwibawa, tempo tenang, jeda hening) dan [URAIAN] ... [/URAIAN] (suara hangat, mengalir).

2. KONTROL INTONASI & KONTEMPLASI (PACING ENGINE):
   - Pengaturan Kecepatan (Speed): 0.7x - 1.2x (Default: 0.88x - 0.92x).
   - Dynamic Smart Pause: Jeda antar paragraf 1.5 detik, jeda setelah kutipan Sabda 2.0 detik.
   - Voice Selector Dropdown: Membaca suara Bahasa Indonesia/Jawa/Regional di browser.

3. INTEGRASI AMBIENT BACKGROUND MUSIC (BGM):
   - Synthesizer nada relaksasi bawaan (432Hz ambient drone) ATAU upload file audio pengiring sendiri.
   - Fitur "Auto-Ducking": Volume musik mengecil otomatis saat suara narator aktif.

4. REAL-TIME PLAYBACK & AUDIO EXPORTER:
   - Player: Play, Pause, Resume, Stop, serta visual sentence highlighting.
   - Audio Export Recorder (MediaRecorder): Merekam narasi + BGM ke file audio (.wav/.webm) siap unduh.

5. DESAIN UI/UX:
   - Tema: Serene Sanctuary Dark Mode (#0f172a, aksen gold #f59e0b).
   - Layout 2 kolom: Editor di kiri, Pengaturan & Player/Download di kanan.
```
