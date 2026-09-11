---
name: n8n-automation
description: Manage, create, and test n8n workflows via API and CLI.
---

# n8n Automation & Workflow Management

Manage n8n workflows directly from Hermes/Sinox on `n8nserver`.

## Key Environment & Endpoints
- **Base URL (Local)**: `http://localhost:5678`
- **Public Domain**: `https://n8n.satyaaditech.web.id`
- **Shared Storage**: `/home/satyaaditech/shorts_factory` -> mounted inside container as `/data_shared`
- **CLI Utility**: `~/.hermes/bin/n8n-manager`
- **Credentials**: `N8N_API_KEY` stored in `~/.hermes/.env`

## Common Commands (`n8n-manager`)

### 1. Health & Status
```bash
~/.hermes/bin/n8n-manager health
```

### 2. List Workflows
```bash
~/.hermes/bin/n8n-manager list --limit=20
~/.hermes/bin/n8n-manager list --filter="YouTube"
~/.hermes/bin/n8n-manager list --active=true
```

### 3. Inspect Workflow
```bash
~/.hermes/bin/n8n-manager get <WORKFLOW_ID>
~/.hermes/bin/n8n-manager get <WORKFLOW_ID> --json
```

### 4. Create & Activate Workflow
```bash
~/.hermes/bin/n8n-manager create --file=/path/to/workflow.json --activate
```

### 5. Update Workflow
```bash
~/.hermes/bin/n8n-manager update <WORKFLOW_ID> --file=/path/to/updated.json
```

### 6. Activate / Deactivate / Delete
```bash
~/.hermes/bin/n8n-manager activate <WORKFLOW_ID>
~/.hermes/bin/n8n-manager deactivate <WORKFLOW_ID>
~/.hermes/bin/n8n-manager delete <WORKFLOW_ID>
```

### 7. Trigger Webhook & Test Execution
```bash
# Trigger active webhook
~/.hermes/bin/n8n-manager trigger <path> --data='{"key": "value"}'

# Trigger test webhook (/webhook-test/)
~/.hermes/bin/n8n-manager trigger <path> --test --data='{"key": "value"}'
```

### 8. Check Executions, Debug & Partial Re-Run
```bash
# List recent executions
~/.hermes/bin/n8n-manager executions --limit=5

# Filter by workflow or status
~/.hermes/bin/n8n-manager executions --workflow-id=<WORKFLOW_ID> --status=error

# Inspect failed execution log and error traces
~/.hermes/bin/n8n-manager executions --id=<EXECUTION_ID>

# Partial Re-Run / Retry from failed node (tanpa mengulang node yang sudah sukses)
~/.hermes/bin/n8n-manager retry <EXECUTION_ID>
```

## Self-Healing & Troubleshooting Protocol
1. **Monitor**: Saat workflow gagal, ambil `EXECUTION_ID` dan periksa node mana yang error serta pesan errornya (`executions --id=<ID>`).
2. **Diagnose & Patch**: Perbaiki kode node / parameter via skrip Python atau API (`n8n-manager update <WF_ID>`).
3. **Partial Re-Run**: Jalankan `n8n-manager retry <EXECUTION_ID>`. n8n akan melanjutkan eksekusi dari node yang gagal tanpa mengulang proses berat (seperti video rendering) yang sudah selesai.

## Workflow JSON Structure Reference
When crafting n8n workflows:
- Nodes array contains objects with `id`, `name`, `type` (e.g. `n8n-nodes-base.webhook`, `n8n-nodes-base.code`, `n8n-nodes-base.httpRequest`, `n8n-nodes-base.respondToWebhook`), `typeVersion`, `position`, and `parameters`.
- Connections map node names to outputs/inputs.
- In JavaScript Code nodes (`n8n-nodes-base.code`), use `$input.first().json` or `$input.all()` to access incoming items.
