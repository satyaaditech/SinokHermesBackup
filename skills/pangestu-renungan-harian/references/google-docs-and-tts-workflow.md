# Alur Google Docs & Audio TTS Renungan Harian

Referensi ini mendokumentasikan tata cara otomatisasi penyimpanan renungan harian Pangestu ke Google Drive (Google Doc) dan pembuatan versi audio TTS beraksen Indonesia.

## 1. Alur Google Drive & Google Doc (Penyimpanan Rapi)

Setiap kali renungan dibentuk (hari ini dan besok), selain disimpan di server lokal, berkas harus diunggah juga ke Google Drive di folder **"Renungan Harian"** (Folder ID: `1Ei8R28btJH6rjCC1lKrfkaCC-KxmKeNW`).

### Format Konversi Terformat Cantik
Agar format Markdown (seperti bold dan italic) terbaca rapi di Google Doc saat diunggah, gunakan alur konversi melalui HTML:
1. Ganti karakter format WhatsApp bold (`*teks*`) menjadi standard markdown bold (`**teks**`).
2. Konversi teks markdown tersebut menjadi HTML dengan parser.
3. Bungkus HTML dalam tag dasar HTML lengkap dengan CSS global (rekomendasi: font Arial, 11pt, line-height 1.6, marjin paragraf rapi).
4. Unggah dengan Drive API `files().create()`:
   - File lokal dibaca sebagai `mimeType: "text/html"`.
   - Target berkas di Drive diset ke `mimeType: "application/vnd.google-apps.document"` agar terkonversi otomatis menjadi Google Doc.

### Pengaturan Izin Akses (Akses Publik Terbatas)
Guna memastikan berkas dibagikan untuk dibaca oleh siapa saja tanpa mengharuskan pembaca masuk/login akun Google (tapi tidak boleh membuka folder/berkas lain), set permission file ID tersebut secara spesifik:
- `role`: `'reader'`
- `type`: `'anyone'`

---

## 2. Pembuatan Versi Audio TTS (Aksen Indonesia)

Para kadang kesiswaan menyukai renungan harian berformat audio/voice note. Gunakan Microsoft Edge Neural TTS untuk suara yang natural dan berwibawa:
- **Setelan Voice**: Pastikan mesin TTS diatur pada aksen Indonesia (`id-ID-GadisNeural` untuk suara wanita yang lembut dan nyaman).
- **Perintah Konfigurasi**:
  ```bash
  hermes config set tts.edge.voice id-ID-GadisNeural
  ```

---

## 3. Sinkronisasi ke Vault Obsidian (exFAT Pitfall)

Saat menyalin berkas renungan `.md` dari `~/share/renungan/` ke basis kawruh Obsidian (`~/shorts_factory/obsidian/BukuPangestu/wiki/renungan/` yang mengarah ke `/mnt/usb-nvme` format exFAT):
* **JANGAN gunakan `shutil.copy2()`**: `copy2` mencoba menyalin atribut dan permission POSIX (`copystat`/`chmod`), yang akan memicu `PermissionError: [Errno 1] Operation not permitted` pada filesystem exFAT.
* **Gunakan `shutil.copyfile()` atau baca-tulis langsung**:
  ```python
  with open(src_path, "r", encoding="utf-8") as f_in:
      content = f_in.read()
  with open(dest_path, "w", encoding="utf-8") as f_out:
      f_out.write(content)
  ```
* **Perbarui Index**: Pastikan `Daftar Renungan.md` dan `log.md` di wiki ikut diperbarui setelah berkas disalin.
  *Catatan kagem Basa Jawi*: Menawi badhe ndamel swanten basa Jawi, gantos dadi `jv-ID-DimasNeural` (swara tiyang jaler) / `jv-ID-SitiNeural` (swara tiyang estri) rumiyin, lajeng wangsulaken dhateng `id-ID-GadisNeural` sakbibaripun:
  ```bash
  hermes config set tts.edge.voice jv-ID-DimasNeural
  # (eksekusi tts)
  hermes config set tts.edge.voice id-ID-GadisNeural
  ```
- **Eksekusi**: Jalankan `text_to_speech_ide` dengan menyuplai teks renungan yang bersih dari markup format (`*` dan `_` dihapus). Simpan hasilnya dalam format `.ogg` ke folder `/home/satyaaditech/share/renungan/` agar bisa dikirimkan langsung sebagai pesen swara (*voice bubble*) di Telegram, dan letakkan juga di server lokal kagem akses browser lumantar Tailscale/LAN.
- **Troubleshooting Timeout / Teks Panjang**: Menawi teks rerasan panjang sanget (>3000 karakter), tool `text_to_speech_ide` kepareng ngalami timeout/kegagalan. Menawi kedadosan kados mekaten, saged ngginakaken printah `edge-tts` lumantar terminal utawi python `subprocess` kanthi nyimpen teks dhateng file sawetara rumiyin:
  ```bash
  edge-tts --voice id-ID-GadisNeural --file /tmp/teks_tts.txt --write-media /home/satyaaditech/share/renungan/output.ogg
  ```
