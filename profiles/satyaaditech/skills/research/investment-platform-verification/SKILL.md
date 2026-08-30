---
name: investment-platform-verification
description: Systematic research workflow to verify if an investment platform, broker, or trading app is legitimate or potentially a scam. Uses multi-angle ddgs searches and produces structured risk assessment.
triggers:
  - "is this broker legit"
  - "scam or legit"
  - "investment platform review"
  - "broker scam check"
  - "trading app verification"
  - "quotex"
  - "qxbroker"
  - "forex broker scam"
---

# Investment Platform Verification Workflow

Systematically research investment platforms, brokers, or trading apps to determine legitimacy and identify red flags.

## When to Use

- User asks "is [platform] a scam?"
- Researching forex/crypto/binary options brokers
- Verifying investment apps before depositing money
- Due diligence on trading platforms

## Research Workflow (6 Angles)

Run these ddgs searches in parallel for comprehensive coverage:

### 1. General Reviews & Scam Reports
```bash
ddgs text -q "[PLATFORM_NAME] broker review scam legit" -m 10
ddgs text -q "[PLATFORM_NAME] trustpilot reviews rating" -m 10
```

### 2. Regulation & Licensing
```bash
ddgs text -q "[PLATFORM_NAME] regulation license FCA SEC ASIC CySEC" -m 10
ddgs text -q "[PLATFORM_NAME] IFMRRC regulation" -m 8
```

### 3. Withdrawal Problems & Complaints
```bash
ddgs text -q "[PLATFORM_NAME] withdrawal problems complaints" -m 10
ddgs text -q "[PLATFORM_NAME] user complaints reddit" -m 8
```

### 4. Official Warnings
```bash
ddgs text -q "FCA warning [PLATFORM_NAME] broker" -m 10
ddgs text -q "Financial Commission [PLATFORM_NAME] warning" -m 8
ddgs text -q "[PLATFORM_NAME] SEC warning" -m 8
```

### 5. Company Structure
```bash
ddgs text -q "[PLATFORM_NAME] LTD company registration Seychelles" -m 8
ddgs text -q "[PLATFORM_NAME] owner country company location" -m 8
```

### 6. Availability & Restrictions
```bash
ddgs text -q "[PLATFORM_NAME] available countries banned" -m 8
ddgs text -q "[PLATFORM_NAME] legal in Europe USA" -m 8
```

## Red Flags Checklist

Mark each red flag found during research:

| # | Red Flag | Weight |
|---|----------|--------|
| ☐ | No tier-1 regulation (FCA, SEC, ASIC, CySEC, BaFin) | CRITICAL |
| ☐ | Claims regulation from non-official body (IFMRRC, etc.) | HIGH |
| ☐ | Offshore company (Seychelles, St. Vincent, etc.) | HIGH |
| ☐ | Official warning from Financial Commission or regulator | CRITICAL |
| ☐ | Multiple withdrawal complaints | HIGH |
| ☐ | Accounts blocked when withdrawing | HIGH |
| ☐ | Not available in regulated markets (EU, USA, Canada) | MEDIUM |
| ☐ | Binary options / CFDs with high leverage | MEDIUM |
| ☐ | Fake Trustpilot reviews (suspicious patterns) | MEDIUM |
| ☐ | Aggressive marketing on social media/Telegram | LOW |

## Scoring System

Count red flags and assign risk level:

- **0-1 red flags:** Likely legitimate (but still verify)
- **2-3 red flags:** Exercise caution, limited investment only
- **4-6 red flags:** High risk, avoid if possible
- **7+ red flags:** Almost certainly a scam, AVOID COMPLETELY

## Output Format

Structure findings for Telegram (NO markdown tables):

```
🚨 VERDIK: [SCAM / HIGH RISK / SUSPICIOUS / LIKELY LEGIT]

📋 REGULASI:
▸ [Status: Regulated/Unregulated]
▸ [Details about claimed vs actual regulation]

⚠️ PERINGATAN RESMI:
▸ [List any official warnings]

💸 MASALAH WITHDRAWAL:
▸ [Summary of user complaints]

🏢 STRUKTUR PERUSAHAAN:
▸ [Company name, location, jurisdiction]

🚩 RED FLAGS DITEMUKAN: [X/10]
1. [Red flag 1]
2. [Red flag 2]
...

💡 REKOMENDASI: [Avoid / Caution / Proceed with care]
```

## Common Scam Patterns

### Pattern 1: Fake Regulation
- Claims IFMRRC, FMRRC, or similar non-government bodies
- IFMRRC cert expired but still displayed
- Mentions "regulated" without specifying by whom

### Pattern 2: Offshore Shell
- Registered in Seychelles, St. Vincent & Grenadines, Marshall Islands
- No physical office address
- Company name changes frequently

### Pattern 3: Withdrawal Trap
- Easy deposits, impossible withdrawals
- "Verification" delays when withdrawing
- Account suspended after profit requests
- Support stops responding

### Pattern 4: Review Manipulation
- Trustpilot flooded with 5-star reviews in short period
- Generic review text ("Great platform!", "Amazing!")
- Negative reviews claim they can't withdraw

## What I Learned From Quotex Research

**Tool Issues Encountered:**
- ddgs CLI uses `-q` and `-m` flags (NOT `-n`)
- Python `duckduckgo_search` module may not be installed in environment
- Use `ddgs text --help` to check available options

**Research Insights:**
- IFMRRC is NOT a real regulator (common trick)
- Financial Commission warning list is authoritative
- TrustScore 51/100 is very low for financial services
- Offshore + no tier-1 reg + withdrawal issues = classic scam profile

## Verification Sources Priority

**Authoritative (weight: HIGH):**
- financialcommission.org (warning list)
- fca.org.uk (UK regulator)
- sec.gov (US regulator)
- asic.gov.au (Australia regulator)

**Reliable (weight: MEDIUM):**
- BrokerChooser, BrokersView, BrokerChecker
- TrustFinance, RealReviews
- trustpilot.com (with skepticism)

**User Reports (weight: LOW-MEDIUM):**
- Reddit (r/Forex, r/BinaryOptions, r/Scams)
- Quora
- ComplaintsBoard, SikayetVar

## Post-Research Actions

After completing research:
1. Cross-reference at least 3 independent sources
2. Check if claims match across sources
3. Look for patterns in user complaints
4. Verify regulation claims on official regulator websites
5. Produce final verdict with confidence level

## Example Search Patterns by Platform Type

**Forex Broker:**
- Add: "spread manipulation", "stop hunting", "slippage"

**Crypto Exchange:**
- Add: "custody issues", "hack history", "withdrawal frozen"

**Binary Options:**
- Add: "price manipulation", "rigged platform"

**Investment App:**
- Add: "Ponzi scheme", "pyramid scheme", "guaranteed returns"
