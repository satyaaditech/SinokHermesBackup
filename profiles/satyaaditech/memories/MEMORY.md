AI Automation Projects: /home/satyaaditech/yt-automation/ - Pipeline untuk research → extract → verify → generate dengan anti-hallucination verification. Target >80% verification rate. Output: script teleprompter bahasa Indonesia. Backup sources: kworb.net, chartika.com, youtrendings.com
§
Finance system v2: Spreadsheet 13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U. Google Drive: root 'finance' (1Rnsy7DuxI_2jHv2aGeDD-leNmOCBoggK) with 2026 subfolder + 23 COA folders. Navigator doc: https://docs.google.com/document/d/1eNOOCM7A7qR8hvQ_AFmAePNij_268b-DrM_YZNJtonA/edit. Skill: finance-automation (auto-classify tx, keyword->COA mapping, receipt upload). User prefers minimal responses after adding tx.
§
Google Workspace OAuth authenticated and active. Token at ~/.hermes/google_token.json, client_secret at ~/.hermes/google_client_secret.json. Scopes: Gmail (read/send/modify), Calendar, Drive, Sheets, Docs, Contacts. Google Cloud project: instant-pivot-497301-n2.
§
User Satya requires ALL reminders/cron jobs to ALWAYS deliver to Telegram — never [SILENT], never empty, never fail. This is critical for automation workflow. When creating any reminder, must use explicit prompt: "Pesan ini WAJIB dikirim, tidak boleh [SILENT], tidak boleh kosong, harus sampai ke Telegram user".
§
User decided to stay with Hermes Agent (not migrate to Workspace):
- Reason: Laptop RAM insufficient (6.7GB < 8GB required)
- Will optimize current setup instead of upgrading
- Open to exploring Workspace later if get VPS/cloud resources
§
Token optimization setup applied to Hermes Agent:
- Disabled 8 toolsets from default profile (browser, vision, image_gen, tts, moa, todo, clarify, session_search)
- Set max_turns from 90 to 40
- Compression threshold: 50% -> 35%, target_ratio: 20% -> 15%, protect_last: 20 -> 15
- Created 'irit' profile with max_turns 25, compression threshold 30%, target_ratio 10%, protect_last 10, and only 6 core toolsets (web, terminal, file, code_execution, skills, memory)
- User prefers cost-efficient token usage for daily operations