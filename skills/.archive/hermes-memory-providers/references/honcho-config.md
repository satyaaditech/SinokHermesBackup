# Honcho Configuration Reference

## Cloud vs Self-Hosted

| | Cloud (app.honcho.dev) | Self-Hosted (Docker) |
|---|---|---|
| **API Key** | Dapat dari [app.honcho.dev](https://app.honcho.dev) | JWT signed dengan `AUTH_JWT_SECRET` server |
| **Base URL** | **Kosongkan** (Hermes pakai default `https://app.honcho.dev`) | Isi URL server (contoh: `http://192.168.0.112:8000`) |
| **Biaya** | Kemungkinan free tier untuk personal/dev use — cek dashboard | **Gratis 100%** (open source, Apache 2.0) |
| **Setup** | `hermes memory setup honcho` → pilih "cloud" | `hermes memory setup honcho` → pilih "local" → masukkan URL |

## Pricing

Honcho open source ([GitHub](https://github.com/plastic-labs/honcho)), lisensi Apache 2.0.

- **Cloud**: Detail paket tidak tercantum publik di website. Cek `app.honcho.dev` setelah login untuk lihat plan aktif.
- **Self-hosted**: Selalu gratis. Spin up server FastAPI sendiri via Docker.

Rekomendasi: mulai dengan cloud dulu, evaluasi free tier. Kalau kena limit, migrasi ke self-hosted.

## Dashboard Fields

| Field | Cloud | Self-Hosted |
|-------|-------|-------------|
| API Key | ✅ Wajib | ✅ Wajib (JWT) |
| Base URL | ❌ Kosongkan | ✅ Wajib |

## Verifikasi

```bash
hermes honcho status    # cek koneksi, peer info, resolved config
hermes memory status    # cek provider aktif
```
