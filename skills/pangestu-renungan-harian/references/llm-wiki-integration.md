# Integrasi LLM Wiki kagem Buku Pangestu

Dokumen punika ngatur tata cara integrasi sarta manajemen basis kawruh (LLM Wiki) Buku Pangestu wonten ing folder Obsidian `/home/satyaaditech/shorts_factory/obsidian/BukuPangestu/`.

---

## 1. Direktori Vault Buku Pangestu
*   `books/`: Panggonan kitab-kitab utama Pangestu ingkang aslinipun permanen lan mboten saged dipun-ewahi (*immutable sources*).
*   `wiki/`: Kaca ringkesan, ulasan, sarta konsep-konsep piwulang Pangestu ingkang saling terhubung mawi `[[wikilinks]]`.
*   `wiki/renungan/`: Cathetan renungan harian padintenan ingkang sampun di-ingest lan dipun-hubungaken otomatis kaliyan konsep utama.
*   `raw/`: Folder *staging* kagem masang data mentah saderengipun dipun-proses.
*   `archive/`: Folder panyimpenan berkas mentah sasampunipun rampung dipun-ingest kagem nyegah pengulangan maos data.

---

## 2. Watak Utama / Konsep Piwulang wejang
Saben istilah kautaman punika kedah dipun-pranalakaken mawi `[[Wikilinks]]` wonten ing cathetan renungan:
- **Tri Sila**: `[[Eling]]`, `[[Pracaya]]`, `[[Mituhu]]`, `[[Panembah]]`
- **Panca Sila (Watak Utama)**: `[[Rila]]` / `[[Rela]]`, `[[Narima]]`, `[[Jujur]]`, `[[Sabar]]`, `[[Budi Luhur]]`
- **Struktur Kejiwaan**: `[[Tripurusa]]`, `[[Suksma Kawekas]]`, `[[Suksma Sejati]]`, `[[Roh Suci]]`, `[[Jiwa]]`, `[[Candrajiwa]]`
- **Pedoman Tindakan**: `[[Dalan Rahayu]]`, `[[Paliwara]]`

---

## 3. Workflow Ingest Renungan Harian
Nalika nindakaken *ingest* renungan anyar saking folder `~/share/renungan/` utawi folder input sanesipun:
1.  Waos teks renungan lan temokaken tanggal sarta basa (Jawi `jv`, Indonesia `id`, Inggris `en`).
2.  Babaraken YAML frontmatter ing nginggil berkas:
    ```yaml
    ---
    title: "Judul Renungan"
    date: YYYY-MM-DD
    tags: [renungan, bahasa-indonesia, sabar, lsp]
    language: id/jv/en
    ---
    ```
3.  Lakukan pemindaian kata kunci (Regex) dhumateng isi renungan kagem dipun-pasangi `[[wikilinks]]` dhumateng konsep utama.
4.  Tulis berkas enggal dhateng `wiki/renungan/`.
5.  Mutakhiraken `wiki/Daftar Renungan.md` kagem ngurutaken renungan kanthi kronologis.
6.  Serat log panyetelan wonten ing `wiki/log.md`.
