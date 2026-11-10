#!/usr/bin/env python3
"""
n8n Dynamic Cluster Workflow Runner v3.0 (Unified Dual-Server Edition)
Empowers Sinox (ROG) and Parjo (Ubuntu) Hermes Agents to seamlessly discover,
trigger, and monitor n8n workflows across both servers in real-time.
"""

import os
import sys
import json
import socket
import urllib.request
import urllib.error

# Server Endpoints & Credentials
ROG_API_KEY_DEFAULT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMmRiMzFjYy1jMzczLTRjNTctYjk3Yy01Y2FkODc2YTQ1NTUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiYjVmMzg1N2MtNjA4Zi00NmI5LTg2YmEtNzljNDcxYmI3YjU2IiwiaWF0IjoxNzk0MjcyNzA0fQ.EWupEvXx6iibwDfHDMEbUYQbBrHySwiexD0Km0nn9Ig"
PARJO_API_KEY_DEFAULT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5MjUyY2Y0Ni04NzFkLTRhNTItOTUwOC04ZTUzMDAxMmFhZGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZjFiOGQ4M2MtMWE3Ny00MDhhLTljMDUtMDk2Y2MwNDAyZDg0IiwiaWF0IjoxNzg5MDk5NDgyfQ.tTYQJ6MJSM0q87C777J3x8V8sjluc5_FasHCYMBvwN0"

def is_running_on_rog():
    host = socket.gethostname().lower()
    if os.name == 'nt' or "laptop" in host or "rog" in host:
        return True
    try:
        req = urllib.request.Request("http://n8n:5678/healthz")
        with urllib.request.urlopen(req, timeout=0.5) as resp:
            if resp.status == 200:
                return True
    except Exception:
        pass
    return False

def get_server_config():
    on_rog = is_running_on_rog()
    
    if on_rog:
        rog_candidates = [
            os.environ.get("N8N_ROG_BASE_URL"),
            "http://n8n:5678",
            "http://127.0.0.1:5678",
            "http://100.74.255.26:5678",
            "http://192.168.1.11:5678"
        ]
        parjo_candidates = [
            os.environ.get("N8N_PARJO_BASE_URL"),
            "http://100.92.237.45:5678",
            "http://192.168.1.6:5678",
            "https://n8n.satyaaditech.web.id"
        ]
    else:
        rog_candidates = [
            os.environ.get("N8N_ROG_BASE_URL"),
            "http://100.74.255.26:5678",
            "http://192.168.1.11:5678"
        ]
        parjo_candidates = [
            os.environ.get("N8N_PARJO_BASE_URL"),
            "http://localhost:5678",
            "http://127.0.0.1:5678",
            "http://100.92.237.45:5678",
            "http://192.168.1.6:5678",
            "https://n8n.satyaaditech.web.id"
        ]

    # Resolve active URL dynamically via fast healthz probe
    def pick_active_url(candidates, default_fallback):
        valid = [c.rstrip("/") for c in candidates if c]
        for url in valid:
            try:
                req = urllib.request.Request(f"{url}/healthz")
                with urllib.request.urlopen(req, timeout=0.6) as resp:
                    if resp.status == 200:
                        return url
            except Exception:
                continue
        return default_fallback

    rog_url = pick_active_url(rog_candidates, "http://n8n:5678" if on_rog else "http://100.74.255.26:5678")
    parjo_url = pick_active_url(parjo_candidates, "http://100.92.237.45:5678" if on_rog else "http://localhost:5678")

    rog_key = os.environ.get("N8N_ROG_API_KEY") or ROG_API_KEY_DEFAULT
    parjo_key = os.environ.get("N8N_PARJO_API_KEY") or os.environ.get("N8N_API_KEY") or PARJO_API_KEY_DEFAULT

    return {
        "rog": {
            "name": "ROG Zephyrus (Sinox)",
            "base_url": rog_url,
            "api_key": rog_key,
            "candidates": [c for c in rog_candidates if c]
        },
        "parjo": {
            "name": "Ubuntu Server (Parjo)",
            "base_url": parjo_url,
            "api_key": parjo_key,
            "candidates": [c for c in parjo_candidates if c]
        }
    }

def fetch_workflows_from_server(server_key, cfg):
    base_url = cfg["base_url"]
    api_key = cfg["api_key"]
    url = f"{base_url}/api/v1/workflows"
    headers = {"X-N8N-API-KEY": api_key, "User-Agent": "Hermes-Dynamic-Runner/3.0"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            workflows = []
            for item in data.get("data", []):
                w_id = item.get("id")
                w_name = item.get("name")
                is_active = item.get("active", False)
                nodes = item.get("nodes", [])

                webhooks = []
                for node in nodes:
                    n_type = node.get("type", "")
                    if any(t in n_type for t in ["webhook", "formTrigger", "chatTrigger"]):
                        params = node.get("parameters", {})
                        wh_path = params.get("path", "")
                        wh_id = node.get("webhookId", "")
                        if not wh_path:
                            if "chat" in n_type and wh_id:
                                wh_path = f"{wh_id}/chat"
                            elif wh_id:
                                wh_path = wh_id

                        wh_method = params.get("httpMethod", "POST" if "chat" not in n_type else "GET/POST")
                        wh_kind = "Form" if "form" in n_type else ("Chat" if "chat" in n_type else "Webhook")
                        wh_node = node.get("name", wh_kind)
                        if wh_path:
                            webhooks.append({"path": wh_path, "method": wh_method, "kind": wh_kind, "node": wh_node})

                workflows.append({
                    "id": w_id,
                    "name": w_name,
                    "active": is_active,
                    "webhooks": webhooks,
                    "server": server_key,
                    "server_name": cfg["name"]
                })
            return workflows, None
    except Exception as e:
        return [], str(e)

def check_health_server(server_key, cfg):
    url = f"{cfg['base_url']}/healthz"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return True, data
    except Exception as e:
        return False, str(e)

def trigger_webhook(server_key, cfg, webhook_path, payload=None):
    base_url = cfg["base_url"]
    clean_path = webhook_path.lstrip("/")
    if not clean_path.startswith("webhook/"):
        full_url = f"{base_url}/webhook/{clean_path}"
    else:
        full_url = f"{base_url}/{clean_path}"

    payload_data = payload or {}
    json_bytes = json.dumps(payload_data).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Hermes-Dynamic-Runner/3.0"
    }

    req = urllib.request.Request(full_url, data=json_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=35.0) as response:
            res_body = response.read().decode("utf-8")
            try:
                parsed = json.loads(res_body)
                return {
                    "status": "success",
                    "http_code": response.status,
                    "server": cfg["name"],
                    "target_url": full_url,
                    "response": parsed
                }
            except Exception:
                return {
                    "status": "success",
                    "http_code": response.status,
                    "server": cfg["name"],
                    "target_url": full_url,
                    "raw_response": res_body
                }
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return {
            "status": "error",
            "http_code": e.code,
            "server": cfg["name"],
            "target_url": full_url,
            "error": err_body
        }
    except Exception as e:
        return {
            "status": "error",
            "server": cfg["name"],
            "target_url": full_url,
            "error": str(e)
        }

def print_help():
    print("=== n8n Dynamic Cluster Workflow Runner v3.0 ===")
    print("Usage:")
    print("  n8n_runner.py list [--target rog|parjo|all]      # Lihat seluruh alur kerja cluster")
    print("  n8n_runner.py health [--target rog|parjo|all]    # Cek kesehatan n8n node")
    print("  n8n_runner.py trigger <wf/webhook> [json] [--target rog|parjo]")
    print("")
    print("Contoh:")
    print("  n8n_runner.py list")
    print("  n8n_runner.py trigger 'Pabrik Konten' '{\"topic\": \"Filsafat Jawa\"}'")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    configs = get_server_config()

    # Parse --target flag if present
    target_arg = "all"
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--target="):
            target_arg = arg.split("=", 1)[1].lower()
        elif arg == "--target" and i + 1 < len(sys.argv):
            target_arg = sys.argv[i + 1].lower()

    if cmd == "health":
        print("=== 🏥 N8N CLUSTER HEALTH CHECK ===")
        targets = ["rog", "parjo"] if target_arg == "all" else [target_arg]
        for t in targets:
            if t not in configs:
                continue
            cfg = configs[t]
            ok, res = check_health_server(t, cfg)
            status_symbol = "✅ ONLINE" if ok else "❌ OFFLINE"
            print(f"[{status_symbol}] {cfg['name']} -> {cfg['base_url']}")
            if not ok:
                print(f"   └─ Error: {res}")
            else:
                print(f"   └─ Response: {res}")
        sys.exit(0)

    if cmd == "list":
        targets = ["rog", "parjo"] if target_arg == "all" else [target_arg]
        for t in targets:
            if t not in configs:
                continue
            cfg = configs[t]
            print(f"\n=== 🌐 SERVER: {cfg['name']} ({cfg['base_url']}) ===")
            wfs, err = fetch_workflows_from_server(t, cfg)
            if err:
                print(f"⚠️ Gagal mengambil workflow: {err}")
                continue

            active_count = sum(1 for w in wfs if w["active"])
            print(f"Total Workflows: {len(wfs)} (Aktif: {active_count})\n")
            for wf in wfs:
                status_tag = "[AKTIF]       " if wf["active"] else "[TIDAK AKTIF] "
                print(f"{status_tag} {wf['name']} (ID: {wf['id']})")
                if wf["webhooks"]:
                    for wh in wf["webhooks"]:
                        print(f"   └─ Webhook ({wh['method']}): /webhook/{wh['path']}")
                else:
                    print("   └─ (Tidak memiliki webhook trigger aktif)")
                print("-" * 65)
        sys.exit(0)

    if cmd in ["trigger", "run"]:
        if len(sys.argv) < 3:
            print("Error: Harap sertakan nama workflow, ID, atau webhook path.")
            print("Contoh: n8n_runner.py trigger 'Pabrik Konten' '{\"topic\": \"Filsafat Jawa\"}'")
            sys.exit(1)

        query = sys.argv[2]
        payload = {}
        for arg in sys.argv[3:]:
            if arg.startswith("{") and arg.endswith("}"):
                try:
                    payload = json.loads(arg)
                    break
                except Exception as e:
                    print(f"Warning: Payload JSON tidak valid ({e}), dilewati.")

        # Search across targets
        targets = ["rog", "parjo"] if target_arg == "all" else [target_arg]
        matched_item = None
        matched_target = None

        clean_q = query.strip().lower()
        for t in targets:
            cfg = configs[t]
            wfs, _ = fetch_workflows_from_server(t, cfg)
            # 1. Match webhook path
            for wf in wfs:
                for wh in wf.get("webhooks", []):
                    if wh["path"].lower() == clean_q or wh["path"].lower() == f"webhook/{clean_q}":
                        matched_item = (wh["path"], wf)
                        matched_target = t
                        break
                if matched_item:
                    break
            if matched_item:
                break

            # 2. Match ID
            for wf in wfs:
                if wf["id"].lower() == clean_q:
                    wh_path = wf["webhooks"][0]["path"] if wf.get("webhooks") else None
                    matched_item = (wh_path, wf)
                    matched_target = t
                    break
            if matched_item:
                break

            # 3. Match Name substring
            for wf in wfs:
                if clean_q in wf["name"].lower():
                    wh_path = wf["webhooks"][0]["path"] if wf.get("webhooks") else None
                    matched_item = (wh_path, wf)
                    matched_target = t
                    break
            if matched_item:
                break

        if not matched_item:
            # Fallback direct webhook trigger on primary target
            prim_target = targets[0]
            cfg = configs[prim_target]
            print(f"Pemicu langsung via Webhook: /webhook/{query} pada {cfg['name']}")
            res = trigger_webhook(prim_target, cfg, query, payload)
            print(json.dumps(res, indent=2, ensure_ascii=False))
            sys.exit(0 if res.get("status") == "success" else 1)

        wh_path, wf = matched_item
        if not wh_path:
            print(f"Error: Workflow '{wf['name']}' ditemukan pada {configs[matched_target]['name']} namun tidak memiliki Webhook aktif!")
            sys.exit(1)

        cfg = configs[matched_target]
        print(f"Target Server: {cfg['name']}")
        print(f"Matched Workflow: '{wf['name']}' (ID: {wf['id']})")
        print(f"Webhook URL: {cfg['base_url']}/webhook/{wh_path}")
        print(f"Payload: {json.dumps(payload)}")
        print("Memicu alur kerja...")

        res = trigger_webhook(matched_target, cfg, wh_path, payload)
        print("\nHasil Pemicu:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("status") == "success" else 1)

if __name__ == "__main__":
    main()
