# Panduan Pembuatan Prompt Visual Google Gemini (Imagen 3) untuk Renungan

Dokumen ini berisi panduan dan arketipe prompt visual untuk menghasilkan poster renungan harian berorientasi portrait (9:16) menggunakan Google Gemini (Imagen 3) atau AI diffusion generator serupa.

---

## 1. Prinsip Utama Prompting Imagen 3 untuk Renungan

1. **Rasio Aspek**: Wajib mencantumkan orientasi portrait vertikal `(9:16 portrait orientation)` atau `--ar 9:16` agar pas untuk tampilan HP / status / e-poster.
2. **Infografis Utuh (Bukan Sekadar Background)**: Jika diminta poster infografis nilai/esensi renungan, prompt HARUS menyertakan teks judul ("RENUNGAN PENYISWAAN"), 3–4 kartu persegi panjang terstruktur berisi nilai-nilai esensi, serta footer laku batin langsung di dalam prompt, memanfaatkan kemampuan text rendering Imagen 3.
3. **Komposisi & Ruang Teks (Safe Zones)**:
   - Tentukan `ultra-clean negative space at top and bottom` agar bagian atas dan bawah gambar dapat disisipkan teks judul Sabda dan refleksi tanpa menabrak detail visual utama.
3. **Pencahayaan & Suasana (Atmosphere)**:
   - Gunakan pencahayaan hangat dan menenangkan: `natural warm directional sunlight`, `golden dawn light`, `soft ambient mist`.
   - Hindari visual ekstrem atau horor; prioritaskan suasana kontemplatif (*heneng-hening*), damai, dan agung.
4. **Palet Warna Spiritual Elegan**:
   - `Deep Indigo Blue`, `Warm Cream Alabaster`, `Terracotta / Burgundy`, `Turquoise Ocean`, `Champagne Gold accents`.

---

## 2. Tiga Arketipe Visual Pilihan

### Arketipe A: Cinematic Fine-Art Surrealist (Metafora Batin)
*Cocok untuk tema: Sabar Momot (Samudra), Angen-Angen (Beban Pikiran), Manembah, Ketenangan Jiwa.*

```text
A breathtaking, cinematic fine-art vertical poster (9:16 portrait orientation). [Deskripsi figur / metafora spiritual, misal: human silhouette whose heart dissolves into a vast turquoise ocean]. In the background, [kondisi alam pendukung, misal: gentle river waters flowing into infinite calm sea]. Floating water lilies and soft golden dawn light rays illuminating morning mist. High-end editorial aesthetic, ultra-clean negative space at top and bottom for typography, soft warm ambient lighting, 35mm film photography, award-winning fine art, 8k resolution.
```

### Arketipe B: Modern Luxury Wisdom Infographic (Struktur Simetris)
*Cocok untuk tema: Hasta Sila, Rila-Legawa, Pengampunan, Nilai Budi Luhur.*

```text
A high-end luxury editorial wisdom poster, vertical 9:16 portrait layout. Minimalist spiritual wisdom design. At the top center, a stylized subtle glowing golden emblem of [simbol, misal: ocean wave and peace dove]. In the center, a balanced zen stone resting peacefully above crystal-clear turquoise flowing water, surrounded by delicate geometric golden line art. Clean, organized parchment-textured background with spacious layout. Palette: Deep indigo, warm alabaster cream, subtle champagne gold accents. Museum gallery print quality, crisp details, 8k resolution.
```

### Arketipe C: Zen Wabi-Sabi Ink & Kintsugi (Estetika Hening & Luwes)
*Cocok untuk tema: Rila (Tan Nabet ing Ati), Penyembuhan Batin, Keikhlasan, Mengampuni.*

```text
A vertical portrait art poster in Japanese and Javanese Zen Wabi-Sabi aesthetic. A majestic, smooth river rock resting in the middle of calm waters, rendered with minimalist sumi-e ink washes and luminous gold kintsugi veins repairing the stone. Gentle morning mist rising from tranquil surface. Ample peaceful negative space in warm raw rice-paper texture. Atmosphere of supreme stillness and profound forgiveness. Masterpiece fine art print, exquisite texture, soft directional illumination, 8k resolution.
```
