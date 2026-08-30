# Multi-Account Failover & Load Balancing in OmniRoute

When multiple active connections exist for the same provider (e.g. multiple `antigravity` Google Gemini accounts), OmniRoute manages routing across them using a combination of Session Affinity (LKGP), Least Recently Used (LRU) tie-breaks, and active rotation on errors.

## 1. Load Balancing (LRU & Consecutive Use)
When a session starts (or after a daily cache reset at ~04:02 WIB), OmniRoute selects from the pool of active and tested connections (`is_active = 1` and `test_status = 'active'`) for the target provider:
- It sorts eligible connections using the `compareLruConnections` algorithm.
- Primary sort: **Recency of use** (`lastUsedAt`). It prefers the connection that hasn't been used the longest (LRU).
- Secondary tie-breaker: **Consecutive Use Count** (`consecutiveUseCount`). It prefers the connection with fewer consecutive uses.
- Tertiary tie-breaker: **Connection Priority** (`priority`). It prefers a lower numeric priority score.

This ensures that load is evenly distributed among the available sibling accounts.

## 2. Session Affinity (LKGP)
To avoid unnecessary provider-switching during a conversation thread (which could cause user session fragmentation):
- Upon the first choice, OmniRoute binds the session key (`session_key`) to the selected connection ID.
- Subsequent calls within the same session will bypass the LRU scoring and stick to that pinned connection (Session Affinity) to preserve thread continuity.

## 3. Dynamic Failover (Backup Logic)
If the pinned connection fails during execution (e.g., hits a rate limit `429`, is quota-exhausted, or returns terminal errors):
- The affinity pin is cleared (`deleteSessionAccountAffinity`).
- OmniRoute rotates the model pool to the remaining active helper accounts.
- The next request automatically selects the next best ready connection.

## 4. Quota Tracking Query (Python Script)
To inspect the state of all active Antigravity account quotas dynamically, execute the following script:
```python
import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.expanduser('~/.omniroute/storage.sqlite')

def get_quota_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
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
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows
```
