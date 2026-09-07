# Pustaka Digital Web Library (kontemplasi.satyaaditech.web.id)

Dokumentasi arsitektur dan aturan pembentukan Web Library Renungan Penyiswaan berbasis GitHub Pages, Cloudflare CNAME, dan Portal Admin Lokal.

## 1. Arsitektur & Jalur File
*   **Sumber Renungan Lokal**: `/home/satyaaditech/share/renungan/` & `/home/satyaaditech/kontemplasi/renungan/` (berkas `.md`, poster, audio).
*   **Repo GitHub Target**: `/home/satyaaditech/kontemplasi/` (`satyaaditech/kontemplasi` -> branch `main`).
*   **Domain Publik**: `https://kontemplasi.satyaaditech.web.id/` (Cloudflare CNAME `kontemplasi` -> `satyaaditech.github.io`).
*   **Server Intranet Port 8000**: `http://192.168.0.113:8000/pustaka/` & `http://100.92.237.45:8000/pustaka/`.
*   **Skrip Sinkronisasi Cepat**: `/home/satyaaditech/kontemplasi/sync_to_github.sh`.

## 2. Portal Admin (`kontemplasi-admin.service`)
*   **Service**: `kontemplasi-admin.service` (Systemd User, port `8088`).
*   **Akses Lokal**: `http://192.168.0.113:8088` (Tailscale: `http://100.92.237.45:8088`).
*   **PIN Akses**: `1949` *(Tahun Sabda Pangestu)*.
*   **Fitur Status Publikasi**:
    *   `published`: Terbit otomatis ke static `index.html` dan live di GitHub Pages.
    *   `draft`: Disimpan di server dan terlihat di dashboard admin, dilewati dari build publik.
    *   `unpublished`: Diarsipkan dari web publik tanpa menghapus berkas naskah.
    *   Tersimpan pada YAML frontmatter markdown: `status: published | draft | unpublished`.
*   **Fitur-Fitur Utama**:
    1. Manajemen Daftar Renungan dengan filter status cepat (`Semua`, `Published`, `Draft`, `Unpublished`).
    2. Pambesut Naskah (*Editor*) berdampingan dengan Live Preview HTML.
    3. Unggah Media (*Drag & Drop*) untuk poster infografis dan rekaman audio.
    4. Tombol 1-Click Deploy (`🚀 Terbitkan ke Website`) untuk sinkronisasi dan build ulang otomatis.

## 3. Aturan Tampilan & Katalog (UI/UX)
1.  **Deduplikasi Cerdas (1 Card per Materi)**:
    *   Jika satu materi memiliki varian bahasa (misal `renungan-mengampuni-ind-2026-09-07.md` dan `renungan-mengampuni-eng-2026-09-07.md`) atau revisi draf, hanya tampilkan **1 kartu tunggal** di katalog.
    *   Sematkan pill bahasa pada kartu (`ID`, `ENG`, `JAWA`).
    *   Di dalam reader modal, sediakan tab switcher bahasa (`🇮🇩 Indonesia`, `ꦗꦮ Basa Jawi`, `🇬🇧 English`) agar pembaca bisa berpindah versi secara instan.
2.  **Urutan Kronologis Mundur (Strict Reverse Chronological)**:
    *   Sortir renungan wajib dari tanggal paling akhir/terkini (paling atas) ke tanggal paling lama (paling bawah).
3.  **Sanitasi Total Karakter Markdown**:
    *   Judul, tanggal, kutipan sabda, dan tags pada kartu depan wajib dibersihkan dari karakter `*`, `#`, `_`, `~`, dan backtick.
4.  **Aturan Ketat Pencocokan Poster (Strict Matching Pitfall)**:
    *   **HANYA** tampilkan poster/infografis jika berkas gambar tersebut adalah infografis/poster beresolusi tinggi asli (misal `poster-*.jpg`, `infografis-*.png`, `newsletter-*.png`) yang cocok eksak dengan tema & tanggal.
    *   **JANGAN PERNAH** memetakan berkas `cover-*.png` (sampul kotak audio) sebagai poster hero. Jika artikel tidak memiliki infografis, biarkan `poster: ""` dan jangan tampilkan badge poster.
5.  **Default Theme**:
    *   Gunakan **Light Mode** sebagai tema baku demi kenyamanan membaca panjang dan perpaduan mulus dengan infografis latar terang.
