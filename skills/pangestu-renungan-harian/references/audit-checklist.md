# Audit Checklist — Editor Daily Bread

Gunakan checklist ini saat mengaudit draft renungan Writer.
Urutan: cek struktur dulu → cek konten → cek nada → cek aturan.

---

## 🔴 Struktur (wajib lengkap — tidak boleh ada blok hilang)

- [ ] Judul diapit 2 emoji yang sesuai tema (contoh: 🧺 *Judul* 🧺)
- [ ] Salam: _Salam Bahagia Bp/Ibu/Sdr semuanya,_ (italic, koma, tanpa seru)
- [ ] 📖 SABDA HARI INI — format: Buku [nama], _\"*sabda*\"_
- [ ] 💭 URAIAN — naratif + kisah nyata + 1 quote pendukung
- [ ] 🧘 PRAKTIK — langkah bernomor, bisa dikerjakan pembaca awam
- [ ] 🎯 RENUNGAN — SATU baris aforisme
- [ ] 📝 APLIKASI — 3 pertanyaan bernomor, introspektif, bukan basa-basi
- [ ] Penutup — "Semoga kita ... Satuhu 🙏"
- [ ] 🔴 Word count: jalankan `wc -w`, target 300–400 kata, batas keras 450 kata (≤3 menit @150wpm). Jika >450, tandai ⚠️ PANJANG di verdict.

---

## 🟡 Konten (substansi — ini yang membedakan bagus/biasa)

### Sabda
- [ ] **🔴 DILARANG KERAS MENYISIPKAN PIKIRAN SENDIRI DALAM KUTIPAN**: Kutipan Sabda/buku referensi wajib 100% murni verbatim apa adanya. Tidak boleh ada satu kata, frasa, sintesis kesimpulan, atau kalimat buatan sendiri yang disisipkan ke dalam blok kutipan/Sabda. Pemahaman, uraian, dan interpretasi HANYA boleh ditulis pada bagian URAIAN/PEMBAHASAN terpisah.
- [ ] Quote spesifik ke tema, bukan generik menyebut tema sekilas
- [ ] Jika tema narima, Sabda harus tentang narima — bukan "Panca Sila secara umum"
- [ ] Ada quote pendukung di tengah uraian (cross-reference)
- [ ] Sumber buku disebut jelas dan tepat sesuai katalog resmi (TKL = **Taman Kamulyan Langgeng**, bukan nama fiktif/singkatan yang salah seperti Tutur Kelem; SSJ = Sasangka Jati; SKH = Sabda Khusus; BRSR = Bawa Raos Ing Salebeting Raos; ASBS = Arsip Sarjana Budi Santosa; UKK = Ulasan Kang Kelana; WSJ = Wahyu Sasangka Jati; UUJM = Ular-Ular Juru Mengeti).
- [ ] **🔴 Sabda VERBATIM dari SATU paragraf utuh** — jangan menyambung fragmen dari paragraf berbeda dengan "...", karena itu cherry-picking yang mendistorsi struktur asli meskipun setiap kata nyata. Cek lokasi sumber di `references/sumber-quickref.md`.
- [ ] **Setiap `...` dalam Sabda harus ada di sumber asli** — ellipsis hanya boleh jika memang ada di paragraf sumber yang sama (menandakan teks asli memang bersambung), BUKAN untuk menyambung paragraf berbeda.

### Kisah Nyata
- [ ] Fakta dasar terverifikasi (nama, tahun, tempat — jangan halusinasi)
- [ ] **Detail medis/penyakit/sakit:** jangan mengarang organ mana yang rusak atau di mana penyakit diderita. Jika tidak yakin, gunakan istilah umum ("kesehatannya", "fisiknya"), BUKAN spesifik ("paru-parunya", "ginjalnya"). Contoh salah: "debu kapur Robben Island merusak paru-paru Mandela" → fakta: kerusakan terjadi di tear ducts, TB di Pollsmoor (1988), bukan Robben Island. Lebih aman: "debu putih merusak kesehatannya."
- [ ] Kisah BENAR-BENAR menggambarkan tema — bukan sekadar inspiring tapi beda makna
- [ ] Contoh salah: Hawking untuk narima → lebih ke overcoming limitation, bukan narima
- [ ] Contoh benar: Jiro Ono untuk narima → menerima 10 kursi, tidak iri, tetap bekerja
- [ ] Hindari kisah yang sudah dipakai di renungan sebelumnya

### Uraian
- [ ] Pembuka: hook relatable (tetangga beli mobil, teman promosi, dsb.)
- [ ] Menerjemahkan Sabda abstrak ke bahasa sehari-hari
- [ ] Tidak terlalu panjang/teoretis — pembaca awam harus bisaikuti
- [ ] Mengalir alami dari Sabda → kisah nyata → refleksi
- [ ] 🔴 SEMUA quote di tengah uraian pakai format bold-italic: `_\"*teks*\"_` — jangan hanya italic `_\"teks\"_` (Writer sering lupa, sudah terjadi 4× di draft Sabar Ronde 1)

### Praktik
- [ ] Bisa dikerjakan pembaca awam, bukan cuma siswa senior
- [ ] Ada durasi jelas (7 hari, 5 menit/hari, dsb.)
- [ ] Ada langkah konkret, bukan instruksi abstrak ("renungkan" tanpa panduan)
- [ ] Ada verifikasi mandiri (hari ke-7 bandingkan dengan hari pertama)

### Renungan (Aforisme)
- [ ] SATU baris, bukan dua
- [ ] Padat, menusuk, quotable
- [ ] Bukan pengulangan judul atau ringkasan uraian

### Aplikasi
- [ ] 3 pertanyaan benar-benar introspektif
- [ ] Bukan pertanyaan yang jawabannya "ya/tidak" doang
- [ ] Menggali lebih dalam dari sekadar permukaan

---

## 🟢 Nada & Persona

- [ ] Praktisi kejiwaan — insight pengalaman, bukan menggurui
- [ ] Akrab tapi hormat — pakai "Anda"/"Kita", ZERO "kamu"
- [ ] Hangat bukan sentimental, praktis bukan teoretis
- [ ] Tidak ada kalimat menggurui ("Anda harus...", "Janganlah Anda...")
- [ ] Tidak ada jargon spiritual berlebihan yang bikin pembaca awam ilfeel

---

## 🔵 Aturan Teknis

- [ ] Semua quote di tengah uraian: italic (_\"...\"_)
- [ ] Sabda dalam Sabda blok: bold dalam italic (_\"*sabda*\"_)
- [ ] Tidak ada kata "kamu" di SELURUH teks
- [ ] Sumber ajaran = Sang Guru Sejati, bukan "Buku Sasangka Jati mengajarkan"
- [ ] "Buku Sasangka Jati" hanya sebagai referensi fisik/kitab
- [ ] Output dalam SATU code block (agar markup WA aman di Telegram)
- [ ] Tidak ada emoji di akhir Sabda (biarkan Sabda murni)
