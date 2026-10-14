# Serat Panembah — Peta Bab & Indeks Sandingan Terverifikasi (Agustus 2026)

Hasil riset saat menyusun ulasan Sasangka Jati Bab 2 (17 Aug 2026). Menghemat
re-grep 8 kitab untuk tugas ulasan/khotbah panembah berikutnya.

## Peta Serat Panembah di dalam Sasangka Jati (JAWA, ssj.html)

Struktur di dalam file Javanese, di bagian AKHIR buku (≈ karakter 339k dari 406k):

- Bab 1 Panembah (3 adeg-adeg: praktik gerak)
- **Bab 2 Teges-teges kang Gegandhengan kalawan Panembahing Raga (Kawula) marang Roh Suci** — 4 adeg-adeg:
  1. Teges-teges lan Pigunane Nganggo Tembung Arab (Hu, Allah, Baitullah) — tetalining eling, lebu-wetuning napas
  2. Wancining Panembah (magrib 3 adegan / subuh 4 adegan) + teges wilangan: 3 = Tripurusa (bali marang Pangeran), 4 = anasir patang prakara (kebutuhan raga)
  3. Keblating Panembah & Patrap: madhep mangulon (bukan tempat Tuhan, tapi tata tunggal sedya / mindeng sawiji), ngadeg jejeg (adil), ngluhurake Asma, sedhakep (pasrah pepesthen), tumelung (rantai: Roh Suci → Suksma Sejati → Suksma Kawekas; "ing atase Roh Suci padha wae" = kesetaraan), sujud (ngrasuk busana, nyuwun pangayoman), timpuh (anindhihi hawa napsu), noleh mangiwa (dosa → disingkirake) / manengen (ganjaran → diangkah)
  4. Patrap Panembahing Raga lan Pujiane — doa batin per adegan + dhikir "Allah, Allah, Allah… kongsi tandhes ing telenging sanubari" + tuwajuh (cipta mindeng sawiji)
- Bab 3 Teges-teges Panembahing Roh Suci marang Suksma Sejati (tataran jiwa dewasa)

## ⚠️ Pitfall: Versi Indonesia TIDAK memuat Serat Panembah

`ssj_ind.html` (SASANGKA JATI INDONESIA) hanya terjemahan sebagian — berhenti
sebelum Serat Panembah (tidak ada "Panembahing Raga" / "Sembah Raga" sama sekali;
hits "Panembah" di awal hanya TOC). Terjemahan kutipan harus dibuat sendiri dari
teks Jawa. Gunakan `ssj.html` (JAWA) untuk Serat Panembah.

## Indeks kutipan sandingan (sudah diverifikasi, bisa dikutip langsung)

| Kitab (slug) | Bagian | Kutipan kunci |
|---|---|---|
| SKH (skh.html) | Peringatan/ayat ke-8 | "Aku tidak akan menuntunmu apabila engkau lupa dan tidak percaya kepada-Ku. Adapun yang menyebabkan lupa itu karena engkau asyik tertarik kepada barang-barang yang kau cintai." |
| SKH | ayat ke-11 | "mulailah bersuci, yaitu membuang rasa cintamu kepada barang-barang yang tidak kekal … gantilah dengan rasa cinta (bakti) kepada-Ku" |
| SKH | ayat (≈11) | "cintamu atau melekatnya hatimu pada barang-barang duniawi itulah yang menjadikan aling-aling yang menutupi hal-hal yang benar (haq)" |
| ASBS (asbs.html) | TOC #28 + body | "Panembah, tapa brata, dan budi darma lebih-lebih merupakan jalan untuk mengurangi dan akhirnya meniadakan Akunya manusia. Bilamana manusia dapat menduduki derajat Suksma Sejati, lenyaplah Akunya sebagai kekuasaan dan kedaulatan angan-angan." |
| UKK (ukk.html) | Bab panembah | "kita harus senantiasa manembah secara teratur dan serius yang berarti kita melatih diri untuk mendekat kepada Sang Guru Sejati … Kandas di tengah jalan berarti masuk ke dalam alam kafiruna." |
| BRSR (brsr.html) | TOC bab VIII, IX, XII | VIII "ASAL SAKA ALLAH, BALI MARANG ALLAH"; IX "ATI KANG SINUCI DHAMPAR PALENGGAHANING ALLAH (KALBU MUKMIN BAITULLAH)"; XII "LALI MARGA KONCATAN PEPADHANG" |
| TKL (tkl.html) | — | "kabeh kang gumelar ing bawana iki, yen sinawang kanthi mursiding ati, sanyata dadi sasmita dhawuhing Gusti"; kesaksian siswa: "angen-angen … tansah jumbal-jumbul tuwin rame kados ing salebetipun pasar malem, kendel boten mobah mosik" (heneng-hening) |
| SPRA (spra.html) | — | "Siswa muda melanjutkan tindakan sikap panembah (pameleng), dan tak berapa lama kemudian, 'les' masuk kembali ke alam luyut (tenang), dan mendengar Sabda Sang Guru Sejati" |

## Resep ekstraksi bab

1. `curl -sL -A "Mozilla/5.0" "https://satyaaditech.github.io/perpustakaan/book/pangestu/ssj.html"` → strip `<article>` → teks.
2. Cari `\nBab 2\n` → awal; `\nBab 3\b` → akhir; slice di antaranya.
3. Judul bab muncul 2× (TOC + body) — pakai kemunculan kedua (≈ akhir file).
4. Tool hasil baca terpotong untuk teks panjang → pakai `execute_code` + slice eksplisit (mis. `txt[4300:6400]`).

## Contoh pakai (output sesi ini)
- `~/share/materi_khotbah/ulasan_sasangka_jati_bab2_2026-08-17.md` (markdown 90-menit)
- Google Doc `1S1-a3yNF2QtxGa6doSR6KLPQOy-RU70qnLGho17_1MU` (folder Materi Olahrasa)
