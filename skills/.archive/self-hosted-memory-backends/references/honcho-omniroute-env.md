# Honcho .env — n8nserver self-hosted via OmniRoute lokal
# Salin ke ~/honcho/.env. Ganti LLM_OPENAI_API_KEY jika OmniRoute berubah.
# OmniRoute base: http://100.92.237.45:20128/v1  (Tailscale, OpenRouter-compatible)
# Model recommendation:
#   - Gunakan custom combo aktif: `daily-chat` (atau `antigravity/gemini-3.7-flash-high`)
#   - JANGAN gunakan virtual combo `auto/cheap` bila free/noauth provider diblokir karena akan gagal 503 "all targets exhausted"

LLM_OPENAI_API_KEY=<OMNIROUTE_API_KEY>

# --- LLM Base: OmniRoute lokal (Tailscale) ---
OMNI_BASE=http://100.92.237.45:20128/v1

# --- Deriver (background user-model builder) ---
DERIVER_MODEL_CONFIG__MODEL=daily-chat
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Dialectic levels (reasoning) — Wajib per-level, tak ada default global ---
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL=daily-chat
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__low__MODEL_CONFIG__MODEL=daily-chat
DIALECTIC_LEVELS__low__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__medium__MODEL_CONFIG__MODEL=daily-chat
DIALECTIC_LEVELS__medium__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__high__MODEL_CONFIG__MODEL=daily-chat
DIALECTIC_LEVELS__high__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__max__MODEL_CONFIG__MODEL=daily-chat
DIALECTIC_LEVELS__max__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Summary ---
SUMMARY_MODEL_CONFIG__MODEL=daily-chat
SUMMARY_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Dream (consolidation) ---
DREAM_DEDUCTION_MODEL_CONFIG__MODEL=daily-chat
DREAM_DEDUCTION_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DREAM_INDUCTION_MODEL_CONFIG__MODEL=daily-chat
DREAM_INDUCTION_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Embedding ---
EMBEDDING_MODEL_CONFIG__MODEL=openrouter/openai/text-embedding-3-small
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
