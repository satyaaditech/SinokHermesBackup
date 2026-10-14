# Root Disk Diagnostics, Zero-Downtime Cleanup, and LVM Expansion

Operational procedures for diagnosing root partition (`/`) exhaustion, safely reclaiming space without service interruption, and executing online LVM expansions on Ubuntu servers.

## 1. Diagnostics & Partition Inspection

### Inspect Root Space & LVM Topology
```bash
# Check filesystem utilization
df -h / /boot /boot/efi

# Inspect physical disk vs LVM volume size
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE
```

**Common Ubuntu Installer Pattern:**
Ubuntu Server often provisions only 100GB to `ubuntu--vg-ubuntu--lv` at installation time, even on 240GB+ SSDs (`sda3`), leaving the remaining space unallocated in the volume group (`ubuntu-vg`).

### Profile Space Consumers (No Sudo Required)
```bash
# Check top directories under /home
du -h -d 1 /home/satyaaditech 2>/dev/null | sort -hr | head -15

# Inspect Docker consumption (images, containers, build cache)
docker system df

# Check systemd journal log disk usage
journalctl --disk-usage
```

---

## 2. Zero-Downtime Safe Disk Cleanup

When root space is constrained (>80%), reclaim disk space safely without impacting running services:

### A. Docker Build Cache (High Yield, Zero Risk)
Docker build cache accumulates multi-gigabyte build artifacts over time that are completely independent of running containers.
```bash
# Reclaim build cache (often frees 10-15+ GB)
docker builder prune -f
```

### B. Stopped Containers & Dangling Images
```bash
# Remove dead/exited containers
docker container prune -f

# Remove untagged (<none>) dangling images
docker image prune -f
```

### C. Targeted Removal of Obsolete Images
Do **not** run `docker image prune -a` blindly if services dynamically spawn worker/sandbox containers (e.g. n8n runner sandbox images).
Instead:
1. Verify active images: `docker ps --format "table {{.Names}}\t{{.Image}}"`
2. Verify orphan images: `docker images`
3. Remove specific obsolete images: `docker rmi <image-id-or-tag>`

### D. What NEVER to Touch
- **Docker Volumes**: Never run `docker volume prune` or `docker system prune --volumes`. Databases (Postgres, pgvector, Redis) and n8n application state reside in persistent Docker volumes.
- **AI Model Weights**: Avoid clearing `~/.cache/whisper` or similar local model caches unless authorized, as re-downloading consumes significant bandwidth and time.

### E. Package Manager & Temporary Cache Cleanup
```bash
# Clean uv Python package cache
uv cache clean

# Clean npm cache
npm cache clean --force

# Clean stale temporary scratch files older than 24 hours
find ~/.hermes/cache/scratch -type f -mtime +1 -delete 2>/dev/null
find ~/.hermes/cache/scratch -type d -empty -delete 2>/dev/null
```

---

## 3. Online LVM Root Expansion (Requires Sudo)

If the physical partition has unallocated space in the LVM volume group, expand the root logical volume online:

```bash
# Single command to expand LV to 100% free VG space and resize ext4 filesystem online
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv -r
```

### Notes & Verifications
- The `-r` (`--resizefs`) flag invokes `resize2fs` automatically and safely while the filesystem is mounted (*live online expansion*).
- Verify the expansion immediately:
  ```bash
  df -h /
  ```
