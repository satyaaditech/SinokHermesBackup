---
name: honcho-memory
description: Setup Honcho memory for Hermes — cloud or self-hosted.
version: 1.0.0
author: Hermes Agent
platforms: [linux]
---

# Honcho Memory for Hermes

Configure Honcho as external memory provider on top of Hermes built-in memory.

## When to Use

- User wants to set up Honcho as memory provider (cloud or self-hosted)
- User asks about Honcho base URL, API key, or pricing
- User wants to self-host Honcho with Docker
- User needs to connect Honcho to OmniRoute/OpenRouter as LLM backend

---

## 1. Cloud vs Self-Hosted Decision

| Faktor | Cloud (app.honcho.dev) | Self-Hosted |
|--------|----------------------|-------------|
| Biaya Honcho | $100 free credits, lalu berbayar | Gratis (AGPL-3.0) |
| Biaya LLM | Sudah termasuk | Butuh API key sendiri |
| Setup | Isi API key, simpan | Docker compose, .env |
| Maintenance | Nol | Update Docker, backup DB |

**Rekomendasi**: Mulai cloud dulu, self-hosted kalau kena limit.

---

## 2. Cloud Setup

1. Daftar di https://app.honcho.dev, dapatkan API key
2. Di dashboard Hermes Memory Provider: pilih `honcho`
3. **API Key**: isi
4. **Base URL**: **KOSONGKAN** — Hermes otomatis pakai `https://app.honcho.dev`

---

## 3. Self-Hosted Setup

### Prasyarat
- Docker + Docker Compose
- LLM API key (Gemini Flash paling murah)

### Langkah
```bash
git clone https://github.com/plastic-labs/honcho.git
cd honcho
cp docker-compose.yml.example docker-compose.yml
cp .env.template .env
```

### Konfigurasi LLM

**OpenRouter / OmniRoute** (Honcho native tidak support OpenRouter, trik lewat OpenAI-compatible):
```bash
LLM_OPENAI_API_KEY=sk-or-v1-xxx        # OpenRouter API key
LLM_OPENAI_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=google/gemini-2.0-flash-001  # model murah via OpenRouter
```

**Gemini langsung** (lebih murah, gratis tier tersedia):
```bash
LLM_GEMINI_API_KEY=xxx
```

### Jalankan
```bash
docker compose up -d
```

### Hubungkan ke Hermes
- **Base URL**: `http://<server-ip>:8000`
- **API key**: kosongkan (kecuali `AUTH_USE_AUTH=true`)

---

## 4. Verifikasi

```bash
hermes memory status
hermes honcho status    # resolved config, connection, peers
```

## Pitfalls

- Base URL cloud diisi → error koneksi. Harus kosong.
- Self-hosted tanpa LLM API key → Honcho jalan tapi dialectic reasoning gagal.
- `AUTH_USE_AUTH=true` tanpa JWT → semua request ditolak.
