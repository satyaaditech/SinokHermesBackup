---
name: n8n-automation
description: Manage, create, and test n8n workflows via API and CLI.
---

# n8n Automation & Workflow Management

Manage n8n workflows directly from Hermes/Sinox on `n8nserver`.

## 🚨 MANDATORY GOLDEN RULE: 100% NATIVE NO-CODE BUILT-IN NODES
- **PRIORITASKAN NATIVE BUILT-IN NODES**: Setiap perancangan dan pembuatan workflow n8n WAJIB mengutamakan node bawaan resmi (`n8n-nodes-base.*` dan `@n8n/n8n-nodes-langchain.*`) untuk menyajikan kanvas visual berwarna penuh yang mudah dipahami, dirawat, dan diaudit.
- **CODE NODE HANYA JIKA SANGAT TERPAKSA**: Penggunaan custom JavaScript/Python Code node `{}` HANYA diizinkan jika fungsi yang dibutuhkan benar-benar mustahil dicapai dengan kombinasi native nodes (misal: regex biner kompleks khusus atau manipulasi buffer tingkat rendah).


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

## Workflow JSON Structure & Native Built-in Nodes Reference
When crafting n8n workflows:
- Nodes array contains objects with `id`, `name`, `type`, `typeVersion`, `position`, and `parameters`.
- Connections map node names to outputs/inputs.
- Always prefer Native Built-in Nodes over generic Code nodes `{}` for visual clarity and maintainability.

### Primary Built-in Node Types (n8n v2.36+):
1. **Flow & Logic**:
   - `n8n-nodes-base.webhook` (Triggers: GET/POST/PUT)
   - `n8n-nodes-base.respondToWebhook` (Fast synchronous HTTP responses)
   - `n8n-nodes-base.scheduleTrigger` (Cron / Interval schedules)
   - `n8n-nodes-base.if` (Multi-rule branching: String, Number, DateTime, Regex)
   - `n8n-nodes-base.switch` (Multi-route dispatch)
   - `n8n-nodes-base.loopOverItems` / `splitInBatches` (Batching / Rate limit avoidance)
   - `n8n-nodes-base.merge` (Append, Merge by Key, Combine, Multiplex)
   - `n8n-nodes-base.errorTrigger` (Global failure catcher & Telegram alert)
   - `n8n-nodes-base.stickyNote` (Visual documentation boxes on canvas)

2. **Data Transformation (No-Code)**:
   - `n8n-nodes-base.set` (Edit Fields: assign, rename, transform JSON)
   - `n8n-nodes-base.filter` / `n8n-nodes-base.removeDuplicates` (Data hygiene)
   - `n8n-nodes-base.summarize` / `n8n-nodes-base.aggregate` (Math & group-by calculations)
   - `n8n-nodes-base.html` / `n8n-nodes-base.markdown` (Extract web content & formatting)

3. **Apps & System Execution**:
   - `n8n-nodes-base.googleSheets` (Append, Update, Read, Delete rows with OAuth2)
   - `n8n-nodes-base.telegram` (Send Text Markdown/HTML, Photo, Video, Audio, Doc, Pin)
   - `n8n-nodes-base.httpRequest` (REST API client with OAuth2, Bearer, Multipart)
   - `n8n-nodes-base.executeCommand` (Linux CLI execution: FFmpeg, Python scripts)
   - `n8n-nodes-base.readWriteFile` (Direct disk storage operations)

4. **AI & LangChain Native Nodes**:
   - `@n8n/n8n-nodes-langchain.agent` (Autonomous Tools calling AI Agent)
   - `@n8n/n8n-nodes-langchain.lmChatOpenAi` (OmniRoute endpoint :20129 connector)
   - `@n8n/n8n-nodes-langchain.toolWorkflow` (Sub-workflows exposed as AI Tools)

## Design Patterns from n8n.io/workflows
1. **Sticky Note Canvas Architecture**: Document major sections with colored sticky notes (Yellow for Overview, Blue for Setup, Green for Quality Gates, Purple for AI/Outputs).
2. **Fast-Response Webhook Pattern**: Return `200 OK` or HTML instantly with `respondToWebhook`, then process heavy background tasks (FFmpeg / Docs / AI).
3. **Sub-Workflow Modularity (`executeWorkflow`)**: Separate heavy reusable tasks (e.g. Video Rendering, Sheet Logging) into isolated sub-workflows.
4. **Centralized Error Notifier**: Dedicate an Error Trigger workflow to post failures directly to Telegram Thread 4038 with retry instructions.

## AI Assistant & Sandbox Infrastructure
- **OmniRoute Adapter**: Port `20129` (`http://172.17.0.1:20129/v1`) translates streaming SSE to standard JSON for n8n AI verification.
- **Code Sandbox**: `http://sandbox-api:8080` (API Key: `satya-sandbox-key-2026`) backed by DinD runner `sandbox-runner-1`.
- **Search Engine**: `http://searxng:8080` (SearXNG self-hosted container).

