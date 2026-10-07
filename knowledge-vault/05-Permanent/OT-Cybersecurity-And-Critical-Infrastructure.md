---
title: OT Cybersecurity and Critical Infrastructure
tags: [ot-cybersecurity, scada, plc-security, critical-infrastructure, iec-62443, security]
updated: 2026-08-31
---

# OT Cybersecurity and Critical Infrastructure

**Purpose:** Comprehensive guide on Operational Technology (OT) cybersecurity, securing industrial control systems (ICS/SCADA/PLCs) against physical sabotage, process tampering, and cyber-physical attacks.

**Summary:** While IT security prioritizes data confidentiality, OT security prioritizes **safety, availability, and physical process integrity**. A breach in OT does not just leak records—it can rupture pipelines, ruin production batches, or endanger human life.

---

## 1. IT Security vs OT Security Comparison

| Attribute | IT (Information Technology) | OT (Operational Technology) |
|---|---|---|
| **Primary Objective** | Confidentiality $\rightarrow$ Integrity $\rightarrow$ Availability (CIA) | Safety $\rightarrow$ Availability $\rightarrow$ Integrity (Safety First) |
| **System Lifetime** | 3–5 years (frequent OS patches/reboots) | 15–30 years (cannot reboot without plant shutdown) |
| **Patching Rhythm** | Weekly / Monthly automated updates | Scheduled annual maintenance shutdowns |
| **Worst-Case Impact** | Data breach, monetary fines, reputational hit | Explosion, equipment destruction, physical casualties |
| **Protocols** | HTTPS, SSH, gRPC, OAuth2 | Modbus, Profinet, EtherNet/IP (often unencrypted legacy) |

---

## 2. The Purdue Enterprise Reference Architecture (PERA / ISA-95)

```text
┌─────────────────────────────────────────────────────────────┐
│ LEVEL 4/5: ENTERPRISE IT NETWORK (ERP, Cloud, Email, Web)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ INDUSTRIAL DMZ (Firewall / Proxy)
┌──────────────────────────────▼──────────────────────────────┐
│ LEVEL 3: OPERATIONS & SCADA (Historians, MES, Engineering)  │
└──────────────────────────────┬──────────────────────────────┘
                               │ OT Internal Segmentation
┌──────────────────────────────▼──────────────────────────────┐
│ LEVEL 2: CONTROL LAYER (HMI, Supervisory PLCs)              │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ LEVEL 1: DIRECT CONTROL (Field PLCs, RTUs, DCS Controllers) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ LEVEL 0: PHYSICAL PROCESS (Sensors, Motors, Valves, Actuators│
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Core OT Defense Vectors
1. **Air-Gapping & Industrial DMZ:** Strict isolation between IT enterprise networks and plant floor networks.
2. **Deep Packet Inspection (DPI) for Industrial Protocols:** Validating that Modbus/Profinet payloads do not contain out-of-range write commands or rogue ladder-logic uploads.
3. **Firmware Integrity & Immutable Logging:** Detecting unauthorized firmware flashes on PLCs and field controllers.

---

## Related Notes
- [[Industrial-Automation-AI-MOC]]
- [[Cybersecurity-And-Agent-Permission-Layers]]
- [[Industrial-Protocols-And-Edge-Data-Pipelines]]
- [[Security]]
