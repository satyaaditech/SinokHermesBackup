# Arsitektur Web Portal Pustaka & Admin Kontemplasi

## 1. Lingkungan & Akses
* **Website Publik**: `https://kontemplasi.satyaaditech.web.id` (GitHub Pages, statis tanpa backend server).
* **Admin Portal**: Server lokal `admin_server.py` pada port `8088` (Systemd: `kontemplasi-admin.service`).
* **Akses Admin Jaringan**: Hanya melalui jaringan Tailscale `http://100.92.237.45:8088` (atau LAN WiFi `http://192.168.0.113:8088`).
* **Kebijakan Keamanan & PIN**: Dilarang mengekspos PIN/password di README, repositori publik, atau pesan chat. Admin Dashboard langsung terbuka bebas login karena sudah diamankan oleh jaringan privat Tailscale.

## 2. 4 Kategori Konten
Portal mengelompokkan materi menjadi 4 kategori:
1. `🌅 Renungan Harian` (`renungan-harian`): Format baku harian (Sabda Suci, Uraian, Praktik, Aplikasi Batin).
2. `✍️ Esai Kontemplasi` (`esai-kontemplasi`): Tulisan panyuraos panjang, kajian tematik mendalam.
3. `👥 Reader’s Voice` (`readers-voice`): Kiriman kesaksian, pengalaman nyata laku batin dari para kadang pembaca.
4. `📜 Ulasan Serat` (`ulasan-serat`): Bedah teks serat piwulang (Sasangka Jati, BRSR, TKL, SKH, UUJM, dll).

## 3. Metadata YAML Frontmatter
Setiap berkas markdown di `renungan/` mendukung metadata:
```yaml
---
title: "Sesirah Tulisan"
date: 2026-09-07
status: published # published | draft | unpublished
category: readers-voice # renungan-harian | esai-kontemplasi | readers-voice | ulasan-serat
author: "Bambang Sutrisno" # Nama kontributor / panyerat
tags: ['kontemplasi', 'bahasa-indonesia', 'sang-guru-sejati']
language: id # id | jv | en
---
```

## 4. Alur Kurasi Mandhiri (Editor-in-Chief)
1. Kiriman naskah pembaca otomatis masuk sebagai `status: draft` dengan kategori `readers-voice`.
2. Admin (Pak Satya) mengkurasi naskah di Admin Editor, menyesuaikan tata bahasa dan melaraskan dengan piwulang luhur.
3. Ubah status menjadi `status: published` dan klik tombol **"🚀 Terbitkan ke Website"** (menjalankan `sync_to_github.sh`).

## 5. Fitur Tabel & Pengurutan (Sorting)
* **Default Sort**: Tanggal dari yang terbaru ke terlama (`sortKey='date'`, `sortAsc=false`).
* **Sortable Columns**: Status, Kategori, Tanggal, Judul/Penulis, Bahasa, Media, Google Doc.
* **Indikator Visual**: `▲` (ascending), `▼` (descending), `⇅` (kolom tidak aktif).

## 6. Pitfall Pengembangan UI & Python f-string
* Saat script Python meng-generate HTML + inline JavaScript, hindari konflik kurung kurawal f-string. Gunakan double braces `{{` dan `}}` untuk seluruh blok JS.
* Verifikasi sintaks JS luaran sebelum commit/push dengan `node -c` atau script runner agar tidak memicu JS SyntaxError yang membuat grid artikel blank.
