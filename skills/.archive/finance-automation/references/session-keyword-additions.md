# Session Keyword Additions Log

Running log of COA keyword additions made across sessions. Purpose: prevent re-work when similar descriptions recur, and document the evolution of the mapping.

## How to use this file

When a transaction description mis-classifies to "Beban Lain-lain" (or wrong COA) because a keyword is missing, add the keyword to `scripts/auto_finance.py` (`COA_RULES`) and `references/coa-keyword-mapping.md`, then record the addition here with session date and rationale.

## Log

### 2026-05-28 — Electronics/accessories default confirmed
- **Keyword**: `casing` (as in "casing HP iPhone")
- **User decision**: Keep as Beban Lain-lain (6900), NOT Peralatan (2000)
- **Rationale**: User explicitly said "Masukan saja ke pengeluaran lain-lain" when asked about category for phone accessories.
- **Status**: ✅ Documented in SKILL.md pitfall #11. Do NOT auto-map `casing` to Peralatan without asking.

### 2026-05-28 — Food keywords expanded
- **Added**: `sarapan`, `sop`
- **To COA**: Beban Makanan (6000)
- **Rationale**: "sarapan pagi sop Happy" mis-classified to Beban Lain-lain. User confirmed it's food expense.
- **Status**: ✅ Merged into `COA_RULES` and mapping table.

### 2026-05-27 (prior session) — Food keywords expanded
- **Added**: `bubur`, `soto`, `bakso`, `nasi`, `mie`, `ayam`
- **To COA**: Beban Makanan (6000)
- **Rationale**: Multiple food descriptions were falling through to Lain-lain.
- **Status**: ✅ Merged into `COA_RULES` and mapping table.

## Pending / To Evaluate

| Keyword | Description Example | Suggested COA | Needs User Confirmation |
|---------|---------------------|---------------|------------------------|
| `casing` | "casing HP iPhone 13 mini Shopee" | ~~Peralatan (2000)~~ → Beban Lain-lain (6900) | ✅ Resolved — user chose to keep as Beban Lain-lain |
| `shopee` | "beli barang di Shopee" | N/A (marketplace, not a COA) | ❌ No — platform keyword, not a classification signal |
| `iphone` | "casing HP iPhone" | N/A (brand, not a COA) | ❌ No — brand keyword, not a classification signal |

## Notes

- **Do NOT add platform keywords** (Shopee, Tokopedia, Grab, Gojek) as COA signals unless they are unambiguous for a single category. Platform names are method/context indicators, not expense type indicators.
- **Do NOT add brand keywords** (iPhone, Samsung, McDonald's) unless the brand is *exclusively* tied to one COA (e.g. "PLN" → Listrik & Air).
- **When in doubt**: ask the user "Mau dimasukkan ke kategori X atau Y?" and record their preference here before adding to the mapping.
