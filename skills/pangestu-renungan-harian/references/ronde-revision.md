# RONDE Revision Cycle

Setelah Orchestrator menerima laporan audit Editor, ada kemungkinan user minta **RONDE revisi** tambahan sebelum final. Ini terjadi saat Editor menemukan kesalahan wajib yang harus diperbaiki, atau user memberikan insight tambahan.

## Kapan RONDE Terjadi

- Editor menemukan kesalahan faktual/konten yang harus diperbaiki
- User memberikan feedback tambahan setelah melihat draft v1
- Revisi yang diminta kompleks (bukan sekadar typo)

## Alur RONDE

```
[USER] beri revisi RONDE N
    │  daftar: kesalahan wajib (1-2) + insight opsional (1-N)
    ▼
[ORCHESTRATOR] analisis revisi, terapkan perubahan
    │ output: draft RONDE N
    ▼
[USER] approve atau minta RONDE N+1
```

## Tipe Revisi dalam RONDE

### 1. WAJIB (harus diperbaiki, draft tidak valid kalau tidak)
- **Sabda splicing**: Sabda menyambung fragmen dari baris berbeda dengan "..." melewati isi. Solusi: kutip HANYA SATU baris utuh, atau dua fragmen dengan pemisah eksplisit "[...]".
- **Fakta salah**: kisah nyata mengandung detail yang tidak akurat (tahun, tempat, nama, detail medis). Solusi: verifikasi via web search, atau ganti dengan istilah umum.

### 2. OPTIONAL (insight Editor, perbaikan kualitas)
- **Inkonsistensi istilah**: "lautan" vs "samudra" → pilih satu.
- **Kalimat ambigu**: kalimat yang bisa dibaca dua makna berbeda.
- **Quote paraphrase**: kutipan yang bukan verbatim tapi diformat seperti direct quote.
- **Abstraksi berlebihan**: metafora yang bagus tapi tidak membumi → konkretkan.

## Contoh Kasus: RONDE 2 Sabar

**Kesalahan wajib dari Editor:**
1. Sabda menyambung baris 161, 163, 164 SSJ → fix: kutip hanya baris 161 utuh
2. "debu putih merusak paru-parunya" → fix: ganti "paru-parunya" dengan "kesehatannya"

**Insight optional dari Editor:**
- "lautan" vs "samudra" → seragamkan ke "lautan"
- Kalimat ambigu "Mandela tidak meninggalkan penjara..." → perjelas
- Quote "mengubah musuh menjadi kawan" adalah paraphrase → jangan format sebagai quote langsung
- Aplikasi #3 "Jamu pahit" abstrak → konkretkan dengan situasi spesifik
