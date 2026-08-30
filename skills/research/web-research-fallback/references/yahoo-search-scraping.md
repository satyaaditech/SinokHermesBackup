# Yahoo Search HTML Scraping (urllib + regex)
*Pola riset web cepat menggunakan Yahoo Search ketika Google/DuckDuckGo terblokir captcha atau mengalami error SSL.*

## Mengapa Menggunakan Yahoo Search?
* **Resiliensi Captcha**: Yahoo Search cenderung tidak se-agresif Google/DuckDuckGo dalam memblokir request langsung dari lingkungan sandbox/cloud.
* **Struktur HTML Sederhana**: Hasil pencarian memiliki pola penanda kelas kontainer (`compText` untuk snippet deskripsi, dan tag `<h3>` untuk judul hasil pencarian) yang mudah dikenali secara konsisten.
* **Tanpa Dependensi Tambahan**: Dapat berjalan menggunakan pustaka bawaan Python (`urllib` dan `re`), tanpa memerlukan `bs4` (BeautifulSoup) atau `requests`.

## Implementasi Kode Python
Gunakan cuplikan modul berikut di dalam `execute_code` untuk melakukan scraping pencarian secara instan:

```python
import urllib.request
import urllib.parse
import re
import ssl

def search_yahoo(query, limit=5):
    # Buat konteks SSL tanpa verifikasi untuk menghindari Certificate Mismatch pada sandbox
    context = ssl._create_unverified_context()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Ekstraksi judul hasil dan kutipan snippet menggunakan regex terarah
            # Judul biasanya diapit oleh h3 class="title" / h3 tag
            h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
            # Deskripsi biasanya diapit oleh div class="compText"
            divs = re.findall(r'<div class="compText[^"]*">(.*?)</div>', html, re.DOTALL)
            
            results = []
            for i in range(min(len(h3s), len(divs), limit)):
                # Bersihkan tag HTML yang tersisa sisa dari snippet dan judul
                t_clean = re.sub(r'<[^>]+>', '', h3s[i]).strip()
                s_clean = re.sub(r'<[^>]+>', '', divs[i]).strip()
                results.append((t_clean, s_clean))
            return results
    except Exception as e:
        return [("Error", str(e))]

# Contoh Penggunaan:
# results = search_yahoo("sirup daun kelor organoleptik")
# for idx, (title, snippet) in enumerate(results):
#     print(f"[{idx+1}] {title}\n    {snippet}\n")
```
