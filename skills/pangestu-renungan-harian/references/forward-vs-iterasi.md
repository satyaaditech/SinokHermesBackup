# Perbandingan Forward vs Iterasi — Studi Kasus

## Forward: Tema "Jujur" (10 Aug 2026)

| Fase | Subagent | Waktu | Catatan |
|------|----------|-------|---------|
| Researcher | deleg_0be799e5 | 83s | 2 Sabda: SSJ + ASBS |
| Writer | deleg_c84d72b8 | 182s | Kisah Abraham Lincoln "Honest Abe" |
| Editor | deleg_c3625422 | 157s | ⚠️ 2 false alarm: (1) klaim Sabda dari Hasta Sila bukan SSJ — salah, (2) klaim quote ASBS tidak ditemukan — salah (cari di folder studi bukan /tmp/) |
| Orchestrator | manual | — | Koreksi false alarm Editor, framing Lincoln sebagai "konon" |

**Yang lolos:** kisah Lincoln "berjalan bermil-mil kembalikan receh" — apokrifal, bukan fakta primer. Editor mendeteksi tapi hanya sebagai 💡 insight. Diperbaiki orchestrator: framing "konon."

**Nilai:** false alarm Editor membuktikan orchestrator harus verifikasi mandiri.

---

## Iterasi: Tema "Sabar" (11 Aug 2026)

| Fase | Subagent | Waktu | Catatan |
|------|----------|-------|---------|
| Researcher | deleg_8a6e1790 | 137s | 2 Sabda: SSJ (baris 161) + UKK |
| Writer v1 | deleg_82fe130e | 272s | Kisah Nelson Mandela 27 tahun |
| Editor R1 | deleg_7f4518a1 | 195s | ⚠️ 2 ❌ wajib + 4 💡 insight |
| Writer v2 | deleg_0de75074 | 257s | Perbaiki: Sabda splicing + "paru-paru"→"kesehatannya" + 4 insight |
| Editor R2 | deleg_55267feb | 41s | ✅ 6/6 LULUS |

**Total: 4 subagent, 902s (±15 menit)**

### Kesalahan yang ditemukan Editor R1:

1. **Sabda splicing ❌** — Writer v1 sambung 3 fragmen (baris 161, 163, 164) dengan "..." melompati baris 162-163. Ini cherry-picking, bukan verbatim.
2. **Fakta Mandela ❌** — "debu putih merusak paru-parunya" — salah. Tambang kapur Robben Island merusak tear ducts, bukan paru-paru. TB Mandela di Pollsmoor (1988), bukan Robben Island.

### Insight tambahan:

3. Metafora "lautan" vs "samudra" inkonsisten — pilih "lautan"
4. Kalimat ambigu tentang Mandela — diperjelas di v2
5. Quote "mengubah musuh jadi kawan" — parafrase, bukan kutipan langsung
6. Aplikasi #3 "jamu pahit" — abstrak, perlu dikonkretkan

---

## Kesimpulan

| Aspek | Forward | Iterasi |
|-------|---------|---------|
| Subagent | 3 | 4-5 |
| Waktu | ±7 menit | ±15 menit |
| Token | 1x | ~2.3x |
| Kualitas | Bagus, cacat kecil bisa lolos | Lebih tinggi, detail faktual tertangkap |
| Risiko Editor | False alarm lebih mungkin | Lebih akurat (audit 2x) |
| Cocok untuk | Rutin harian | Edisi khusus, tema kompleks |
