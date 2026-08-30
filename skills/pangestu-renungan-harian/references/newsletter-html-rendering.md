# Rendering Newsletter & E-Card Otomatis (HTML/CSS to Image)

Dokumentasi workflow otomatisasi pembuatan newsletter/e-card visual "selevel Canva" menggunakan HTML/CSS template dan Puppeteer (Headless Browser) secara lokal tanpa API eksternal.

## 1. Alur Otomatisasi
1. **HTML/CSS Template**: Desain tata letak fluid menggunakan CSS flexbox/grid, border tradisional, font lokal (`DejaVu Serif`), dan drop-cap majalah.
2. **Text Injector (Node.js/Python)**: Membaca naskah Markdown dan mengganti variabel placeholder (seperti `{TITLE}`, `{SABDA}`, dll).
3. **Puppeteer Renderer**: Headless browser membuka file HTML lokal dengan viewport yang diatur khusus (misal 1200x1950px) lalu mengambil screenshot halaman utuh (`page.screenshot({ fullPage: true })`).

---

## 1b. Multi-Page (Carousel) & Rendering Tips
* **Tata Letak Multi-Halaman**: Untuk naskah panjang (misal renungan + praktik + aplikasi), jangan dipaksa dalam satu frame karena teks akan menabrak border. Set tinggi halaman tetap (seperti `height: 2150px;`) untuk tiap `.page` div, lalu set viewport Puppeteer tinggi akumulatif (misal `1200x4500px`) dan tangkap screenshot per halaman id (#page-1, #page-2).
* **Emoji Glif Rusak (`🗎`)**: Browser headless OS Linux server minimal sering kali mem-fallback emoji kesiswaan (seperti `🧘`, `🎯`) menjadi kotak berkas `🗎` karena tidak adanya font emoji sistem. Ganti emoji tersebut dengan **ikon SVG inline kustom** dalam template HTML agar rendering dijamin 100% konsisten dan tajam.
* **Regex Global**: Gunakan `html.replace(/{DATE_STR}/g, dateStr)` agar tanggal ter-update di beberapa tempat sekaligus.
* **Direktori Share & Telegram Send**: Simpan gambar kustom di folder share `/home/satyaaditech/share/renungan/` dan kirimkan langsung sebagai gambar fisik via `sendPhoto` Bot API menggunakan requests python (timeout=25s) agar carousel gambar tampil siap-geser (*swipe-able*) di Telegram.

---

## 2. Penanganan Masalah & Pitfall Instalasi Puppeteer

### Pitfall #1: Chrome Extraction Error (Missing `unzip`)
Saat menjalankan install script Chromium di VM Linux minimalis (`install.mjs`), proses install sering kali crash dengan pesan kegagalan ekstraksi zip:
```text
Extraction failed: no zip archiver is available. Install `unzip` (or `tar.exe` on Windows), or add the optional `yauzl` dependency.
```

**Solusi**:
Jika VM tidak memiliki akses `sudo` untuk menginstall paket `unzip` sistem, lakukan instalasi pustaka JavaScript pendukung `yauzl` secara lokal pada folder Node.js:
```bash
npm install yauzl --no-audit --no-fund
```
Hapus cache instalasi yang rusak/gagal sebelumnya:
```bash
rm -rf ~/.cache/puppeteer/chrome/ ~/.cache/puppeteer/chrome-headless-shell/
```
Jalankan kembali script instalasi untuk mengunduh browser bawaan Puppeteer:
```bash
node node_modules/puppeteer/install.mjs
```

---

## 3. Template Render Script Node.js (`render.js`)
Gunakan template script berikut untuk menghasilkan berkas gambar secara andal:

```javascript
const fs = require('fs');
const puppeteer = require('puppeteer');

(async () => {
  try {
    const template = fs.readFileSync('template.html', 'utf8');

    // Suntik data ke template
    let html = template
      .replace('{DATE_STR}', "Selasa, 25 Agustus 2026")
      .replace('{TITLE}', "Judul Renungan")
      .replace('{SUB_TITLE}', "Subjudul Renungan")
      .replace('{SABDA}', "Isi kutipan...")
      .replace('{URAIAN_COL_1}', "Paragraf 1 dan 2...")
      .replace('{URAIAN_COL_2}', "Paragraf 3 dan 4...");

    fs.writeFileSync('output.html', html, 'utf8');

    // Jalankan headless Chrome
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 1950 });
    
    // Buka file lokal menggunakan protokol file://
    await page.goto('file://' + __dirname + '/output.html', { waitUntil: 'networkidle0' });
    
    // Screenshot
    await page.screenshot({ path: 'output.png', fullPage: true });
    await browser.close();
    console.log("Render Success!");
  } catch (error) {
    console.error("Render Failed:", error);
  }
})();
```
