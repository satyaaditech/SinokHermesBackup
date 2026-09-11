# n8n Automation via Docker CLI and REST API

This reference details patterns for programmatic inspection, creation, execution, and testing of n8n workflows on `n8nserver`.

## Server & Container Topology
- **Container Name**: `n8n_app` (runs as user `node`)
- **Web UI & REST API Port**: `5678` (`http://localhost:5678`, public via Cloudflare Tunnel `https://n8n.satyaaditech.web.id/`)
- **Data Directory**: `/opt/n8n/n8n_data` (mounted inside container as `/home/node/.n8n`)
- **Shared Data Directory**: `/home/satyaaditech/shorts_factory` (mounted inside container as `/data_shared`)
- **Database**: SQLite at `/opt/n8n/n8n_data/database.sqlite`

---

## Method 1: Direct Docker CLI (No API Key Required)

Run CLI commands directly inside the running container as user `node`:

### 1. List All Workflows
```bash
docker exec -u node n8n_app n8n list:workflow
```
Returns list of workflows in format `<workflow_id>|<workflow_name>`.

### 2. Export Workflow to JSON
```bash
# Export single workflow to shared directory
docker exec -u node n8n_app n8n export:workflow --id=<workflow_id> --output=/data_shared/workflow_<workflow_id>.json

# Export all workflows
docker exec -u node n8n_app n8n export:workflow --all --output=/data_shared/workflows_backup/
```

### 3. Import Workflow from JSON
```bash
# Import workflow from shared directory
docker exec -u node n8n_app n8n import:workflow --input=/data_shared/new_workflow.json --activeState=fromJson
```

### 4. Execute Workflow Directly via CLI
```bash
docker exec -u node n8n_app n8n execute --id=<workflow_id> --rawOutput
```

---

## Method 2: n8n REST API (Full Programmatic CRUD & Webhooks)

Requires an API Key generated from n8n Web UI:
- Navigate to **Settings** (gear icon) -> **n8n API** -> **Create an API key** (`n8n_api_...`).

### Base Endpoints
- Base URL: `http://localhost:5678/api/v1`
- Header: `X-N8N-API-KEY: <api_key>`

### Common API Operations

1. **List Workflows**:
   ```bash
   curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/workflows
   ```

2. **Get Workflow by ID**:
   ```bash
   curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/workflows/<workflow_id>
   ```

3. **Create Workflow**:
   ```bash
   curl -s -X POST http://localhost:5678/api/v1/workflows \
     -H "X-N8N-API-KEY: $N8N_API_KEY" \
     -H "Content-Type: application/json" \
     -d @workflow_payload.json
   ```

4. **Activate / Deactivate Workflow**:
   ```bash
   curl -s -X POST http://localhost:5678/api/v1/workflows/<workflow_id>/activate \
     -H "X-N8N-API-KEY: $N8N_API_KEY"
   ```

5. **Test Webhook Trigger**:
   - Production URL: `https://n8n.satyaaditech.web.id/webhook/<path>` or `http://localhost:5678/webhook/<path>`
   - Test URL: `http://localhost:5678/webhook-test/<path>`
   ```bash
   curl -s -X POST http://localhost:5678/webhook/<path> \
     -H "Content-Type: application/json" \
     -d '{"test": true, "message": "hello"}'
   ```
