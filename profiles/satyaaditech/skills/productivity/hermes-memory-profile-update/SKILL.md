---
name: hermes-memory-profile-update
description: Workflow untuk mengupdate profil user dan memory di Hermes Agent. Cara membaca, mengedit, dan memperbarui USER.md dan MEMORY.md dengan benar.
dependencies: ["memory", "read_file"]
---

# Hermes Memory Profile Update

Cara mengupdate profil user dan memory di Hermes Agent dengan benar.

## Overview

Hermes menyimpan informasi persistent di dua file utama:
- **USER.md** → Profil user (siapa kamu, preferensi, persona)
- **MEMORY.md** → Fakta environment, project details, lessons learned

## When to Use

- User minta mengubah profil/persona
- User ingin update preferensi komunikasi
- Perlu mengoreksi informasi yang salah di memory
- Menambah fokus/interests baru user

## Steps

### 1. Baca Memory Saat Ini

```python
read_file(path="~/.hermes/memories/USER.md")
read_file(path="~/.hermes/memories/MEMORY.md")
```

### 2. Identifikasi Yang Perlu Diubah

- Cari entry yang outdated atau salah
- Note exact text (harus persis untuk replace)

### 3. Update Menggunakan Memory Tool

**Untuk Replace Entry:**
```python
# Single line works best
memory(
    action="replace",
    target="user",  # atau "memory"
    old_text="- Entry lama yang mau diganti",
    content="- Entry baru"
)
```

**⚠️ PENTING:** `old_text` harus EXACT MATCH (persis sama, termasuk spacing)

**Jika Multi-line Replace Gagal:**
- Coba replace per baris
- Atau hapus entry lama + tambah entry baru

**Untuk Add Entry Baru:**
```python
memory(
    action="add",
    target="user",
    content="""New Entry Title:
- Detail 1
- Detail 2
- Detail 3"""
)
```

### 4. Verifikasi Perubahan

```python
read_file(path="~/.hermes/memories/USER.md")
```

## Common Pitfalls

1. **Multi-line replace sering gagal** → Gunakan single line atau pecah jadi beberapa replace
2. **Exact match required** → Copy-paste exact text dari file
3. **User vs Memory target** → Jangan sampai salah target file
4. **Character limits** → USER.md max 1,375 chars, MEMORY.md max 2,200 chars

## Example Workflows

### Update User Persona

```python
# Step 1: Read current
read_file(path="~/.hermes/memories/USER.md")

# Step 2: Replace old persona
memory(
    action="replace",
    target="user",
    old_text="- Content creator dengan fokus YouTube",
    content="- AI automation enthusiast"
)

# Step 3: Add new interests
memory(
    action="add",
    target="user",
    content="- Tertarik broad automation: research, data, integrations"
)

# Step 4: Verify
read_file(path="~/.hermes/memories/USER.md")
```

### Fix Incorrect Information

```python
# Hapus entry salah
memory(
    action="remove",
    target="memory",
    old_text="Informasi yang salah"
)

# Tambah yang benar
memory(
    action="add",
    target="memory",
    content="Informasi yang benar"
)
```

## Best Practices

1. **Selalu baca dulu** sebelum edit → hindari replace yang gagal
2. **USER.md = preferences** (bisa berubah sesuai keinginan user)
3. **MEMORY.md = facts** (project details, environment, lessons learned)
4. **Gunakan "add" untuk baru**, "replace" untuk update, "remove" untuk hapus
5. **Verifikasi setelah edit** → pastikan changes tersimpan dengan benar