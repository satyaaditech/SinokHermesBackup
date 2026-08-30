# Panduan Pembuatan Infografis Hibrida (AI + Pillow)

Dokumen punika ngemot tata cara ndamel infografis kreatif ingkang jangkep lan cetha, nggabungaken kemampuan **AI Image Generator** (kagem latar wingking) lan **Python Pillow** (kagem teks/diagram presisi).

## Kenapa Kudu Hibrida?
* **Watesan AI**: Mesin AI Image Generator (kados Dene Gemini Imagen) asring ngasilaken seratan teks ingkang risak, typo, utawi awujud aksara acak ingkang mboten saged dipun-waos nalika ngginakaken basa Jawi/Indonesia.
* **Solusi Hibrida**: 
  1. Ndamel gambar latar wingking (background) ingkang **resik tanpa teks babar pisan (textless)** ngginakaken prompt AI.
  2. Numpuk teks bener, pethikan, lan diagram ing nginggilipun ngginakaken script Python (PIL/Pillow) kanthi ukuran lan tatakrama tata werna ingkang presisi.

---

## 1. Tahap Ndamel Background mawi AI (Gemini Imagen)
Nalika ndamel background lumantar API `/v1/images/generations` (`antigravity/gemini-3.1-flash-image`), gunakaken prompt ingkang negasaken bilih gambar kudu resik tanpa teks:

* **Conto Prompt**: 
  > *"A beautiful, clean, spiritual Javanese background design for a poster. The background is a soft textured cream-colored card with subtle light-blue and golden watercolor splashes. In the corners and borders, there is minimalist elegant line art of Kawung batik pattern. The central and lower body of the poster is clean, empty, and left open for text overlay. Soft and peaceful mood, vertical orientation, no text or words at all."*

### Penanganan Timeout & Transient 503:
Proses Gambar AI kerep mbetahaken wektu luwih saking 60 detik lan saged ketaman status 503 saking upstream. Gunakaken aturan:
1. **Background Process**: Run script proses generator ing background ngginakaken terminal (`background=True, notify_on_complete=True`).
2. **Retry Loop**: Script Python kudu ngemot loop nyoba (retry) ngantos kaping 3-4 kanthi ngginakaken *exponential backoff* sakdurunge nyerah.
3. **Programmatic Fallback**: Menawi AI pas nembe mati utawi kuota telas, script kudu otomatis ngalih ngginakaken background werna polos/gradasi buatan Pillow piyambak, supados proses tetep ngasilaken produk final.

---

## 2. Tahap Tumpukan Teks (Pillow Composition)
Supados teks gampang dipun-waos ing nginggilipun background AI ingkang rame/warna-warnani:

* **Overlay Card (Semi-Transparent)**: Gambaraken kothak background putih kanthi transparansi (misal `#FFFFFFDD` utawi `#FFFFFFEE`) ing ngisor teks utama lan kothak pethikan.
* **Gaussian Blur**: Aplikasiaken sithik filter blur (`ImageFilter.GaussianBlur(1)`) wonten ing background sakdurunge ditumpaki teks.
* **Tatanan Font**: Gunakaken font standar sistem (kados dene `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`) kanthi variasi ukuran:
  * Title: 36 - 38px Bold
  * Section/Sub-judul: 24px Bold
  * Quote/Pethikan: 18px Oblique/Italic
  * Body/Katrangan: 16px Regular
* **Wrap Text**: Tansah wrap teks pethikan lan katrangan nganggo `textwrap.fill(text, width=N)` supados mboten metu saking garis pinggir bingkai.
