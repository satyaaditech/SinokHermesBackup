# Date Verification — Incident Log

## Incident: 28 May 2026 Calendar Query Error

**What happened:**
- Current date: Wednesday, 27 May 2026
- User asked: "besok ada jadwal apa" (tomorrow = 28 May)
- Agent manually calculated date as 29 May (off by +1)
- Query returned empty results
- User corrected: "salah, seharusnya 28 Mei"

**Root cause:**
Mental date arithmetic (`27 + 1 = 28` was computed as `29`). Cognitive interference from previous context where 28 May was referenced as "today" in transaction records.

**Fix applied:**
- Immediate: Re-queried calendar with correct date (28 May)
- Permanent: Added "Date Verification — Zero Tolerance Rule" to `cron-reminder-notification/SKILL.md`
- Memory rule: NEVER calculate dates mentally; ALWAYS use `datetime.now() + timedelta(days=N)`

**Verification snippet (Python):**
```python
from datetime import datetime, timedelta
today = datetime.now()
print(f"Today     : {today.strftime('%Y-%m-%d %A')}")
print(f"Tomorrow  : {(today + timedelta(days=1)).strftime('%Y-%m-%d %A')}")
print(f"Yesterday : {(today - timedelta(days=1)).strftime('%Y-%m-%d %A')}")
```

## Related Impact

This error class also affects:
- Finance transaction dates (auto_finance.py defaults to `datetime.now()`)
- Cron job scheduling (wrong target date = reminder fires on wrong day)
- Report generation (date ranges shifted by 1 day)

**User expectation:** 100% appointment accuracy. Zero tolerance for missed events due to date errors.
