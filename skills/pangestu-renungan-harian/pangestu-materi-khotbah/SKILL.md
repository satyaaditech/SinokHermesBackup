---
name: pangestu-materi-khotbah
description: Use when producing Pangestu khotbah/ulasan materials.
---

# Pangestu Materi Khotbah / Ulasan (Long-Form)

User (Pak Satya) gets assignments to present ulasan (e.g. Sasangka Jati chapters) for
90-minute sessions and needs deep, grounded teaching material. Distinct from
`pangestu-renungan-harian` (short daily renungan for TG thread 1096) — this class is
long-form: structure, cross-refs, wow insights, applications.

## Output contract (user's explicit standards)
- **Deep tapi membumi**: insights must be genuinely new ("wow effect" — something an
  ordinary reader wouldn't think of), but language must stay simple and grounded.
- **Urutan Kronologis Posisi**: Urutan panjelasan wonten ing ulasan/khotbah wajib runtut jumbuh kaliyan urut-urutan posisi fisik manembah nalika dipunlampahi (jejeg/takbir -> sedhakep -> sujud -> timpuh -> noleh/salam).
- **Deep Insight ing Saben Gerakan**: Saben gerakan panembah kedah dipun-paringi pamawas lebet (deep insight / wow effect) sasmita lair batinipun.
- **Cross-ref & quote menyatu inline**: every sandingan (SKH, ASBS, UKK, BRSR, TKL, SPRA)
  is woven INTO the section it supports, immediately followed by its application —
  never a detached list at the end. Utamake cross-ref saka BRSR kagem kaprigelan batin lan laku kasunyatan.
- **Contoh sehari-hari** for each big idea (analogies: HP mode jangan-gangguan, pasar
  malam batin, remote reset, akuntansi batin).
- **Purity of Pangestu canon**: NO external syncretic references (Dalai Lama, Taoism,
  Sufism, Zen rejected in past sessions). Internal cross-refs only.
- **Pendekatan Segar (Fresh Approach)**: Ulasan mengenai tema "Asal Saka Allah, Bali Marang Allah" (Sangkan Paraning Urip) tidak harus selalu dikaitkan dengan gerakan fisik panembah secara kronologis. Dapat menggunakan alur perjalanan Jiwa (analogi Aktor Teater, Siklus Batin/Mendung-Samudra, dan Mimpi Buruk/VR di Alam Antara).
- **Format Bersih Google Docs**: Saat mempublikasikan salinan ke Google Docs (misal folder 'Materi Olahrasa' `1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`), pastikan format yang diunggah berupa teks asli dokumen (tanpa simbol markdown seperti `*`, `**`, `###`). Gunakan script `md_to_doc.py` untuk mengonversinya.
- **Quota Report**: Jangan sertakan quota report di akhir respon jika user secara eksplisit memintanya dalam arahan turn tersebut.
- **Sasmita & Sangkan Paraning Urip**: Lihat panduan pemetaan sasmita gerakan panembah terhadap ajaran Sangkan Paraning Urip (BRSR Bab VIII) di `references/sasmita_sangkan_paran.md` sebagai acuan teoretis, analogi digital, dan kutipan kunci yang valid.
- Save to `~/share/materi_khotbah/ulasan_<topik>_<YYYY-MM-DD>.md`.
- Publish a Google Doc copy in Drive folder 'Materi Olahrasa' (`1Bh9ZIizra0I-3hmlqcHjhLJi3-eTAI4U`)
  via the `google-docs-publish` skill (native formatting, no markdown symbols).
- Anti-redundancy: scan `~/share/materi_khotbah/` before writing so each new piece has a
  fresh angle/metaphor (e.g. do not reuse the "tongkat ketaatan" metaphor twice).

## Workflow (proven Aug 2026: Serat Panembah Bab 2/3, Sasangka Jati Bab 2)
1. **Grab the source chapter from the Elibrary** — see `pangestu-buku-studi` skill for
   slugs + extraction; ⚠️ its notes are user-owned, re-verify quotes yourself.
   For Serat Panembah: use the JAWA file `ssj.html` (Indonesian `ssj_ind.html` does NOT
   contain Serat Panembah). Chapter map + verified cross-ref index in
   `references/serat-panembah-crossrefs.md`.
2. **Harvest cross-refs**: batch-fetch the 8 canon books (spra, skh, asbs, ukk, wsj, brsr,
   olahrasa, tkl), grep key terms (`panembah`, `sembah`, `eling`, `sasmita`, `Baitullah`,
   `luyut`), pull ±300–700 char contexts. Only quote what you actually found.
3. **Find 2–3 wow insights** nobody expects, e.g. from Sasangka Jati Bab 2:
   - panembah = "kamus sasmita" (body-language prayer) + teknologi anti-lupa (tetalining eling)
   - one full panembah = miniatur perjalanan hidup (lahir → sujud → hisab)
   - napas = only bodily function both automatic AND conscious → jembatan eling
   - magrib = doa perpisahan dengan dunia; subuh = doa perekrutan dunia
   - "ing atase Roh Suci padha wae" = kesetaraan radikal di hadapan Tuhan
   - noleh kiri-kanan = akuntansi batin (kolom dosa/ganjaran)
4. **Structure 90 minutes**: table jadwal (menit × bagian), tesis utama, gerakan demi
   gerakan/adegan, refleksi merajut, penutup dengan 3 kata kunci. Include original Javanese
   quote + Indonesian translation for every key passage.
5. **Save markdown**, then **publish Google Doc** via `google-docs-publish` and verify
   no markdown symbols leaked. Deliver link + local `:8000` link in Telegram.

## Pitfalls
- Do not fabricate quotes: every sandingan must be grep-verified in the actual book text.
- Serat Panembah Bab numbering: Bab 2 = teges-teges (meanings) of Panembahing Raga; Bab 3 =
  Panembahing Roh Suci marang Suksma Sejati. Bab 1 = praktik gerak.
- read_file output truncates on long extracted texts — slice via execute_code instead.
