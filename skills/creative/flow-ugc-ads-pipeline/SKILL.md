---
name: flow-ugc-ads-pipeline
description: "Use when creating multi-shot UGC affiliate ads in Flow."
version: 1.0.0
author: Sinox Agent
license: MIT
metadata:
  hermes:
    tags: [ugc, flow-ugc-ads, google-flow, veo, affiliate-video]
    category: creative
---

# Google Flow UGC Ad Production Pipeline

Menghasilkan paket produksi lengkap untuk iklan video UGC multi-shot di Google Flow berdasarkan standar riset Claude UGC & 15-Angle Conversion Matrix.

## Standar Output 6-Blok (Production-Ready Package)

Setiap permintaan pembuatan naskah UGC Google Flow WAJIB menghasilkan 6 modul terstruktur berikut:

### Blok 0: Persiapan & Sanitasi Aset (Pre-Flight Inspection)
1. **Character Sheet Sanitization**:
   - DILARANG mengunggah seluruh lembar *character reference sheet* (kolase/grid yang berisi banyak pose, teks, atau ekspresi) ke dalam Google Flow.
   - Perintahkan user untuk meng-*crop* satu foto wajah/setengah badan utama yang bersih dan simpan sebagai `creator.png` (`@Creator`).
2. **Multi-Angle Product Separation**:
   - DILARANG menggabungkan sudut produk (depan, belakang, detail) ke dalam 1 gambar grid.
   - Pisahkan menjadi file bersih tersendiri: `@Product_Front`, `@Product_Back`, `@Product_Detail`.
   - Filter dan buang foto referensi produk yang memiliki warna lampu berbeda atau model orang lain di latar belakang.
3. **Contextual Wardrobe & Hairstyle Override**:
   - Ubah pakaian kasual bawaan avatar (misal tank top & jeans) menjadi pakaian yang relevan dengan produk (misal setelan olahraga), dan sesuaikan gaya rambut (misal kuncir ponytail longgar untuk adegan aktif/olahraga).

### Blok 1: Shot List 5-Babak (atau 3-Babak) Terstruktur
Format konversi direct-response:
* **Shot 1 (Hook / Empathy)**: Membangun suasana, menunjukkan masalah/kebutuhan.
* **Shot 2 (Product Reveal & Core Feature)**: Memperkenalkan produk, mengisi 30–40% frame.
* **Shot 3 (Use Case A / Comfort & Ease)**: Demonstrasi penggunaan santai atau fitur kenyamanan.
* **Shot 4 (Use Case B / High Performance & Efficiency)**: Demonstrasi penggunaan intensitas tinggi atau efisiensi.
* **Shot 5 (Payoff & Call to Action)**: Kepuasan hasil, gestur ramah, dan ajakan checkout ke keranjang belanja.

### Blok 2: Prompt Granular Per-Shot Bertagging Aset
* Menyertakan tag eksplisit (`creator.png`, `product-front.jpg`, dll.).
* Menggunakan instruksi visual *Anti-Cinematic Realism* (handheld camera, candid, pencahayaan alami jendela/ruangan, tekstur kulit berpori alami).
* Pacing dialog: Maksimal 12–16 kata per durasi 8–10 detik. Dialog dalam format Sentence case.

### Blok 3: Instruksi Briefing Agent Mode (1-Click Tempel)
* Blok naskah konsolidasi yang mencakup Master Lock dan urutan seluruh shot untuk dieksekusi sekali jalan di Agent Mode (`Confirm before generating: Never`).

### Blok 4: Skrip Voiceover ElevenLabs Terpisah
* Skrip dialog bersih tanpa tag visual untuk dubbing audio terpisah.
* Preset parameter ElevenLabs: `Stability: 0.5, Similarity: 0.75, Style: 0.3`.
* Rekomendasi penyatuan audio VO + klip visual Flow di CapCut.

### Blok 5: Catatan Produksi & Mitigasi Glitch (Risk Warnings)
* Identifikasi shot berisiko tinggi (misal: gerakan kaki cepat, tampilan angka/teks pada layar elektronik yang rawan glitch).
* Prinsip efisiensi: *"Mengubah dialog gratis, sedangkan regenerasi klip memakan kredit."*
* **Surgical Revision Rule**: Jika ada revisi pada satu scene tertentu, hanya generate ulang scene yang bermasalah tersebut, jangan generate ulang seluruh 5 shot.
