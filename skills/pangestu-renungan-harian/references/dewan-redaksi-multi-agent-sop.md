# SOP Dewan Redaksi Multi-Agent (True Multi-Agent Editorial Council)
**Standar Mutu & Panduan Operasional Resmi untuk Sinox (Hermes Agent)**

Dokumen ini adalah acuan baku (*ground truth reference*) bagi Sinox dalam memproduksi Naskah Renungan Harian Pangestu (*Renungan Penyiswaan*) berbobot mutu adiluhung, presisi secara kanonikal, dan relevan dengan problematika batin manusia modern.

---

## 1. LATAR BELAKANG & KEGAGALAN "SINGLE-AGENT ROLEPLAY"

Sebelumnya, kerap terjadi fenomena di mana satu model AI berpura-pura memerankan 4 peran (Riset, Briefing, Penulisan, Review) dalam satu obrolan chat tunggal (*theatrical single-agent roleplaying*). Praktik ini terbukti memiliki cacat mendasar:
1. **Self-Confirmation Bias**: Penulis yang mengoreksi tulisannya sendiri dalam satu konteks memori akan selalu memaklumi kelemahan logikanya sendiri.
2. **Hyper-Correction Buta**: Ketika ditegur mengenai larangan menyelipkan doa ritual, model justru menghapus salam berkah resmi kanonikal (*Satuhu*), lalu menganggap kata "doa" sebagai hal tabu tanpa memahami esensinya.
3. **Klise Dangkal & Kehilangan Ruh**: Mengganti tema layar ponsel dengan klise arisan keluarga atau menjiplak teknik mindfulness Barat (5-4-3-2-1 grounding, wheel of awareness) yang mencabut akar luhur Olahrasa Pangestu.

Untuk memastikan naskah selalu berada pada taraf **"Mahakarya Jiwa Kelas Dunia"** (sugih insight, bernyawa, menggetarkan sanubari), dibentuklah sistem **True Multi-Agent Editorial Council**.

---

## 2. ARSITEKTUR ENGINE MULTI-AGENT INDEPENDEN

Sistem dijalankan melalui script terminal resmi di Hermes:
```bash
python3 ~/.hermes/skills/pangestu-renungan-harian/scripts/hermes_editorial_council.py [--row N | --date YYYY-MM-DD]
```

Engine ini bekerja secara modular dalam 5 langkah:

```
[Google Sheet V8] 
       │
       ▼
Step 1: Deterministic Scanner & Fact/Timeline Lock
       │  (Kunci Judul dari Col G, validasi timeline 1932 vs berabad-abad, scan 7 hari)
       ▼
Step 2: Agent 1 (Writer) — Fase 1: Deliberasi Internal (<inner_deliberation>)
       │  (Verifikasi konteks & tokoh pustaka, bedhah luka batin & paradoks ego)
       ▼
Step 2: Agent 1 (Writer) — Fase 2: Penulisan Mahakarya 4-Pilar
       │  (Judul sheet, Kutipan 100% Verbatim, Laku 30 detik aplikatif, Zero kata kamu)
       ▼
Step 3: Agent 2 (Critic) — Adversarial Gatekeeper Audit
       │  (Audit dingin via Rubrik 5 Dimensi Terbobot + Hard Veto Floor)
       ▼
Step 4: Adversarial Revision Loop (Hingga Skor >= 95 & 0 Defect)
       │  (Maksimal 3 ronde koreksi bedah terarah)
       ▼
Step 5: Ecosystem Sync
          (Google Sheet V8 Col G-N, Status Menunggu ACC Manual Pak Satya,
           Arsip Markdown & Audit Dossier JSON)
```

### Penjelasan Peran:

1. **Step 1: Deterministic Scanner, Timeline Verification & Dual-Tier Blacklist**:
   - **Kepatuhan Judul Mutlak**: Judul naskah WAJIB mengambil persis dari jadwal produksi Google Sheet `Master Produksi V8` Kolom G (`Judul Rencana`). DILARANG KERAS merubah atau mengarang judul sendiri!
   - **Base Blacklist Permanen (Kesalahan Fatal Onto-Terminologis)**:
     * DILARANG KERAS menulis "Ajaran Pangestu" (yang benar adalah: "Ajaran Sang Guru Sejati". Pangestu adalah paguyuban/wadah, bukan nama ajarannya).
     * DILARANG menyebut Sang Guru Sejati dengan sebutan "beliau" (SGS adalah wujud imateriil / Utusan Suksma Kawekas).
   - **Paugeran Timeline Sejarah (Arahan Pak Satya)**:
     * Frasa seperti `"berabad-abad lampau/lalu"` atau `"ribuan tahun lalu"` MASIH BOLEH digunakan jika merujuk pada ajaran agama/filsafat dunia yang memang berusia berabad-abad (Islam, Kristen, Hinduisme, Stoikisme kuno).
     * DILARANG KERAS dialamatkan ke Ajaran Sang Guru Sejati yang diwahyukan pada 14 Februari 1932 di Surakarta kepada Bp. R. Soenarto Mertowardojo (karena usianya belum genap satu abad). AI wajib mengecek timeline objek yang dibicarakan.
   - **Dynamic Blacklist (Filter Rotasi 7 Hari — Objek Keseharian)**:
     * Objek keseharian (*ponsel, laptop, kopi, meja kerja, obrolan keluarga, dsb.*) adalah hal yang wajar (*common*) dan **TETAP BOLEH DIPAKAI**.
     * Diberlakukan jeda rotasi 7 hari: tidak boleh diulang dalam rentang 7 hari terakhir.
     * Ketika digunakan kembali setelah 7 hari, **WAJIB** disajikan dengan analogi, sudut pandang, dan konteks batin yang sama sekali **BARU** (dilarang mengulang formula lama).
   - Memastikan judul seri: `Renungan Penyiswaan`.
   - Mengunci kalimat berkah resmi penutup:
     `Semoga kita semua senantiasa berlimpah dengan sih, tuntunan, pepadang, dan pangayoman dari Sang Guru Sejati. Satuhu. 🙏`

2. **Step 2: Agent 1 (Writer: Master Educator & Sastrawan Rohani)**:
   - Proses LLM mandiri via OmniRoute (`localhost:20128`), `temperature: 0.7`, `max_tokens: 4096`.
   - **Inner Deliberation Scaffold**: Wajib merumuskan blok perenungan internal `<inner_deliberation>` sebelum menulis teks:
     * Memeriksa konteks beberapa paragraf sebelum dan sesudah kutipan dalam Pustaka Pangestu.
     * Mengetahui secara pasti siapa yang berbicara (apakah Sabda langsung SGS, atau tuturan tokoh seperti Bp. Pangrasa / Prabawa dalam BRSR).
     * Memastikan kutipan memiliki relevansi kuat sebagai solusi atas pergulatan batin pembaca.
   - Menghasilkan naskah 4-Pilar Lean Murni yang mengalir laksana percakapan sahabat seperjalanan (*kanca lumaku*), hangat, jujur, tanpa nada menggurui (zero kata "kamu"/"Anda").
   - **Kutipan Verbatim 100% No Edit No Halusinasi**: Teks Jawa asli wajib verbatim tanpa rekayasa. Terjemahan disajikan ringkas, padat arti, dan pemenggalan kalimat enak dipahami.
   - **Laku Penyiswaan Fleksibel & Aplikatif**: Langkah mikro-praktik 30 detik dibuat luas (tidak monoton kening/napas dada), yang terpenting aplikatif dan mudah dilakukan siapa saja.

3. **Step 3: Agent 2 (Critic: The Ruthless Gatekeeper)**:
   - Proses LLM terpisah secara adversarial dengan `temperature: 0.1`, `max_tokens: 2048`.
   - Menguji naskah dengan **Rubrik 5 Dimensi Terbobot (Total 100 Poin)**:
     1. *Integritas Kanonikal, Judul & Sejarah (20 Poin - VETO MUTLAK)*: Judul persis spreadsheet, kutipan 100% verbatim no-edit, atribusi tokoh valid, timeline sejarah valid, bebas "Ajaran Pangestu", salam penutup *Satuhu* utuh.
     2. *Kedalaman Wawasan & Relevansi Solusi (25 Poin)*: Kutipan benar-benar menjadi solusi atas pergulatan batin; ada *aha-moment* membongkar ilusi pikiran modern.
     3. *Keaslian Analogi & Anti-Monoton (20 Poin)*: Bebas props 7 hari, analogi segar dan membumi.
     4. *Kualitas Laku Mikro-Praktik 30 Detik (20 Poin)*: Aplikatif, luwes, dan mudah dipraktikkan.
     5. *Keindahan Bahasa & Suara Kanca Lumaku (15 Poin)*: Sudut pandang "kita", zero kata "kamu", pemenggalan terjemahan enak dipahami.
   - Mengeluarkan format JSON murni:
     ```json
     {
       "verdict": "PASS" | "REVISE",
       "score": 0-100,
       "dimension_scores": {
         "kanonikal_judul_sejarah": 20,
         "kedalaman_insight_solusi": 25,
         "keaslian_analogi": 20,
         "laku_aplikatif": 20,
         "bahasa_kanca_lumaku": 15
       },
       "defects_found": ["daftar kelemahan spesifik"],
       "surgical_revision_instructions": "instruksi konkret perbaikan"
     }
     ```

4. **Step 4: Adversarial Revision Loop**:
   - Jika status `REVISE` atau skor < 95, kritik dikembalikan ke Agent Writer untuk ditulis ulang secara paripurna hingga tuntas dan lulus standar dewan redaksi (maksimal 3 ronde).

5. **Step 5: Komit & Sinkronisasi**:
   - Memperbarui Google Sheet `Master Produksi V8` Kolom G s.d. N.
   - Kolom 15 [Status Naskah] diset ke `Menunggu ACC Manual Pak Satya` (atau mempertahankan status `ACC` bila sebelumnya telah disetujui Pak Satya).
   - Menyimpan arsip naskah ke `/home/satyaaditech/share/renungan/[date]_[slug].md`.
   - Menyimpan berkas audit ke `/home/satyaaditech/share/renungan/[date]_audit_dossier.json`.

---

## 3. PENGAMANAN BERLAPIS (5-LAYER DEFENSE IN DEPTH)

Untuk mencegah kebocoran halusinasi, disiplin palsu, dan naskah dangkal:

1. **Layer 1: Deterministic Scripture Injection**:
   - Bagian I (KUTIPAN TUNTUNAN) diinjeksi secara deterministik oleh kode Python dari sumber kanonikal sah. LLM sama sekali dilarang memparafrasekan atau merekayasa teks Sabda Jawa!
2. **Layer 2: Ground-Truth Truth Feeding to Critic**:
   - Auditor Critic diberikan teks asli Sabda Jawa dan Terjemahan. Critic dilarang keras mengarang kutipan sendiri atau menyarankan kutipan parafrase.
3. **Layer 3: Larangan Keras Psikologi Pop Murahan**:
   - Dilarang keras menggunakan jargon klise: *amygdala hijack, mode siaga tempur, affect labeling, 200 milidetik, grounding 5-4-3-2-1*.
   - Wajib membedah pergulatan batin dengan kearifan asli Pangestu: *Sabar minangka segaraning kawruh* (samudra berhati lapang yang momot, mengendapkan amarah tanpa meluap).
4. **Layer 4: Real Consensus Enforcement (Anti-Bailout)**:
   - Jika setelah 3 ronde revisi skor Critic masih < 95 atau verdict REVISE, sistem DILARANG menyatakan lulus. Status di Google Sheet wajib diset: `GAGAL AUDIT DEWAN REDAKSI` agar tidak ada naskah cacat yang lolos ke tahap produksi.
5. **Layer 5: Laku Penyiswaan Berakar Olahrasa Pangestu**:
   - Mikro-praktik 30 detik wajib aplikatif dan berakar pada Olahrasa luhur: *Eling ing napas batin (10s)*, *Sikap Samudra / Momot (10s)*, dan *Sumarah & Lerem ing Sanubari (10s)*.

---

## 4. CHECKPOINT ACC MANUAL (DISIPLIN MUTLAK)

1. Sinox menjalankan `hermes_editorial_council.py`.
2. Data hanya boleh masuk ke status `Menunggu ACC Manual Pak Satya` jika lolos konsensus mutlak (`PASS`, skor $\ge$ 95, 0 cacat).
3. Sinox melaporkan naskah lengkap dan ringkasan audit skor ke Telegram pribadi Pak Satya dan Thread 1096.
4. **🛑 STOP & DILARANG MELANJUTKAN KE RENDER AUDIO/VIDEO SEBELUM DI-ACC OLEH PAK SATYA!**
