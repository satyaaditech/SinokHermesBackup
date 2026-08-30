# Publish Renungan — Recipe Aman (anti timeout, anti link hilang)

Kacathet 26-08-2026 sawise kasalahan: `publish()` dipunpanggil foreground → timeout tool (60s) manglajeng proses dipunpejahi ing tengah TTS → link Google Doc boten nyisip ing `.md` → lapor marang Pak Satya tanpa link Drive.

## Kenapa musti background
`publish_renungan.publish()` nindakake: buat 2 Google Doc → upload HTML → `edge-tts` jawa (jv-ID-DimasNeural) + ind (id-ID-GadisNeural) → `ffmpeg` dadi `.ogg`. Total wadose ±6 menit. Wates wekdal tool foreground namung 60 detik. Mboten bakal rampung.

## Urutan aman
1. Gawe wrapper `publish_runner.py` sing nggawe `jawa_template`, `ind_template`, lan paths. Template mesti ditutup `Google Doc: [DOC_URL]` (placeholdere bakal diganti dadi URL asli dening `publish()`).
2. Jalankan **background**:
   ```bash
   python3 /tmp/publish_runner.py > /tmp/publish.log 2>&1 &
   ```
   (utawa tool `terminal(background=true, notify_on_complete=true)`)
3. Sawise rampung (exit 0), **verifikasi link**: tail file `.md` output:
   ```bash
   tail -n 1 ~/share/renungan/renungan-<tema>-<tgl>.md
   ```
   Mesti keluar `Google Doc: https://docs.google.com/document/d/<id>/edit`.
   Uga versi `-ind`: `tail -n 1 ...-ind-<tgl>.md`.
4. Baru lapor marang Pak Satya yen "sampun rampung", bareng 2 link Drive. BISA dipetik URL saka isi file, ora sampeyan tulis manual.
5. Yen garapan urutan: swojo kudu verifikasi link dhisik — penerusan laporan mboten wonten link = workflow blunder.

## Tandha kegagalan
- File `.md` isih metu placeholder `[DOC_URL]` → publish mboten rampung, jalankan malih ing background lan priksa `/tmp/publish.log`.
- `.ogg` mboten digawe → TTS/ffmpeg gagal (priksa subprocess error ing log).

## Cathetan
- `edge-tts` mbutuhake suara `jv-ID-DimasNeural` (Jawa) lan `id-ID-GadisNeural` (Indonesia).

## Varian: Basa Indonesia Saja (Tanpa Audio, Tanpa Cover)
Menawi dipun-suwun nggawe renungan versi basa Indonesia kemawon, tanpa audio (TTS) lan tanpa cover:
1. Kita saged ngginakaken script `publish_renungan_simple.py` lan nimbali fungsi `publish_simple(ind_template, date_str, date_iso, ind_out_path)`.
2. Amargi mboten wonten proses nggawe audio (edge-tts/ffmpeg) lan cover (Pillow), proses punika saged rampung cepet banget (namung 2-5 detik kagem ngubungi Google Drive API).
3. Proses punika saged dipun-lampahi sacara **foreground** (mboten kedah background / screen).
4. Pembaruan wiki tetep kedah dipun-lampahi:
   - Nyimpen md file wonten ing `wiki/renungan/` lan `~/share/renungan/`.
   - Nganyari `Daftar Renungan.md` lan `log.md` kanthi kronologis.
- Ora nggabungaken cover+publish ing siji script foreground — ubahana dadi loro langkah, publish ing background.