# Buku Pangestu LLM Wiki Implementation Reference

This reference documents the specific implementation of Karpathy's LLM Wiki pattern for the Buku Pangestu (Paguyuban Ngesti Tunggal) spiritual studies vault.

---

## 1. Vault Directory Structure
The vault is located at `/home/satyaaditech/shorts_factory/obsidian/BukuPangestu/` (which maps to the NVMe filesystem at `/mnt/usb-nvme/obsidian/BukuPangestu/`).

- **`books/`**: Immutable source texts of Pangestu books (e.g. `ssj.md`, `skh.md`, `brsr.md`).
- **`wiki/`**: Managed knowledge base where compiled concepts, entities, and summaries live. Link files using `[[wikilinks]]`. Notable files:
  - `wiki/index.md` (Main catalog/index).
  - `wiki/log.md` (Chronological log of ingested documentation).
  - Concept assets (e.g. `Candrajiwa.md`, `Dalan Rahayu.md`, `Paliwara.md`, `Jujur.md`, `Rela.md`, etc.).
- **`raw/`**: Staging directory for newly added documents, articles, or transcripts to be processed.
- **`archive/`**: Storage folder for raw files after they are successfully ingested and merged into the wiki.
- **`inbox/`**: Temporary notes typed by the user or captured quickly.
- **`AGENT.md`**: Embedded guidelines defining the instructions, rules, and workflows for managing the wiki.

---

## 2. Samba Network Mapping & macOS Storage Resolution
### The Issue
Samba shares `/etc/samba/smb.conf` the directory `/home/satyaaditech/shorts_factory` as the share `[ShortsFactory]`. The server's main local storage SSD where this folder lives has very low capacity (~21 GB free). Meanwhile, the supplementary NVMe drive `/mnt/usb-nvme` has 239 GB free. But macOS clients mounting `ShortsFactory` see the low 21 GB capacity and cannot see hidden NVMe directories.

### The Bind Mount Solution
To resolve this, the NVMe mount points are mapped into `ShortsFactory` via bind mounts:
1. Mount the entire NVMe root to `ShortsFactory/nvme`:
   ```bash
   sudo mount --bind /mnt/usb-nvme /home/satyaaditech/shorts_factory/nvme
   ```
2. Make it persistent across server reboots by appending it to the user's crontab:
   ```text
   @reboot sudo mount --bind /mnt/usb-nvme /home/satyaaditech/shorts_factory/nvme
   ```
This exposes the entire NVMe partition directly under the `nvme/` folder in the Samba share, displaying the correct 239 GB capacity on macOS and allowing full directory navigation (`obsidian/`, `other/`).

---

## 3. Communication & Style Guide (Javanese Krama Alus)
When managing or interacting with the user regarding the Buku Pangestu Wiki, adhere strictly to these Javanese language conventions:

- **Strict Javanese Krama Alus**: Write in refined, formal Javanese without code-switching to Indonesian (e.g., use **"nggampilaken"** instead of "memudahkan", and **"ing salebeting"** instead of "di dalam" or "njero").
- **Honorific Word Choice (Mundhut vs Nyuwun)**:
  - When the user asks the agent a question: **"mundhut pirsa"**.
  - When the agent asks the user a question: **"nyuwun pirsa"**.
- **WIB Greetings**:
  - 04:00 - 10:00: Sugeng enjang
  - 10:00 - 15:00: Sugeng siyang
  - 15:00 - 18:00: Sugeng sonten
  - 18:00 - 04:00: Sugeng dalu
