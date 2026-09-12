# Standar Format Tabel Komparasi, Novelties, & Penerapan Laku Nyata

## 1. Struktur Wajib 4 Pilar Saben Pembaruan (Novelty)
Saben pembaruan (novelty / pergeseran paradigma) ing materi khotbah utawi ulasan wajib kasusun mawi 4 elemen pokok:

1. **Tabel Komparasi 2 Kolom**:
   - **Kolom Kiri**: *Sadèrèngipun (Tataran Syariat / Formal)* — Nggambaraken pamahaman umum/lahiriah/padintenan kanthi tuladha nyata tanpa nyacad agami sanès.
   - **Kolom Tengen**: *Sang Guru Sejati (Tataran Kasampurnan)* — Nggambaraken pamawas kasampurnan ingkang langkung jero, luhur, lan murni.
2. **Deep Insight (Wawasan Kasunyatan)**:
   - Dudutan teologis-ontologis batiniah ingkang jero nanging gampil dipun-tampi nalar.
3. **Laku Padintenan (Praktik Nyata Sehari-hari)**:
   - Protokol langkah operasional konkrit ing kulawarga, pakaryan/bisnis, bebrayan agung, lan olah batin supados boten mandheg ing téori kémawon.
4. **Pethikan Sabda Suci (100% Verbatim)**:
   - Kutipan sabda kanonikal (SSJ, BRSR, TKL, SKH, UUJM) tanpa owah-owahan tembung babar pisan.
   - **STRICT ANTI-PARAPHRASE GUARD**: Dilarang nyampurake ukara sintesis, panyuraos panulis, utawa parafrase ing salebeting tanda pethik / kutipan. Kutipan kedah 100% karakter-mbaka-karakter cocog kaliyan berkas babon asli (`buku_ssj_jawa.txt`, `buku_brsr.txt`, lsp).
   - Format: **Bold Italic** (`#1B365D`) tumrap sabda, lan **Bold Only** (`#0E4A6F`) tumrap sumber kanonikal.

---

## 2. Aturan Tegas Tabel Natif (Native Table Rule)

### A. Wonten ing Presentasi Web (HTML5 Deck)
- **DILARANG** nggantos tabel mawi format kartu (`div class="grid..."` utawi `div class="flex..."`) nalika format tabel dipun-suwun dening pangguna.
- **WAJIB** ngginakaken elemen tabel HTML baku (`<table class="...">`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`).
- **Garis Pembatas (Border)**: Wajib gadhah garis tabel ingkang tegas (misal `border-2 border-gold/40`), header kontras (`<th>` Slate vs Gold), lan werna sèl ingkang cetha dipun-waos.

### B. Wonten ing Google Docs
- **DILARANG** namung ngandelaken konversi markdown biasa ingkang ngowahi tabel dados teks katitik (bullet list / formatted text).
- **WAJIB** ngasilaken elemen tabel Google Docs sejati (`insertTable` request via Google Docs API) kanthi sel-sel ingkang kapisah lan karesikan layout ingkang rapi.

---

## 3. Strict Verbatim Anti-Paraphrase Quality Gate

### A. Prinsip Kemurnian Sabda 100% Verbatim
- Saben pethikan ingkang dipun-tandhani minangka kutipan sabda suci utawi wejangan **DILARANG KASARANA PARAFRASE UTAWI DUDUTAN RINGKES**.
- Teks ingkang dipun-kutip wajib awujud **exact character-for-character substring match** saking berkas master kanonikal (`/home/satyaaditech/share/pangestu_studi/buku_ssj_jawa.txt`, `buku_brsr.txt`, `buku_skh.txt`, `buku_tkl.txt`, `buku_uujm.txt`).
- Menawi namung awujud sintesis / dudutan panyuraos, **DILARANG** dipun-paringi tanda kutip sabda suci utawi dipun-klaim minangka sabda verbatim; kedah dipun-lebetaken dhateng kolom Deep Insight utawi Uraian.

### B. Daftar Pitfall & Tuntunan Koreksi Verbatim
| Tema | ❌ Pitfall Sintesis / Parafrase (DILARANG) | ✅ Teks Asli Verbatim 100% (WAJIB) | Sumber Kanonikal |
| :--- | :--- | :--- | :--- |
| **Pasemon Impen** | *"Panembah iku wancine jiwa wungu saka nendraning kadonyan, sowan ing ngarsaning Gusti Kang Maha Suci"* | *"Dene kahanane kaya dene wong ‘turu’ kang ngimpi nggladrah, maneka warna solan-salin panandhang kang rinasa ing sajroning impen (sajroning alam antara) manut apa kang diimpi-impi lan kang dipengini lan tansah nyawang (ketok-ketoken) apa kang ditresnani. Sirnaning panandhang sajroning impen manawa kang ‘turu’ (lali) mau banjur tangi, tegese Jiwa nuli eling marang Allah."* | BRSR Bab I (Bab Alam Antara) |
| **Kabutuhaning Kawula** | *"Awit Panjenengane iku ora kagungan kaperluan apa-apa marang panembahing kawula... yen panembah iku dudu kaperluane Gusti..."* | *"Panembahing kawula marang Pangeran (Suksma Kawekas), iku satuhune dudu pakoning Pangeran, tegese: Pangeran ora mundhut disembah-sembah para kawulane, sarana tembung panglingga murda, utawa puji pangalembana lan sapanunggalane, amarga sanadyan ora dipuji-puji lan dialembana, Pangeran iku sejatine pancen wus Mahaluhur lan Mahaagung... mulane panembah iku sejatine iya mung dadi kuwajibaning kawula lan uga dadi kabutuhaning para kawula dhewe..."* | SSJ Panembah Bab 1 Adeg 3 |
| **Sang Patih & Sang Nata** | *"ora beda karo sawijining Patih kang arep ngabekti marang Ratune, nanging mung ngadhep gambare bae..."* | *"...kaya upamane Sang Patih kang manembah Sang Ratu ana ing dalem kadhatoning Sang Nata. Terange: Pangeran lan Ingsun (Suksma Kawekas lan Suksma Sejati) wus dumunung aneng kang padha manembah utawa nunggal kalawan Roh Sucine, dadi panembahe mau kaya pepindhane sapatemoning Sang Patih lan Sang Nata, ing dalem kadhatoning Ratu..."* | SSJ Panembah Bab 5 Adeg 3 |
| **Pasabinan Batin** | *"Lebure dosa iku kudu sarana ngolah pasabinan batin... lukune rila..."* | *"...kaya upamane sawah, kang kudu diolah manut samesthine, kayata: digaru, diluku, dirabuk, lan dioncori banyu, supaya wiji kang dhinedher (disebar), bisa thukul kalawan subur lan ngetokake asil kang mikuwati uripe. Dene kang minangka lukune iku rila, garune temen, rabuke sabar lan narima, lan banyu kang minangka siramane, yaiku: eling, pracaya, mituhu..."* | SSJ Sangkan Paran Bab 4 |
| **Panalangsa Satriyatama** | *"Panalangsa iku jumeneng dadi watak satriyatama, yaiku wani ngakoni kliruning lakune..."* | *"...iku kalebu utama, awit iku saperangan saka wataking satriyatama; aja kaya si cubluk kang mbaguguk nguthawaton, yen dielingake kleruning tindak-tanduke lan kesalahane banjur briga-brigi kumaki, abandha wani muni-muni, wekasan kaesi-esi ing bumi."* | BRSR Bab XIV |

---

## 4. Peta 10 Pembaruan Hakiki Sang Guru Sejati
1. **Pembaruan 1: Hakikat Sesuluh & Teken** (Purwaka & Dalan Rahayu Bab 2 Adeg 3) — Ngurmati kamardikaning pamikir.
2. **Pembaruan 2: Wulang Wuruk Dhiri** (Panembah Bab 1 Adeg 3 & Bab 5 Adeg 1) — Kabutuhaning kawula & auto-edukasi jiwa.
3. **Pembaruan 3: Padaleman ing Sanubari** (Panembah Bab 5 Adeg 3) — Desakralisasi ruang fisik; pasemon Sang Patih.
4. **Pembaruan 4: 7 Kamar Batin & 3 Warana** (Panembah Bab 5 Adeg 3) — Peta 1–4 Napsu, 5–7 Padalemaning Gusti mawi kori Cipta, Nalar, Maya.
5. **Pembaruan 5: Sesuci Batin & Wewangian Sejati** (Panembah Bab 5 Adeg 2) — Resiking ati saka napsu; wewangian yaiku Budi Darma.
6. **Pembaruan 6: Sasmita 6 Sikap Fisik** (Panembah Bab 2 Adeg 1–3) — Nyirep 4 anasir & napsu: Kiyam (Siti), Ruku (Latu), Sujud (Toya), Tahiyat (Swasana), Salam (Budi Darma).
7. **Pembaruan 7: Penataan Wanci Miturut Jiwa** (Panembah Bab 2 Adeg 2 & Bab 5 Adeg 1) — Mudha (2 wanci), Diwasa/Sepuh (3 wanci) kanggé nenangi elingan & kalantipan.
8. **Pembaruan 8: Undha-Usuking Panembah** (Panembah Bab 3 & 4) — Panembahing Rasa (Sila Tumpuk) & Sukma (Suku Tunggal / Luluh nunggal saedhat).
9. **Pembaruan 9: Living Worship (24 Jam)** (Panembah Bab 5 Adeg 1) — Ambadan eling; makarya temen lan resik minangka panembah nyata.
10. **Pembaruan 10: Pasabinan Batin & Panalangsa** (SSJ Sangkan Paran Bab 4 & BRSR XIV) — Olah sawah batin (Luku, Garu, Rabuk, Banyu) & watak satriyatama.
