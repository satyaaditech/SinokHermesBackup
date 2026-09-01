# Troubleshooting Broken Models in OmniRoute Combos

## Problem
When upstream providers (like Antigravity) deprecate or remove models, Hermes chat sessions may begin failing with 400 errors or immediate drops. For example, Antigravity deprecation returns plain text mid-stream: `Gemini 3.5 Flash is no longer available. Please switch to Gemini 3.7 Flash in the latest version of Antigravity.`. This happens because the active combo (e.g., `daily-chat`) is attempting to route to a dead model ID.

## Resolution Workflow (Telegram & OmniRoute)
The user explicitly defined this as the correct, safe workflow to restore service without breaking session routing:

1. **Edit the Combo**: Access OmniRoute (via Dashboard or modifying the SQLite DB). Open the configuration for the failing combo (e.g., `daily-chat`).
2. **Re-route to Active Models**: Remove the dead/invalid model from the combo's fallback chain and slot in a currently active model of equivalent capability (e.g., swap a deprecated flash model for `qwen3.7-plus` or a newer `gemini` variant).
3. **Save**: Save the updated combo configuration.
4. **Restart Gateway**: Restart the OmniRoute gateway service to clear routing caches and force it to pick up the new combo data.
5. **Drop Telegram Session State**: In the Telegram chat, the user **MUST send `/new`**. This is critical: existing Telegram sessions often lock onto the exact old model ID mid-conversation. Even if the gateway is fixed, continuing an old session may still trigger errors. `/new` forces a fresh request through the updated gateway route.
6. **Check Hermes Auxiliary Vision**: If a Flash model was deprecated/replaced, verify and update `auxiliary.vision` in Hermes config (`hermes config get auxiliary.vision`). Auxiliary vision points directly to an upstream model ID rather than a combo, so it will 404 if not updated (`hermes config set auxiliary.vision.model antigravity/antigravity/antigravity/gemini-3.7-flash-low`). Note the multi-level prefix quirk from OmniRoute's model listing.

## Introspection Techniques (Headless/CLI)

If you need to verify which models are dead or active without the OmniRoute UI:

**1. Querying Combo Configurations via SQLite**
Combos are stored as JSON in the local database.
```python
import sqlite3, json, os

db = os.path.expanduser('~/.omniroute/storage.sqlite')
c = sqlite3.connect(db).cursor()
# The 'data' column contains the JSON definition of the models in the combo
c.execute("SELECT name, data FROM combos WHERE name = 'daily-chat'")
print(json.loads(c.fetchone()[1]))
```

**2. Verifying Available Provider Models via API**
To verify which models are currently broadcasted as available by OmniRoute for a specific provider (e.g., `antigravity`), hit the standard `v1/models` endpoint locally:
```python
import urllib.request, json
req = urllib.request.Request("http://localhost:20128/v1/models")
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    ag_models = [m['id'] for m in data.get('data', []) if m['id'].startswith('antigravity/')]
    print(ag_models)
```