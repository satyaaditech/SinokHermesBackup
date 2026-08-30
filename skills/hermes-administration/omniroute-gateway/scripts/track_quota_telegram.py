import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.expanduser('~/.omniroute/storage.sqlite')

def get_quota_report():
    if not os.path.exists(DB_PATH):
        return f"Error: Database tidak ditemukan di {DB_PATH}"
        
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
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        conn.close()
        return f"Query database gagal: {e}"
        
    conn.close()
    
    if not rows:
        return "Tidak ada data quota snapshot untuk penyedia 'antigravity'."
        
    data = {}
    for r in rows:
        email, model, pct, exh, reset = r
        if email not in data:
            data[email] = []
        data[email].append({
            'model': model,
            'remaining': pct,
            'exhausted': exh,
            'reset': reset
        })
        
    now_utc = datetime.now(timezone.utc)
    output = []
    output.append("📊 LAPORAN SISA KUOTA ANTIGRAVITY")
    output.append(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB\n")
    
    for email in sorted(data.keys()):
        models = data[email]
        output.append(f"🔹 Akun: {email}")
        output.append("```text")
        for m in models:
            model_display = m['model'].replace('gemini-', 'g-').replace('claude-', 'c-')
            pct = m['remaining']
            pct_int = int(round(pct))
            
            bar_len = int(round(pct_int / 10))
            bar_len = max(0, min(10, bar_len))
            bar = "█" * bar_len + "░" * (10 - bar_len)
            
            reset_str = m['reset']
            time_left_str = ""
            if reset_str:
                try:
                    reset_dt = datetime.fromisoformat(reset_str.replace('Z', '+00:00'))
                    delta = reset_dt - now_utc
                    total_sec = int(delta.total_seconds())
                    if total_sec > 0:
                        h = total_sec // 3600
                        m_left = (total_sec % 3600) // 60
                        time_left_str = f" ({h}h {m_left}m)"
                except Exception:
                    pass
            
            line = f"{model_display:<21}{bar} {pct_int:3d}%{time_left_str}"
            output.append(line)
        output.append("```\n")
        
    return "\n".join(output)

if __name__ == "__main__":
    print(get_quota_report())
