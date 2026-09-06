# Ekstraksi Artikel Blog via Feed JSON (Blogger & WordPress)
*Metode cepat dan andal untuk membaca daftar artikel atau isi blog tanpa perlu parsing HTML penuh atau dependensi pihak ketiga (bs4).*

---

## 1. Blogger / Blogspot (Termasuk Custom Domain)

Tanda-tanda: URL berakhiran `.blogspot.com` atau memiliki parameter `?m=1`.

### Endpoint Feed JSON
Blogger menyediakan feed JSON bawaan yang sangat bersih dan mendukung pagination:
- **Semua Artikel:** `https://<DOMAIN>/feeds/posts/default?alt=json&start-index=1&max-results=150`
- **Berdasarkan Label / Kategori:** `https://<DOMAIN>/feeds/posts/default/-/<LABEL>?alt=json`

### Script Ekstraksi Python (Zero-Dependency / Stdlib Only)
```python
import urllib.request
import json

def fetch_blogger_posts(domain_url, max_posts=100):
    domain = domain_url.split('?')[0].rstrip('/')
    posts = []
    start = 1
    while len(posts) < max_posts:
        feed_url = f"{domain}/feeds/posts/default?alt=json&start-index={start}&max-results=50"
        req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                entries = data.get('feed', {}).get('entry', [])
                if not entries:
                    break
                for e in entries:
                    title = e.get('title', {}).get('$t', '').strip()
                    published = e.get('published', {}).get('$t', '')[:10]
                    link = next((l.get('href') for l in e.get('link', []) if l.get('rel') == 'alternate'), '')
                    categories = [c.get('term') for c in e.get('category', []) if c.get('term')]
                    posts.append({
                        'title': title,
                        'published': published,
                        'url': link,
                        'categories': categories
                    })
                start += len(entries)
        except Exception as err:
            print(f"Blogger feed error: {err}")
            break
    return posts
```

---

## 2. WordPress REST API

Tanda-tanda: Situs berbasis WordPress (`/wp-content/`, `/wp-json/`).

### Endpoint REST API
- **Daftar Postingan:** `https://<DOMAIN>/wp-json/wp/v2/posts?per_page=100&page=1`
- **Pencarian Kata Kunci:** `https://<DOMAIN>/wp-json/wp/v2/posts?search=<QUERY>`

### Script Ekstraksi Python
```python
import urllib.request
import json

def fetch_wordpress_posts(domain_url, max_pages=1):
    domain = domain_url.rstrip('/')
    posts = []
    for page in range(1, max_pages + 1):
        api_url = f"{domain}/wp-json/wp/v2/posts?per_page=50&page={page}&_fields=id,date,title,link"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                items = json.loads(resp.read().decode('utf-8'))
                if not items or not isinstance(items, list):
                    break
                for item in items:
                    posts.append({
                        'title': item.get('title', {}).get('rendered', ''),
                        'published': item.get('date', '')[:10],
                        'url': item.get('link', '')
                    })
        except Exception as err:
            print(f"WordPress API error: {err}")
            break
    return posts
```
