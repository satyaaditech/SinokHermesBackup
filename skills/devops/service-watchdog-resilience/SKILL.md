---
name: service-watchdog-resilience
description: "Use when building or fixing service watchdogs and proxies."
version: 1.0.0
author: Parjo Agent
license: MIT
metadata:
  hermes:
    tags: [devops, systemd, watchdog, self-healing, proxy, reliability]
    category: devops
---

# Service Watchdog & Self-Healing Resilience

Engineering patterns and pitfalls for autonomous self-healing watchdogs, network forward proxies, and background health monitors on Linux servers. Prevents false-alarm service flapping, packet-drop cascading failures, and alert notification storms.

## Core Rules & Architecture

### 1. Probe Timeout vs. Service Connect Timeout Margin
* **The Golden Margin Rule**: A watchdog probe socket timeout MUST exceed the target service's internal connection fallback budget by at least 1.5x–2.0x.
* **Mechanism**: If a proxy attempts fallback to secondary endpoints upon packet drop (e.g. 2.0s per endpoint), a watchdog socket timeout shorter than the total fallback window (e.g. 4.0s vs 5.0s) will prematurely abort with a false-positive failure while the proxy was actively recovering.
* **Standard**: Set watchdog socket connect timeouts to 6.0s–8.0s for network probes over public/international transit.

### 2. Multi-Endpoint Pool & Fast Failover (Mitigating International Jitter)
* **Never Single-IP Hardcode**: Never hardcode a single remote IP address for critical network proxies over public routing where international links experience transient SYN drops (~10–20% packet jitter).
* **Pool Architecture**: Define a prioritized list of official IP addresses (e.g., multiple IPv6 anycast endpoints + IPv4 fallback).
* **Fast Timeout**: Cap per-attempt connection timeout to 1.5s–2.0s per IP. If the first IP drops a SYN packet, failover to the secondary IP occurs in under 2.2s—well within client retry windows.

### 3. Sustained Failure Thresholds (Anti-Flapping)
* **Never Trigger Healing on 1–2 Transient Glitches**: With 30-second polling intervals, requiring only 2 consecutive failed checks means a brief 35-second network hiccup will trigger a service restart.
* **Threshold Standard**: Require at least 3–4 consecutive failed cycles (90–120 seconds of sustained downtime) before initiating an automatic `systemctl restart` or container recycle.
* **Avoid Unnecessary Restarts**: Forcibly restarting a running proxy daemon drops active streaming connections and causes cascading client disconnection errors.

### 4. Alert Notification Rate-Limiting (Storm Prevention)
* **Failure Alerts (Always Immediate)**: If self-healing fails after attempting recovery (`Auto-healing FAILED`), dispatch an alert to admin channels immediately.
* **Success Alerts (Rate-Limited)**: Routine success notifications (`Auto-healing SUCCESS`) MUST be rate-limited to at most once per 1–2 hours per component.
* **Mechanism**: When network jitter triggers periodic recovery cycles, sending unthrottled messages creates notification fatigue and chat clutter ("pesan bertumpuk"). Suppress redundant success alerts while preserving full diagnostic logging in local log files.

## Verification Checklist

When diagnosing a flapping self-healing system:
1. Check watchdog log history for repeating failure intervals (`grep -E "check failed|Auto-healing" watchdog.log`).
2. Measure packet loss and SYN latency to upstream endpoints via direct socket loops (`socket.create_connection`).
3. Verify TLS handshake completion across IPv6 vs IPv4 to detect ISP-level SNI filtering or DPI blocks.
4. Ensure systemd user units run under proper lingering (`loginctl enable-linger <user>`) to survive session disconnects.
