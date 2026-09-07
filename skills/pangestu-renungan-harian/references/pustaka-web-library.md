# Pustaka Web Library (`kontemplasi.satyaaditech.web.id` & `/pustaka/`)

## 1. Arsitektur & Lingkungan
* **Lokasi Lokal**: `/home/satyaaditech/share/pustaka/`
* **Akses Lokal / LAN**: `http://192.168.0.113:8000/pustaka/` (di-serve oleh `share_server.py` port 8000)
* **Akses Cloudflare / Custom Domain**: `https://kontemplasi.satyaaditech.web.id` (via GitHub Pages `satyaaditech.github.io` / repo `kontemplasi`)
* **Zero Overhead**: Beban RAM 0 MB, CPU Idle 0% (karena berupa static single page application client-side).

## 2. Pengelolaan Poster / Infografis
* Poster infografis (seperti `poster-*.jpg`, `infografis-*.png`, `cover-*.png` di `~/share/renungan/`) otomatis dideteksi dan di-link ke renungan terkait berdasarkan tanggal atau stem nama berkas.
* **Tampilan Seamless**:
  * Jika renungan memiliki poster/infografis: Tampil lencana `🖼️ Poster` di kartu depan, dan saat dibuka (Reader View), poster tampil di bagian atas dengan bingkai elegan serta fitur **Lightbox Zoom** (klik untuk memperbesar resolusi penuh).
  * Jika renungan TIDAK memiliki poster: Layout otomatis runtut dan rapi tanpa ada kotak kosong atau broken image.

## 3. Alur Pembaruan Otomatis (Build Script)
Setiap selesai menyusun atau memperbarui renungan harian baru di `~/share/renungan/`:
1. Jalankan generator:
   ```bash
   python3 /home/satyaaditech/share/pustaka/build_pustaka.py
   ```
2. Waktu eksekusi hanya ~0.15 detik.
3. Sinkronisasi ke repository GitHub Pages jika diaktifkan:
   ```bash
   git add . && git commit -m "Update renungan $(date +%F)" && git push
   ```
