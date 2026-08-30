# Quota Monitoring for OmniRoute

Details on how to inspect provider quotas, particularly for the proxy provider `antigravity`.

## DB Location & Schema
- SQLite Path: `~/.omniroute/storage.sqlite`
- Key tables:
  - `quota_snapshots`: Stores current/historical quota limits, next resets, and remaining percentages.
  - `provider_connections`: Details provider credentials and metadata (e.g. emails/projects mapped to connection IDs).

## Checking Quota Via Python Script
There is a helper script already configured to query and print the remaining quota percentages for all active Antigravity connections:
```bash
python3 ~/track_quota.py
```

To format and display the exact Telegram-compliant layout directly, use the script bundled in this skill:
```bash
python3 /home/satyaaditech/.hermes/skills/hermes-administration/omniroute-gateway/scripts/track_quota_telegram.py
```

## SQL Query
If querying the database manually via Python (e.g. when `sqlite3` binary is not installed):
```sql
SELECT 
    pc.email,
    s.window_key,
    s.remaining_percentage,
    s.is_exhausted,
    s.next_reset_at
FROM quota_snapshots s
INNER JOIN provider_connections pc ON s.connection_id = pc.id
INNER JOIN (
    SELECT connection_id, window_key, MAX(created_at) as max_created
    FROM quota_snapshots
    WHERE provider = 'antigravity'
    GROUP BY connection_id, window_key
) m ON s.connection_id = m.connection_id 
   AND s.window_key = m.window_key 
   AND s.created_at = m.max_created
WHERE s.provider = 'antigravity'
ORDER BY pc.email, s.window_key;
```

## Formatting & Presentation Requirements (Telegram)
When presenting the Antigravity remaining quota report to the user, ensure it strictly follows this layout. Wrap each account's list in a markdown code block to preserve column alignment on mobile clients.

### Required Output Template

```text
📊 LAPORAN SISA KUOTA ANTIGRAVITY
Waktu: YYYY-MM-DD HH:mm:ss WIB

🔹 Akun: satyaaditech@gmail.com
c-opus-4-6-thinking  ██████████ 100% (4h 56m)
c-sonnet-4-6         ██████████ 100% (4h 56m)
g-2.5-flash          ██████████  96% (4h 50m)
```

### Specific Formatting Rules
1. **Model Key Aliases**: Shorten standard key prefixes:
   - `gemini-` -> `g-`
   - `claude-` -> `c-`
2. **Left Alignment**: Align the model name column left to exactly 21 characters: `{model_display:<21}`.
   - Do NOT insert any additional spaces between the aligned name and the progress bar.
   - Example: `c-opus-4-6-thinking  ██████████` (exactly 2 spaces after the name).
3. **Percentage Formatting**: Round the remaining percentage to the nearest integer. Right-align it to a width of 3 characters: `{pct_int:3d}%`.
4. **Time Remaining Calculation**: Calculate the difference between `next_reset_at` and current UTC time. Format as ` ({hours}h {minutes}m)`. Omit the parenthetical suffix if `next_reset_at` is empty or not in the future.

## Agent Guidelines & Pitfalls
- **"Status Antigravity" Warning**: When the Javanese/Indonesian user asks check status of "antigravity" (e.g. "status antigravity"), they are referring to the **Antigravity provider quota** (API/Model usage limits on OmniRoute gateway). Do *not* interpret this as a query about the agent's system-level prompt identity or backend status. Immediately run `python3 ~/track_quota.py` or inspect the database to report their remaining quota.
