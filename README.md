# Sinok (Hermes Agent) System Backup

Repository ini berisi cadangan (backup) otomatis untuk konfigurasi, memori, profil, dan katrampilan (skills) dari sistem **Hermes Agent (Sinok)** milik Satya Adi Dharma.

## 📂 Struktur Direktori Terlacak

Berikut adalah berkas dan folder penting yang dicadangkan dalam repository ini:
*   `config.yaml` - Konfigurasi utama sistem Hermes (model, provider, toolset, kustomisasi visual).
*   `SOUL.md` - Definisi kepribadian, instruksi, dan persona Sinok.
*   `memories/` - Memori jangka panjang (fakta penting tentang pengguna, preferensi, dan catatan sistem).
*   `profiles/` - Berkas konfigurasi dan state spesifik untuk masing-masing profil Hermes.
*   `skills/` - Katrampilan (reusable skills/procedures) yang dibuat secara manual atau otomatis oleh agen.
*   `scripts/` - Skrip kustom yang digunakan oleh cron job atau agen (termasuk skrip backup ini sendiri).
*   `models.json` & `tui-theme-boot.json` - Setelan tema tampilan TUI dan metadata model pendukung.

## 🔒 Berkas yang Dikecualikan (.gitignore)

Untuk masalah keamanan dan penyimpanan, berkas-berkas rahasia atau sementara berikut **tidak dicadangkan**:
*   `.env` - Menyimpan API Keys dan credential tokens sensitif.
*   `auth.json` / `auth.lock` - Akses OAuth dan token login.
*   `*.db`, `*.db-wal`, `*.db-shm` - Database lokal sqlite (data chat history, session state).
*   `**/cache/` & `**/logs/` - Berkas cache dan log sistem.

## ⚙️ Mekanisme Backup Otomatis

Backup dijalankan secara otomatis menggunakan sistem Task Scheduler (cron job) bawaan Hermes:
*   **Nama Task**: `hermes-config-backup`
*   **Waktu Eksekusi**: Setiap hari pukul 23:00 WIB.
*   **Skrip Pengeksekusi**: `scripts/backup.sh` (berbasis `backup.sh` di folder `~/.hermes/scripts/`).
*   **Cara Kerja**:
    1. Skrip akan memindai folder `~/.hermes/` untuk melihat jika ada perubahan pada file yang terlacak (misal, memori baru ditambahkan, atau skill baru ditulis).
    2. Jika terdeteksi perubahan, skrip akan melakukan `git commit` dengan timestamp saat itu dan langsung melakukan `git push` ke GitHub melalui SSH.
    3. Jika tidak ada perubahan baru, skrip tidak akan melakukan aksi apapun (silent).

## 🔄 Cara Melakukan Pemulihan (Restore)

Jika sistem Hermes mengalami crash atau ingin dipindahkan ke server/komputer baru:
1. Pastikan Git dan SSH Key di server baru telah dikonfigurasi dan dikenali oleh GitHub Anda.
2. Lakukan clone repositori ini langsung ke direktori home sebagai `.hermes`:
   ```bash
   git clone git@github.com:satyaaditech/SinokHermesBackup.git ~/.hermes
   ```
3. Salin berkas `.env` lama Anda (yang berisi API keys) ke dalam folder `~/.hermes/.env` (buat baru jika hilang).
4. Jalankan sistem Hermes di komputer baru. Sistem akan otomatis memuat seluruh konfigurasi, memori, dan skill Anda yang ada di repositori ini.
