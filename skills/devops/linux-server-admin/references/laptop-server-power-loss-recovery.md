# Laptop as Headless Server: Power Loss Recovery Without UPS

Repurposing a laptop as a home/headless Linux server has advantages (built-in screen, keyboard, battery backup), but when the battery is removed or dead, sudden power loss leaves the server powered off even after mains power returns.

## Diagnosis: Power Supply & Hardware State

Check if battery or AC line is detected:
```bash
ls -la /sys/class/power_supply/
cat /sys/class/power_supply/*/type
```
If only `ACAD` / `line_power_ACAD` is listed and no `BAT0`/`BAT1`, the laptop operates strictly on mains power without battery backup, making it vulnerable to instant hard shutdowns during power cuts.

Check machine vendor and model:
```bash
cat /sys/class/dmi/id/product_name /sys/class/dmi/id/sys_vendor
```

## Remediation Strategies (Without External UPS)

### 1. Battery Replacement (The "Native UPS" Strategy)
A laptop battery functions as an integrated UPS. Even an inexpensive aftermarket/OEM replacement battery providing 15–30 minutes of runtime prevents hard shutdowns during transient brownouts and brief outages.

### 2. BIOS Settings for Auto Power-On After AC Loss
Standard laptops remain in ACPI G3 (mechanical off) state when AC power is restored. To enable automatic boot upon AC return:
1. Enter BIOS setup during boot (`Esc`, `F10`, or `Del` depending on vendor).
2. Navigate to **Advanced** -> **Power Management Options** or **Boot Options**.
3. Look for:
   - **`AC Power On`** or **`Power-On on AC`** -> set to **Enabled**.
   - **`Restore on AC Power Loss`** / **`State After G3`** -> set to **Power On** (avoid *Stay Off* / *Last State*).
4. Save and exit (`F10`).
*Note:* Some consumer laptops hide this setting; check if an unlocked or updated BIOS provides it.

### 3. Scheduled BIOS RTC Power-On (Fallback)
If "AC Power On" is absent in BIOS:
- Use RTC alarm wakeup. Verify hardware and battery health without root:
  ```bash
  cat /proc/driver/rtc                          # check batt_status: okay
  cat /sys/class/rtc/rtc0/device/power/wakeup   # should report 'enabled'
  ```

### 4. Wake-on-LAN (WOL) Remote Boot (Headless Setup)
If the laptop cannot auto-boot on AC restore, WOL allows remote powering on across the local network:
1. Verify NIC wakeup capability from sysfs (no root needed):
   ```bash
   cat /sys/class/net/<interface>/device/power/wakeup   # should report 'enabled'
   ```
2. Enable Network Boot in BIOS:
   - In HP InsydeH2O BIOS: Navigate to **System Configuration** -> **Boot Options** -> set **Internal Network Adapter Boot** (or **Network Boot**) to **Enabled**.
3. Send Magic Packet from router or mobile app (e.g. Android Wake-on-LAN) once mains power returns.

### 5. DMI & BIOS Probing Without Root
Do not guess BIOS capabilities or require `sudo dmidecode`. Inspect DMI tables directly via sysfs:
```bash
for field in sys_vendor product_name product_sku board_name bios_vendor bios_version bios_date; do
  echo "$field: $(cat /sys/class/dmi/id/$field 2>/dev/null)"
done
```
Consumer series laptops (e.g. HP Notebook 15 with InsydeH2O) often omit "AC Power On" / "Restore on AC" compared to enterprise lines (ProBook/EliteBook). In such cases, battery replacement or WOL via Realtek NIC (`enp1s0`) is the definitive recovery path. **BIOS Power-On** (RTC Wake) to schedule automatic power-on at fixed intervals or times (e.g., daily at 06:00, 12:00, 18:00) so the machine automatically recovers within hours of an outage.

### 4. Wake-on-LAN (WOL)
For machines wired via Ethernet (`enp1s0`):
- Ensure WOL is enabled in BIOS and network driver (`ethtool -s <interface> wol g`).
- When power returns and the local router boots up, a magic packet can be sent from a mobile app or another LAN device to boot the server remotely.

### 5. Telegram Boot Notification (Startup Signal)
To immediately know when the server has rebooted and regained internet access after an outage, create a systemd oneshot service or `@reboot` script that sends a Telegram notification via Bot API or webhook once network connectivity is established.
