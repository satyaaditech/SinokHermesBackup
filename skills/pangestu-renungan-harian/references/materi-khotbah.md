# Panduan Penyusunan Materi Khotbah / Ulasan Pangestu & Google Drive Integration
*Dokumen rujukan untuk tim redaksi/agen dalam menyusun bahan ceramah, presentasi, dan ulasan olahrasa.*

---

## 1. Perbedaan Mendasar dari Renungan Harian
Sangat penting untuk membedakan antara renungan harian dan materi khotbah/ulasan:

*   **Renungan Harian:**
    *   **Folder:** `~/share/renungan/`
    *   **Format:** Mengikuti format baku strictly (SABDA -> URAIAN -> PRAKTIK -> RENUNGAN -> APLIKASI).
    *   **Tujuan:** Dikirimkan ke thread 1096 Telegram.
*   **Materi Khotbah/Ulasan:**
    *   **Folder Local:** `~/share/materi_khotbah/`
    *   **Folder Drive:** Folder Google Drive bernama `"Materi Olahrasa"` (ID `1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`) dalam bentuk **Google Doc**.
    *   **Format:** Ulasan akademis/spiritual terstruktur (bukan lima seksi kaku).
    *   **Tujuan:** Digunakan untuk pidato/kotbah/rapat olahrasa secara lisan (tidak dikirimkan langsung ke thread Telegram secara otomatis).

---

## 2. Kemurnian Ajaran Pangestu (Anti-Mixing)
*   **Aturan Mutlak:** JANGAN pernah mencampurkan penjelasan ajaran spiritual Pangestu dengan filosofi atau sistem keyakinan luar (seperti Buddha/Dalai Lama, Zen, Taoisme/Wu Wei, teologi Kristen/Kenosis, tasawuf/Sufisme, dll.).
*   Penjelasan teologi harus murni bersandar pada istilah kepangestuan (Tripurusa, Suksma Kawekas, Suksma Sejati, Roh Suci).

---

## 3. Menghadirkan Makna Mendalam (Deep) & Aplikatif
Untuk menghasilkan ulasan yang bernyawa dan berbobot (*WOW*):
*   **Kedalaman Batin (Deep):** Hubungkan setiap gerakan fisik/wadag dengan keadaan spiritual batin yang sesuai ajaran kitab. Jangan sekadar menulis rujukan baris.
    *   *Zikir Napas Hu-Allah (Adeg-adeg 1):* Menarik napas “Hu” menyadari Baitullah di dalam diri, menghembuskan napas “Allah” menyelaraskan kepasrahan kepada asal-mula hidup.
    *   *Ngadeg Jejeg (Berdiri Tegak):* Keadilan Tuhan yang tegak. Ketaatan (*taat*) adalah **tongkat** penopang agar batin yang lemah tidak miring/goyah diterpa cobaan hidup.
    *   *Sedhakep (Melipat Tangan di Dada):* Tindakan fisik menindih jantung (pusat gejolak nafsu raga) untuk mewadahi karsa batin Guru Sejati dengan memadamkan nafsu kemauan (*karep*).
    *   *Tumelunging Badan (Bungkuk):* Kepala (otak/logika) sejajar dengan punggung kasar, simbol meluluhkan kesombongan intelektual di hadapan Guru Sejati, serta lambang kesetaraan segenap Roh Suci.
    *   *Sujud:* Puncak pembumian ego. Obat penawar kebanggaan rohani agar semadi tidak tersesat ing tengah marga.
    *   *Lungguh Timpuh (Duduk Simpuh):* Secara fisik menduduki/menindih organ gerak kaki (alat wadak mengejar hasrat duniawi) sebagai perwujudan menjinakkan hawa nafsu wadag agar bisa *mati sajroning urip*.
*   **Doa Verbatim Dwibahasa:** Selalu tulis doa batin asli secara utuh (tidak boleh disingkat `...`) dalam bahasa Jawa asli, diikuti terjemahan lurus bahasa Indonesia agar dipahami secara mendalam.
*   **Aplikasi Universal:** Contoh cerminan laku sehari-hari harus dapat dirasakan semua kelompok umur (bukan hanya lansia), meliputi lingkup keluarga (anak/menantu), pekerjaan (integritas, suap, kepemimpinan), dan sosial (menghalau gosip/iri, berbuat ramah/rukun).

---

---

## 4. Alur Integrasi Google Drive
Ketika pengguna meminta draf ulasan ditaruh di Google Drive dalam bentuk Google Doc:
1.  **Grup Folder:** Tempatkan di dalam folder induk bernama `"Materi Olahrasa"`.
2.  **Konversi Format:** Konversikan file `.md` ke format HTML menggunakan Python library `markdown`.
3.  **Proses Unggah/Pembaruan:**
    *   Gunakan Drive API v3 untuk `create` (jika file baru) atau `update` (jika memperbarui ulasan yang sudah ada agar ID dokumen dan link akses tetap sama).
    *   Metadata upload wajib diset `mimeType="application/vnd.google-apps.document"` agar Google Drive mengonversi file HTML otomatis menjadi Google Doc yang terformat rapi.
4.  **Pengaturan Berbagi:** Atur hak akses permission bertipe `anyone` dengan peran `reader` agar dapat diakses instan oleh siapa saja tanpa hambatan izin akses.

---

## 5. Standar Revisi 18-08-2026 (Ulasan Basa Jawi Krama Alus)

Pak Satya paring dhawuh revisi kagem materi ulasan Serat Panembah Bab 2 (contone: `~/share/materi_khotbah/ulasan_sasangka_jati_bab2_jawi_2026-08-18.md`). Punika dados standar énggal kagem ulasan ingkang badhe dipunaturaken kanthi lisan:

1.  **Basa pangantar:** Krama Alus murni (menawi dipunpundhut presentasi Jawi). Kutipan kitab tetep verbatim miturut basa aslinipun (Jawi utawi Indonesia, tanpa dipunéwahi).
2.  **Cross-reference berlapis** — pola ingkang dipunpundhut Pak Satya:
    *   Andharan → kutipan sumber utama (Sasangka Jati) → "Keterangan punika dipunandharaken langkung jero wonten ing buku X ..." + kutipan → "Langkung tebih malih ..." + kutipan sanes.
    *   Saben perangan minimal 2-3 buku sandingan (SKH, ASBS, UKK, BRSR, TKL, WSJ, SPRA) kanthi kutipan ingkang saestu kabukti wonten sumber.
3.  **Struktur:** PAMBUKA → TESIS → PERANGAN per adeg-adeg → REFLEKSI → PANUTUP; saben perangan wonten "Lampah Sadinten".
4.  **Format Google Docs:** Judul H1 (tengah), seksi H2, kutipan NORMAL_TEXT miring + indent 36pt, list angka (createParagraphBullets NUMBERED_DECIMAL_ALPHA_ROMAN), bullet (BULLET_DISC_CIRCLE_SQUARE). Tanpa simbol markdown.
5.  **Teknik unggah anyar (gantos metode HTML):** Gawé/rebuild Google Doc mawi Docs API langsung — `insertText` ing index paragraf kapisan (Drive-create doc wiwit index 1, boten 0), lajeng `updateParagraphStyle` (wajib nyakup `fields`!), `updateTextStyle`, lan `createParagraphBullets`. Referensi script: pola ing `/tmp/rebuild_doc_ulasan.py` (bisa dipunadopsi).
6.  **Ingkang boten pareng:** ngoko, tandha penthung, label versi, campuran filosofi luar (tetep kemurnian Pangestu).
