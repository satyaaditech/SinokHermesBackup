# Provider OpenCode Go — DeepSeek V4 Pro

Provider untuk Writer + Editor renungan Pangestu.
Model wajib: **deepseek-v4-pro** (berbayar, kualitas tinggi).

## 🔑 API Key (Aktif per 11 Ags 2026)

Key disimpan di config Hermes:
```bash
hermes config set delegation.api_key "sk-L3iZxkUqxuFjvtGh6yR3I5cFKbXdpTaD98fDZ556sinsoebKNkVYVH9R8wPYt2a4"
```

**PENTING**: Jangan pakai `${OPENCODE_API_KEY}` (env var) — subagent Hermes tidak selalu mewarisi environment. Set langsung di config dengan string literal.

## Verifikasi Model + Saldo

Cek model yang tersedia:
```bash
curl -s https://opencode.ai/zen/go/v1/models \
  -H "Authorization: Bearer sk-L3iZxkUqxuFjvtGh6yR3I5cFKbXdpTaD98fDZ556sinsoebKNkVYVH9R8wPYt2a4" \
  | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"
```

Cek saldo (sebelum dispatch — WAJIB):
```bash
curl -s -o /dev/null -w "%{http_code}" https://opencode.ai/zen/go/v1/chat/completions \
  -H "Authorization: Bearer sk-L3iZxkUqxuFjvtGh6yR3I5cFKbXdpTaD98fDZ556sinsoebKNkVYVH9R8wPYt2a4" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"test"}],"max_tokens":5}'
```

- **200** → siap dispatch
- **401** → saldo habis — jangan dispatch, fallback tulis langsung
- Top-up: https://opencode.ai/workspace/wrk_01KS8Q1HE9FDYBSZ8ZV66GGYT2/billing

## Konfigurasi Hermes (Direct Base URL)

Ini yang bekerja untuk subagent. Tidak perlu `custom_providers`.

```bash
# Hapus provider named kalau ada
hermes config unset delegation.provider

# Set direct endpoint
hermes config set delegation.base_url "https://opencode.ai/zen/go/v1"
hermes config set delegation.api_key "sk-L3iZxkUqxuFjvtGh6yR3I5cFKbXdpTaD98fDZ556sinsoebKNkVYVH9R8wPYt2a4"
hermes config set delegation.model "deepseek-v4-pro"
```

## ⚠️ WAJIB: Restore config SETELAH selesai

Config delegasi default sesi = OmniRoute (server TS 100.92.237.45:20128/v1). Kalau tidak di-restore, sesi berikutnya subagent ikut pakai OpenCode dan bisa error/boros saldo.

```bash
hermes config set delegation.base_url "http://localhost:20128/v1"
hermes config set delegation.api_key ""
hermes config set delegation.model "auto/best-reasoning"
```

Urutan sesi: set OpenCode → dispatch Researcher/Writer/Editor → apply revisi → RESTORE OmniRoute → kirim final.

❌ JANGAN pakai `custom_providers` — formatnya rawan error.
❌ JANGAN pakai env var `OPENCODE_API_KEY` — subagent tidak inherit environment.

✅ Direct base_url + api_key literal sudah TERBUKTI bekerja.
- Tes Researcher: 13 detik, completed, HTTP 200 (11 Ags 2026)
- Model: `deepseek-v4-pro`
- Prompt tokens: 7, completion tokens: 10, reasoning tokens: 10
- Cost: $0 (tes ringan)
