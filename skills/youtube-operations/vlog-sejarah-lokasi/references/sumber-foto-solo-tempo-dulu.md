# Sumber Foto Solo Tempo Dulu — Quick Reference

Database lengkap: `/home/satyaaditech/yt-automation/Vlog/DAFTAR_SUMBER_FOTO_SOLO_TEMPO_DULU.md`

## Prioritas (yang terbukti jalan via curl)
1. **Wikimedia Commons** — kategori per dekade: `Category:Surakarta in the 1930s` dst. (1850s–1950s); `Category:Surakarta by year`; `Category:Images from KIT, Geografische Herkomst - Surakarta` (37 file Tropenmuseum); `Category:History of Surakarta`
2. **Tropenmuseum** — prefiks `COLLECTIE TROPENMUSEUM ... TMnr ...`, CC BY-SA 3.0
3. **KITLV Leiden** — prefiks `KITLV` / `KITLV Axxx`, CC BY 4.0, resolusi TIFF tinggi
4. **Nationaal Archief NL** — nationaalarchief.nl/onderzoeken/zoeken?q=Surakarta
5. **Delpher** — koran Hindia Belanda, delpher.nl/nl/kranten?query=Soerakarta
6. **Google News RSS** — untuk menemukan artikel berisi foto arsip (Tribun/Espos/Solopos)

## Istilah kunci Belanda untuk pencarian
Soerakarta, Solo, spoorweg (kereta api), overweg (palang pintu), spoorbrug (jembatan rel), kraton, Soesoehoenan, stoomwals (mesin paving), bestrating (pengerasan jalan)

## Trik teknis
- Unduh via `Special:FilePath/<File:...>` bukan API (hindari rate limit)
- Beri sleep 3-5 detik antar request API Wikimedia
- TIFF → JPG: PIL `im.thumbnail((1600,1600))`
- File TIFF dengan tanda kurung `(NIS)` di nama: perlu encode penuh via urllib.parse.quote
- Nama file asli kadang ejaan lama: "Nederlandsch-Indische" bukan "Nederlands-Indische"

## Tidak tersedia online (butuh kontak/kunjungan)
- Foto spesifik Simpang Joglo 1980-an/Belanda (tidak ada di arsip publik online)
- ANRI (Cloudflare), Perpusnas (Cloudflare), Arsip Jateng, Museum Radya Pustaka
- Komunitas FB/IG (solotempoedoele dll) — foto 1960-1990 kolektor pribadi, perlu izin

## Lisensi (wajib untuk YouTube)
- CC BY-SA / CC BY → kredit wajib di deskripsi: "arsip Tropenmuseum Amsterdam (CC BY-SA 3.0) & KITLV Leiden (CC BY 4.0) via Wikimedia Commons"
- Public Domain → bebas, tetap kredit sopan
- Foto jurnalistik (Tribun/Espos) → B-roll pendek + kredit, atau minta izin
