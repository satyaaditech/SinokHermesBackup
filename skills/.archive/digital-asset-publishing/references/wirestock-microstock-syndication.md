# Wirestock Microstock Syndication & Gumroad API Automation

## 1. Wirestock (Microstock Global Syndication)
Wirestock acts as a single-entry distributor to automatically syndicate video/image assets across major stock platforms: **Adobe Stock, Shutterstock, Pond5, Freepik, and Getty Images/iStock**.

### Onboarding & Navigation (2026 UI Flow):
1. **Account Creation:**
   - URL: `https://wirestock.io/signup`
   - Select: **`Join as Creator`** (Left card, for selling content and collecting royalties; do not select "AI Lab").
   - Skills selection: Check `AI / Generative Art` (critical), `Video Production`, and `3D`.
2. **Locating Submission Portals:**
   - Note: Standalone `/upload` or `/media/upload` URLs return 404 in the modern UI.
   - Go to Left Sidebar -> **`Projects`** (`wirestock.io/projects?projectsTab=active`).
   - For VFX/video loops: Select **`Original Raw Video & VFX Video`** (Commission-based stock submission card).
   - Alternatively, monitor earnings and accepted assets under **`Dashboard -> Stock`**.
3. **Submission Compliance & Toggles:**
   - **AI Declaration:** Mandatory toggle `AI Generated` -> specify source (`Google Veo` / `Google`).
   - **Easy Submission:** Enable Wirestock AI auto-tagging to generate relevant titles and ~30 SEO keywords.
   - **Payouts:** Connect PayPal via Account Settings once earnings accumulate.

### Pitfalls & Fallback:
- **Project Connection Errors:** If Wirestock encounters project submission timeouts or connection errors (*"Couldn't connect to this project"*), bypass third-party aggregators and upload AI videos directly to **Adobe Stock Contributor** (`https://contributor.stock.adobe.com`) to retain 100% direct royalty earnings without middleman commission splits.

---

## 2. Gumroad API & CLI Automation
Gumroad provides a REST API (`https://api.gumroad.com/v2/`) and webhook architecture that allows fully automated product publishing and real-time sales notifications.

### Capabilities:
1. **Automated Product Creation (`POST /v2/products`):**
   - Parameters: `name`, `price` (in cents, e.g. `999` for $9.99), `description`, `url` (custom slug), `published: true`.
   - Programmatically attach cover images and downloadable ZIP artifacts via multipart form data.
2. **Sales Webhooks (Instant Telegram Pings):**
   - Webhook URL configured in Gumroad `Settings -> Advanced -> Webhooks`.
   - Point to n8n server endpoint (`http://192.168.0.113:5678/webhook/...`) or FastAPI daemon.
   - On sale event: Parse buyer country, gross amount, and product name -> deliver Telegram bot notification to Pak Satya.
