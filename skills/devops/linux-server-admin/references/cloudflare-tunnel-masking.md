# Cloudflare Tunnel Domain Masking for n8n

Configuration and maintenance of Cloudflare Tunnel (`cloudflared`) routing external web traffic to locally hosted services (e.g., n8n docker container).

## Service Information
On the host machine (`n8nserver`), the tunnel runs as a systemd service:
- **Service Name**: `cloudflared.service`
- **Config Path**: `/etc/cloudflared/config.yml`
- **Command**: `/usr/bin/cloudflared --no-autoupdate --config /etc/cloudflared/config.yml tunnel run`

## Configuration (`/etc/cloudflared/config.yml`)
```yaml
tunnel: b221a2b0-6dab-40de-942f-cc8ad2e2a646
credentials-file: /etc/cloudflared/b221a2b0-6dab-40de-942f-cc8ad2e2a646.json

ingress:
  # Route traffic for n8n custom domain to local docker port
  - hostname: n8n.satyaaditech.web.id
    service: http://localhost:5678

  # Catch-all: reject other hostnames with 404
  - service: http_status:404
```

## DNS Setup (Cloudflare Dashboard)
The target domain is configured as a `CNAME` record pointing to the Cloudflare-managed tunnel endpoint:
- **Hostname**: `n8n.satyaaditech.web.id`
- **Type**: `CNAME`
- **Target**: `b221a2b0-6dab-40de-942f-cc8ad2e2a646.cfargotunnel.com`
- **Proxy Status**: Proxied (Orange cloud)

## Common Commands
Check service status:
```bash
systemctl status cloudflared
```
Restart tunnel after config changes:
```bash
sudo systemctl restart cloudflared
```
View active logs:
```bash
journalctl -u cloudflared -f
```
