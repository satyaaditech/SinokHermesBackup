# Arsitektur Web Pustaka & Admin Portal Kontemplasi

Dokumentasi arsitektur portal publik, dashboard admin, dan integrasi remote storage untuk publikasi renungan serta kajian Pangestu.

## 1. Portal Publik (`https://kontemplasi.satyaaditech.web.id`)
* **Hosting & Deployment**: GitHub Pages (`satyaaditech/kontemplasi`), CNAME Cloudflare `kontemplasi.satyaaditech.web.id`.
* **Generator Static Site**: `/home/satyaaditech/kontemplasi/build_pustaka.py`.
* **Kategori Konten (4 Tab)**:
  1. `renungan-harian` (🌅 Renungan Harian)
  2. `esai-kontemplasi` (✍️ Esai Kontemplasi)
  3. `readers-voice` (👥 Reader’s Voice)
  4. `ulasan-serat` (📜 Ulasan Serat)
* **Fitur & Interaksi Web**:
  - **Direct Deep-Link Sharing**: Setiap artikel memiliki hash URL unik (contoh: `#renungan-kamardikan-2026-08-17`). Saat URL dibuka, website otomatis mendeteksi hash dan langsung membuka jendela baca (*modal reader*) artikel tersebut.
  - **Tombol `🔗 Bagikan`**: Menggunakan Web Share API (`navigator.share`) di perangkat mobile/macOS untuk membuka share drawer natif, atau fallback menyalin link langsung ke clipboard.
  - **Tombol `📋 Salin WA`**: Menyalin format WhatsApp bersih tanpa markup rusak.
  - **Multi-bahasa per Materi**: Tab ID / JV / EN di dalam modal reader.
  - **Lightbox Infografis**: Klik poster untuk zoom resolusi penuh.
* **Wajib Footer Link**:
  Setiap renungan harian yang diterbitkan wajib menyertakan baris teks berikut:
  `Untuk kumpulan kontemplasi lainnya bisa diakses di https://kontemplasi.satyaaditech.web.id`

---

## 2. Admin Portal (`http://100.92.237.45:8088`)
* **Akses Jaringan**: Khusus jaringan privat Tailscale (`100.92.237.45:8088`) dan LAN lokal (`192.168.0.113:8088`).
* **Autentikasi**: **Tanpa PIN/Password prompt** (PIN dihapus demi privasi & kepraktisan, keamanan dijamin oleh perimeter Tailscale).
* **Layanan Systemd**: `~/.config/systemd/user/kontemplasi-admin.service` (`systemctl --user restart kontemplasi-admin.service`).
* **Fitur Utama Admin**:
  1. **Pre-rendered Table**: Data 50+ naskah dan metrik counter langsung di-render ke HTML server-side (*0 ms latency*).
  2. **Sorting & Filtering**: Sorting kolom tanggal (default: terbaru → terlama), judul, status, kategori, dan bahasa. Filter cepat 4 kategori dan 3 status (*Published, Draft, Unpublished*).
  3. **Menu Hapus (`🗑️ Hapus` / `POST /api/delete`)**: Hapus naskah dari tabel dan editor dengan konfirmasi dialog pengaman. Menghapus berkas dari `renungan/` dan `share/`.
  4. **Markdown Editor + Live Preview**: Edit isi naskah, ubah kategori, nama penulis, dan status artikel.
  5. **Media Upload**: Unggah poster infografis (.png/.jpg) dan audio (.mp3/.ogg) ke direktori web.
  6. **1-Click Deploy (`🚀 Terbitkan`)**: Menjalankan `sync_to_github.sh` untuk me-rebuild static site dan push ke remote GitHub.

---

## 3. Integrasi Remote Storage & Obsidian via Tailscale (SMB)
* **Samba Share**: `[ShortsFactory]` di `/home/satyaaditech/shorts_factory`.
* **macOS Finder Mount**: `smb://100.92.237.45/ShortsFactory` (Go -> Connect to Server `Cmd + K`).
* **Pitfall macOS Symlink vs Bind Mount**:
  - Protokol Samba (`smbd`) secara default memiliki `wide links = no` sehingga shortcut/symlink yang mengarah ke luar share directory (seperti `/mnt/usb-nvme`) **tidak akan muncul / diblokir** di Finder macOS.
  - **Solusi**: Gunakan `mount --bind` agar folder NVMe menjadi direktori fisik asli di dalam share:
    ```bash
    sudo mkdir -p /home/satyaaditech/shorts_factory/ObsidianVault
    sudo mount --bind /mnt/usb-nvme/obsidian /home/satyaaditech/shorts_factory/ObsidianVault
    sudo mkdir -p /home/satyaaditech/shorts_factory/NVMe_Disk
    sudo mount --bind /mnt/usb-nvme /home/satyaaditech/shorts_factory/NVMe_Disk
    sudo mkdir -p /home/satyaaditech/shorts_factory/ShareFolder
    sudo mount --bind /home/satyaaditech/share /home/satyaaditech/shorts_factory/ShareFolder
    ```
  - Bind mount didaftarkan di `crontab -l` dengan trigger `@reboot`.
* **Akses Obsidian dari MacBook**:
  - Buka Obsidian di MacBook -> Open folder as vault -> Pilih `/Volumes/ShortsFactory/ObsidianVault`.

---

## 4. Pitfall Kritis dalam Pengembangan Web & Python HTTP
1. **Server Concurrency**: Wajib menggunakan `ThreadingHTTPServer` dari modul `http.server`. Jangan gunakan `HTTPServer` standar karena bersifat single-threaded dan mudah deadlock jika browser membuka koneksi keep-alive atau melakukan concurrent fetch.
2. **Karakter Newline dalam Python String Template**:
   - Jika menulis kode JavaScript di dalam Python multiline string `""" ... """`, karakter `\n` di dalam string JS (misalnya pada `prompt('...\\n...')` atau `confirm('...\\n...')`) akan dikonversi menjadi newline mentah `0x0A` yang merusak sintaks JS (*SyntaxError: Invalid or unexpected token*).
   - **Solusi**: Wajib escape ganda menjadi `\\\\n` agar menghasilkan literal `\n` di JavaScript browser.
3. **Sinkronisasi ID DOM**:
   - Pastikan ID elemen audio pada script builder (`modalAudioPlayer`) selalu sinkron dengan tag `<audio id="modalAudioPlayer">` dan selalu sertakan guard `if (audioPlayer) audioPlayer.pause();`.
