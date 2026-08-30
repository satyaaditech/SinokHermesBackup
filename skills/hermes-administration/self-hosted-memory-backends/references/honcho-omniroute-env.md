# Honcho .env — n8nserver self-hosted via OmniRoute lokal
# Salin ke ~/honcho/.env. Ganti LLM_OPENAI_API_KEY jika OmniRoute berubah.
# OmniRoute base: http://100.92.237.45:20128/v1  (Tailscale, OpenRouter-compatible)
# Model hemat: auto/cheap

LLM_OPENAI_API_KEY=<OMNIROUTE_API_KEY>

# --- Deriver (background user-model builder) ---
DERIVER_MODEL_CONFIG__MODEL=auto/cheap
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Dialectic levels (reasoning) — Wajib per-level, tak ada default global ---
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL=auto/cheap
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__low__MODEL_CONFIG__MODEL=auto/cheap
DIALECTIC_LEVELS__low__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__medium__MODEL_CONFIG__MODEL=auto/cheap
DIALECTIC_LEVELS__medium__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__high__MODEL_CONFIG__MODEL=auto/cheap
DIALECTIC_LEVELS__high__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DIALECTIC_LEVELS__max__MODEL_CONFIG__MODEL=auto/cheap
DIALECTIC_LEVELS__max__MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Summary ---
SUMMARY_MODEL_CONFIG__MODEL=auto/cheap
SUMMARY_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Dream (consolidation) ---
DREAM_DEDUCTION_MODEL_CONFIG__MODEL=auto/cheap
DREAM_DEDUCTION_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1
DREAM_INDUCTION_MODEL_CONFIG__MODEL=auto/cheap
DREAM_INDUCTION_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1

# --- Embedding (OmniRoute mendukung embedding OpenAI-compatible) ---
EMBEDDING_MODEL_CONFIG__MODEL=openrouter/openai/text-embedding-3-small
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=http://100.92.237.45:20128/v1