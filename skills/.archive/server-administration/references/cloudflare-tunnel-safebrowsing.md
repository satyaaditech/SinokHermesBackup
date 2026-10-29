# Cloudflare Tunnel & Google Safe Browsing False Positives

## The Problem
When exposing self-hosted services (e.g. n8n, Home Assistant, Bitwarden) to the internet via Cloudflare Tunnels (using subdomains under `.web.id` or newly purchased domains), Google Safe Browsing and Microsoft SmartScreen automated scanners frequently flag the site as a **Deceptive Site / Dangerous Site** (Phishing).

This happens because:
1. The domain represents a login portal (`/signin` or `/home/workflows`) but has no other public-facing content.
2. The domain is on a ccTLD/subdomain commonly abused for phishing, combined with a shared Cloudflare Tunnel IP footprint.

## Resolution Workflow (Google Search Console & Cloudflare)

### Step 1: Add and Verify the Domain in Google Search Console
1. Navigate to [Google Search Console](https://search.google.com/search-console).
2. Add a new property: select the **Domain** verification type on the left (e.g. `satyaaditech.web.id`), rather than URL Prefix.
3. Use the **"Verify with Cloudflare"** automatic option. It redirects you to log into Cloudflare and authorize Google to add the verification TXT record to the DNS zone automatically.

### Step 2: Request Review
1. Once ownership is verified, go to **Keamanan & Tindakan Manual (Security & Manual Actions)** -> **Masalah Keamanan (Security Issues)**.
2. Click **Minta Peninjauan (Request Review)**.
3. Submit a brief justification (in Indonesian or English):
   > *"Situs ini adalah server n8n pribadi (self-hosted automation console) untuk keperluan otomatisasi internal saya sendiri. Halaman login tersebut sepenuhnya aman dan dilindungi kata sandi untuk akses privat, tidak ada aktivitas phishing, penipuan, atau malware. Mohon peninjauan kembali agar peringatan berbahaya ini dihapus. Terima kasih."*
4. Google typically reviews and clears the warning within **12 to 72 hours**.

### Local Troubleshooting
* If the warning persists on specific devices after clearance, clear the browser cache/cookies or test in Incognito mode.
