---
name: n8n-workflow-runner
description: Menjalankan, memantau, dan menemukan (discover) workflow otomatisasi n8n yang terpasang di server ASUS ROG (Sinox) secara REAL-TIME. Gunakan skill ini ketika user meminta menjalankan alur otomatisasi, membuat video, memproses data, atau mengecek workflow baru di n8n.
---

# n8n Real-Time Dynamic Workflow Runner (ROG Server Engine)

Skill ini memungkinkan Hermes Agent (**Sinox** maupun **Parjo**) untuk mendeteksi dan mengeksekusi seluruh workflow di **n8n Server ROG** secara otomatis dan dinamis tanpa konfigurasi manual.

## 🚀 Kemampuan Otomatis Real-Time (Live Discovery)
- **Deteksi Otomatis Workflow Baru:** Kapan pun ada workflow baru yang dibuat, diedit, atau diaktifkan di n8n ROG, kedua server (**Sinox & Parjo**) akan **langsung mengetahui nama, status, dan webhook-nya secara instan** melalui endpoint discovery cluster ROG.
- **Fuzzy Matching:** Agent cukup menyebutkan sebagian nama workflow (misal: "Pabrik Konten", "Gemini Chat", "Scraping") atau ID-nya; script akan mencocokkan webhook-nya secara otomatis.

---

## 🛠️ Cara Penggunaan oleh Agent

### 1. Melihat Seluruh Workflow n8n yang Sedang Aktif di ROG:
```bash
python ~/.hermes/skills/n8n-workflow-runner/scripts/n8n_runner.py list
```

### 2. Memicu (Trigger) Workflow Berdasarkan Nama / Webhook:
```bash
python ~/.hermes/skills/n8n-workflow-runner/scripts/n8n_runner.py trigger "<nama_workflow_atau_webhook>" '<payload_json>'
```

#### Contoh:
* Memicu workflow Pabrik Konten dengan topik tertentu:
  ```bash
  python ~/.hermes/skills/n8n-workflow-runner/scripts/n8n_runner.py trigger "Pabrik Konten" '{"topic": "Refleksi Jiwa", "format": "1080p"}'
  ```

* Memicu workflow baru yang baru saja dibuat Pak Satya di kanvas n8n:
  ```bash
  python ~/.hermes/skills/n8n-workflow-runner/scripts/n8n_runner.py trigger "Nama Workflow Baru" '{"data": "contoh"}'
  ```

---

## 📋 Prosedur Respon ke User
1. Jika Pak Satya menanyakan workflow apa saja yang ada di n8n, jalankan `n8n_runner.py list` dan laporkan daftar workflow beserta status aktifnya.
2. Saat mengeksekusi workflow, laporkan konfirmasi bahwa workflow telah berhasil dipicu (`Workflow was started`) beserta target webhook yang dieksekusi.
